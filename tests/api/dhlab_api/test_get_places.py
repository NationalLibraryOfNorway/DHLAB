import pytest

import dhlab.api.dhlab_api as api
from tests.api.utils import TEST_URN_DIGIBOK
from tests.api.dhlabtest import DHLabTest

class TestGetPlaces(DHLabTest):
    @pytest.fixture(autouse=True)
    def api_fn_fixture(self):
        self.api_fn = self.init_api_fn(
            api.get_places, [TEST_URN_DIGIBOK]
        )

