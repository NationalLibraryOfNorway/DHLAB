import pytest

import dhlab.api.dhlab_api as api
from tests.api.dhlabtest import DHLabTest

class TestGetDispersion(DHLabTest):
    @pytest.fixture(autouse=True)
    def api_fn_fixture(self):
        self.api_fn = self.init_api_fn(
            api.get_dispersion,
        )

