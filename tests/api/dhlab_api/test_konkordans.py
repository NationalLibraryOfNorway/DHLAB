import pytest
from tests.api.utils import TestFunctionAlias
import dhlab.api.dhlab_api as api

class TestGetDocumentCorpus(TestFunctionAlias):
    @pytest.fixture(autouse=True)
    def fn_alias(self):
        self.fn_alias = api.konkordans

    @pytest.fixture(autouse=True)
    def fn_orig(self):
        self.fn_alias = api.concordance

