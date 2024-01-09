import pytest
import dhlab as dh
import pandas as pd

test_urns = """URN:NBN:no-nb_digibok_2008091004038
URN:NBN:no-nb_digibok_2021030248529
URN:NBN:no-nb_digibok_2020100607613"""

urns = test_urns.split()

pytestmark = pytest.mark.parametrize("urn", urns)

class TestDispersion:

    def test_dispersion(self, urn):
        d = dh.Dispersion(urn, wordbag = ['han', 'hun'])
        assert isinstance(d.dispersion, pd.DataFrame)
        assert isinstance(d.frame, pd.DataFrame)
        assert isinstance(d, dh.Dispersion)
        assert len(d.dispersion) > 0
        assert len(d.dispersion.columns) == 2
        
    def test_dispersion_dict(self, urn):
        d = dh.Dispersion(urn, wordbag = {'han':['han', 'hun']})
        assert isinstance(d.dispersion, pd.DataFrame)
        assert len(d.dispersion) > 0
        assert len(d.dispersion.columns) == 1
        
    def test_dispersion_str(self, urn):
        d = dh.Dispersion(urn, wordbag = 'han')
        assert isinstance(d.dispersion, pd.DataFrame)
        assert len(d.dispersion) > 0
        assert len(d.dispersion.columns) == 1
        
    def test_plot(self, mocker, urn):
        d = dh.Dispersion(urn, wordbag = 'han')
        mock_plot = mocker.patch('dhlab.Dispersion.plot')
        d.plot()
        mock_plot.assert_called_once()