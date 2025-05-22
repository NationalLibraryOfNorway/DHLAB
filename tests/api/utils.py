from abc import abstractmethod
from typing import Callable
import pytest
import requests
from unittest.mock import MagicMock

TEST_URN_DIGIBOK = "URN:NBN:no-nb_digibok_2008091004038"
TEST_URN_LIST = [TEST_URN_DIGIBOK] # TODO: Add more URNs
TEST_PLACENAMES = ["Oslo", "London"]
TEST_WORDS = ["og", "eller"]
TEST_WORDS_COMMA_SEPARATED = ",".join(TEST_WORDS)
TEST_WORD = TEST_WORDS[0]
INVALID_URN = "Invalid URN 36b43144-94fc-43b2-ba26-f67570a217d9" # Randomly generated UUID

def _mocked_request_fn(
    request_fn,
    response: requests.Response,
    methods: list[str] | None = None,
    urls: list[str] | None = None,
):
    def wrapped_request_fn(*args, **kwargs) -> requests.Response:
        method = args[0] if len(args) > 0 else kwargs['method']
        url =    args[1] if len(args) > 1 else kwargs['url']

        if (methods is None or method in methods) and (urls is None or url in urls):
            resp = response
        else:
            resp = request_fn(*args, **kwargs)

        return resp
            
    return wrapped_request_fn

def mock_api_call(
    method: str | list[str] | None = None,
    url: str | list[str] | None = None,
    response: requests.Response | None = None,
    session: requests.Session | None = None,
) -> requests.Session:
    """Abstract away api-calling implementation details

    Modifies the passed `session`.

    :param method: Methods to mock the calls of (`"POST"`, `"GET"`, ...). If `None`, mock all calls.
    :param url: Urls to mock the calls of. If `None`, mock all calls.
    :param response: Desired response from api call. If `None`, initialized as `MagicMock(spec=Response())`
    :param session: `requests.Session` instance to modify. If `None`, create new `Session`.

    :return: Modified `session`.
    """
    if session is None:
        session = requests.Session()

    if response is None:
        response = MagicMock(spec=requests.Response)

    if isinstance(method, str):
        method = [method]
    if isinstance(url, str):
        url = [url]

    # XXX: Overwrites original session instance
    session.request = _mocked_request_fn(session.request, response, method, url)

    return session

class TestFunctionAlias():
    @abstractmethod
    @pytest.fixture(autouse=True)
    def fn_alias(self):
        ...

    @abstractmethod
    @pytest.fixture(autouse=True)
    def fn_orig(self):
        ...

    def test_alias_fn(self, fn_alias: Callable, fn_orig: Callable):
        assert fn_alias is fn_orig

        # TODO: assert original function is tested?

