import requests
import unittest.mock
from dhlab.api.nb_ngram_api import get_ngram
from dhlab.api.utils import DHLabApiError
import pytest


@pytest.mark.parametrize(
    "status_code", [404, 500, 504, 418,]
)
def test_empty_list_on_non_200_status(status_code: int) -> None:
    """Empty list should be returned if the response status code is not 200"""
    session = unittest.mock.MagicMock(spec=requests.Session)
    session.get.return_value.status_code = status_code

    with pytest.raises(DHLabApiError):
        get_ngram("test", session=session)


def test_deserialised_on_200_status() -> None:
    """Deserialised JSON should be returned if the response status code is 200"""
    session = unittest.mock.MagicMock(spec=requests.Session)
    session.get.return_value.status_code = 200
    session.get.return_value.text = '[{"test_key": "test_value"}]'

    assert get_ngram("test", session=session) == [{"test_key": "test_value"}]
