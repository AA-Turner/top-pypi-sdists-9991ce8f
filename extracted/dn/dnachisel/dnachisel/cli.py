#!/usr/bin/env python

"""
DNA Chisel Command Line Interface

Usage:
  dnachisel <source> <target> [--circular] [--mute] [--with_sequence_edits]

Where ``source`` is a fasta or Genbank file, and target can be one of:
- A folder name or a zip name (extension .zip). In this case a complete report
  along with the sequence will be generated.
- A Genbank file. In this case, only the optimized sequence file is created.
  The with_sequence_edits option specifies that edits are also annotated in the
  Genbank file. Note that the filename must end with '.gb'.

Note: this CLI will be developed on a per-request basis, so don't hesitate to
ask for more handles and options on Github
(https://github.com/Edinburgh-Genome-Foundry/DnaChisel/issues)

Example to output the result to a genbank:

>>> dnachisel annotated_record.gb optimized_record.gb

Example to output the result to a folder:

>>> dnachisel annotated_record.gb optimization_report/

Example to output the result to a zip archive:

>>> dnachisel annotated_record.gb optimization_report.zip
"""


def main():
    import os
    from docopt import docopt
    from dnachisel import DnaOptimizationProblem, CircularDnaOptimizationProblem

    params = docopt(__doc__)
    source, target = params["<source>"], params["<target>"]

    # VERBOSE PRINT
    def verbose_print(*args):
        if not params["--mute"]:
            print(*args)

    # PARSE THE CIRCULARITY

    if params["--circular"]:
        problem_class = CircularDnaOptimizationProblem
    else:
        problem_class = DnaOptimizationProblem
    problem = problem_class.from_record(
        source, logger=None if params["--mute"] else "bar"
    )
    problem.max_random_iters = 10000
    verbose_print(
        "\n\nBefore optimization:\n\n",
        problem.constraints_text_summary(),
        problem.objectives_text_summary(),
    )

    if target.lower().endswith(".gb"):  # save genbank
        if params["--with_sequence_edits"]:
            annotate_edits = True
        else:
            annotate_edits = False
        verbose_print("Resolving Constraints...")
        problem.resolve_constraints()
        verbose_print("Optimizing...")
        problem.optimize()
        problem.to_record(filepath=target, with_sequence_edits=annotate_edits)

    else:  # save into zip or folder
        project_name = os.path.basename(source)
        problem.optimize_with_report(
            target, project_name=project_name, file_path=source
        )

    verbose_print(
        "\n\nAfter optimization:\n\n",
        problem.constraints_text_summary(),
        problem.objectives_text_summary(),
        "\n\n",
        "Result written to %s" % target,
    )


if __name__ == "__main__":
    main()
