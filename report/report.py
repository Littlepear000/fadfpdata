from fadfpdata.myclass.ecosdata import EcosData
from fadfpdata.utils.core import *
from fadfpdata.myclass.weovint import WeoVint

class report:
    def __init__(
            self,
            ecosdatav: str = 'latest',
            weovintv: str = 'latest',
            dummyv: str = 'latest',
    ):
        self.ecosdatav = ecosdatav
        self.weovintv = weovintv
        self.dummyv = dummyv

        self.ecosdatad = EcosData(version=self.ecosdatav)
        self.weovintd = WeoVint(version=self.weovintv)
        self.dummyd = Dummy(version=self.dummyv)