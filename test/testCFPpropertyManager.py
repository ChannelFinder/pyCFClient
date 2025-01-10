from __future__ import print_function

import unittest
from channelfinder.cfPropertyManager import CFPropertyManager
import re
import os

from _testConf import _testConf, ChannelFinderClientTestCase

import urllib3

urllib3.disable_warnings()


class CFPropertyManagerTest(ChannelFinderClientTestCase):
    cfglines = []

    def setUp(self):
        print("\n---------------------------------------------------------------\n")

    def test_run(self):
        """
        Tests main program full sweep.
        """
        CFPropertyManager.run(
            "cf-property-manager-test-dbl", "cf-property-manager-test-cfg"
        )
        os.remove("cf-property-manager-test-cfg")
        os.remove("cf-property-manager-test-dbl")

    def test_dbl_read(self):
        """
        Tests accessibility of cfg file, does not check format
        """
        CFPropertyManager.SERVICE_URL = _testConf.get("DEFAULT", "BaseURL")
        CFPropertyManager.username = _testConf.get("DEFAULT", "username")
        CFPropertyManager.password = _testConf.get("DEFAULT", "password")
        CFPropertyManager.startClient()
        fo = open("cf-property-manager-test-dbl", "w+")
        fo.write("UT:RF-Cu:1{LD}Time:ShtDwn-I")
        fo.close()
        dbllines = CFPropertyManager.readDBL("cf-property-manager-test-dbl")
        for line in dbllines:
            self.assertTrue(line in CFPropertyManager.dbllines)
        return dbllines

    def test_regex_error(self):
        """
        Tests bad regex error raise.
        """
        fo = open("cf-property-manager-test-bad-cfg", "w+")
        fo.write("property=[")
        fo.close()
        cfglines = cfglines = CFPropertyManager.readConfiguration(
            "cf-property-manager-test-bad-cfg"
        )
        for properties in cfglines:
            print(properties[0] + " = " + properties[1])
            try:
                self.assertRaises(Exception, re.compile, properties[1])

            except Exception as e:
                print("Invalid regular expression: ", properties[1])
                print("CAUSE:", e.message)
        os.remove("cf-property-manager-test-bad-cfg")
        return cfglines

    def test_regex(self):
        """
        Tests validity of regular expression.
        """
        fo = open("cf-property-manager-test-cfg", "w+")
        fo.write(
            "devName=[{][^:}][^:}]*\ndevType=[:][^{]*?[:}](?!.*[{])\nIGNORE=.*WtrSkid.*"
        )
        fo.close()
        cfglines = CFPropertyManager.readConfiguration("cf-property-manager-test-cfg")
        for properties in cfglines:
            expression = None
            print(properties[0] + " = " + properties[1])
            try:
                expression = re.compile(properties[1])
                self.assertTrue(expression != None)

            except Exception as e:
                print("Invalid regular expression: ", properties[1])
                print("CAUSE:", e.message)
        return cfglines

    def test_cfg_read(self):
        """
        Tests accessibility of cfg file, does not check format
        """
        global cfglines
        CFPropertyManager.SERVICE_URL = _testConf.get("DEFAULT", "BaseURL")
        CFPropertyManager.username = _testConf.get("DEFAULT", "username")
        CFPropertyManager.password = _testConf.get("DEFAULT", "password")
        CFPropertyManager.startClient()
        fo = open("cf-property-manager-test-cfg", "w+")
        fo.write(
            "devName=[{][^:}][^:}]*\ndevType=[:][^{]*?[:}](?!.*[{])\nIGNORE=.*WtrSkid.*"
        )
        fo.close()
        cfglines = CFPropertyManager.readConfiguration("cf-property-manager-test-cfg")
        for line in cfglines:
            self.assertTrue(line in CFPropertyManager.cfglines)
        return cfglines


if __name__ == "__main__":
    unittest.main()
