import pathlib
import great_expectations as gx
import tempfile

temp_dir = tempfile.TemporaryDirectory()
full_path_to_project_directory = pathlib.Path(temp_dir.name).resolve()
data_directory = pathlib.Path(
    gx.__file__,
    "..",
    "..",
    "tests",
    "test_sets",
    "taxi_yellow_tripdata_samples",
).resolve(strict=True)

# <snippet name="tests/integration/docusaurus/expectations/how_to_edit_an_expectation_suite_no_validator.py get_data_context">
import great_expectations as gx

context = gx.data_context.FileDataContext.create(full_path_to_project_directory)
# </snippet>


context.sources.add_pandas(name="my_datasource",).add_csv_asset(
    name="my_data_asset", filepath_or_buffer="./data/yellow_tripdata_sample_2019-01.csv"
)

# <snippet name="tests/integration/docusaurus/expectations/how_to_edit_an_expectation_suite_no_validator.py get_data_asset_and_build_batch_request">
data_asset = context.get_datasource("my_datasource").get_asset("my_data_asset")
batch_request = data_asset.build_batch_request()
# </snippet>


# <snippet name="tests/integration/docusaurus/expectations/how_to_edit_an_expectation_suite_no_validator.py create_expectation_suite">
suite = context.add_expectation_suite(expectation_suite_name="my_suite")
# </snippet>

# <snippet name="tests/integration/docusaurus/expectations/how_to_edit_an_expectation_suite_no_validator.py create_expectation_1">
from great_expectations.core.expectation_configuration import ExpectationConfiguration

# Create an Expectation
expectation_configuration = ExpectationConfiguration(
    # Name of expectation type being added
    expectation_type="expect_table_columns_to_match_ordered_list",
    # These are the arguments of the expectation
    # The keys allowed in the dictionary are Parameters and
    # Keyword Arguments of this Expectation Type
    kwargs={
        "column_list": [
            "account_id",
            "user_id",
            "transaction_id",
            "transaction_type",
            "transaction_amt_usd",
        ]
    },
    # This is how you can optionally add a comment about this expectation.
    # It will be rendered in Data Docs.
    # See this guide for details:
    # `How to add comments to Expectations and display them in Data Docs`.
    meta={
        "notes": {
            "format": "markdown",
            "content": "Some clever comment about this expectation. **Markdown** `Supported`",
        }
    },
)
# Add the Expectation to the suite
suite.add_expectation(expectation_configuration=expectation_configuration)
# </snippet>

# <snippet name="tests/integration/docusaurus/expectations/how_to_edit_an_expectation_suite_no_validator.py create_expectation_2">
expectation_configuration = ExpectationConfiguration(
    expectation_type="expect_column_values_to_be_in_set",
    kwargs={
        "column": "transaction_type",
        "value_set": ["purchase", "refund", "upgrade"],
    },
    # Note optional comments omitted
)
suite.add_expectation(expectation_configuration=expectation_configuration)
# </snippet>

# <snippet name="tests/integration/docusaurus/expectations/how_to_edit_an_expectation_suite_no_validator.py create_expectation_3">
expectation_configuration = ExpectationConfiguration(
    expectation_type="expect_column_values_to_not_be_null",
    kwargs={
        "column": "account_id",
        "mostly": 1.0,
    },
    meta={
        "notes": {
            "format": "markdown",
            "content": "Some clever comment about this expectation. **Markdown** `Supported`",
        }
    },
)
suite.add_expectation(expectation_configuration=expectation_configuration)
# </snippet>

# <snippet name="tests/integration/docusaurus/expectations/how_to_edit_an_expectation_suite_no_validator.py create_expectation_4">
expectation_configuration = ExpectationConfiguration(
    expectation_type="expect_column_values_to_not_be_null",
    kwargs={
        "column": "user_id",
        "mostly": 0.75,
    },
    meta={
        "notes": {
            "format": "markdown",
            "content": "Some clever comment about this expectation. **Markdown** `Supported`",
        }
    },
)
suite.add_expectation(expectation_configuration=expectation_configuration)
# </snippet>

# TODO: update or replace expectation

# <snippet name="tests/integration/docusaurus/expectations/how_to_edit_an_expectation_suite_no_validator.py save_expectation_suite">
context.save_expectation_suite(expectation_suite=suite)
# </snippet>
