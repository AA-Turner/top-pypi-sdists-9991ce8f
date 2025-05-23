import json

import pytest

from great_expectations.core.expectation_diagnostics.supporting_types import (
    ExpectationRendererDiagnostics,
)
from great_expectations.core.metric_function_types import (
    SummarizationMetricNameSuffixes,
)
from great_expectations.expectations.expectation import ColumnMapExpectation
from great_expectations.expectations.registry import _registered_expectations
from tests.expectations.fixtures.expect_column_values_to_equal_three import (
    ExpectColumnValuesToEqualThree,
    ExpectColumnValuesToEqualThree__BrokenIteration,
    ExpectColumnValuesToEqualThree__SecondIteration,
)


@pytest.mark.unit
def test_expectation_self_check():
    my_expectation = ExpectColumnValuesToEqualThree(column="values")
    expectation_diagnostic = my_expectation.run_diagnostics()
    print(json.dumps(expectation_diagnostic.to_dict(), indent=2))

    assert expectation_diagnostic.to_dict() == {
        "examples": [],
        "library_metadata": {
            "maturity": "EXPERIMENTAL",
            "tags": [],
            "contributors": [],
            "requirements": [],
            "has_full_test_suite": False,
            "manually_reviewed_code": False,
            "library_metadata_passed_checks": False,
            "problems": ["No library_metadata attribute found"],
        },
        "description": {
            "camel_name": "ExpectColumnValuesToEqualThree",
            "snake_name": "expect_column_values_to_equal_three",
            "short_description": "",
            "docstring": "",
        },
        "execution_engines": {
            "PandasExecutionEngine": False,
            "SqlAlchemyExecutionEngine": False,
            "SparkDFExecutionEngine": False,
        },
        "gallery_examples": [],
        "renderers": [
            {
                "is_standard": False,
                "is_supported": True,
                "name": "atomic.diagnostic.failed",
                "samples": [],
            },
            {
                "name": "atomic.diagnostic.observed_value",
                "is_supported": True,
                "is_standard": False,
                "samples": [],
            },
            {
                "name": "atomic.prescriptive.failed",
                "is_supported": True,
                "is_standard": False,
                "samples": [],
            },
            {
                "name": "atomic.prescriptive.summary",
                "is_supported": True,
                "is_standard": False,
                "samples": [],
            },
            {
                "name": "renderer.answer",
                "is_supported": False,
                "is_standard": True,
                "samples": [],
            },
            {
                "name": "renderer.diagnostic.meta_properties",
                "is_supported": True,
                "is_standard": False,
                "samples": [],
            },
            {
                "name": "renderer.diagnostic.observed_value",
                "is_supported": True,
                "is_standard": True,
                "samples": [],
            },
            {
                "name": "renderer.diagnostic.status_icon",
                "is_supported": True,
                "is_standard": True,
                "samples": [],
            },
            {
                "name": "renderer.diagnostic.unexpected_statement",
                "is_supported": True,
                "is_standard": True,
                "samples": [],
            },
            {
                "name": "renderer.diagnostic.unexpected_table",
                "is_supported": True,
                "is_standard": True,
                "samples": [],
            },
            {
                "name": "renderer.prescriptive",
                "is_supported": True,
                "is_standard": True,
                "samples": [],
            },
            {
                "name": "renderer.question",
                "is_supported": False,
                "is_standard": True,
                "samples": [],
            },
        ],
        "metrics": [],
        "tests": [],
        "backend_test_result_counts": [],
        "errors": [],
        "coverage_score": 0.0,
        "maturity_checklist": {
            "beta": [
                {
                    "doc_url": None,
                    "message": "Has basic input validation and type checking",
                    "passed": False,
                    "sub_messages": [
                        {
                            "message": "No example found to get kwargs for ExpectationConfiguration",  # noqa: E501 # FIXME CoP
                            "passed": False,
                        },
                    ],
                },
                {
                    "doc_url": None,
                    "message": "Has both statement Renderers: prescriptive and diagnostic",
                    "passed": True,
                    "sub_messages": [],
                },
                {
                    "doc_url": None,
                    "message": "Has core logic that passes tests for all applicable Execution Engines and SQL dialects",  # noqa: E501 # FIXME CoP
                    "passed": False,
                    "sub_messages": [
                        {
                            "message": "There are no test results",
                            "passed": False,
                        }
                    ],
                },
            ],
            "experimental": [
                {
                    "doc_url": None,
                    "message": "Has a valid library_metadata object",
                    "passed": False,
                    "sub_messages": [
                        {
                            "message": "No library_metadata attribute found",
                            "passed": False,
                        },
                    ],
                },
                {
                    "doc_url": None,
                    "message": 'Has a docstring, including a one-line short description that begins with "Expect" and ends with a period',  # noqa: E501 # FIXME CoP
                    "passed": False,
                    "sub_messages": [],
                },
                {
                    "doc_url": None,
                    "message": "Has at least one positive and negative example case, and all test cases pass",  # noqa: E501 # FIXME CoP
                    "passed": False,
                    "sub_messages": [],
                },
                {
                    "doc_url": None,
                    "message": "Has core logic and passes tests on at least one Execution Engine",
                    "passed": False,
                    "sub_messages": [
                        {
                            "message": "There are no test results",
                            "passed": False,
                        }
                    ],
                },
            ],
            "production": [
                {
                    "doc_url": None,
                    "message": "Has a full suite of tests, as determined by a code owner",
                    "passed": False,
                    "sub_messages": [],
                },
                {
                    "doc_url": None,
                    "message": "Has passed a manual review by a code owner for code standards and style guides",  # noqa: E501 # FIXME CoP
                    "passed": False,
                    "sub_messages": [],
                },
            ],
        },
    }


@pytest.mark.unit
def test_include_in_gallery_flag():
    my_expectation = ExpectColumnValuesToEqualThree__SecondIteration(column="values")
    report_object = my_expectation.run_diagnostics()
    # print(json.dumps(report_object["examples"], indent=2))

    assert len(report_object["gallery_examples"][0]["tests"]) == 1
    assert report_object["gallery_examples"][0]["tests"][0].to_dict() == {
        "title": "positive_test_with_mostly",
        "exact_match_out": False,
        "input": {"column": "mostly_threes", "mostly": 0.6},
        "include_in_gallery": True,
        "suppress_test_for": [],
        "only_for": None,
        "output": {
            "success": True,
            "unexpected_index_list": [6, 7],
            "unexpected_list": [2, -1],
        },
    }


@pytest.mark.skip("This raises a Spark error on my machine.")
@pytest.mark.spark
def test_self_check_on_an_existing_expectation():
    expectation_name = "expect_column_values_to_match_regex"
    expectation = _registered_expectations[expectation_name]

    report_object = expectation().run_diagnostics()
    # print(json.dumps(report_object, indent=2))

    report_object["description"].pop("docstring")  # Don't try to exact match the docstring

    # one of the test cases in the examples for this expectation is failing on our CI
    # and the number of items depends on the flags
    # we will not verify the contents of `tests` or `errors`
    report_object.pop("tests")
    report_object.pop("errors")

    assert report_object == {
        "description": {
            "camel_name": "ExpectColumnValuesToMatchRegex",
            "snake_name": "expect_column_values_to_match_regex",
            "short_description": "Expect column entries to be strings that match a given regular expression.",  # noqa: E501 # FIXME CoP
        },
        "execution_engines": {
            "PandasExecutionEngine": True,
            "SqlAlchemyExecutionEngine": True,
            "SparkDFExecutionEngine": True,
        },
        "renderers": {
            "standard": {
                "renderer.answer": 'Less than 90.0% of values in column "a" match the regular expression ^a.',  # noqa: E501 # FIXME CoP
                "renderer.diagnostic.unexpected_statement": "\n\n1 unexpected values found. 20% of 5 total rows.",  # noqa: E501 # FIXME CoP
                "renderer.diagnostic.observed_value": "20% unexpected",
                "renderer.diagnostic.status_icon": "",
                "renderer.diagnostic.unexpected_table": None,
                "renderer.prescriptive": "a values must match this regular expression: ^a, at least 90 % of the time.",  # noqa: E501 # FIXME CoP
                "renderer.question": 'Do at least 90.0% of values in column "a" match the regular expression ^a?',  # noqa: E501 # FIXME CoP
            },
            "custom": [],
        },
        "metrics": [
            f"column_values.nonnull.{SummarizationMetricNameSuffixes.UNEXPECTED_COUNT.value}",
            f"column_values.match_regex.{SummarizationMetricNameSuffixes.UNEXPECTED_COUNT.value}",
            "table.row_count",
            "column_values.match_regex.unexpected_values",
        ],
        "examples": [
            {
                "data": {
                    "a": ["aaa", "abb", "acc", "add", "bee"],
                    "b": ["aaa", "abb", "acc", "bdd", None],
                    "column_name with space": ["aaa", "abb", "acc", "add", "bee"],
                },
                "tests": [
                    {
                        "title": "negative_test_insufficient_mostly_and_one_non_matching_value",
                        "exact_match_out": False,
                        "in": {"column": "a", "regex": "^a", "mostly": 0.9},
                        "out": {
                            "success": False,
                            "unexpected_index_list": [4],
                            "unexpected_list": ["bee"],
                        },
                        "suppress_test_for": ["sqlite", "mssql"],
                        "include_in_gallery": True,
                    },
                    {
                        "title": "positive_test_exact_mostly_w_one_non_matching_value",
                        "exact_match_out": False,
                        "in": {"column": "a", "regex": "^a", "mostly": 0.8},
                        "out": {
                            "success": True,
                            "unexpected_index_list": [4],
                            "unexpected_list": ["bee"],
                        },
                        "suppress_test_for": ["sqlite", "mssql"],
                        "include_in_gallery": True,
                    },
                ],
            }
        ],
        "library_metadata": {
            "contributors": ["@great_expectations"],
            "maturity": "production",
            "requirements": [],
            "tags": ["core expectation", "column map expectation"],
        },
        # "test_report": [
        #     {
        #         "test_title": "negative_test_insufficient_mostly_and_one_non_matching_value",
        #         "backend": "pandas",
        #         "success": "true",
        #     },
        #     {
        #         "test_title": "positive_test_exact_mostly_w_one_non_matching_value",
        #         "backend": "pandas",
        #         "success": "true",
        #     },
        # ],
    }


@pytest.mark.skip(
    reason="Timeout of 30 seconds reached trying to connect to localhost:8088 (trino port)"
)
@pytest.mark.all_backends
def test_expectation__get_renderers():
    expectation_name = "expect_column_values_to_match_regex"
    my_expectation = _registered_expectations[expectation_name]()

    from great_expectations.expectations.registry import (
        _registered_metrics,
        _registered_renderers,
    )

    # supported_renderers = my_expectation._get_registered_renderers(
    #     expectation_name,
    #     _registered_renderers,
    # )
    examples = my_expectation._get_examples()
    my_expectation_config = my_expectation._get_expectation_configuration_from_examples(examples)
    my_metric_diagnostics_list = my_expectation._get_metric_diagnostics_list(
        expectation_config=my_expectation_config
    )
    my_execution_engine_diagnostics = my_expectation._get_execution_engine_diagnostics(
        metric_diagnostics_list=my_metric_diagnostics_list,
        registered_metrics=_registered_metrics,
    )
    my_test_results = my_expectation._get_test_results(
        expectation_type=expectation_name,
        test_data_cases=examples,
        execution_engine_diagnostics=my_execution_engine_diagnostics,
        raise_exceptions_for_backends=False,
    )
    renderer_diagnostics = my_expectation._get_renderer_diagnostics(
        expectation_type=expectation_name,
        test_diagnostics=my_test_results,
        registered_renderers=_registered_renderers,
    )

    assert isinstance(renderer_diagnostics, list)
    assert len(renderer_diagnostics) == 10
    for element in renderer_diagnostics:
        print(json.dumps(element.to_dict(), indent=2))
        assert isinstance(element, ExpectationRendererDiagnostics)

    print([rd.name for rd in renderer_diagnostics])
    assert {rd.name for rd in renderer_diagnostics} == {
        "renderer.diagnostic.unexpected_statement",
        "renderer.diagnostic.meta_properties",
        "renderer.diagnostic.unexpected_table",
        "renderer.diagnostic.status_icon",
        "renderer.answer",
        "atomic.prescriptive.summary",
        "atomic.diagnostic.observed_value",
        "renderer.question",
        "renderer.prescriptive",
        "renderer.diagnostic.observed_value",
    }

    # assert renderer_diagnostics[0].to_dict() == {
    #     "name": "renderer.diagnostic.meta_properties",
    #     "is_supported": True,
    #     "is_standard": False,
    #     "samples": [
    #         ""
    #     ]
    # }

    # Expectation with no new renderers specified
    print([x for x in _registered_expectations if "second" in x])
    expectation_name = "expect_column_values_to_equal_three___second_iteration"
    my_expectation = _registered_expectations[expectation_name]()

    # supported_renderers = my_expectation._get_registered_renderers(
    #     expectation_name,
    #     _registered_renderers,
    # )
    examples = my_expectation._get_examples()
    my_expectation_config = my_expectation._get_expectation_configuration_from_examples(examples)
    my_metric_diagnostics_list = my_expectation._get_metric_diagnostics_list(
        expectation_config=my_expectation_config
    )
    my_execution_engine_diagnostics = my_expectation._get_execution_engine_diagnostics(
        metric_diagnostics_list=my_metric_diagnostics_list,
        registered_metrics=_registered_metrics,
    )
    my_test_results = my_expectation._get_test_results(
        expectation_type=expectation_name,
        test_data_cases=examples,
        execution_engine_diagnostics=my_execution_engine_diagnostics,
        raise_exceptions_for_backends=False,
    )
    renderer_diagnostics = my_expectation._get_renderer_diagnostics(
        expectation_type=expectation_name,
        test_diagnostics=my_test_results,
        registered_renderers=_registered_renderers,
    )

    assert isinstance(renderer_diagnostics, list)
    for element in renderer_diagnostics:
        print(json.dumps(element.to_dict(), indent=2))
        assert isinstance(element, ExpectationRendererDiagnostics)

    assert len(renderer_diagnostics) == 10
    assert {rd.name for rd in renderer_diagnostics} == {
        "renderer.diagnostic.observed_value",
        "renderer.prescriptive",
        "renderer.diagnostic.meta_properties",
        "renderer.diagnostic.status_icon",
        "renderer.diagnostic.unexpected_table",
        "atomic.diagnostic.observed_value",
        "atomic.prescriptive.summary",
        "renderer.answer",
        "renderer.question",
        "renderer.diagnostic.unexpected_statement",
    }

    # Expectation with no renderers specified
    print([x for x in _registered_expectations if "second" in x])
    expectation_name = "expect_column_values_to_equal_three___third_iteration"
    my_expectation = _registered_expectations[expectation_name]()

    # supported_renderers = my_expectation._get_registered_renderers(
    #     expectation_name,
    #     _registered_renderers,
    # )
    examples = my_expectation._get_examples()
    my_expectation_config = my_expectation._get_expectation_configuration_from_examples(examples)
    my_metric_diagnostics_list = my_expectation._get_metric_diagnostics_list(
        expectation_config=my_expectation_config
    )
    my_execution_engine_diagnostics = my_expectation._get_execution_engine_diagnostics(
        metric_diagnostics_list=my_metric_diagnostics_list,
        registered_metrics=_registered_metrics,
    )
    my_test_results = my_expectation._get_test_results(
        expectation_type=expectation_name,
        test_data_cases=examples,
        execution_engine_diagnostics=my_execution_engine_diagnostics,
        raise_exceptions_for_backends=False,
    )
    renderer_diagnostics = my_expectation._get_renderer_diagnostics(
        expectation_type=expectation_name,
        test_diagnostics=my_test_results,
        registered_renderers=_registered_renderers,
    )

    assert isinstance(renderer_diagnostics, list)
    assert len(renderer_diagnostics) == 10
    for element in renderer_diagnostics:
        print(json.dumps(element.to_dict(), indent=2))
        assert isinstance(element, ExpectationRendererDiagnostics)

    assert len(renderer_diagnostics) == 10
    assert {rd.name for rd in renderer_diagnostics} == {
        "renderer.diagnostic.observed_value",
        "renderer.prescriptive",
        "renderer.diagnostic.meta_properties",
        "renderer.diagnostic.status_icon",
        "renderer.diagnostic.unexpected_table",
        "atomic.diagnostic.observed_value",
        "atomic.prescriptive.summary",
        "renderer.answer",
        "renderer.question",
        "renderer.diagnostic.unexpected_statement",
    }


@pytest.mark.unit
def test_expectation_is_abstract():
    # is_abstract determines whether the expectation should be added to the registry (i.e. is fully implemented)  # noqa: E501 # FIXME CoP
    assert ColumnMapExpectation.is_abstract()
    assert not ExpectColumnValuesToEqualThree.is_abstract()


@pytest.mark.unit
def test_run_diagnostics_on_an_expectation_with_errors_in_its_tests():
    expectation_diagnostics = ExpectColumnValuesToEqualThree__BrokenIteration(
        column="values"
    ).run_diagnostics()
    # print(json.dumps(expectation_diagnostics.to_dict(), indent=2))

    tests = expectation_diagnostics["tests"]

    assert len(tests) == 5
    first_to_dict = tests[0].to_dict()
    del first_to_dict["validation_result"]
    assert first_to_dict == {
        "test_title": "positive_test_with_mostly",
        "backend": "pandas",
        "test_passed": True,
        "include_in_gallery": True,
        "error_diagnostics": None,
    }

    assert set(tests[3].keys()) == {
        "test_title",
        "backend",
        "test_passed",
        "include_in_gallery",
        "error_diagnostics",
        "validation_result",
    }
    assert tests[3]["test_passed"] is False

    assert set(tests[4].keys()) == {
        "test_title",
        "backend",
        "test_passed",
        "include_in_gallery",
        "error_diagnostics",
        "validation_result",
    }
    assert tests[4]["test_passed"] is False
