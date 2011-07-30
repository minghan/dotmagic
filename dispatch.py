import sys, os
import yaml
import pprint as pp

FILENAME = ".dotmagic.yaml"

CONFIG = {}

def run():

    # read .dotmagic.yaml
    # load the yaml file

    env_map = {}

    homepath = os.getenv('HOME')
    path = os.path.join(homepath, FILENAME) 

    f = open(path)
    # use yaml.load(f) to load a single document
    doc = yaml.load(f)
    CONFIG = doc
    f.close()

    pp.pprint(doc)


    # parse the cmd line args

    try:
        cmd = sys.argv[1]
    except IndexError:
        print "Usage: %s [pull|checkout|try]" % (sys.argv[0])
        sys.exit()
    
    if cmd == 'repo':
        pass
    elif cmd == 'pull':
        pass
    elif cmd == 'checkout':
        pass
    elif cmd == 'try':
        pass

    
