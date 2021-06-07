import re
from os import getenv, path



excluded_headers = [
    'content-encoding',
    'content-length',
    'transfer-encoding',
    'connection',
    'Authorization'
]


def getFilename_fromCd(cd):

    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None

    return fname[0]


def getAbsoluteRelative(path_, absolute=True):
    if absolute:
        return path_.replace('%DATA_STORAGE%', getenv('DATA_STORAGE'))
    else:
        return path_.replace(getenv('DATA_STORAGE'), '%DATA_STORAGE%')
