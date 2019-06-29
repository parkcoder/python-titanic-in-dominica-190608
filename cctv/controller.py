from cctv.cctv_pop import CCTVModel
from cctv.crime_police import CrimeModel
from cctv.police_norm import PoliceNormModel

class CCTVController:
    def __init__(self):
        # self._m = CCTVModel()
        # self._m = CrimeModel()
        self._m = PoliceNormModel()

    def test(self):
        m = self._m
        m.hook()


