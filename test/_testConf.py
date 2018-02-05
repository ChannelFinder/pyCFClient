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
import os.path

import sys
if (sys.version_info > (3, 0)):
    # Python 3 code in this block
    from configparser import ConfigParser
else:
    # Python 2 code in this block
    from ConfigParser import SafeConfigParser as ConfigParser


def __loadConfig():
    dflt={'BaseURL':'https://barkeria-vm:8181/ChannelFinder',
          'username' : 'cf-update',
          'password' : '1234',
          'owner' : 'cf-update',
          'channelOwner' : 'cf-channels',
          'channelUsername' : 'channel',
          'channelPassword' : '1234',          
          'propOwner' : 'cf-properties',
          'propUsername' : 'property',
          'propPassword' : '1234',
          'tagOwner' : 'cf-tags',
          'tagUsername' : 'tag',
          'tagPassword' : '1234'
        }
    cf=ConfigParser(defaults=dflt)
    cf.read([
        '/etc/channelfinderapi.conf',
        os.path.expanduser('~/channelfinderapi.conf'),
        'channelfinderapi.conf'
    ])
    return cf

_testConf=__loadConfig()