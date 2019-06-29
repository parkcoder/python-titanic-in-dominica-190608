from cctv.cctv_pop import CCTVModel
from cctv.crime_police import CrimeModel

class CCTVController:
    def __init__(self):
        # self._m = CCTVModel()
        self._m = CrimeModel()

    def test(self):
        m = self._m
        m.hook()


