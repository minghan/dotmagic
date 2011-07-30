import sys, os
import yaml
import pprint as pp
import lockfile
import urllib2
import tempfile

FILENAME = ".dotmagic.yaml"
LOCKFILE = "GLOBAL.LOCK"

CONFIG = {}
homepath = os.getenv('HOME')
magicpath = os.path.join(homepath, ".dotmagic")

def run():
    global CONFIG

    # read .dotmagic.yaml
    # load the yaml file

    env_map = {}

    path = os.path.join(homepath, FILENAME) 

    f = open(path)
    # use yaml.load(f) to load a single document
    doc = yaml.load(f)
    CONFIG = doc
    f.close()

    pp.pprint(CONFIG)


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
        checkout(param)
    elif cmd == 'try':
        pass

    

def fetch(user):
    global CONFIG

    lockpath = os.path.join(magicpath, LOCKFILE)
    lock = lockfile.FileLock(lockpath)
    
    # acquire the global lock
    try:
        lock.acquire(timeout=5)
    except lockfile.LockTimeout:
        sys.stderr.write("dotmagic is currently running. Please try again later.\n")
        return

    # download tar file
    try:
        url = "/".join([CONFIG["REPO"], "api", "fetch", user]);
        print("Attempting to download from %s..." % url) # TODO: do we need a progress bar?
        infile = urllib2.urlopen(url)
    except urllib2.URLError:
        sys.stderr.write("Error downloading for user %s. Check your repo configuration.\n" % user)
        return

    outfile = tempfile.NamedTemporaryFile()
    outfile.write(infile.read())
    outfile.flush()
    
    # create the output directory, empty it, then untar into it
    os.system("mkdir -p %s/repo/%s" % (magicpath, user))
    os.system("rm -rf %s/repo/%s/*" % (magicpath, user))
    os.system("tar -xvzf %s -C %s/repo/%s" % (outfile.name, magicpath, user))
    outfile.close()

    # now we unlock the filelock
    lock.release()
    return

def checkout(user):
    lockpath = os.path.join(magicpath, LOCKFILE)
    lock = lockfile.FileLock(lockpath)
    
    # acquire the global lock
    try:
        lock.acquire(timeout=5)
    except lockfile.LockTimeout:
        sys.stderr.write("dotmagic is currently running. Please try again later.\n")
        return

    userpath = os.path.join(magicpath, "repo", user)
    if not os.path.exists(userpath):
        sys.stderr.write("Could not find user %s data. Did you forget to do 'dotmagic fetch %s'?" % (user, user))
        return

    # check if we need to backup the data first
    # if backup directory already exists, then we do not need to :)
    backuppath = os.path.join(magicpath, "backup")
    need_backup = not os.path.exists(backuppath)

    if need_backup:
        os.system("mkdir -p %s" % backuppath)

    filelist = os.listdir(userpath)
    print("Files in userpath: %s" % filelist)
    unrecognized = []
    for filename in filelist:
        if filename == "meta.yaml":
            continue

        # assume we have the whitelist
        #if filename in globals():
        #    whitelist = globals()[filename].WHITELIST
        #else:
        #    unrecognized.append(filename)
        #    continue

        if filename != "vim":
            continue

        whitelist = [".vimrc", ".vim"]

        for f in whitelist:
            fulluserpath = os.path.join(userpath, f)
            fullhomepath = os.path.join(homepath, f)
            if os.path.exists(fulluserpath):
                if os.path.isdir(fulluserpath):
                    cmd = "cp -R %s %s"
                else:
                    cmd = "cp %s %s"

                if need_backup:
                    os.system(cmd % (fullhomepath, backuppath))

                os.system(cmd % (fulluserpath, fullhomepath))

    if unrecognized:
        sys.stderr.write("Rcfiles for these programs could not be loaded: %s\n" % " ".join(unrecognized))

    lock.release()
    return
