import gzip
import base64
import os
from pathlib import Path
from typing import Dict


# this is base64 encoded source code
file_data: Dict = {'dspipe/run.py': 'H4sIAB/m3l4C/5VTy27bMBC86ysW8UUCBClWmwAt4FPT9tJbczc25NoiQpECd2nX/fqSkmIIqNHHRQ8OObszOzTD6IPAi7fyXnNzsP4MyKAfJX8WZobV4ViDIL9yDSfDEa35SUWxgU89qdcJAU0jOU1OGWJAp0F6MgHoB6koxjtgQYlcLNTNGOhk6FxOtM1zej4HNK6sqkz8eTpGmQQGr8mCZNS441zNOGWjzr/rug18J4JeZOSPbftWKRDqxKO94sb4llxrUYilDdE1vQz22lNauNXPZo1/Jfnmj8Y9oWBZ1awSc7QU9r1n2d09dE3XbZvu/l2zffhwt8Kzk7tt97itrVdo91dk9wUt0yQ7MoGPMkYprj43qFQMqC5ltVocrZf9PB50iriczqse3ZFgxIADCYVpEIFS3zXw/1iD+jSR/N0f7fdplGPwqQlepFS3ur+1ETbzOGfNYHjVOo+kzMGorGuSAHM6DxlUKROLWn5L6fyy5qW4fiWB1qMuU4Cr31cnKZNvjBe4+Lgwasjy0qDzjOtUnEkArZ2vwJK4nL2U6tXOq03GnZJ2nZzca392LMnmYWXcsj+lB26l/x9uyJ8D+ws98yvB1QMAAA==', 'dspipe/cfg.py': 'H4sIAB/m3l4C/22NMQrDMAxFd59C0MEOBJNkyFDILboHY4ticGIjKdDcvnZDO1WT9Ph6P+S1EBbKHplhgQcdqFTcSiaB4AQlbqiCrCyukuXHbFvMNExDP/dj1yK4h/+BcWoJdYOUXYBaJugFA3jCgLtEl1gJnXcFdb7ds5RY8IMOik18EXtITGyb6nRbMto2Ddt26M4+UYyuD7pT+PJY5LIWx/wGshwvjOwAAAA=', 'dspipe/tasks.py': 'H4sIAB/m3l4C/7VVy27bMBC86ysI+CAJsOU0CIrAgIqiLdL2ZrS9BYbBiCubDUUqJJUgKPrv3aWedpO06cPwQSJ3hzPL2dVMVrWxnomXvlTmLuper4zyZ8JltMa4e2o789xdu35HNXIn+xd3rYBbPe8fMsExGLyLSmuqYRW0g+pKAevSPnEtTHVhLDj/VnHnZCnB9qA17iIj/NciivrVotxF0YwJKKUGdmfsdeBbUDr7ggzfg3+HpyedkpZ1Rjvrm3WATFeMzZjjt8CIZ2l5BeEYbm8a8KgCgO29r91quexhLHDh9yBM4TJplqCXinvkvfTc7lBptveVihj+hN86XPQsb4uUIR1YczrFg02QOW+Uz1FI1oemyKeXQjTaUJexz89hwsVtyD2gAlr8HhEMTEOSKxC8UWC3e+NGFWNiiArwHUKsTMEVRcfzyaYrrKy9NDqPP+CepjKbklW82NPd2UZrqXfMQmU8jMdOMAqjS7nb1tzvcyELnzgoWsACTRPPGWHmccdjMUAsApf0WE8wUK/no/ZPSDo/OT99RMuaUFDHMW/Ga8lqawpw7l9oILakIep4UcEwWZXpagCXVjpUdNx2mTJcbGkzSUcR5dZbLjXG14K8wC9IfkJhIXNeGNVU2uWXcQncNxa+fY+z0tiK+0SmDJ+YZAhgud5BcpZufga/jO/jDZ4QQNvWGGJmzIQScrUa48dEpADx5lVOEofO2AzZYZmaNulTqGtuGllcq/ujbo6i12O3YAgOmGQyGyixGyACajQ+6OL+mc3WjpXQaePsWVvoDPDk+Glv1GzrIXxw5Rtj1CMtOo0nBcOcCBcz7lFP3YNbavOkdSZ2CKWVum58kgbrJNPS0gLryihCjZ89IftSzQhrEU5aENDo47IlcSBy5Drlm0mcNper+WrxYjOx/oH+zOE8Go0yTUl/YahgJGLMTOOR559rJaRFC9KKfcSU64Nb/S++/ELqHrIk3TDg97DT3bIN38Kw8xcGGsIqI0BhzMMf+0Rvv5orl5/OaapgALW9h/zkCCArpX/wPueHo+eh6w0A6Q+tM9zBAQkAAA==', 'dspipe/__init__.py': 'H4sIAB/m3l4C/wMAAAAAAAAAAAA=', 'dspipe/visualize.py': 'H4sIAB/m3l4C/62SwWrEIBCG73mK3KKQTul1IdeeC93bsoRZnQRZo+KYpfv2Nclm27QLvVREnNFv/H/VDMHHVPLZEkZXmCVMyGdeg4BOI5e5B12sSdX1RaGpK1GpMaK6Cu3bEClEr4i5yeuwychdUeY2eE22bJYTYJ/HfUTjftBbEvyYwpiEBOtRCzkX0l2bJnJT6+0OicdUiMYlcXMLA6VoFMPqoWXlI4m19KG6Vsd6VgxZjjYq3dfAWK8Ou3r39HKUUi53EaxP7XJB6LIK8Yfp/3SWqa+TMxo0vFM0WcRioCNMY6Tv8tq6NE7TR/PIFChvx8HxUv326gOmyaM1JwjXaTb/Cpt+KwDOk/aCdswKkBU5bVzfvKJlkjChcMK4vopNwHihzvSiykYzys/znuD6Sn4ClRfcn6QCAAA=', 'dspipe/export.py': 'H4sIAB/m3l4C/5VRPW/bMBDd9SsO8GAZMKgl6BDAW5uMHRogY8CIJ4sIxRPIYxz/+95RktumXapB0n29e+/dDn6MNvl4hmdKb0OgSwYbHXwvPBfOzQ4yIozMc77vOveFtcUktI5HdNRn46nD2AXLmLnrKQT7SkkiM/IUGj/NlBheKfCdy0anwWZYgf5VNrOfMTdbiW1+k2gHtjBBtu+4DYOzbEGSEusMJJyp6YfzS41OsNdvtBPul2yiwYdacDjYEnjfbILqTuOj53YDOK79p99mjxCot6HWT0+p4AF2cBHjwMelBBM5hMGnzEoaP7AvLAkVq1Jke1VknuT9iPxVNLSHG49UYqt1xaV6gqp7suwFPFyrAU63VY3OJ+yZ0vVm0BkjqvugdDMMlBabeoq5TJjUL1nySfiD/H77UL/r9uPmwcFseMJRVlxGjHClAjap3dZdFW8ueVzZHnVRFE51D04kTBSocfRS207wYEPGxg+wpu4bkOe/D5EwIy83qADrzf/EOSNXiHbp2dUuM5cgJ0z47vHyd6X9hWeU36fOW749/AQCGRaFPAMAAA==', 'setup.py': 'H4sIAB/m3l4C/0srys9VKE4tKS0oyc/PKVbIzC3ILyqBiOgopGXmpcQXJCZnJ6anFnNxgUU1uBSAIC8xN9VWPaW4ILMgVV0HLFSWWlScmZ9nq26gZwgVgmm1RTFIQ1OHSxMAGQWxpHkAAAA=', 'dspipe/README.md': 'H4sIAB/m3l4C/41SwY7UMAy95yss7QGQmPbCaW8IiRNISMsFIbTjpm6bndSJEoeZ8vU4me4CKw57apo8Pz+/5xsYgpd3Y+4mH85wgC8pPJAV+Epr9CiUzc0NfPCEDMgjZIseB08Qd1yWVKyURDCFBCMKKsYR2ydINuaJDM5OFrBhXQPDSNnNDBFFKHFuBItIzLd9PyuuDJ0ie08UtXW/C+2rUFNV3T22NuYomE9d3I63cA7p1GapVxnAHO00X58iJlxJm7VRgix6soEnN1dYKnyF0YVsEfoP00+XC3r3i67AkglCkVjkKn4qqXEio9+ye1bi4sbDsyrH8FDiViVxEBpCONWizibSSDZcvRaEKC4oJUxOjW8OqrWi1tIIFUksDn1j+15rqpgV5cfrRzfHYHOHnJ0m1zzdz30LRfpEE6Wa2T3GSDw6S7n/9v7zp7uNBS/dIqt/87ZKbNm52lgCaEj1s4v5RwqYP3szJGS7GPNRLUoUCUU9wJlgCwXGwK8EmJQRvQdZgtpTmyhTbjlZpaieqbVg/yLslD4w6dSqQW/p4rI4nnV6P6qhJdefYxVpG/Aw7PWHQ33ydLgSvWTpxnwv+xJ3lbE7mt9ZbPhCOwMAAA==', 'dspipe/reports/README.md': 'H4sIAB/m3l4C/1NWVihKLcgvKilW0C3IS9fT0wMADNJGVRIAAAA='}


for path, encoded in file_data.items():
    print(path)
    path = Path(path)
    path.parent.mkdir(exist_ok=True)
    path.write_bytes(gzip.decompress(base64.b64decode(encoded)))


def run(command):
    os.system('export PYTHONPATH=${PYTHONPATH}:/dspipe/working && ' + command)


run('python setup.py develop --install-dir /dspipe/working')
run('python dspipe/run.py')
