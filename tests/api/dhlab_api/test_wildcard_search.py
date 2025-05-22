import pytest
import pandera as pa

import dhlab.api.dhlab_api as api
from tests.api.dhlabtest import DHLabTest

class TestWildcardSearch(DHLabTest):
    @pytest.fixture(autouse=True)
    def api_fn_fixture(self):
        self.api_fn = self.init_api_fn(
            api.wildcard_search,
            args=["ord*en*"]
        )

    def test_returned_df_schema(self):
        ret = self.call_api_fn()

        # Docstring assumes this dataframe schema:
        schema = pa.DataFrameSchema(
            {"freq": pa.Column(int)},
            index=pa.Index(str)
        )

        schema.validate(ret)

