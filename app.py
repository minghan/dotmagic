import os

HOME_FOLDER = os.getenv('HOME')                      # folder
CONFIG_FOLDER = os.path.expanduser("~/.dotmagic")    # folder
CONFIG_FILEPATH = os.path.join(CONFIG_FOLDER, "config")
VERSION = 1 # integer numbering from 0
