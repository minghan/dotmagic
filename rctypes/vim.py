WHITELIST = ['.vimrc', '.vim']


# $ dotmagic try minghan /usr/local/bin/vim somefile.cpp
"""
def prog_match(progname):
    '''
    Check that the sys.argv[3] returns true
    '''
    return os.path.basename(progname) == 'vim'

def host_prog(argv):
    os.system(argv + " -S " + 'some.vimrc')
    pass

def unhost_prog()
    pass
"""


"""

class RCType(object):
    WHITELIST = []

    def __init__(self):
        pass

    def is_progmatch(self, argv):
        raise NotImplementedError
        return re.search("vim$", argv)


    def cleanup(self, 

class Vim(RCType):


    def __init__(self):

        RCType.__init__(self)
globals()['some class']

"""
