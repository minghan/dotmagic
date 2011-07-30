import sys, os
import yaml
import pprint as pp
import lockfile
import urllib2
import tempfile
import subprocess

import rctypes

FILENAME = ".dotmagic.yaml"
LOCKFILE = "GLOBAL.LOCK"

CONFIG = {}
homepath = os.getenv('HOME')
magicpath = os.path.join(homepath, ".dotmagic")
configpath = os.path.join(homepath, FILENAME) 

def run():

    # read .dotmagic.yaml
    # load the yaml file

    env_map = {}

    global CONFIG
    f = open(configpath)
    CONFIG = yaml.load(f)
    f.close()

    #pp.pprint(CONFIG)

    lockpath = os.path.join(magicpath, LOCKFILE)
    lock = lockfile.FileLock(lockpath)
    
    # acquire the global lock
    try:
        lock.acquire(timeout=5)
    except lockfile.LockTimeout:
        sys.stderr.write("dotmagic is currently running. Please try again later.\n")
        return
        
    # parse the cmd line args

    callee = sys.argv[0]

    try:
        cmd = sys.argv[1]
        if cmd == 'fetch' or cmd == 'checkout':
            param = sys.argv[2]
    except IndexError:
        usage(callee)


    if cmd == 'restore':
        restore()
    elif cmd == 'fetch':
        fetch(param)
    elif cmd == 'checkout':
        checkout(param)
    elif cmd == 'try':
        try:
            user = sys.argv[2]
            params = sys.argv[3:]
        except IndexError:
            pass
        else:
            tryuser(user, params)
    elif cmd == 'config':
        config(sys.argv[2:])
    else:
        usage(callee)

    # now we unlock the filelock
    lock.release()
    
def usage(prog):
    print "Usage: %s [fetch|checkout] <param>" % prog
    print "       %s [try] <user> <program>" % prog
    print "       %s [restore]" % prog
    return

def fetch(user):
    # download tar file
    try:
        url = "/".join([CONFIG['repo'], "api", "fetch", user]);
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

    return

def checkout(user):
    userpath = os.path.join(magicpath, "repo", user)
    if not os.path.exists(userpath):
        sys.stderr.write("Could not find user %s data. Did you forget to do 'dotmagic fetch %s'?" % (user, user))
        return

    backuppath = os.path.join(magicpath, "backup")

    filelist = os.listdir(userpath)
    unrecognized = []

    types_list = rctypes.import_all()

    for filename in filelist:
        if filename == "meta.yaml":
            continue

        if filename not in types_list: continue
        mod = sys.modules['dotmagic.rctypes.%s' % filename]
        whitelist = mod.WHITELIST

        # check if we need to backup this path
        fullbackuppath = os.path.join(backuppath, filename)
        need_backup = not os.path.exists(fullbackuppath)
        if need_backup:
            print("Creating backup: mkdir -p %s" % fullbackuppath)
            os.system("mkdir -p %s" % fullbackuppath)

        for f in whitelist:
            fulluserpath = os.path.join(userpath, filename, f)
            fullhomepath = os.path.join(homepath, f)
            print("Check if %s exist" % fulluserpath)
            if os.path.exists(fulluserpath):
                print("%s exists!" % fulluserpath)
                if os.path.isdir(fulluserpath):
                    cmd = "cp -R %s %s"
                else:
                    cmd = "cp %s %s"

                if need_backup:
                    print("Running %s" % (cmd % (fullhomepath, fullbackuppath)))
                    os.system(cmd % (fullhomepath, fullbackuppath))

                print("Running %s" % (cmd % (fulluserpath, homepath)))
                os.system(cmd % (fulluserpath, homepath))

    if unrecognized:
        sys.stderr.write("Rcfiles for these programs could not be loaded: %s\n" % " ".join(unrecognized))

    return


def tryuser(user, params):
    rctype = os.path.basename(params[0])

    userpath = os.path.join(magicpath, "repo", user)
    if not os.path.exists(userpath) or not rctypes.import_mod(rctype):
        sys.stderr.write("User invalid or rctype unsupported")
        return

    mod = sys.modules['dotmagic.rctypes.%s' % rctype]
    whitelist = mod.WHITELIST

    dirpath = os.path.join(magicpath, 'tmp', rctype) # ~/.dotmagic/tmp/vim/
    os.system("mkdir -p %s" % dirpath)
    for f in whitelist:
        # backup the file to ~/.dotmagic/tmp/rctype/
        oldpath = os.path.join(homepath, f)
        newpath = os.path.join(magicpath, "tmp", rctype, f)
        if os.path.exists(oldpath):
            cmd = "mv -f %s %s" % (oldpath, newpath)
            os.system(cmd)

        # copy in the correct file
        repopath = os.path.join(magicpath, "repo", user, rctype, f)
        if os.path.exists(repopath):
            os.system("cp -rf %s %s" % (repopath, oldpath))

    # run the prog
    p = subprocess.Popen(params)
    p.wait() # block

    # restore the files
    for f in whitelist:
        newpath = os.path.join(homepath, f)
        oldpath = os.path.join(magicpath, "tmp", rctype, f)
        if os.path.exists(oldpath):
            os.system("rm -rf %s" % newpath)
            cmd = "mv -f %s %s" % (oldpath, newpath)
            os.system(cmd)

def config(params):
    """params is a string list"""

    import getopt
    
    # yaml file alr read... CONFIG var

    # getopt

    optlist, args = getopt.getopt(params, "", ['repo='])
    print optlist, args

    for (key, value) in optlist: # key comes with -- prefix
        key = key[2:]
        CONFIG[key] = value
        
    # writes back the yaml
    stream = file(configpath, 'w')
    yaml.dump(CONFIG, stream)
    stream.close()

    return

def restore():
    return
    """
    backuppath = os.path.join(magicpath, "backup")
    filelist = os.listdir(backuppath)

    types_list = rctypes.import_mod(filelist)

    # look thru each folder in the backup dir
    # then use whitelist to retrieve list of valid files
    for filename in filelist:
        if filename == "meta.yaml": continue
        if not os.path.isdir(filename): continue

        rctype = filename
        mod = sys.modules['dotmagic.rctypes.%s' % filename]
        whitelist = mod.WHITELIST

        for f in whitelist:
            fullpath = os.join.path(magicpath, 'backup', rctype ,f)
            if os.path.exists(fullpath):
                

    # remove the backup folder?
    """
