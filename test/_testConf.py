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
import unittest
from testcontainers.compose import DockerCompose

import sys

if sys.version_info[0] < 3:
    # Python 2 code in this block
    from ConfigParser import SafeConfigParser as ConfigParser
else:
    # Python 3 code in this block
    from configparser import ConfigParser


def channelFinderDocker():
    return DockerCompose("test", compose_file_name="docker-compose.yml")


class ChannelFinderClientTestCase(unittest.TestCase):
    channelFinderCompose = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.channelFinderCompose = channelFinderDocker()
        cls.channelFinderCompose.start()
        cls.channelFinderCompose.wait_for(
            _testConf.get("DEFAULT", "BaseURL") + "/ChannelFinder"
        )
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.channelFinderCompose is not None:
            cls.channelFinderCompose.stop()
        return super().tearDownClass()


def __loadConfig():
    dflt = {
        "BaseURL": "http://localhost:8080/ChannelFinder",
        "username": "admin",
        "password": "adminPass",
        "owner": "cf-update",
        "channelOwner": "cf-channels",
        "channelUsername": "admin",
        "channelPassword": "adminPass",
        "propOwner": "cf-properties",
        "propUsername": "admin",
        "propPassword": "adminPass",
        "tagOwner": "cf-tags",
        "tagUsername": "admin",
        "tagPassword": "adminPass",
    }
    cf = ConfigParser(defaults=dflt)
    cf.read(
        [
            "/etc/channelfinderapi.conf",
            os.path.expanduser("~/channelfinderapi.conf"),
            "channelfinderapi.conf",
        ]
    )
    return cf


_testConf = __loadConfig()
