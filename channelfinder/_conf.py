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

from configparser import ConfigParser


def __loadConfig():
    dflt = {"BaseURL": "http://localhost:8080/ChannelFinder"}
    cf = ConfigParser(defaults=dflt)
    #    print os.path.normpath(os.path.expanduser('~/channelfinderapi.conf'))
    cf.read(
        [
            "/etc/channelfinderapi.conf",
            os.path.expanduser("~/.channelfinderapi.conf"),
            "channelfinderapi.conf",
        ]
    )
    return cf


basecfg = __loadConfig()
