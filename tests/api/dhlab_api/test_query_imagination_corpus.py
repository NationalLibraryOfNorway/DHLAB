import dhlab.api.dhlab_api as api
from tests.api.dhlabtest import DHLabTest

import pytest

class TestQueryImaginationCorpus(DHLabTest):
    @pytest.fixture(autouse=True)
    def api_fn_fixture(self):
        self.api_fn = self.init_api_fn(
            api.query_imagination_corpus,
        )

