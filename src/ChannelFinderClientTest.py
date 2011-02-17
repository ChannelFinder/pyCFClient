'''
Created on Feb 15, 2011

@author: shroffk
'''
import unittest
from unittest.test.test_result import __init__
from ChannelFinderClient import ChannelFinderClient
from Channel import Channel

class ConnectionTest(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testConnection(self):        
        baseurl = 'https://channelfinder.nsls2.bnl.gov:8181/ChannelFinder'
        self.assertNotEqual(ChannelFinderClient(BaseURL=baseurl), None, 'failed to create client')
        badBaseurl = ['', 'noSuchURL', 'https://channelfinder.nsls2.bnl.gov:8181/ChannelFinder/resources/']
        for url in badBaseurl:
            with self.assertRaises(Exception):ChannelFinderClient(BaseURL=url)
    
    def testParser(self):
        baseurl = 'https://channelfinder.nsls2.bnl.gov:8181/ChannelFinder'
        client = ChannelFinderClient(BaseURL=baseurl)
        allChannels = client.getAllChannels()
        for channel in allChannels:
            # All Channels should have names and owners
            # All Properties should have name and owner
            # All Tags should have name and owner
            pass

class OperationTest(unittest.TestCase):
    
    def setUp(self):
        baseurl = 'https://channelfinder.nslse.bnl.gov:8181/ChannelFinder'
        self.client = ChannelFinderClient(BaseURL=baseurl)
        
        pass
    
    def tearDown(self):
        pass
    
    def addRemoveChannelTest(self):
        # Add a channel
        channel = Channel('channelName', 'channelOwner')
        pass
    
    def addRemoveChannelsTest(self):
        pass
    

class QueryTest(unittest.TestCase):
    
    def setUp(self):
        baseurl = 'https://channelfinder.nsls2.bnl.gov:8181/ChannelFinder'
        self.client = ChannelFinderClient(BaseURL=baseurl)
        pass


    def tearDown(self):
        pass
    
    def testQueryChannel(self):
        pass
    
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testConnection']
    
    unittest.main()
