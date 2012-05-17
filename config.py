"""
Handles all config related issues
in the ~/.dotmagic/dotmagic file
"""

import ConfigParser

import app


def read(config_filepath):
    """Returns a dictionary assuming config_filepath is valid"""

    config = ConfigParser.SafeConfigParser()
    # allow_no_value: False (default)
    config.readfp(open(config_filepath))

    return {
        'core': {
            'username': config.get('core', 'username'),
            'version': config.getint('core', 'version'),
            'url': config.get('core', 'url')
        },
        'apps': {
            'whitelist': set(eval(config.get('apps', 'whitelist')))
        }
    }


def write(config_filepath, config_dict = None):
    """Writes the given dictionary to the given filepath"""

    config_dict = config_dict or default()
    
    config = ConfigParser.SafeConfigParser()

    config.add_section('core')
    for (k,v) in config_dict['core'].items():
        config.set('core', k, str(v))

    config.add_section('apps')
    config.set('apps', 'whitelist', str(list(config_dict['apps']['whitelist'])))

    with open(config_filepath, 'wb') as config_file:
        config.write(config_file)

def default():
    """Returns a dictionary containing default values"""
    return {
        'core': {
            'username':  '',
            'version': int(app.VERSION),
            'url': ''
        },
        'apps': {
            'whitelist': set()
        }
    }

