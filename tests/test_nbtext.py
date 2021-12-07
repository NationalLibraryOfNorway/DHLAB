import pytest
from dhlab import nbtext


@pytest.mark.parametrize(
    "input_data",
    [
        "https://www.nb.no/items/URN:NBN:no-nb_digibok_2019100726008",
        "URN:NBN:no-nb_digibok_2019100726008",
        "digibok_2019100726008",
        ["2019100726008", "2019100726008", "2019100726008"]
    ]
)
def test_pure_urn(input_data):
    # when
    result = set(nbtext.pure_urn(input_data))
    # then
    assert len(result) == 1
    assert result == {"2019100726008"}
