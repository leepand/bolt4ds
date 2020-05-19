import numpy as np
import pandas as pd
import scipy
import sklearn as skl

__author__ = 'leepand'
__weixin__ = 'pandasasa'


def _parse_version(version_string):
    """
    根据库中的__version__字段，转换为tuple，eg. '1.11.3'->(1, 11, 3)
    :param version_string: __version__字符串对象
    :return: tuple 对象
    """
    version = []
    for x in version_string.split('.'):
        try:
            version.append(int(x))
        except ValueError:
            version.append(x)
    return tuple(version)


"""numpy 版本号tuple"""
np_version = _parse_version(np.__version__)
"""sklearn 版本号tuple"""
skl_version = _parse_version(skl.__version__)
"""pandas 版本号tuple"""
pd_version = _parse_version(pd.__version__)
"""scipy 版本号tuple"""
sp_version = _parse_version(scipy.__version__)
#pd_version




def _default_index(n):
    from pandas import RangeIndex
    return RangeIndex(0, n, name=None)