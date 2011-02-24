'''
Created on Feb 15, 2011

@author: shroffk
'''
import unittest
from unittest.test.test_result import __init__
from ChannelFinderClient import ChannelFinderClient
from Channel import Channel, Property, Tag

#===============================================================================
# 
#===============================================================================
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
            
#===============================================================================
# 
#===============================================================================
class JSONparserTest(unittest.TestCase):
    
    multiChannels = {u'channels': {u'channel': [{u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:0', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'0'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'19'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}, {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:1', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'1'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'22'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}, {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:2', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'2'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'38'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}, {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:3', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'3'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'65'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}, {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:4', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'4'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'78'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}, {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:5', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'5'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'79'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}, {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:6', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'6'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'90'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}, {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:7', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'7'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'5'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}, {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:8', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'8'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'64'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}, {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:9', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'9'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'85'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}]}}
    singleChannels = {u'channels': {u'channel': {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:2', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'2'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'38'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}}}
    channel = {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:0', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'0'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'19'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}
    noChannel = {u'channels': None}
#------------------------------------------------------------------------------ 
    def testSingleChannelsParsing(self):
        reply = ChannelFinderClient.decodeChannels(self.singleChannels)
        self.assertTrue(len(reply) == 1, 'Parse Error');
        self.assertTrue(len(reply[0].Properties) == len (self.singleChannels[u'channels'][u'channel'][u'properties']['property']), 'single channel peoperties not parsed correctly')
        self.assertTrue(len(reply[0].Tags) == len(self.singleChannels[u'channels'][u'channel'][u'tags']['tag']), 'tags not correctly parsed')
        pass
    
    def testMultiChannelsParsing(self):
        reply = ChannelFinderClient.decodeChannels(self.multiChannels)
        self.assertTrue(len(reply) == len(self.multiChannels[u'channels'][u'channel']), 'incorrect number of channels in parsed result')
        pass
    
    def testNoChannelParsing(self):
        reply = ChannelFinderClient.decodeChannels(self.noChannel)
        self.assertTrue(not reply, 'failed parsing an emplty channels list')
    
#------------------------------------------------------------------------------ 
    def testChannel(self):
        reply = ChannelFinderClient.decodeChannel(self.channel)
        self.assertTrue(reply.Name == self.channel[u'@name'])
        self.assertTrue(reply.Owner == self.channel[u'@owner'])
        self.assertTrue(len(reply.Properties) == len(self.channel[u'properties'][u'property']))
        self.assertTrue(len(reply.Tags) == len(self.channel[u'tags'][u'tag']))
        
#------------------------------------------------------------------------------ 
    def testEncodeChannel(self):
        encodedChannel = ChannelFinderClient.encodeChannels([Channel('Test_first:a<000>:0:0', 'shroffk', \
                           [Property('Test_PropA', 'shroffk', '0'), Property('Test_PropB', 'shroffk', '19'), Property('Test_PropC', 'shroffk', 'ALL')], \
                           [Tag('Test_TagA', 'shroffk'), Tag('Test_TagB', 'shroffk')])])

        self.assertTrue(encodedChannel[u'channels'][u'channel'] == self.channel)
        
    def testEncodeChannels(self):
        self.assertTrue(self.multiChannels == ChannelFinderClient.encodeChannels(ChannelFinderClient.decodeChannels(self.multiChannels)))

#===============================================================================
# 
#===============================================================================
class OperationTest(unittest.TestCase):
    
    def setUp(self):
        baseurl = 'https://channelfinder.nsls2.bnl.gov:8181/ChannelFinder'
        self.client = ChannelFinderClient(BaseURL=baseurl, username='boss', password='1234')
        pass
    
    def tearDown(self):
        pass
    
    def testaddRemoveChannel(self):
        # Add a channel
        testChannel = Channel('pyChannelName', 'pyChannelOwner')
        self.client.add(channel=testChannel)
        result = self.client.find(name='pyChannelName')
        self.assertTrue(len(result) == 1, 'incorrect number of channels returned')
        self.assertTrue(result[0].Name == 'pyChannelName', 'incorrect channel returned')
        self.client.remove(channel=testChannel.Name) 
        result = self.client.find(name='pyChannelName')
        self.assertTrue(result == None, 'incorrect number of channels returned')  
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
