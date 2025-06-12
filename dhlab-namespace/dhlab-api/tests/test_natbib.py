import pytest
from dhlab.metadata.natbib import metadata_query, metadata_from_urn
import pandas as pd

@pytest.mark.skip()
def test_metadata_query():
    conditions = [
        ["245", "a", "kongen"],
    ]
    res = metadata_query(conditions)
    assert len(res) > 0
    assert isinstance(res, list)


def test_metadata_from_urn():
    pass


def test_metadata():
    pass
