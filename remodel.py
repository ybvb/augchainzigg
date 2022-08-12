import augchainzigg as acz
import ziggurat as zigg
import os
import shutil
import numpy as np

zigg.road_to_ziggurat(testing=False)
acz.AugChainZigg.__setup__()
acz.AugChainZigg.infinite_load()
shutil.rmtree(zigg.remodel)

zigg.Tools.exists_path(zigg.remodel)
#for sybl in acz.AugChainZigg.aczswpss:
    #try: acz.Sts.Lstm.augchainzigg(sybl=sybl,col="XOR",path=zigg.remodel)
    #except ValueError: pass
    #try: acz.Sts.Lstm.augchainzigg(sybl=sybl,col="+CZ",path=zigg.remodel)
    #except (ValueError,IndexError): pass

for sybl in acz.AugChainZigg.aczswpss:
    try: acz.Sts.Lstm.augchainzigg(sybl=sybl,col="XOR",path=zigg.remodel)
    except ValueError: pass
    