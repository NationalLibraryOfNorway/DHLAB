from abc import ABC, abstractmethod
import functools
from typing import Any, Callable
from unittest.mock import MagicMock
import warnings
import inspect
import pytest
import requests
from typeguard import typechecked
from dhlab.api.utils import DHLabApiError
import tests.api.utils as apitest


class DHLabTest(ABC):
    api_ret = {}

    @abstractmethod
    @pytest.fixture(autouse=True)
    def api_fn_fixture(self) -> functools.partial:
        """Set api_fn to be tested. Should usually be called with set_api_fn."""
        ...

    @staticmethod
    def _test_alias_fn(fn_alias: Callable, fn_orig: Callable):
        assert inspect.isfunction(fn_alias)
        assert inspect.isfunction(fn_orig)
        assert fn_alias is fn_orig

        # TODO: assert original function is tested?

    @staticmethod
    def init_api_fn(
        api_fn: Callable,
        args: list | None = None,
        kwargs: dict[str, Any] | None = None,
        typecheck: bool = True,
        aliased_fn: Callable | None = None,
    ):
        """api_fn needs to be defined as a pytest fixture in every file containing an inheriting class."""
        if aliased_fn:
            DHLabTest._test_alias_fn(api_fn, aliased_fn)
            pytest.skip(allow_module_level=True)

        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}

        if typecheck:
            api_fn = functools.wraps(api_fn)(typechecked(api_fn))

        return functools.partial(api_fn, *args, **kwargs)

    def call_api_fn(self, _cache: bool = True, **kwargs):
        if _cache:
            cache_key = frozenset(kwargs.items())
            if cache_key in self.api_ret:
                return self.api_ret[cache_key]

        try:
            ret = self.api_fn(**kwargs)
        except DHLabApiError:
            # args/kwargs from the partial function are shown at `{self.api_fn}`
            warnings.warn(f"Server error when calling {self.api_fn}, {kwargs=}. Skipping test.")
            pytest.skip()

        if _cache:
            self.api_ret[cache_key] = ret

        return ret

    @pytest.mark.parametrize("error_status_code", (404, 500, 504, 418,))
    def test_error_status_codes(self, error_status_code):
        mock_response = MagicMock(spec=requests.Response)
        mock_response.reason = "Mocked reason"
        mock_response.status_code = error_status_code
        session = apitest.mock_api_call(response=mock_response)

        with pytest.raises(DHLabApiError):
            self.api_fn(session=session)

    def test_call(self):
        self.call_api_fn(_cache=False)

