import glob
import pytest

import great_expectations as gx

from great_expectations.data_context.util import file_relative_path
from tests.test_utils import _get_batch_request_from_validator
from tests.datasource.new_fixtures import (
    test_dir_oscar
)

# !!!
@pytest.mark.skip(reason="Temporarily broken 6/16; Will re-enable after fixing.")
def test_ZEP_scenario_1(test_dir_oscar):
    context = gx.get_context(lite=True)

    # Use the built-in datasource to get a validator, runtime-style
    my_validator_1 = context.sources.default_pandas_reader.read_csv(test_dir_oscar+"/A/data-202201.csv")
    my_validator_1.head()
    my_validator_1.expect_column_values_to_be_between("x", min_value=1, max_value=2)

    # Add a configured asset and use it to fetch a Validator
    context.sources.default_pandas_reader.add_asset(
        name="oscar_A",
        base_directory=test_dir_oscar+"/A",
    )
    my_batch_request_2 = context.sources.default_pandas_reader.assets.oscar_A.get_batch_request(
        filename="data-202202.csv"
    )
    my_validator_2 = context.sources.default_pandas_reader.assets.oscar_A.get_validator(
        filename="data-202202.csv"
    )
    my_validator_2.head()
    my_validator_2.expect_column_values_to_be_between("x", min_value=1, max_value=2)

    return
    # Refine the asset configuration by adding a more detailed regex
    context.sources.default_pandas_reader.add_asset(
        name="oscar_A",
        base_directory=test_dir_oscar+"/A",
        regex="file-(.*)/.csv",
        batch_identifiers=["number"]
    )
    # context.sources.default_pandas_reader.assets.oscar_A.list_batches()
    my_batch_request_3 = context.sources.default_pandas_reader.assets.oscar_A.get_batch_request(
        number=1
    )
    # my_validator_3 = context.sources.default_pandas_reader.assets.oscar_A.get_validator(
    #     number=1
    # )
    # my_validator_3.head()
    # my_validator_3.expect_column_values_to_be_between("x", min_value=1, max_value=2)

    # Get a batch request spanning multiple files, and use it to configure a profiler
    #!!! Need to figure out the syntax for BatchRequests that can span ranges and multiple Batches.
    #!!! This implementation strikes me as error-prone.
    # my_batch_request = context.sources.default_pandas_reader.assets.my_asset.get_batch_request()
    # assistant_result = context.assistants.onboarding.run(my_batch_request)

    # Add multiple assets
    # !!! DX TBD

    # Add a checkpoint to routinely check this in the future
    # !!! DX TBD
    # context.add_checkpoint()


@pytest.mark.skip(reason="Doesn't work yet")
def test_ZEP_scenario_2(test_dir_alpha):
    context = gx.get_context(lite=True)

    # !!! DX TBD
    context.add_sql_datasource(
        name="my_sqlite_db",
        connection_string="postgresql+psycopg2://user:password@hostname/database_name"
    )
    # Use the built-in datasource to get a validator, runtime-style
    my_validator_1 = context.sources.my_sqlite_db.read_table("users")
    my_validator_1.head()
    my_validator_1.expect_column_values_to_be_between("x", min_value=1, max_value=2)

    # Add a single configured asset
    context.sources.my_sqlite_db.add_asset(
        name="my_asset",
        base_directory=test_dir_alpha,
    )
    return
    my_validator_2 = context.sources.default_pandas_reader.assets.my_asset.get_validator(
        filename="B.csv"
    )
    my_validator_2.head()
    my_validator_2.expect_column_values_to_be_between("x", min_value=1, max_value=2)

    # Refine the asset configuration by adding a more detailed regex
    context.sources.default_pandas_reader.add_asset(
        name="my_asset",
        base_directory=test_dir_alpha,
        regex="(.*)\\.csv",
    )
    my_validator_3 = context.sources.default_pandas_reader.assets.my_asset.get_validator(
        filename="B"
    )
    my_validator_3.head()
    my_validator_3.expect_column_values_to_be_between("x", min_value=1, max_value=2)

    # Get a batch request spanning multiple files, and use it to configure a profiler
    #!!! Need to figure out the syntax for BatchRequests that can span ranges and multiple Batches.
    #!!! This implementation strikes me as error-prone.
    my_batch_request = context.sources.default_pandas_reader.assets.my_asset.get_batch_request()
    assistant_result = context.assistants.onboarding.run(my_batch_request)

    