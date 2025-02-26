import pytest

import dhlab.api.dhlab_api as api
from tests.api.utils import TEST_WORD
from tests.api.dhlabtest import DHLabTest

class TestWordForm(DHLabTest):
    @pytest.fixture(autouse=True)
    def api_fn_fixture(self):
        self.api_fn = self.init_api_fn(
            api.word_form, [TEST_WORD]
        )

