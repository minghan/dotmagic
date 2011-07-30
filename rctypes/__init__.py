import os
import re
        

packpath = os.path.dirname(__file__)

def import_mod(modname):

    modname = str(modname).lower()

    path = os.path.join(packpath, modname + ".py")
    if os.path.isfile(path):
        try:
            __import__('%s' % __name__, globals(), locals(), [modname])
            return True
        except ImportError:
            return False

def import_all(blacklist=[]):
    """
    Returns a list of string of all the rctypes present 
    and attempts to import them
    """
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

        if import_mod(modname):
            ok_list.append(modname)

    return ok_list

