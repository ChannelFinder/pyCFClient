# -*- coding: utf-8 -*-
"""
Internal module

Used to read the channelfinderapi.conf file

example file
cat ~/channelfinderapi.conf
[DEFAULT]
BaseURL=http://localhost:8080/ChannelFinder
username=MyUserName
password=MyPassword
"""


import sys
import os.path

if (sys.version_info > (3, 0)):
    # Python 3 code in this block
    from configparser import ConfigParser
else:
    # Python 2 code in this block
    from ConfigParser import SafeConfigParser as ConfigParser


def __loadConfig():
    dflt={'BaseURL':'http://barkeria-vm:8080/ChannelFinder'
        }
    cf=ConfigParser(defaults=dflt)
#    print os.path.normpath(os.path.expanduser('~/channelfinderapi.conf'))
    cf.read([
        '/etc/channelfinderapi.conf',
        os.path.expanduser('~/channelfinderapi.conf'),
        'channelfinderapi.conf'
    ])
    return cf
_conf=__loadConfig()