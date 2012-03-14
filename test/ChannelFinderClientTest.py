'''
Copyright (c) 2010 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on Feb 15, 2011

@author: shroffk
'''
import unittest

from channelfinder import ChannelFinderClient
from channelfinder import Channel, Property, Tag
from channelfinder.util import ChannelUtil

from _testConf import _testConf
#===============================================================================
# 
#===============================================================================
class ConnectionTest(unittest.TestCase):

    def testConnection(self):        
#        baseurl = 'http://channelfinder.nsls2.bnl.gov:8080/ChannelFinder'
        self.assertNotEqual(ChannelFinderClient(), None, 'failed to create client')
        badBaseurl = ['', 'noSuchURL']
        for url in badBaseurl:
            self.assertRaises(Exception, ChannelFinderClient, BaseURL=url, msg='message')
#            with self.assertRaises(Exception):ChannelFinderClient(BaseURL=url)
            
#===============================================================================
# Test JSON Parsing
#===============================================================================
class JSONparserTest(unittest.TestCase):
    
    multiChannels = {u'channels': {u'channel': [{u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:0', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'0'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'19'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}, {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:1', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'1'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'22'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}, {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:2', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'2'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'38'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}, {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:3', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'3'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'65'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}, {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:4', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'4'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'78'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}, {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:5', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'5'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'79'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}, {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:6', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'6'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'90'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}, {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:7', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'7'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'5'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}, {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:8', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'8'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'64'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}, {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:9', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'9'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'85'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}]}}
    singleChannels = {u'channels': {u'channel': {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:2', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'2'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'38'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}}}
    channel = {u'@owner': u'shroffk', u'@name': u'Test_first:a<000>:0:0', u'properties': {u'property': [{u'@owner': u'shroffk', u'@name': u'Test_PropA', u'@value': u'0'}, {u'@owner': u'shroffk', u'@name': u'Test_PropB', u'@value': u'19'}, {u'@owner': u'shroffk', u'@name': u'Test_PropC', u'@value': u'ALL'}]}, u'tags': {u'tag': [{u'@owner': u'shroffk', u'@name': u'Test_TagA'}, {u'@owner': u'shroffk', u'@name': u'Test_TagB'}]}}
    noChannel = {u'channels': None}
         
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSingleChannelsParsing(self):
        reply = ChannelFinderClient()._ChannelFinderClient__decodeChannels(self.singleChannels)
        self.assertTrue(len(reply) == 1, 'Parse Error');
        self.assertTrue(len(reply[0].Properties) == len (self.singleChannels[u'channels'][u'channel'][u'properties']['property']), 'single channel peoperties not parsed correctly')
        self.assertTrue(len(reply[0].Tags) == len(self.singleChannels[u'channels'][u'channel'][u'tags']['tag']), 'tags not correctly parsed')
        pass
    
    def testMultiChannelsParsing(self):
        reply = ChannelFinderClient()._ChannelFinderClient__decodeChannels(self.multiChannels)
        self.assertTrue(len(reply) == len(self.multiChannels[u'channels'][u'channel']), 'incorrect number of channels in parsed result')
        pass
    
    def testNoChannelParsing(self):
        reply = ChannelFinderClient()._ChannelFinderClient__decodeChannels(self.noChannel)
        self.assertTrue(not reply, 'failed parsing an emplty channels list')

    def testChannel(self):
        reply = ChannelFinderClient()._ChannelFinderClient__decodeChannel(self.channel)
        self.assertTrue(reply.Name == self.channel[u'@name'])
        self.assertTrue(reply.Owner == self.channel[u'@owner'])
        self.assertTrue(len(reply.Properties) == len(self.channel[u'properties'][u'property']))
        self.assertTrue(len(reply.Tags) == len(self.channel[u'tags'][u'tag']))
        
    def testEncodeChannel(self):
        encodedChannel = ChannelFinderClient()._ChannelFinderClient__encodeChannels(\
                                                            [Channel('Test_first:a<000>:0:0', 'shroffk', \
                                                                     [Property('Test_PropA', 'shroffk', '0'), \
                                                                      Property('Test_PropB', 'shroffk', '19'), \
                                                                      Property('Test_PropC', 'shroffk', 'ALL')], \
                                                                      [Tag('Test_TagA', 'shroffk'), \
                                                                       Tag('Test_TagB', 'shroffk')])])
#        print encodedChannel[u'channels'][u'channel']
        self.assertTrue(encodedChannel[u'channels'][u'channel'] == self.channel)
        
    def testEncodeChannels(self):
        self.assertTrue(self.multiChannels == \
                        ChannelFinderClient()._ChannelFinderClient__encodeChannels(ChannelFinderClient()._ChannelFinderClient__decodeChannels(self.multiChannels)))

#===============================================================================
# 
#===============================================================================
class OperationTest(unittest.TestCase):
    
    def setUp(self):
        '''Default Owners'''
        self.channelOwner = _testConf.get('DEFAULT', 'channelOwner')
        self.propOwner = _testConf.get('DEFAULT', 'propOwner')
        self.tagOwner = _testConf.get('DEFAULT', 'tagOwner')
        '''Default Clients'''
        self.client = ChannelFinderClient(BaseURL=_testConf.get('DEFAULT', 'BaseURL'), \
                                          username=_testConf.get('DEFAULT', 'username'), \
                                          password=_testConf.get('DEFAULT', 'password'))
        self.clientCh = ChannelFinderClient(BaseURL=_testConf.get('DEFAULT', 'BaseURL'), \
                                          username=_testConf.get('DEFAULT', 'channelUsername'), \
                                          password=_testConf.get('DEFAULT', 'channelPassword'))
        self.clientProp = ChannelFinderClient(BaseURL=_testConf.get('DEFAULT', 'BaseURL'), \
                                          username=_testConf.get('DEFAULT', 'propUsername'), \
                                          password=_testConf.get('DEFAULT', 'propPassword'))
        self.clientTag = ChannelFinderClient(BaseURL=_testConf.get('DEFAULT', 'BaseURL'), \
                                          username=_testConf.get('DEFAULT', 'tagUsername'), \
                                          password=_testConf.get('DEFAULT', 'tagPassword'))            
    
    def testSetDeleteChannel(self):
        '''
        Set and Delete a channel
        '''
        try:
            testChannel = Channel('pyChannelName', self.channelOwner)
            self.clientCh.set(channel=testChannel)
            result = self.client.find(name='pyChannelName')
            self.assertTrue(len(result) == 1, 'incorrect number of channels returned')
            self.assertTrue(result[0].Name == 'pyChannelName', 'incorrect channel returned')
        finally:
            self.clientCh.delete(channelName=testChannel.Name) 
            result = self.client.find(name='pyChannelName')
            self.assertTrue(result == None, 'incorrect number of channels returned')
    
    def testSetRemoveChannels(self):
        '''
        Test Set and Delete on a list of channels
        '''
        testChannels = [Channel('pyChannel1', self.channelOwner), \
                        Channel('pyChannel2', self.channelOwner), \
                        Channel('pyChannel3', self.channelOwner)]
        try:
            self.clientCh.set(channel=Channel('existingChannel', self.channelOwner))
            self.assertTrue(len(self.client.find(name='existingChannel')) == 1, \
                            'Failed to add channel')
            self.clientCh.set(channels=testChannels)
            self.assertTrue(len(self.client.find(name='existingChannel')) == 1, \
                            'Failed to add channels without destroying exisitng channels')
            r = self.client.find(name='pyChannel*')
            self.assertTrue(len(r) == 3, \
                            'ERROR: # of channels returned expected ' + str(len(r)) + ' expected 3')
        finally:
            # delete each individually
            for ch in testChannels:
                self.clientCh.delete(channelName=str(ch.Name))
            self.clientCh.delete(channelName='existingChannel')
    
    
    def testSetRemoveChannelsCheck(self):
        '''
        This test will check that a POST in the channels resources is destructive
        '''
        testProp = Property('testProp', self.propOwner)        
        try:            
            self.clientProp.set(property=testProp)     
            testProp.Value = 'original'
            testChannels = [Channel('pyChannel1', self.channelOwner, properties=[testProp]), \
                            Channel('pyChannel2', self.channelOwner), \
                            Channel('pyChannel3', self.channelOwner)] 
            self.clientCh.set(channel=testChannels[0])
            self.assertEqual(len(self.client.find(name='pyChannel*')), 1, \
                             'Failed to set a single channel correctly')
            self.assertTrue(testProp in self.client.find(name='pyChannel1')[0].Properties, \
                            'Failed to add pychannel1 correctly')
            testChannels[0] = Channel('pyChannel1', self.channelOwner)
            self.clientCh.set(channels=testChannels)
            self.assertEqual(len(self.client.find(name='pyChannel*')), 3, \
                             'Failed to set a list of channels correctly')
            self.assertTrue(not self.client.find(name='pyChannel1')[0].Properties or \
                            testProp not in self.client.find(name='pyChannel1')[0].Properties, \
                            'Failed to set pychannel1 correctly')
        finally:
            for ch in testChannels:
                self.clientCh.delete(channelName=ch.Name)
            self.clientProp.delete(propertyName=testProp.Name)
                
        
    
    def testSetRemoveTag(self):
        testTag = Tag('pyTag', self.tagOwner)
        self.clientTag.set(tag=testTag)
        self.assertTrue(self.client.findTag(tagName=testTag.Name).Name == testTag.Name, \
                        'testTag with name _pyTag_ not added')
        self.clientTag.delete(tagName=testTag.Name)
        self.assertEqual(self.client.findTag(tagName=testTag.Name), None, \
                         'tag not removed correctly')
#        self.assertIsNone(self.client.findTag(tagName=testTag.Name), 'tag not removed correctly')
        pass
    
    def testSetRemoveTags(self):
        testTags = []
        testTags.append(Tag('pyTag1', self.tagOwner))
        testTags.append(Tag('pyTag2', self.tagOwner))
        testTags.append(Tag('pyTag3', self.tagOwner))
        try:
            self.clientTag.set(tags=testTags)
            ''' Check if all the tags were correctly Added '''
            for tag in testTags:
                self.assertTrue(self.client.findTag(tagName=tag.Name), \
                                'Error: tag ' + tag.Name + ' was not added')
        finally:
            ''' delete the Tags '''
            for tag in testTags:
                self.clientTag.delete(tagName=tag.Name)
            ''' Check all the tags were correctly removed '''
            for tag in testTags:
                self.assertEqual(self.client.findTag(tagName='pyTag1'), None, \
                                 'Error: tag ' + tag.Name + ' was not removed')
    
    def testGetAllTags(self):
        testTags = []
        testTags.append(Tag('pyTag1', self.tagOwner))
        testTags.append(Tag('pyTag2', self.tagOwner))
        testTags.append(Tag('pyTag3', self.tagOwner))
        try:
            self.clientTag.set(tags=testTags)
            allTags = self.client.getAllTags();
            ''' this test introduces a race condition '''
            for tag in testTags:
                self.assertTrue(tag in allTags, 'tag ' + tag.Name + ' missing')
        finally:
            ''' delete the Tags '''
            for tag in testTags:
                self.client.delete(tagName=tag.Name)
            ''' Check all the tags were correctly removed '''
            for tag in testTags:
                self.assertNotEqual(self.client.findTag(tagName=tag.Name), \
                                    'Error: tag ' + tag.Name + ' was not removed')
    
    def testSetRemoveProperty(self):
        testProperty = Property('pyProp', self.propOwner, value=33)
        try:
            self.clientProp.set(property=testProperty)
            self.assertTrue(self.client.findProperty(propertyName=testProperty.Name), \
                            'Error: ' + testProperty.Name + ' failed to be added')
        finally:
            self.clientProp.delete(propertyName=testProperty.Name)
            self.assertEqual(self.client.findProperty(propertyName=testProperty.Name), \
                                None, \
                                'Error: ' + testProperty.Name + ' failed to delete')
    
    def testSetRemoveProperties(self):
        testProps = []
        testProps.append(Property('pyProp1', self.propOwner))
        testProps.append(Property('pyProp2', self.propOwner))
        testProps.append(Property('pyProp3', self.propOwner))
        try:
            self.clientProp.set(properties=testProps)
            for prop in testProps:
                self.assertTrue(self.client.findProperty(propertyName=prop.Name), \
                                'Error: property ' + prop.Name + ' was not added.')
        finally:
            for prop in testProps:
                self.client.delete(propertyName=prop.Name)
            for prop in testProps:
                self.assertEqual(self.client.findProperty(propertyName=prop.Name), None)
    
    def testGetAllPropperties(self):
        testProps = []
        testProps.append(Property('pyProp1', self.propOwner))
        testProps.append(Property('pyProp2', self.propOwner))
        testProps.append(Property('pyProp3', self.propOwner))
        try:
            self.client.set(properties=testProps)
            allProperties = self.client.getAllProperties()
    #        self.assertTrue(len(allProperties) == (initial + 3), 'unexpected number of properties')
            for prop in testProps:
                self.assertTrue(prop in allProperties, 'property ' + prop.Name + ' missing')
        finally:
            # delete the Tags
            for prop in testProps:
                self.client.delete(propertyName=prop.Name)
            # Check all the tags were correctly removed
            for prop in testProps:
                self.assertEqual(self.client.findProperty(propertyName=prop.Name), None, \
                                 'Error: property ' + prop.Name + ' was not removed')
    
    def testSetRemoveSpecialChar(self):
        spChannel = Channel('special{}<chName:->*?', self.channelOwner)
        spProperty = Property('special{}<propName:->*?', self.propOwner, 'sp<Val:->*?')
        spTag = Tag('special{}<tagName:->*?', self.tagOwner)
        spChannel.Properties = [spProperty]
        spChannel.Tags = [spTag]
        
        self.client.set(tag=spTag)
 #       print self.client.findTag(spTag.Name)
        self.assertNotEqual(self.client.findTag(spTag.Name), None, 'failed to set Tag with special chars')
        self.client.set(property=spProperty)
        self.assertNotEqual(self.client.findProperty(spProperty.Name), None, 'failed to set Property with special chars')
        self.client.set(channel=spChannel)
        foundChannels = self.client.find(name=spChannel.Name)
        self.assertNotEqual(foundChannels[0], None, 'failed to set channel with special chars')
        self.assertTrue(foundChannels[0].Name == spChannel.Name and \
                        spTag in foundChannels[0].Tags and \
                        spProperty in foundChannels[0].Properties, \
                        'Returned channel missing required properties and/or tags')
        self.client.delete(channelName=spChannel.Name)
        self.assertEqual(self.client.find(name=spChannel.Name), None, 'failed to delete channel with special char')
        self.client.delete(tagName=spTag.Name)
        self.assertTrue(self.client.findTag(spTag.Name) == None)
        self.client.delete(propertyName=spProperty.Name)
        self.assertTrue(self.client.findProperty(spProperty.Name) == None)
    
    def testQuotes(self):
        spChannel = Channel('\'"Name', self.channelOwner)
        self.client.set(channel=spChannel)
        self.assertTrue(len(self.client.find(name='\'"Name')) == 1)
        self.client.delete(channelName='\'"Name')

#===============================================================================
#  Set Operation Test
#===============================================================================
class SetOperationTest(unittest.TestCase):
    def setUp(self):
        self.ChannelOwner = _testConf.get('DEFAULT', 'channelOwner')
        self.propOwner = _testConf.get('DEFAULT', 'propOwner')
        self.tagOwner = _testConf.get('DEFAULT', 'tagOwner')
        self.client = ChannelFinderClient(BaseURL=_testConf.get('DEFAULT', 'BaseURL'), \
                                          username=_testConf.get('DEFAULT', 'username'), \
                                          password=_testConf.get('DEFAULT', 'password'))
        self.testChannels = [Channel('pyTestChannel1', self.ChannelOwner), \
                        Channel('pyTestChannel2', self.ChannelOwner), \
                        Channel('pyTestChannel3', self.ChannelOwner)]
        self.client.set(channels=self.testChannels)
        self.assertTrue(len(self.client.find(name='pyTestChannel*')) == 3, \
                        'Error: Failed to set channel')
        pass
    
    def tearDown(self):
#        self.client.delete(channelName='pySetChannel')
        for ch in self.testChannels:
            self.client.delete(channelName=ch.Name)
        pass
    
    def testSetRemoveTag2Channel(self):
        ''' 
        Set Tag to channel removing it from all other channels
        for non destructive operation check TestUpdateAppend
        '''
        testTag = Tag('pySetTag', self.tagOwner)
        try:
            self.client.set(tag=testTag, channelName=self.testChannels[0].Name)
            self.assertTrue(testTag in self.client.find(name='pyTestChannel1')[0].Tags, \
                            'Error: Tag-pySetTag not added to the channel-pyTestChannel1')
            self.client.set(tag=testTag, channelName=self.testChannels[1].Name)
            # check if the tag has been added to the new channel and removed from the old channel
            self.assertTrue(self.__checkTagExists(self.testChannels[1].Name, testTag) and 
                            not self.__checkTagExists(self.testChannels[0].Name, testTag), \
                            'Error: Tag-pySetTag not added to the channel-pyTestChannel2')
            self.client.delete(tag=testTag, channelName=self.testChannels[1].Name)
            self.assertTrue(not self.__checkTagExists(self.testChannels[1].Name, testTag), \
                              'Error: Failed to delete the tag-pySetTag from channel-pyTestChannel1')
        finally:
            self.client.delete(tagName=testTag.Name)
    
    # TODO set a check for removing the tag from a subset of channels which have that tag
    
    def testSetRemoveTag2Channels(self):
        testTag = Tag('pySetTag', self.tagOwner)
        # the list comprehension is used to construct a list of all the channel names
        channelNames = [channel.Name for channel in self.testChannels]
        try:
            self.client.set(tag=testTag, channelNames=channelNames)
            responseChannelNames = [channel.Name for channel in self.client.find(tagName=testTag.Name)]
            for ch in channelNames :
                self.assertTrue(ch in responseChannelNames, 'Error: tag-pySetTag not added to channel ' + ch)
            self.client.delete(tag=testTag, channelNames=channelNames)
            response = self.client.find(tagName=testTag.Name)
            if response:
                responseChannelNames = [channel.Name for channel in response]
                for ch in channelNames :
                    self.assertFalse(ch in responseChannelNames, 'Error: tag-pySetTag not removed from channel ' + ch)
        finally:
            self.client.delete(tagName=testTag.Name)
       
    def __checkTagExists(self, channelName, tag):
        '''
        utility method which return true is channelName contains tag
        '''
        ch = self.client.find(name=channelName)[0]
        if ch.Tags != None and tag in ch.Tags:
            return True
        else:
            return False
    
    
    def testSetRemoveProperty2Channel(self):
        '''
        Set Property on a channel and remove it from all others
        **Destructive operation for non destructive addition of properties check TestUpdateAppend
        '''
        testProperty = Property('pySetProp', self.propOwner)
        chName = self.testChannels[0].Name
        try:
            testProperty.Value = 'testValue'
            self.client.set(property=testProperty, channelName=chName)
            ch = self.client.find(name=chName)[0]
            responsePropertyNames = [property.Name for property in  self.client.find(name=chName)[0].Properties]
            self.assertTrue(testProperty.Name in responsePropertyNames, \
                            'Error: Property-pySetProp not added to the channel-' + chName)
            self.client.delete(property=testProperty, channelName=chName)
            self.assertTrue(self.client.find(name=chName)[0].Properties == None or \
                             testProperty.Name in \
                             [property.Name for property in  self.client.find(name=chName)[0].Properties], \
                            'Error: Property-pySetProp not removed from the channel-' + chName)
        finally:
            self.client.delete(propertyName=testProperty.Name)

    def testSetRemoveProperty2Channels(self):
        testProperty = Property('pySetProp', self.propOwner, '55')
        channelNames = [channel.Name for channel in self.testChannels]
        try:
            self.client.set(property=testProperty, channelNames=channelNames)
            responseChannelNames = [channel.Name for channel in self.client.find(property=[(testProperty.Name, '*')])]
            for ch in channelNames:
                self.assertTrue(ch in responseChannelNames, 'Error: failed to set the property to the channels')
            self.client.delete(property=testProperty, channelNames=channelNames)
            response = self.client.find(property=[(testProperty.Name, '*')])
            if response:
                responseChannelNames = [channel.Name for channel in response]
                for ch in channelNames :
                    self.assertFalse(ch in responseChannelNames, 'Error: property-pySetProp not removed from channel ' + ch)
        finally:
            self.client.delete(propertyName=testProperty.Name)            
    
       
    def testSetChannels(self):
        '''
        This method creates a set of channels and then updates the property values
        using the set method with the channels parameter.
        '''
        prop1 = Property('originalProp1', self.propOwner, value='originalVal')
        prop2 = Property('originalProp2', self.propOwner, value='originalVal')
        ch1 = Channel('orgChannel1', self.ChannelOwner, properties=[prop1, prop2])
        ch2 = Channel('orgChannel2', self.ChannelOwner, properties=[prop1, prop2])
        ch3 = Channel('orgChannel3', self.ChannelOwner, properties=[prop1])
        channels = [ch1, ch2, ch3]
        self.client.set(property=prop1)
        self.client.set(property=prop2)
        self.client.set(channels=channels)
        chs = self.client.find(property=[('originalProp1', 'originalVal'), \
                                         ('originalProp2', 'originalVal')])
        self.assertTrue(len(chs) == 2)
#        for p in chs[0].Properties:
#            if len(p) == 2: 
#                p[1] = 'newVal'
        for ch in chs:
            if (ch.Properties[0]).Name == 'originalProp1':
                (ch.Properties[0]).Value = 'newVal'
        self.client.set(channels=chs)
        self.assertTrue(len(self.client.find(property=[('originalProp1', 'newVal')])) == 2, \
                        'failed to update prop value')
        for ch in channels:
            self.client.delete(channelName=ch.Name)
        self.client.delete(propertyName=prop1.Name)
        self.client.delete(propertyName=prop2.Name)
        pass
    
#===============================================================================
# 
#===============================================================================
    
#===============================================================================
# Update Opertation Tests
#===============================================================================
class UpdateOperationTest(unittest.TestCase):
    def setUp(self):
        '''Default set of Owners'''
        self.channelOwner = _testConf.get('DEFAULT', 'channelOwner')
        self.propOwner = _testConf.get('DEFAULT', 'propOwner')
        self.tagOwner = _testConf.get('DEFAULT', 'tagOwner')
        '''Default set of clients'''
        self.client = ChannelFinderClient()
        self.clientCh = ChannelFinderClient(BaseURL=_testConf.get('DEFAULT', 'BaseURL'), \
                                            username=_testConf.get('DEFAULT', 'channelUsername'), \
                                            password=_testConf.get('DEFAULT', 'channelPassword'))
        self.clientProp = ChannelFinderClient(BaseURL=_testConf.get('DEFAULT', 'BaseURL'), \
                                            username=_testConf.get('DEFAULT', 'propUsername'), \
                                            password=_testConf.get('DEFAULT', 'propPassword'))
        self.clientTag = ChannelFinderClient(BaseURL=_testConf.get('DEFAULT', 'BaseURL'), \
                                            username=_testConf.get('DEFAULT', 'tagUsername'), \
                                            password=_testConf.get('DEFAULT', 'tagPassword'))
        ''' Test Properties and Tags '''
        self.orgTag = Tag('originalTag', self.tagOwner)
        self.orgProp = Property('originalProp', self.propOwner, 'originalValue')
        
        self.clientTag.set(tag=self.orgTag)
        self.clientProp.set(property=self.orgProp)
        
        self.clientCh.set(channel=Channel('originalChannelName', \
                                          self.channelOwner, \
                                          properties=[self.orgProp], \
                                          tags=[self.orgTag]))
        ch = self.client.find(name='originalChannelName')
        self.assertTrue(len(ch) == 1 and 
                        self.orgProp in ch[0].Properties and \
                        self.orgTag in ch[0].Tags);
        pass
    
    def UpdateTagName(self):
        newTagName = 'updatedTag'
        self.assertTrue(self.client.findTag(self.orgTag.Name) != None)
        self.clientTag.update(tag=Tag(newTagName, self.tagOwner), \
                           originalTagName=self.orgTag.Name)
        self.assertTrue(self.client.findTag(self.orgTag.Name) == None and \
                        self.client.findTag(newTagName) != None)
        # check that renaming the Tag does not remove it from any channel
        channelTags = self.client.find(name='originalChannelName')[0].Tags
        self.assertTrue(self.orgTag not in channelTags and \
                        Tag(newTagName, self.tagOwner) in channelTags)
        self.clientTag.update(tag=self.orgTag, originalTagName=newTagName)
    
    def testUpdateTagOwner(self):
        pass
    
    # removed test till bug in the sevice is fixed - channelfinder needs to check for the existance of oldname not name
    def UpdatePropName(self):
        newPropName = 'updatedProperty'
        self.assertTrue(self.client.findProperty(self.orgProp.Name) != None)
        self.clientProp.update(property=Property(newPropName, self.propOwner), \
                                         originalPropertyName=self.orgProp.Name)
        self.assertTrue(self.client.findProperty(self.orgProp.Name) == None and \
                        self.client.findProperty(newPropName) != None)
        # check to ensure that the Property is renamed and not removed from any channels
        channelProperties = self.client.find(name='originalChannelName')[0].getProperties()
        self.assertTrue(self.orgProp.Name not in channelProperties.keys() and \
                        newPropName in channelProperties.keys())
        self.clientProp.update(property=self.orgProp, originalPropertyName=newPropName)
        
    
    def testUpdatePropOwner(self):
        pass
    
    def testUpdateChannelName(self):
        ch = self.client.find(name='originalChannelName')[0]
        newChannel = Channel('updatedChannelName', ch.Owner, properties=ch.Properties, tags=ch.Tags)
        self.clientCh.update(originalChannelName='originalChannelName', \
                           channel=newChannel)
        self.assertTrue(self.client.find(name='originalChannelName') == None)
        self.assertTrue(len(self.client.find(name='updatedChannelName')) == 1)
        # reset the channel back
        self.clientCh.update(originalChannelName='updatedChannelName', \
                           channel=ch)
        self.assertTrue(len(self.client.find(name='originalChannelName')) == 1)
        self.assertTrue(self.client.find(name='updatedChannelName') == None)
    
    def UpdateChannelOwner(self):
        ch = self.client.find(name='originalChannelName')[0]
        newChannel = Channel(ch.Name, self.tagOwner, properties=ch.Properties, tags=ch.Tags)
        self.clientCh.update(originalChannelName='originalChannelName', \
                           channel=newChannel)
        self.assertTrue(self.client.find(name='originalChannelName')[0].Owner == self.tagOwner)                             
        pass
    
    def testUpdateChannel(self):
        '''
        the test updates the channel name and owner
        it also updates an existing property
        and adds a new property and tag
        leaving an existing tag untouched
        
        TODO
        using the lowest lever _tagOwner_ as the newOwner
        '''
        ch = self.client.find(name='originalChannelName')[0]
        updatedProp = Property('originalProp', self.propOwner, 'updatedValue')
        newTag = Tag('updatedTag', self.tagOwner)
        newProp = Property('newProp', self.propOwner, 'newValue')
        try:
            self.clientTag.set(tag=newTag)
            self.clientProp.set(property=newProp)
            newChannel = Channel('updatedChannelName', self.channelOwner, \
                                 properties=[updatedProp, newProp], \
                                 tags=[newTag])
            self.clientCh.update(originalChannelName='originalChannelName', \
                               channel=newChannel)
            foundChannel = self.client.find(name='updatedChannelName')[0]
            self.assertTrue(foundChannel.Name == 'updatedChannelName' and
                            foundChannel.Owner == self.channelOwner and \
                            updatedProp in foundChannel.Properties and\
                            newProp in foundChannel.Properties and \
                            newTag in foundChannel.Tags and \
                            self.orgTag in foundChannel.Tags)
            
        finally:
            #reset
            self.clientCh.update(originalChannelName='updatedChannelName', \
                               channel=ch)
            self.assertTrue(len(self.client.find(name='originalChannelName')), \
                            'failed to reset the updated channels')
            if self.clientTag.findTag(newTag.Name):
                self.clientTag.delete(tagName=newTag.Name)
            if self.clientProp.findProperty(newProp.Name):
                self.clientProp.delete(propertyName=newProp.Name)
                
    def testUpdateChannel2(self):
        '''
        Update a channels using update(channel=updatedChannel)
        '''
        pass
    
    def testUpdateProperty(self):
        '''
        Update a single property using update(property=updatedProperty)
        '''
        pass
    
    def testUpdateTag(self):
        '''
        Update a single tag using update(tag=updatedTag)
        '''
        pass
 
 
    def tearDown(self):
        self.clientCh.delete(channelName='originalChannelName')
        self.clientTag.delete(tagName='originalTag')
        self.clientProp.delete(propertyName='originalProp')
        pass

#===============================================================================
# Update operations to append tags and properties
#===============================================================================

class UpdateAppendTest(unittest.TestCase):
    
    def setUp(self):
        '''Default Owners'''
        self.ChannelOwner = _testConf.get('DEFAULT', 'channelOwner')
        self.propOwner = _testConf.get('DEFAULT', 'propOwner')
        self.tagOwner = _testConf.get('DEFAULT', 'tagOwner')
        '''Default Client''' 
        self.client = ChannelFinderClient(BaseURL=_testConf.get('DEFAULT', 'BaseURL'), \
                                          username=_testConf.get('DEFAULT', 'username'), \
                                          password=_testConf.get('DEFAULT', 'password'))
        self.clientProp = ChannelFinderClient(BaseURL=_testConf.get('DEFAULT', 'BaseURL'), \
                                          username=_testConf.get('DEFAULT', 'propUsername'), \
                                          password=_testConf.get('DEFAULT', 'propPassword'))
        self.clientTag = ChannelFinderClient(BaseURL=_testConf.get('DEFAULT', 'BaseURL'), \
                                          username=_testConf.get('DEFAULT', 'tagUsername'), \
                                          password=_testConf.get('DEFAULT', 'tagPassword'))
        
        self.Tag1 = Tag('tag1', self.tagOwner)
        self.Tag2 = Tag('tag2', self.tagOwner)
        self.Prop1 = Property('prop1', self.propOwner, 'initialVal')
        self.Prop2 = Property('prop2', self.propOwner, 'initialVal')
        self.ch1 = Channel('orgChannel1', self.ChannelOwner, tags=[self.Tag1, self.Tag2])
        self.ch2 = Channel('orgChannel2', self.ChannelOwner, tags=[self.Tag2])
        self.ch3 = Channel('orgChannel3', self.ChannelOwner)
        self.channels = [self.ch1, self.ch2, self.ch3]
        self.clientTag.set(tags=[self.Tag1, self.Tag2])
        self.clientProp.set(properties=[self.Prop1, self.Prop2])
        self.client.set(channels=self.channels)
        # originally 1 channel has tag Tag1 and 2 channels have tag Tag2
        self.assertTrue(len(self.client.find(tagName=self.Tag1.Name)) == 1)
        self.assertTrue(len(self.client.find(tagName=self.Tag2.Name)) == 2)     
        pass
    
    def tearDown(self):
        self.clientTag.delete(tagName=self.Tag1.Name)
        self.clientTag.delete(tagName=self.Tag2.Name)
        self.clientProp.delete(propertyName=self.Prop1.Name)
        self.clientProp.delete(propertyName=self.Prop2.Name)
        for channel in self.channels:
            self.client.delete(channelName=channel.Name)
        self.assertTrue(self.client.find(name='orgChannel?') == None)
        pass
    
    def testUpdateAppendTag2Channel(self):
        '''
        Add tag to channel3 without removing it from the first 2 channels
        '''
        self.clientTag.update(tag=self.Tag2, channelName=self.ch3.Name)
        self.assertTrue(len(self.client.find(tagName=self.Tag2.Name)) == 3)
    
    def testUpdateAppendTag2Channels(self):
        '''
        Add tag to channels 2-3 without removing it from channel 1
        '''
        channelNames = [ channel.Name for channel in self.channels]
        self.clientTag.update(tag=self.Tag1, channelNames=channelNames)
        self.assertTrue(len(self.client.find(tagName=self.Tag1.Name)) == 3)

    def testUpdateAppendProperty2Channel(self):
        '''
        Test to update a channel with a property 
        '''
        self.assertTrue(len(self.client.find(name=self.ch3.Name)) == 1 and \
                         self.client.find(name=self.ch3.Name)[0].Properties == None, \
                         'the channel already has properties')
        self.clientProp.update(property=self.Prop1, channelName=self.ch3.Name)
        self.assertTrue(len(self.client.find(name=self.ch3.Name)) == 1 and \
                        self.Prop1 in self.client.find(name=self.ch3.Name)[0].Properties, \
                            'failed to update the channel with a new property')
        '''Check that Value of the property is correctly added'''
        self.Prop2.Value = 'val'
        self.clientProp.update(property=self.Prop2, channelName=self.ch3.Name)
        chs = self.client.find(name=self.ch3.Name)
        self.assertTrue(len(chs) == 1 and \
                        self.Prop1 in chs[0].Properties and \
                        self.Prop2 in chs[0].Properties , \
                        'Failed to update the channel with a new property without disturbing the old one')
        self.client.set(channel=self.ch3)
       
    def testUpdateAppendProperty2Channels(self):
        '''
        Update a channels with a property
        '''
        self.assertTrue(len(self.client.find(name=self.ch2.Name)) == 1 and \
                         self.client.find(name=self.ch2.Name)[0].Properties == None, \
                         'the channel already has properties')
        self.assertTrue(len(self.client.find(name=self.ch3.Name)) == 1 and \
                         self.client.find(name=self.ch3.Name)[0].Properties == None, \
                         'the channel already has properties')
        self.Prop1.Value = 'testVal'        
        self.clientProp.update(property=self.Prop1, channelNames=[self.ch2.Name, self.ch3.Name])
        self.assertTrue(len(self.client.find(name=self.ch2.Name)) == 1 and \
                        self.Prop1 in self.client.find(name=self.ch2.Name)[0].Properties, \
                            'failed to update the channel with a new property')
        self.assertTrue(len(self.client.find(name=self.ch3.Name)) == 1 and \
                        self.Prop1 in self.client.find(name=self.ch3.Name)[0].Properties, \
                            'failed to update the channel with a new property')
    
    def UserOwnerCheck(self):
        '''
        the _user_ belonging to cf-properties and another group(cf-asd) sets the owner = group
        but should still be able to update the property
        '''
        try:
            self.clientProp.set(property=Property('testProperty', 'cf-asd'))
            self.assertTrue(Property('testProperty', 'cf-asd') in self.client.getAllProperties(), \
                            'failed to add testProperty')
            self.client.set(channel=Channel('testChannel', 'cf-channels'))
            self.clientProp.update(property=Property('testProperty', 'cf-asd', 'val'), channelName='testChannel')
            self.assertEqual(len(self.client.find(property=[('testProperty', '*')])), 1,
                                 'Failed to update testChannel with testProperty')
        finally:
            self.clientProp.delete(propertyName='testProperty')
            self.client.delete(channelName='testChannel')

 
#===========================================================================
# Query Tests
#===========================================================================

class QueryTest(unittest.TestCase):
    
    def setUp(self):        
        '''Default Owners'''
        self.ChannelOwner = _testConf.get('DEFAULT', 'channelOwner')
        self.propOwner = _testConf.get('DEFAULT', 'propOwner')
        self.tagOwner = _testConf.get('DEFAULT', 'tagOwner')
        '''Default Client'''
        self.client = ChannelFinderClient(BaseURL=_testConf.get('DEFAULT', 'BaseURL'), \
                                          username=_testConf.get('DEFAULT', 'username'), \
                                          password=_testConf.get('DEFAULT', 'password'))
        pass


    def tearDown(self):
        pass
    
    def testQueryChannel(self):
        pass
     
    def testNoneReturn(self):
        '''
        find for non existing entities should return None instead of a 404
        '''
        self.assertEqual(self.client.find(name='NonExistingChannelName'), None, \
                        'Failed to return None when searching for a non existing channel')
    
    def testMultiValueQuery(self):
        '''
        add multiple search values for the same parameter
        Expected behaviour
        
        Logically OR'ed
        name=pattern1,pattern2 => return channels with name matching pattern1 OR pattern2
        propName=valPattern1, valPattern2 => return channels with property 'propName' 
                                             with values matching valPattern1 OR valPattern2
        
        Logically AND'ed
        tagName=pattern1, pattern2 => return channels with tags matching pattern1 AND pattern2
        '''
        tagA = Tag('tagA', self.tagOwner)
        tagB = Tag('tagB', self.tagOwner)
        self.client.set(tag=tagA)
        self.client.set(tag=tagB)
        propA = Property('propA', self.propOwner)
        propB = Property('propB', self.propOwner)
        self.client.set(property=propA)
        self.client.set(property=propB)
        self.client.set(channel=Channel('pyTestChannelA', \
                                          self.ChannelOwner, \
                                          tags=[tagA], \
                                          properties=[Property('propA', self.propOwner, '1')]))
        self.client.set(channel=Channel('pyTestChannelB', \
                                          self.ChannelOwner, \
                                          tags=[tagB], \
                                          properties=[Property('propB', self.propOwner, '2')]))
        self.client.set(channel=Channel('pyTestChannelAB', \
                                          self.ChannelOwner, \
                                          tags=[tagA, tagB], \
                                          properties=[Property('propA', self.propOwner, 'a'), \
                                                        Property('propB', self.propOwner, 'b')]))
        '''Tag Queries'''
        self.assertEqual(len(self.client.find(tagName='tagA')), 2, \
                         'failed to successfully complete a query for tagA')
        self.assertEqual(len(self.client.find(tagName='tagB')), 2, \
                         'failed to successfully complete a query for tagB')
        self.assertEqual(len(self.client.find(tagName='tagA,tagB')), 1, \
                         'failed to complete a query with ORed tagNames')
        '''Property Queries'''
        chs = self.client.find(property=[('propA', '*')])
        self.assertEqual(len(chs), 2, \
                         'Failed of query propA expected 2 found ' + str(len(chs)))
        chs = self.client.find(property=[('propA', '1')])
        self.assertEqual(len(chs), 1, \
                         'Failed of query propA expected 1 found ' + str(len(chs)))
        '''conditions AND'ed'''
        '''channels which have both propA and propB'''
        chs = self.client.find(property=[('propA', '*'), ('propB', '*')])
        self.assertEqual(len(chs), 1, \
                         'Failed of query propA expected 1 found ' + str(len(chs)))
        '''conditions OR'ed'''
        '''channels which have propA = pattern1 OR pattern2'''
        chs = self.client.find(property=[('propA', '1'), ('propA', 'a')])
        self.assertEqual(len(chs), 2, \
                         'Failed of query propA expected 2 found ' + str(len(chs)))
        
        ''' Check Find with multiple parameters '''
        chs = self.client.find(name='pyTestChannel*', \
                               tagName=tagA.Name, \
                               property=[('propA', '*')])
        self.assertEqual(len(chs), 2, 'expected 2 found ' + str(len(chs)))
        chs = self.client.find(name='pyTestChannel*', \
                               tagName=tagA.Name, \
                               property=[('propA', 'a')])
        self.assertEqual(len(chs), 1, 'expected 1 found ' + str(len(chs)))        
        
        self.client.delete(channelName='pyTestChannelA')
        self.client.delete(channelName='pyTestChannelB')
        self.client.delete(channelName='pyTestChannelAB')
        
        self.client.delete(tagName=tagA.Name)
        self.client.delete(tagName=tagB.Name)
        self.client.delete(propertyName=propA.Name)
        self.client.delete(propertyName=propB.Name)
    
   
        
#===============================================================================
#  ERROR tests
#===============================================================================
class ErrorTest(unittest.TestCase):
    
    def setUp(self):
        '''Default Owners'''
        self.ChannelOwner = _testConf.get('DEFAULT', 'channelOwner')
        self.propOwner = _testConf.get('DEFAULT', 'propOwner')
        self.tagOwner = _testConf.get('DEFAULT', 'tagOwner')
        '''Default Client'''
        self.client = ChannelFinderClient(BaseURL=_testConf.get('DEFAULT', 'BaseURL'), \
                                          username=_testConf.get('DEFAULT', 'username'), \
                                          password=_testConf.get('DEFAULT', 'password'))
        
        self.client.set(property=Property('existingProperty', self.propOwner))
        
    def tearDown(self):
        self.client.delete(propertyName='existingProperty')
    
    def testSetChannelWithNonExistingProp(self):
        self.assertRaises(Exception, \
                          self.client.set, \
                          channel=Channel('channelName', \
                                            self.ChannelOwner, \
                                            properties=[Property('nonExisitngProperty', 'owner')]))
    
    def testSetChannelWithNonExistingTag(self):
        self.assertRaises(Exception, \
                          self.client.set, \
                          channel=Channel('channelName', \
                                          self.ChannelOwner, \
                                          tags=[Tag('nonExisitngTag', 'owner')]))
        
    def testUpdateChannelWithNonExistingProp(self):
        self.assertRaises(Exception, \
                          self.client.update, \
                          channel=Channel('channelName', \
                                          self.ChannelOwner, \
                                          properties=[Property('nonExisitngProperty', 'owner')]))
    
    def testUpdateChannelWithNonExistingTag(self):
        self.assertRaises(Exception,
                          self.client.update,
                          channel=Channel('channelName', \
                                          self.ChannelOwner, \
                                          tags=[Tag('nonExisitngTag', 'owner')]))
    
    def testUpdateNonExistingChannel(self):
        pass
    
    def testUpdateNonExistingProperty(self):
        pass
    
    def testUpdateNoneExistingTag(self):
        pass
    
    def testIncorrectFindArguments(self):
        self.assertRaises(Exception, \
                          self.client.find, \
                          processVariable='zzz')
        self.assertRaises(Exception, \
                          self.client.find, \
                          properties='zzz')
        self.assertRaises(Exception, \
                          self.client.find, \
                          tag='zzz')
        
    def testCreateChannelWithNullPropertyValue(self):
        self.assertRaises(Exception, \
                          self.client.set, \
                          channel=Channel('channelName', \
                                            self.ChannelOwner, \
                                            properties=[Property('existingProperty', self.propOwner)]))
        self.assertFalse(self.client.find(name='channelName'), \
                         'Failed: should not be able to create a channel with a property with value null')
        
    def testUpdateChannelWithNullPropertyValue(self):
        self.client.set(channel=Channel('channelName', \
                                            self.ChannelOwner))
        try:
            self.assertRaises(Exception, \
                              self.client.update, \
                              channel=Channel('channelName', \
                                              self.ChannelOwner, \
                                              properties=[Property('existingProperty', self.propOwner)]))
            self.assertFalse('existingProperty' in ChannelUtil.getAllProperties(self.client.find(name='channelName')), \
                             'Failed: should not be able to update a channel with a property with value null')
        finally:
            self.client.delete(channelName='channelName')
            
    def testCreateChannelWithEmptyPropertyValue(self):
        self.assertRaises(Exception, \
                          self.client.set, \
                          channel=Channel('channelName', \
                                            self.ChannelOwner, \
                                            properties=[Property('existingProperty', self.propOwner, '')]))
        self.assertFalse(self.client.find(name='channelName'), \
                         'Failed: should not be able to create a channel with a property with empty value string')
        
    def testUpdateChannelWithEmptyPropertyValue(self):
        self.client.set(channel=Channel('channelName', \
                                            self.ChannelOwner))
        try:
            self.assertRaises(Exception, \
                              self.client.update, \
                              channel=Channel('channelName', \
                                              self.ChannelOwner, \
                                              properties=[Property('existingProperty', self.propOwner,'')]))
            self.assertFalse('existingProperty' in ChannelUtil.getAllProperties(self.client.find(name='channelName')), \
                             'Failed: should not be able to update a channel with a property with empty value string')
        finally:
            self.client.delete(channelName='channelName')
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testConnection']
  #  suite = unittest.TestLoader().loadTestsFromTestCase(ErrorTest)
  #  unittest.TextTestRunner(verbosity=2).run(suite)
    
#    print sys.path
    
    unittest.main()
