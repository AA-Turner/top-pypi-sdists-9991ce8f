# -*- coding:utf-8 -*-

#  ************************** Copyrights and license ***************************
#
# This file is part of gcovr 8.3, a parsing and reporting tool for gcov.
# https://gcovr.com/en/8.3
#
# _____________________________________________________________________________
#
# Copyright (c) 2013-2025 the gcovr authors
# Copyright (c) 2013 Sandia Corporation.
# Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
# the U.S. Government retains certain rights in this software.
#
# This software is distributed under the 3-clause BSD License.
# For more information, see the README.rst file.
#
# ****************************************************************************

# cspell:ignore xmlcharrefreplace

import functools
import logging
import os
from typing import Any, Callable, Optional, Union

from jinja2 import (
    BaseLoader,
    Environment,
    ChoiceLoader,
    FileSystemLoader,
    FunctionLoader,
    PackageLoader,
    Template,
)
from markupsafe import Markup
import pygments
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_for_filename


from ...coverage import (
    BranchCoverage,
    CallCoverage,
    ConditionCoverage,
    CoverageContainer,
    CoverageContainerDirectory,
    CoverageStat,
    DecisionCoverage,
    DecisionCoverageConditional,
    DecisionCoverageStat,
    DecisionCoverageSwitch,
    DecisionCoverageUncheckable,
    FileCoverage,
    LineCoverage,
)
from ...options import Options
from ...utils import (
    chdir,
    commonpath,
    force_unix_separator,
    get_md5_hexdigest,
    get_version_for_report,
    open_text_for_writing,
)


LOGGER = logging.getLogger("gcovr")
PYGMENTS_CSS_MARKER = "/* Comment.Preproc */"


# html_theme string is <theme_directory>.<color> or only <color> (if only color use default)
# examples: github.green github.blue or blue or green
def get_theme_name(html_theme: str) -> str:
    """Get the theme name without the color."""
    return html_theme.split(".")[0] if "." in html_theme else "default"


def get_theme_color(html_theme: str) -> str:
    """Get the theme color from the theme name."""
    return html_theme.split(".")[1] if "." in html_theme else html_theme


@functools.lru_cache(maxsize=1)
def templates(options: Options) -> Environment:
    """Get the Jinja2 environment for the templates."""
    # As default use the package loader
    loader: BaseLoader = PackageLoader(
        "gcovr.formats.html",
        package_path=get_theme_name(options.html_theme),
    )

    # If a directory is given files in the directory have higher precedence.
    if options.html_template_dir is not None:
        loader = ChoiceLoader([FileSystemLoader(options.html_template_dir), loader])

    return Environment(
        loader=loader,
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )


@functools.lru_cache(maxsize=1)
def user_templates() -> Environment:
    """Get the Jinja2 environment for the user templates."""

    def load_user_template(template: str) -> Optional[str]:
        contents = None
        try:
            with open(template, "rb") as f:
                contents = f.read().decode("utf-8")
        # This exception can only occur if the file gets inaccessible while gcovr is running.
        except FileNotFoundError:  # pragma: no cover
            pass

        return contents

    return Environment(
        loader=FunctionLoader(load_user_template),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )


class CssRenderer:
    """Class for rendering the CSS template with Jinja2."""

    @staticmethod
    def __load_css_template(options: Options) -> Template:
        """Load the CSS template."""
        if options.html_css is not None:
            template_path = os.path.relpath(options.html_css)
            return user_templates().get_template(template_path)

        return templates(options).get_template("style.css")

    @staticmethod
    def render(options: Options) -> str:
        """Get the rendered CSS content."""
        template = CssRenderer.__load_css_template(options)
        return template.render(
            tab_size=options.html_tab_size, single_page=options.html_single_page
        )


class NullHighlighting:
    """Class if no syntax highlighting is available for the given file."""

    def get_css(self) -> str:
        """Get the empty CSS."""
        return ""

    @staticmethod
    def highlighter_for_file(_: str) -> Callable[[str], list[str]]:
        """Get the default highlighter which only returns the content as raw text lines."""
        return lambda code: [line.rstrip() for line in code.split("\n")]


class PygmentsHighlighting:
    """Class for syntax highlighting in report."""

    def __init__(self, style: str) -> None:
        self.formatter = None
        try:
            self.formatter = HtmlFormatter(nowrap=True, style=style)
        except ImportError as e:  # pragma: no cover
            LOGGER.warning(f"No syntax highlighting available: {str(e)}")

    def get_css(self) -> str:
        """Get the CSS for the syntax highlighting."""
        if self.formatter is None:  # pragma: no cover
            return ""
        return (
            f"\n\n/* pygments syntax highlighting */\n{self.formatter.get_style_defs()}"
        )

    def highlighter_for_file(self, filename: str) -> Callable[[str], list[str]]:
        """Get the highlighter for the given filename."""
        if self.formatter is None:  # pragma: no cover
            return NullHighlighting.highlighter_for_file(filename)

        try:
            lexer = get_lexer_for_filename(filename, None, stripnl=False)
            formatter = self.formatter
            return lambda code: [
                Markup(line.rstrip())
                for line in pygments.highlight(code, lexer, formatter).split("\n")
            ]
        except pygments.util.ClassNotFound:  # pragma: no cover
            return NullHighlighting.highlighter_for_file(filename)


@functools.lru_cache(maxsize=1)
def get_formatter(options: Options) -> Union[PygmentsHighlighting, NullHighlighting]:
    """Get the formatter for the selected theme."""
    highlight_style = (
        templates(options)
        .get_template(f"pygments.{get_theme_color(options.html_theme)}")
        .render()
    )
    return (
        PygmentsHighlighting(highlight_style)
        if options.html_syntax_highlighting
        else NullHighlighting()
    )


def coverage_to_class(
    coverage: Optional[float], medium_threshold: float, high_threshold: float
) -> str:
    """Get the coverage class depending on the threshold."""
    if coverage is None:
        return "coverage-unknown"
    if coverage == 0:
        return "coverage-none"
    if coverage < medium_threshold:
        return "coverage-low"
    if coverage < high_threshold:
        return "coverage-medium"
    return "coverage-high"


class RootInfo:
    """Class holding the information used in Jinja2 template."""

    def __init__(self, options: Options) -> None:
        self.medium_threshold = options.html_medium_threshold
        self.high_threshold = options.html_high_threshold
        self.medium_threshold_line = options.html_medium_threshold_line
        self.high_threshold_line = options.html_high_threshold_line
        self.medium_threshold_branch = options.html_medium_threshold_branch
        self.high_threshold_branch = options.html_high_threshold_branch
        self.link_function_list = (options.html_details or options.html_nested) and (
            options.html_single_page != "static"
        )
        self.relative_anchors = options.html_relative_anchors
        self.single_page = options.html_single_page

        self.version = get_version_for_report()
        self.head = options.html_title
        self.date = options.timestamp.isoformat(sep=" ", timespec="seconds")
        self.encoding = options.html_encoding
        self.directory = ""
        self.branches = dict[str, Any]()
        self.conditions = dict[str, Any]()
        self.decisions = dict[str, Any]()
        self.calls = dict[str, Any]()
        self.functions = dict[str, Any]()
        self.lines = dict[str, Any]()

    def set_directory(self, directory: str) -> None:
        """Set the directory for the report."""
        self.directory = directory

    def get_directory(self) -> str:
        """Get the directory for the report."""
        return (
            "." if self.directory == "" else force_unix_separator(str(self.directory))
        )

    def set_coverage(self, covdata: CoverageContainer) -> None:
        """Update this RootInfo with a summary of the CoverageContainer."""
        stats = covdata.stats
        self.lines = dict_from_stat(stats.line, self.line_coverage_class, 0.0)
        self.functions = dict_from_stat(stats.function, self.coverage_class)
        self.branches = dict_from_stat(stats.branch, self.branch_coverage_class)
        self.conditions = dict_from_stat(stats.condition, self.coverage_class)
        self.decisions = dict_from_stat(stats.decision, self.coverage_class)
        self.calls = dict_from_stat(stats.call, self.coverage_class)

    def line_coverage_class(self, coverage: Optional[float]) -> str:
        """Get the coverage class for the line."""
        return coverage_to_class(
            coverage, self.medium_threshold_line, self.high_threshold_line
        )

    def branch_coverage_class(self, coverage: Optional[float]) -> str:
        """Get the coverage class for the branch."""
        return coverage_to_class(
            coverage, self.medium_threshold_branch, self.high_threshold_branch
        )

    def coverage_class(self, coverage: Optional[float]) -> str:
        """Get the coverage class for all other types."""
        return coverage_to_class(coverage, self.medium_threshold, self.high_threshold)


#
# Produce an HTML report
#
def write_report(
    covdata: CoverageContainer, output_file: str, options: Options
) -> None:
    """Write the HTML report"""
    css_data = CssRenderer.render(options)
    medium_threshold = options.html_medium_threshold
    high_threshold = options.html_high_threshold
    medium_threshold_line = options.html_medium_threshold_line
    high_threshold_line = options.html_high_threshold_line
    medium_threshold_branch = options.html_medium_threshold_branch
    high_threshold_branch = options.html_high_threshold_branch
    exclude_calls = options.exclude_calls
    show_decision = options.show_decision

    data = dict[str, Any]()
    root_info = RootInfo(options)
    data["info"] = root_info

    data["SHOW_DECISION"] = show_decision
    data["EXCLUDE_CALLS"] = exclude_calls
    data["EXCLUDE_FUNCTION_COVERAGE"] = not any(
        filter(
            lambda filecov: any(  # type: ignore [arg-type]
                filter(
                    lambda linecov: linecov.function_name is not None,  # type: ignore [arg-type]
                    filecov.lines.values(),
                )
            ),
            covdata.values(),
        )
    )
    data["EXCLUDE_CONDITIONS"] = not any(
        filter(lambda filecov: filecov.condition_coverage().total > 0, covdata.values())  # type: ignore [arg-type]
    )
    data["USE_BLOCK_IDS"] = options.html_block_ids
    data["COVERAGE_MED"] = medium_threshold
    data["COVERAGE_HIGH"] = high_threshold
    data["LINE_COVERAGE_MED"] = medium_threshold_line
    data["LINE_COVERAGE_HIGH"] = high_threshold_line
    data["BRANCH_COVERAGE_MED"] = medium_threshold_branch
    data["BRANCH_COVERAGE_HIGH"] = high_threshold_branch

    self_contained = options.html_self_contained
    if self_contained is None:
        self_contained = (
            not (options.html_details or options.html_nested)
            or options.html_single_page
        )

    if output_file.endswith(os.sep):
        if options.html_single_page:
            output_file += "coverage_single_page.html"
        elif options.html_nested:
            output_file += "coverage_nested.html"
        elif options.html_details:
            output_file += "coverage_details.html"
        else:
            output_file += "coverage.html"

    if PYGMENTS_CSS_MARKER in css_data:
        LOGGER.info(
            "Skip adding of pygments styles since {PYGMENTS_CSS_MARKER!r} found in user stylesheet"
        )
    else:
        css_data += get_formatter(options).get_css()

    if self_contained:
        data["css"] = css_data
    else:
        css_output = os.path.splitext(output_file)[0] + ".css"
        with open_text_for_writing(css_output) as f:
            f.write(css_data)

        if options.html_relative_anchors:
            css_link = os.path.basename(css_output)
        else:  # pragma: no cover  Can't be checked because of the reference compare
            css_link = css_output
        data["css_link"] = css_link

    data["theme"] = get_theme_color(options.html_theme)

    root_info.set_coverage(covdata)

    # Generate the coverage output (on a per-package basis)
    # source_dirs = set()
    files = []
    filtered_fname = ""
    sorted_keys = covdata.sort_coverage(
        sort_key=options.sort_key,
        sort_reverse=options.sort_reverse,
        by_metric="branch" if options.sort_branches else "line",
        filename_uses_relative_pathname=True,
    )

    if options.html_nested:
        covdata.populate_directories(sorted_keys, options.root_filter)

    cdata_fname = dict[str, str]()
    cdata_sourcefile = dict[str, Optional[str]]()
    for f in sorted_keys + [v.dirname for v in covdata.directories]:
        filtered_fname = options.root_filter.sub("", f)
        if filtered_fname != "":
            files.append(filtered_fname)
        cdata_fname[f] = filtered_fname
        if options.html_details or options.html_nested or options.html_single_page:
            if os.path.normpath(f) == os.path.normpath(options.root_dir):
                cdata_sourcefile[f] = output_file
            else:
                cdata_sourcefile[f] = _make_short_source_filename(
                    output_file, filtered_fname.rstrip(os.sep)
                )
                if options.html_single_page and cdata_sourcefile[f] is not None:
                    # Remove the prefix to get shorter links
                    cdata_sourcefile[f] = str(cdata_sourcefile[f]).split(
                        ".", maxsplit=1
                    )[1]
        else:
            cdata_sourcefile[f] = None

    # Define the common root directory, which may differ from options.root_dir
    # when source files share a common prefix.
    root_directory = ""
    if len(files) > 1:
        common_dir = commonpath(files)
        if common_dir != "":
            root_directory = common_dir
    else:
        directory, _ = os.path.split(filtered_fname)
        if directory != "":
            root_directory = str(directory) + os.sep

    root_info.set_directory(root_directory)

    if options.html_details or options.html_nested:
        (output_prefix, output_suffix) = os.path.splitext(os.path.abspath(output_file))
        if output_suffix == "":
            output_suffix = ".html"
        functions_output_file = f"{output_prefix}.functions{output_suffix}"
        data["FUNCTIONS_FNAME"] = os.path.basename(functions_output_file)
        if options.html_single_page:
            # Remove the prefix to get shorter links
            data["FUNCTIONS_FNAME"] = data["FUNCTIONS_FNAME"].split(".", maxsplit=1)[1]

    if options.html_single_page:
        write_single_page(
            options,
            root_info,
            output_file,
            covdata,
            sorted_keys,
            cdata_fname,
            cdata_sourcefile,
            data,
        )
    else:
        if options.html_nested:
            write_directory_pages(
                options,
                root_info,
                output_file,
                covdata,
                cdata_fname,
                cdata_sourcefile,
                data,
            )
        else:
            write_root_page(
                options,
                root_info,
                output_file,
                covdata,
                cdata_fname,
                cdata_sourcefile,
                data,
                sorted_keys,
            )
            if not options.html_details:
                return

        write_source_pages(
            options,
            root_info,
            functions_output_file,
            covdata,
            cdata_fname,
            cdata_sourcefile,
            data,
        )


def write_root_page(
    options: Options,
    root_info: RootInfo,
    output_file: str,
    covdata: CoverageContainer,
    cdata_fname: dict[str, str],
    cdata_sourcefile: dict[str, Any],
    data: dict[str, Any],
    sorted_keys: list[str],
) -> None:
    """Generate the root HTML file that contains the high level report."""
    files = []
    for f in sorted_keys:
        files.append(
            get_coverage_data(
                root_info, covdata[f], cdata_sourcefile[f], cdata_fname[f]
            )
        )

    html_string = (
        templates(options)
        .get_template("directory_page.html")
        .render(**data, entries=files)
    )
    with open_text_for_writing(
        output_file, encoding=options.html_encoding, errors="xmlcharrefreplace"
    ) as fh:
        fh.write(html_string + "\n")


def write_source_pages(
    options: Options,
    root_info: RootInfo,
    functions_output_file: str,
    covdata: CoverageContainer,
    cdata_fname: dict[str, str],
    cdata_sourcefile: dict[str, Any],
    data: dict[str, Any],
) -> None:
    """Write a page for each source file."""
    error_no_files_not_found = 0
    all_functions = {}
    for fname, cdata in covdata.items():
        file_data, functions, file_not_found = get_file_data(
            options, root_info, fname, cdata_fname, cdata_sourcefile, cdata
        )
        all_functions.update(functions)
        if file_not_found:
            error_no_files_not_found += 1

        html_string = (
            templates(options)
            .get_template("source_page.html")
            .render(**data, **file_data)
        )
        with open_text_for_writing(
            cdata_sourcefile[fname],
            encoding=options.html_encoding,
            errors="xmlcharrefreplace",
        ) as fh:
            fh.write(html_string + "\n")

    html_string = (
        templates(options)
        .get_template("functions_page.html")
        .render(
            **data,
            all_functions=[all_functions[k] for k in sorted(all_functions)],
        )
    )
    with open_text_for_writing(
        functions_output_file,
        encoding=options.html_encoding,
        errors="xmlcharrefreplace",
    ) as fh:
        fh.write(html_string + "\n")

    if error_no_files_not_found != 0:
        raise RuntimeError(f"{error_no_files_not_found} source file(s) not found.")


def write_directory_pages(
    options: Options,
    root_info: RootInfo,
    output_file: str,
    covdata: CoverageContainer,
    cdata_fname: dict[str, str],
    cdata_sourcefile: dict[str, Any],
    data: dict[str, Any],
) -> None:
    """Write a page for each directory."""
    # The first directory is the shortest one --> This is the root dir
    root_key = next(iter(sorted([d.dirname for d in covdata.directories])))

    directory_data = {}
    for dircov in covdata.directories:
        directory_data = get_directory_data(
            options, root_info, cdata_fname, cdata_sourcefile, dircov
        )
        html_string = (
            templates(options)
            .get_template("directory_page.html")
            .render(**data, **directory_data)
        )
        filename = None
        if dircov.dirname in [root_key, ""]:
            filename = output_file
        elif dircov.dirname in cdata_sourcefile:
            filename = cdata_sourcefile[dircov.dirname]
        else:
            LOGGER.warning(
                f"There's a subdirectory {dircov.dirname!r} that there's no source files within it"
            )

        if filename:
            with open_text_for_writing(
                filename, encoding=options.html_encoding, errors="xmlcharrefreplace"
            ) as fh:
                fh.write(html_string + "\n")


def write_single_page(
    options: Options,
    root_info: RootInfo,
    output_file: str,
    covdata: CoverageContainer,
    sorted_keys: list[str],
    cdata_fname: dict[str, str],
    cdata_sourcefile: dict[str, Any],
    data: dict[str, Any],
) -> None:
    """Write a single page HTML report."""
    error_no_files_not_found = 0
    files = []
    all_functions = {}
    for filename, filecov in covdata.items():
        file_data, functions, file_not_found = get_file_data(
            options, root_info, filename, cdata_fname, cdata_sourcefile, filecov
        )
        all_functions.update(functions)
        if file_not_found:
            error_no_files_not_found += 1

        files.append(file_data)

    all_files = []
    for f in sorted_keys:
        all_files.append(
            get_coverage_data(
                root_info, covdata[f], cdata_sourcefile[f], cdata_fname[f]
            )
        )
    directories = list[dict[str, Any]]([{"entries": all_files}])
    if root_info.single_page == "js-enabled":
        for dircov in covdata.directories:
            directories.append(
                get_directory_data(
                    options, root_info, cdata_fname, cdata_sourcefile, dircov
                )
            )
    if len(directories) == 1:
        directories[0]["dirname"] = "/"  # We need this to have a correct id in HTML.

    html_string = (
        templates(options)
        .get_template("single_page.html")
        .render(
            **data,
            files=files,
            directories=directories,
            all_functions=[all_functions[k] for k in sorted(all_functions)],
        )
    )
    with open_text_for_writing(
        output_file,
        encoding=options.html_encoding,
        errors="xmlcharrefreplace",
    ) as fh:
        fh.write(html_string + "\n")

    if error_no_files_not_found != 0:
        raise RuntimeError(f"{error_no_files_not_found} source file(s) not found.")


def get_coverage_data(
    root_info: RootInfo,
    cdata: Union[CoverageContainerDirectory, FileCoverage],
    link_report: str,
    cdata_fname: str,
) -> dict[str, Any]:
    """Get the coverage data"""

    medium_threshold = root_info.medium_threshold
    high_threshold = root_info.high_threshold
    medium_threshold_line = root_info.medium_threshold_line
    high_threshold_line = root_info.high_threshold_line
    medium_threshold_branch = root_info.medium_threshold_branch
    high_threshold_branch = root_info.high_threshold_branch

    def coverage_class(coverage: Optional[float]) -> str:
        return coverage_to_class(coverage, medium_threshold, high_threshold)

    def line_coverage_class(coverage: Optional[float]) -> str:
        return coverage_to_class(coverage, medium_threshold_line, high_threshold_line)

    def branch_coverage_class(coverage: Optional[float]) -> str:
        return coverage_to_class(
            coverage, medium_threshold_branch, high_threshold_branch
        )

    stats = cdata.stats

    lines = {
        "total": stats.line.total,
        "exec": stats.line.covered,
        "coverage": stats.line.percent_or(
            100.0 if isinstance(cdata, FileCoverage) and cdata.lines else "-"
        ),
        "class": line_coverage_class(
            stats.line.percent_or(
                100.0 if isinstance(cdata, FileCoverage) and cdata.lines else None
            )
        ),
    }

    branches = {
        "total": stats.branch.total,
        "exec": stats.branch.covered,
        "coverage": stats.branch.percent_or("-"),
        "class": branch_coverage_class(stats.branch.percent),
    }

    conditions = {
        "total": stats.condition.total,
        "exec": stats.condition.covered,
        "coverage": stats.condition.percent_or("-"),
        "class": branch_coverage_class(stats.condition.percent),
    }

    decisions = {
        "total": stats.decision.total,
        "exec": stats.decision.covered,
        "unchecked": stats.decision.uncheckable,
        "coverage": stats.decision.percent_or("-"),
        "class": coverage_class(stats.decision.percent),
    }

    functions = {
        "total": stats.function.total,
        "exec": stats.function.covered,
        "coverage": stats.function.percent_or("-"),
        "class": coverage_class(stats.function.percent),
    }

    calls = {
        "total": stats.call.total,
        "exec": stats.call.covered,
        "coverage": stats.call.percent_or("-"),
        "class": coverage_class(stats.call.percent),
    }
    display_filename = force_unix_separator(
        os.path.relpath(
            os.path.realpath(cdata_fname), os.path.realpath(root_info.directory)
        )
    )

    if link_report is not None:
        if root_info.relative_anchors or root_info.single_page:
            link_report = os.path.basename(link_report)

    return {
        "filename": display_filename,
        "link": link_report,
        "lines": lines,
        "branches": branches,
        "conditions": conditions,
        "decisions": decisions,
        "functions": functions,
        "calls": calls,
    }


def get_directory_data(
    options: Options,
    root_info: RootInfo,
    cdata_fname: dict[str, str],
    cdata_sourcefile: dict[str, str],
    covdata_dir: CoverageContainerDirectory,
) -> dict[str, Any]:
    """Get the data for a directory to generate the HTML"""
    relative_path = cdata_fname[covdata_dir.dirname]
    if relative_path == ".":
        relative_path = ""
    directory_data = dict[str, Any](
        {
            "dirname": (
                cdata_sourcefile[covdata_dir.dirname]
                if cdata_fname[covdata_dir.dirname]
                else "/"
            ),
        }
    )

    sorted_keys = covdata_dir.sort_coverage(
        sort_key=options.sort_key,
        sort_reverse=options.sort_reverse,
        by_metric="branch" if options.sort_branches else "line",
        filename_uses_relative_pathname=True,
    )

    files = []
    for key in sorted_keys:
        fname = covdata_dir[key].filename
        files.append(
            get_coverage_data(
                root_info,
                covdata_dir[key],
                cdata_sourcefile[fname],
                cdata_fname[fname],
            )
        )

    directory_data["entries"] = files

    return directory_data


def get_file_data(
    options: Options,
    root_info: RootInfo,
    filename: str,
    cdata_fname: dict[str, str],
    cdata_sourcefile: dict[str, str],
    cdata: FileCoverage,
) -> tuple[dict[str, Any], dict[tuple[str, str, int], dict[str, Any]], bool]:
    """Get the data for a file to generate the HTML"""
    formatter = get_formatter(options)

    file_data = dict[str, Any](
        {
            "filename": cdata_fname[filename],
            "html_filename": os.path.basename(cdata_sourcefile[filename]),
            "source_lines": [],
            "function_list": [],
        }
    )
    file_data.update(
        get_coverage_data(
            root_info, cdata, cdata_sourcefile[filename], cdata_fname[filename]
        )
    )
    functions = dict[tuple[str, str, int], dict[str, Any]]()
    # Only use demangled names (containing a brace)
    for f_cdata in sorted(
        cdata.functions.values(), key=lambda f_cdata: f_cdata.demangled_name
    ):
        for lineno in sorted(f_cdata.count.keys()):
            f_data = dict[str, Any]()
            f_data["name"] = f_cdata.demangled_name
            f_data["filename"] = cdata_fname[filename]
            f_data["html_filename"] = os.path.basename(cdata_sourcefile[filename])
            f_data["line"] = lineno
            f_data["count"] = f_cdata.count[lineno]
            f_data["blocks"] = f_cdata.blocks[lineno]
            f_data["excluded"] = f_cdata.excluded[lineno]
            if f_cdata.name is not None:
                function_stats = cdata.filter_for_function(f_cdata).stats
                f_data["line_coverage"] = function_stats.line.percent_or(100.0)
                f_data["branch_coverage"] = function_stats.branch.percent_or("-")
                f_data["condition_coverage"] = function_stats.condition.percent_or("-")

            file_data["function_list"].append(f_data)
            functions[
                (
                    f_cdata.name or f_cdata.demangled_name,
                    str(f_data["filename"]),
                    int(f_data["line"]),
                )
            ] = f_data

    with chdir(options.root_dir):
        max_line_from_cdata = max(cdata.lines.keys(), default=0)
        try:
            file_not_found = True
            with open(
                filename,
                "r",
                encoding=options.source_encoding,
                errors="replace",
            ) as source_file:
                file_not_found = False
                lines = formatter.highlighter_for_file(filename)(source_file.read())
                ctr = 0
                for ctr, line in enumerate(lines, 1):
                    file_data["source_lines"].append(
                        source_row(
                            ctr, line, cdata.lines.get(ctr), options.html_block_ids
                        )
                    )
                if ctr < max_line_from_cdata:
                    LOGGER.warning(
                        f"File {filename} has {ctr} line(s) but coverage data has {max_line_from_cdata} line(s)."
                    )
        except IOError as e:
            if filename.endswith("<stdin>"):
                file_not_found = False
                file_info = "!!! File from stdin !!!"
            else:
                file_info = "!!! File not found !!!"
                LOGGER.warning(f"File {filename} not found: {repr(e)}")
            # Python ranges are exclusive. We want to iterate over all lines, including
            # that last line. Thus, we have to add a +1 to include that line.
            for ctr in range(1, max_line_from_cdata + 1):
                file_data["source_lines"].append(
                    source_row(
                        ctr,
                        file_info if ctr == 1 else "",
                        cdata.lines.get(ctr),
                        options.html_block_ids,
                    )
                )

    return file_data, functions, file_not_found


def dict_from_stat(
    stat: Union[CoverageStat, DecisionCoverageStat],
    coverage_class: Callable[[Optional[float]], str],
    default: Optional[float] = None,
) -> dict[str, Any]:
    """Get a dictionary from the stats."""
    coverage_default = "-" if default is None else default
    data = {
        "total": stat.total,
        "exec": stat.covered,
        "coverage": stat.percent_or(coverage_default),
        "class": coverage_class(stat.percent_or(default)),
    }

    if isinstance(stat, DecisionCoverageStat):
        data["unchecked"] = stat.uncheckable

    return data


def source_row(
    lineno: int, source: str, linecov: Optional[LineCoverage], html_block_ids: bool
) -> dict[str, Any]:
    """Get information for a row"""
    linebranch = None
    linecondition = None
    linedecision = None
    linecall = None
    linecount: Union[str, int] = ""
    covclass = ""
    if linecov:
        if linecov.is_excluded:
            covclass = "excludedLine"
        elif linecov.is_covered:
            linebranch = source_row_branch(linecov.branches)
            covclass = (
                "coveredLine"
                if linebranch is None or linebranch["taken"] == linebranch["total"]
                else "partialCoveredLine"
            )
            linecondition = source_row_condition(linecov.conditions)
            linedecision = source_row_decision(linecov.decision)
            linecount = linecov.count
        elif linecov.is_uncovered:
            covclass = "uncoveredLine"
            linedecision = source_row_decision(linecov.decision)
        linecall = source_row_call(linecov.calls)
    return {
        "lineno": lineno,
        "block_ids": []
        if linecov is None or not html_block_ids
        else linecov.block_ids or [],
        "source": source,
        "covclass": covclass,
        "linebranch": linebranch,
        "linecondition": linecondition,
        "linedecision": linedecision,
        "linecall": linecall,
        "linecount": linecount,
    }


def source_row_branch(branches: dict[int, BranchCoverage]) -> Optional[dict[str, Any]]:
    """Get branch information for a row"""
    if not branches:
        return None

    taken = 0
    total = 0
    items = []

    for branchno, branchcov in branches.items():
        if branchcov.is_covered:
            taken += 1
        if branchcov.excluded:
            total -= 1
        total += 1
        items.append(
            {
                "name": branchno,
                "taken": branchcov.is_covered,
                "count": branchcov.count,
                "excluded": branchcov.excluded,
            }
        )
        if branchcov.destination_block_id is not None:
            items[-1]["source_block_id"] = branchcov.source_block_id
            items[-1]["destination_block_id"] = branchcov.destination_block_id

    return {
        "taken": taken,
        "total": total,
        "branches": items,
    }


def source_row_condition(
    conditions: dict[int, ConditionCoverage],
) -> Optional[dict[str, Any]]:
    """Get condition information for a row."""
    if not conditions:
        return None

    count = 0
    covered = 0
    items = []

    for condition_id in sorted(conditions):
        prefix = f"{condition_id}-" if len(conditions) > 1 else ""
        condition = conditions[condition_id]
        count += condition.count
        covered += condition.covered
        for index in range(0, condition.count // 2):
            items.append(
                {
                    "name": None
                    if condition.count == 2 and prefix == ""
                    else f"{prefix}{index}",
                    "not_covered_true": index in condition.not_covered_true,
                    "not_covered_false": index in condition.not_covered_false,
                }
            )

    return {
        "count": count,
        "covered": covered,
        "condition": items,
    }


def source_row_decision(
    decision: Optional[DecisionCoverage],
) -> Optional[dict[str, Any]]:
    """Get decision information for a row"""
    if decision is None:
        return None

    items = list[dict[str, Any]]()

    if isinstance(decision, DecisionCoverageUncheckable):
        items.append(
            {
                "uncheckable": True,
            }
        )
    elif isinstance(decision, DecisionCoverageConditional):
        items.append(
            {
                "uncheckable": False,
                "taken": decision.count_true > 0,
                "count": decision.count_true,
                "name": "true",
            }
        )
        items.append(
            {
                "uncheckable": False,
                "taken": decision.count_false > 0,
                "count": decision.count_false,
                "name": "false",
            }
        )
    elif isinstance(decision, DecisionCoverageSwitch):
        items.append(
            {
                "uncheckable": False,
                "taken": decision.count > 0,
                "count": decision.count,
                "name": "true",
            }
        )
    else:
        raise RuntimeError(f"Unknown decision type {decision!r}")

    return {
        "taken": len([i for i in items if i.get("taken", False)]),
        "uncheckable": len([i for i in items if i["uncheckable"]]),
        "total": len(items),
        "decisions": items,
    }


def source_row_call(callcov: dict[int, CallCoverage]) -> Optional[dict[str, Any]]:
    """Get call information for a source row."""
    if not callcov:
        return None

    invoked = 0
    total = 0
    items = []

    for call_id in sorted(callcov):
        call = callcov[call_id]
        if call.is_covered:
            invoked += 1
        total += 1
        items.append(
            {
                "invoked": call.is_covered,
                "name": call_id,
            }
        )

    return {
        "invoked": invoked,
        "total": total,
        "calls": items,
    }


def _make_short_source_filename(output_file: str, filename: str) -> str:
    r"""Make a short-ish file path for --html-detail output.

    Args:
        output_file (str): The output path.
        filename (str): Path from root to source code.
    """

    (output_prefix, output_suffix) = os.path.splitext(os.path.abspath(output_file))
    if output_suffix == "":
        output_suffix = ".html"

    filename = filename.replace(os.sep, "/").replace("<stdin>", "stdin")
    source_filename = (
        ".".join(
            (
                output_prefix,
                os.path.basename(filename),
                get_md5_hexdigest(filename.encode("utf-8")),
            )
        )
        + output_suffix
    )
    return source_filename
