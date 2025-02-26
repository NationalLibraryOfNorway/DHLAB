import pytest

import dhlab.api.dhlab_api as api
from tests.api.utils import TEST_WORDS
from tests.api.dhlabtest import DHLabTest

class TestWordParadigmMany(DHLabTest):
    @pytest.fixture(autouse=True)
    def api_fn_fixture(self):
        self.api_fn = self.init_api_fn(
            api.word_paradigm_many, [TEST_WORDS]
        )

