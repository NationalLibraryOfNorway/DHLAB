import pytest

import dhlab.api.dhlab_api as api
from tests.api.utils import TEST_PLACENAMES
from tests.api.dhlabtest import DHLabTest

class TestGeoLookup(DHLabTest):
    @pytest.fixture(autouse=True)
    def api_fn_fixture(self):
        self.api_fn = self.init_api_fn(
            api.geo_lookup, [TEST_PLACENAMES]
        )

