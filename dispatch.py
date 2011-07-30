import sys, os
import yaml
import pprint as pp
import lockfile
import urllib2

FILENAME = ".dotmagic.yaml"
LOCKFILE = ".dotmagic/GLOBAL.LOCK"

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
        if cmd != "restore":
            param = sys.argv[2]
    except IndexError:
        print "Usage: %s [fetch|checkout|try] [param]\n       %s [restore]" % (sys.argv[0], sys.argv[0])
        sys.exit()
    
    if cmd == 'repo':
        pass
    elif cmd == 'fetch':
        fetch(param)
    elif cmd == 'checkout':
        pass
    elif cmd == 'try':
        pass

    

def fetch(user):
    homepath = os.getenv('HOME')
    lockpath = os.path.join(homepath, ".dotmagic", "GLOBAL.LOCK")
    lock = FileLock(lockpath)
    
    try:
        lock.acquire(timeout=5)
    except LockTimeout:
        sys.stderr.write("dotmagic is currently running. Please try again later.\n")
        return

    # lock is now acquired!

    # download tar file
    infile = urllib2.urlopen("/".join([CONFIG["REPO"], "api", "fetch", user]))
    outfile = tempfile.NamedTemporaryFile()
    outfile.write(infile.read())
    
    # create the output directory
    os.system("mkdir -p ~/.dotmagic/repo/%s" % user)
    os.system("tar -xvzf %s -C ~/.dotmagic/repo/%s" % (outfile.name, user))
    outfile.close()

    # now we unlock the filelock
    lock.release()
