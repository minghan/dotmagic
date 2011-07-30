import os
import re

def import_all(blacklist=[]):
    """
    Returns a list of string of all the rctypes present 
    and attempts to import them
    """
    packpath = os.path.dirname(__file__)
    # listdir does not return . and ..
    # assumes that no *files* are folders
    # assmes that py modules are suffixed with *.py

    pattern = re.compile("^(.*).py$")
    blacklist.append('__init__')

    ok_list = []
    for f in os.listdir(packpath):
        res = pattern.match(f)
        if res is None: continue

        modname = res.group(1)
        if modname in blacklist: continue

        path = os.path.join(packpath, f)
        if os.path.isfile(path):
            try:
                __import__('%s.%s' % (__name__, modname), globals(), locals(), [], -1)
            except ImportError:
                pass
            else:
                ok_list.append(modname)

    return ok_list

