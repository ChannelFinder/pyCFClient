'''
Copyright (c) 2010 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on Feb 15, 2011

@author: shroffk
'''
import unittest

from channelfinder import ChannelFinderClient
#from channelfinder import Channel, Property, Tag
from channelfinder.util import ChannelUtil
from collections import Counter
from _testConf import _testConf
#===============================================================================
# 
#===============================================================================
class ConnectionTest(unittest.TestCase):

    def testConnection(self):
        
        testUrl = getDefaultTestConfig("BaseURL")
        self.assertNotEqual(ChannelFinderClient(BaseURL=testUrl, username=getDefaultTestConfig('username'), password=getDefaultTestConfig('password')), None, 'failed to create client')
        badBaseurl = ['', 'noSuchURL']
        for url in badBaseurl:
            self.assertRaises(Exception, ChannelFinderClient, BaseURL=url, msg='message')
            
#===============================================================================
# Test JSON Parsing
#===============================================================================
'''
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
        self.assertTrue(len(reply[0][u'properties']) == len (self.singleChannels[u'channels'][u'channel'][u'properties']['property']), 'single channel peoperties not parsed correctly')
        self.assertTrue(len(reply[0][u'tags']) == len(self.singleChannels[u'channels'][u'channel'][u'tags']['tag']), 'tags not correctly parsed')
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
        self.assertTrue(reply[u'name'] == self.channel[u'@name'])
        self.assertTrue(reply[u'owner'] == self.channel[u'@owner'])
        self.assertTrue(len(reply[u'properties']) == len(self.channel[u'properties'][u'property']))
        self.assertTrue(len(reply[u'tags']) == len(self.channel[u'tags'][u'tag']))
        
    def testEncodeChannel(self):
        encodedChannel = ChannelFinderClient()._ChannelFinderClient__encodeChannels(\
                                                            [{u'name':u'Test_first:a<000>:0:0', u'owner':u'shroffk', \
                                                                     u'properties':[{u'name':u'Test_PropA', u'owner':u'shroffk', u'value':u'0'}, \
                                                                      {u'name':u'Test_PropB', u'owner':u'shroffk', u'value':u'19'}, \
                                                                      {u'name':u'Test_PropC', u'owner':u'shroffk', u'value':u'ALL'}], \
                                                                      u'tags':[{u'name':u'Test_TagA', u'owner':u'shroffk'}, \
                                                                       {u'name':u'Test_TagB', u'owner':u'shroffk'}]}])
#        print encodedChannel[u'channels'][u'channel']
        print "TEST "+ str(encodedChannel[u'channels'][u'channel']) + "  ==  " + str(self.channel)
        self.assertTrue(encodedChannel[u'channels'][u'channel'] == self.channel)

    def testEncodeChannels(self):
        self.assertTrue(self.multiChannels == \
                        ChannelFinderClient()._ChannelFinderClient__encodeChannels(ChannelFinderClient()._ChannelFinderClient__decodeChannels(self.multiChannels)))
'''

#===============================================================================
# Test all the tag operations
#===============================================================================
class OperationTagTest(unittest.TestCase):

    def setUp(self):
        '''Default Owners'''
        self.channelOwner = _testConf.get('DEFAULT', 'channelOwner')
        self.tagOwner = _testConf.get('DEFAULT', 'tagOwner')
        '''Default Clients'''
        self.client = ChannelFinderClient(BaseURL=_testConf.get('DEFAULT', 'BaseURL'), \
                                          username=_testConf.get('DEFAULT', 'username'), \
                                          password=_testConf.get('DEFAULT', 'password'))
        self.clientTag = ChannelFinderClient(BaseURL=_testConf.get('DEFAULT', 'BaseURL'), \
                                          username=_testConf.get('DEFAULT', 'tagUsername'), \
                                          password=_testConf.get('DEFAULT', 'tagPassword'))
        self.testChannels = [{u'name':u'pyTestChannel1', u'owner':self.channelOwner}, \
                        {u'name':u'pyTestChannel2', u'owner':self.channelOwner}, \
                        {u'name':u'pyTestChannel3', u'owner':self.channelOwner}]
        self.client.set(channels=self.testChannels)
        self.assertTrue(len(self.client.find(name=u'pyTestChannel*')) == 3, \
                        'Error: Failed to set channel')
        pass

    def tearDown(self):
        for ch in self.testChannels:
            self.client.delete(channelName=ch[u'name'])
        pass

    def testCreateAndDeleteTag(self):
        testTag = {'name':'setTestTag', 'owner':self.tagOwner}
        try:
            result = self.clientTag.set(tag=testTag)
            foundtag = self.client.findTag(testTag['name'])
            self.assertIsNotNone(foundtag, 'failed to create a test tag')
            self.assertTrue(checkTagInList([foundtag], [testTag]), 'tag not created correctly')
        finally:
            self.clientTag.delete(tagName=testTag['name'])
            foundtag = self.client.findTag(testTag['name'])
            self.assertIsNone(foundtag, 'failed to delete the test tag')

    def testCreateAndDeleteTagWithChannel(self):
        testTag = {'name':'setTestTag', 'owner':self.tagOwner, 'channels':[self.testChannels[0]]}
        try:
            result = self.clientTag.set(tag=testTag)
            foundtag = self.client.findTag(testTag['name'])
            self.assertIsNotNone(foundtag, 'failed to create a test tag')
            self.assertTrue(checkTagInList([foundtag], [testTag]), 'tag not created correctly')
            '''check the created tag was added to the channel'''
            self.assertTrue(checkTagOnChannel(self.client, self.testChannels[0]['name'], foundtag), \
                            'Failed to correctly set the created tag to the appropriate channel')
        finally:
            self.clientTag.delete(tagName=testTag['name'])
            foundtag = self.client.findTag(testTag['name'])
            self.assertIsNone(foundtag, 'failed to delete the test tag')

    def testCreateAndDeleteTags(self):
        testTags = []
        testTags.append({u'name':u'pyTag1', u'owner':self.tagOwner})
        testTags.append({u'name':u'pyTag2', u'owner':self.tagOwner})
        testTags.append({u'name':u'pyTag3', u'owner':self.tagOwner})
        try:
            self.clientTag.set(tags=testTags)
            '''Check if all the tags were correctly Added '''
            for tag in testTags:
                self.assertTrue(self.client.findTag(tagName=tag[u'name']), \
                                'Error: tag ' + tag[u'name'] + ' was not added')
        finally:
            '''delete the Tags '''
            for tag in testTags:
                self.clientTag.delete(tagName=tag[u'name'])
            '''Check all the tags were correctly removed '''
            for tag in testTags:
                self.assertEqual(self.client.findTag(tagName='pyTag1'), None, \
                                 'Error: tag ' + tag[u'name'] + ' was not removed')

    def testSetRemoveTag2Channel(self):
        '''
        Set Tag to channel removing it from all other channels
        for non destructive operation check TestUpdateAppend
        '''
        testTag = {u'name':u'pySetTag', u'owner':self.tagOwner}
        try:
            self.client.set(tag=testTag)
            self.client.set(tag=testTag, channelName=self.testChannels[0][u'name'])

            self.assertTrue(checkTagOnChannel(self.client, 'pyTestChannel1', testTag) , \
                            'Error: Tag-pySetTag not added to the channel-pyTestChannel1')

            self.client.set(tag=testTag, channelName=self.testChannels[1][u'name'])
            # check if the tag has been added to the new channel and removed from the old channel
            self.assertTrue(checkTagOnChannel(self.client, self.testChannels[1][u'name'], testTag) and
                            not checkTagOnChannel(self.client, self.testChannels[0][u'name'], testTag), \
                            'Error: Tag-pySetTag not added to the channel-pyTestChannel2')

            self.client.delete(tag=testTag, channelName=self.testChannels[1][u'name'])
            self.assertTrue(not checkTagOnChannel(self.client, self.testChannels[1][u'name'], testTag), \
                              'Error: Failed to delete the tag-pySetTag from channel-pyTestChannel1')
        finally:
            self.client.delete(tagName=testTag[u'name'])

    # TODO set a check for removing the tag from a subset of channels which have that tag

    def testSetRemoveTag2Channels(self):
        '''
        Set tags to a set of channels and remove it from all other channels
        '''
        testTag = {u'name':u'pySetTag', u'owner':self.tagOwner}
        # the list comprehension is used to construct a list of all the channel names
        channelNames = [channel[u'name'] for channel in self.testChannels]
        try:
            self.client.set(tag=testTag, channelNames=channelNames)
            responseChannelNames = [channel[u'name'] for channel in self.client.find(tagName=testTag[u'name'])]
            for ch in channelNames :
                self.assertTrue(ch in responseChannelNames, 'Error: tag-pySetTag not added to channel ' + ch)
            self.client.delete(tag=testTag, channelNames=channelNames)
            response = self.client.find(tagName=testTag[u'name'])
            if response:
                responseChannelNames = [channel[u'name'] for channel in response]
                for ch in channelNames :
                    self.assertFalse(ch in responseChannelNames, 'Error: tag-pySetTag not removed from channel ' + ch)
        finally:
            self.client.delete(tagName=testTag[u'name'])

    def testUpdateTag(self):
        '''
        Add a tag to a group of channels without removing it from existing channels
        '''
        tag = {'name':'initialTestTag', 'owner':self.tagOwner}
        tag['channels'] = [self.testChannels[0]]
        try:
            '''Create initial tag'''
            self.clientTag.set(tag=tag)
            self.assertIsNotNone(self.client.findTag(tag['name']), 'failed to create a test tag')
            '''Update tag with new channels'''
            tag['channels'] = [self.testChannels[1], self.testChannels[2]]
            self.clientTag.update(tag=tag)

            for channel in self.testChannels:
                self.assertTrue(checkTagOnChannel(self.client, channel['name'], tag), 'Failed to updated tag')
        finally:
            '''cleanup'''
            self.client.delete(tagName=tag['name'])
            self.assertIsNone(self.client.findTag(tag['name']), 'failed to delete the test tag:'+tag['name'])

    def testUpdateTags(self):
        '''
        Add tags to a group of channels without removing it from existing channels
        '''
        tag1 = {'name':'pyTestTag1', 'owner':self.tagOwner}
        tag1['channels'] = [self.testChannels[0]]
        tag2 = {'name':'pyTestTag2', 'owner':self.tagOwner}
        tag2['channels'] = [self.testChannels[0]]

        try:
            '''Create initial tags which are set on the pyTestChannel1'''
            self.clientTag.set(tags=[tag1,tag2])
            self.assertIsNotNone(self.client.findTag(tag1['name']), 'failed to create a test tag: pyTestTag1')
            self.assertIsNotNone(self.client.findTag(tag1['name']), 'failed to create a test tag: pyTestTag2')
            '''Update tags with new channels'''
            tag1['channels'] = [self.testChannels[1], self.testChannels[2]]
            tag2['channels'] = [self.testChannels[1], self.testChannels[2]]
            self.clientTag.update(tags = [tag1, tag2])
            '''Check that the all channels have been updated with the tags'''
            for channel in self.testChannels:
                self.assertTrue(checkTagOnChannel(self.client, channel['name'], tag1) and \
                                checkTagOnChannel(self.client, channel['name'], tag2), \
                                'Failed to updated tags')
        finally:
            '''cleanup'''
            self.client.delete(tagName=tag1['name'])
            self.client.delete(tagName=tag2['name'])
            self.assertIsNone(self.client.findTag(tag1['name']), 'failed to delete the test tag:'+tag1['name'])
            self.assertIsNone(self.client.findTag(tag2['name']), 'failed to delete the test tag:'+tag2['name'])

    def testGetAllTags(self):
        '''Test setting multiple tags and listing all tags'''
        testTags = []
        testTags.append({'name':'testTag1', 'owner':self.tagOwner})
        testTags.append({'name':'testTag2', 'owner':self.tagOwner})
        testTags.append({'name':'testTag3', 'owner':self.tagOwner})
        try:
            self.client.set(tags=testTags)
            allTags = self.client.getAllTags()
            self.assertTrue(checkTagInList(allTags, testTags), 'Failed to create multiple tags')
        finally:
            # delete the Tags
            for tag in testTags:
                self.client.delete(tagName=tag['name'])
            # Check all the tags were correctly removed
            for tag in testTags:
                self.assertEqual(self.client.findTag(tagName=tag[u'name']), None, \
                                 'Error: property ' + tag[u'name'] + ' was not removed')

#===============================================================================
# Test all the property operations
#===============================================================================

class OperationPropertyTest(unittest.TestCase):

    def setUp(self):
        '''Default Owners'''
        self.channelOwner = _testConf.get('DEFAULT', 'channelOwner')
        self.propOwner = _testConf.get('DEFAULT', 'propOwner')
        '''Default Clients'''
        self.client = ChannelFinderClient(BaseURL=_testConf.get('DEFAULT', 'BaseURL'), \
                                          username=_testConf.get('DEFAULT', 'username'), \
                                          password=_testConf.get('DEFAULT', 'password'))
        self.clientProp = ChannelFinderClient(BaseURL=_testConf.get('DEFAULT', 'BaseURL'), \
                                          username=_testConf.get('DEFAULT', 'propUsername'), \
                                          password=_testConf.get('DEFAULT', 'propPassword'))
        self.testChannels = [{u'name':u'pyTestChannel1', u'owner':self.channelOwner}, \
                        {u'name':u'pyTestChannel2', u'owner':self.channelOwner}, \
                        {u'name':u'pyTestChannel3', u'owner':self.channelOwner}]
        self.client.set(channels=self.testChannels)
        self.assertTrue(len(self.client.find(name=u'pyTestChannel*')) == 3, \
                        'Error: Failed to set channel')
        pass

    def tearDown(self):
        for ch in self.testChannels:
            self.client.delete(channelName=ch[u'name'])
        pass

    def testCreateAndDeleteProperty(self):
        '''
        Create and delete a single property
        '''
        testProperty = {'name':'setTestProp', 'owner':self.propOwner}
        try:
            result = self.clientProp.set(property=testProperty)
            foundProperty = self.client.findProperty(testProperty['name'])
            self.assertIsNotNone(foundProperty, 'failed to create a test property')
            self.assertTrue(checkPropInList([foundProperty], [testProperty]), 'property not created correctly')
        finally:
            self.client.delete(propertyName=testProperty['name'])
            foundProperty = self.client.findProperty(testProperty['name'])
            self.assertIsNone(foundProperty, 'failed to delete the test property')

    def testCreateAndDeletePropertyWithChannel(self):
        '''
        Create and delete a single property
        '''
        ch = self.testChannels[0]
        ch['properties'] = [ {'name':'setTestProp', 'owner':self.propOwner, 'value':'testValue1'} ]
        testProperty = {'name':'setTestProp', 'owner':self.propOwner, 'channels':[ch]}
        try:
            result = self.clientProp.set(property=testProperty)
            foundProperty = self.client.findProperty(testProperty['name'])
            self.assertIsNotNone(foundProperty, 'failed to create a test property')
            self.assertTrue(checkPropInList([foundProperty], [testProperty]), 'property not created correctly')
            '''check the created property was added to the channel'''
            self.assertTrue(checkPropertyOnChannel(self.client, self.testChannels[0]['name'], foundProperty), \
                            'Failed to correctly set the created property to the appropriate channel')
        finally:
            self.client.delete(propertyName=testProperty['name'])
            foundProperty = self.client.findProperty(testProperty['name'])
            self.assertIsNone(foundProperty, 'failed to delete the test property')

    def testCreateAndDeletePropertyWithChannels(self):
        '''
        Create and delete a single property
        '''
        ch1 = self.testChannels[0]
        ch1['properties'] = [ {'name':'setTestProp', 'owner':self.propOwner, 'value':'testValue1'} ]
        ch2 = self.testChannels[1]
        ch2['properties'] = [ {'name':'setTestProp', 'owner':self.propOwner, 'value':'testValue2'} ]
        testProperty = {'name':'setTestProp', 'owner':self.propOwner, 'channels':[ch1, ch2]}
        try:
            result = self.clientProp.set(property=testProperty)
            foundProperty = self.client.findProperty(testProperty['name'])
            self.assertIsNotNone(foundProperty, 'failed to create a test property')
            self.assertTrue(checkPropInList([foundProperty], [testProperty]), 'property not created correctly')
            '''check the created property was added to the channel'''
            self.assertTrue(checkPropertyOnChannel(self.client, self.testChannels[0]['name'], foundProperty), \
                            'Failed to correctly set the created property to the appropriate channel')
            self.assertTrue(checkPropertyOnChannel(self.client, self.testChannels[1]['name'], foundProperty), \
                            'Failed to correctly set the created property to the appropriate channel')
        finally:
            self.client.delete(propertyName=testProperty['name'])
            foundProperty = self.client.findProperty(testProperty['name'])
            self.assertIsNone(foundProperty, 'failed to delete the test property')

    def testCreateAndDeleteProperties(self):
        '''
        Create and delete a set of properties
        '''
        testProperty1 = {'name':'pyTestProp1', 'owner':self.propOwner}
        testProperty2 = {'name':'pyTestProp2', 'owner':self.propOwner}
        try:
            result = self.clientProp.set(properties=[testProperty1, testProperty2])
            self.assertTrue(checkPropInList(self.clientProp.getAllProperties(), [testProperty1, testProperty2]), 'property not created correctly')
        finally:
            self.client.delete(propertyName=testProperty1['name'])
            self.client.delete(propertyName=testProperty2['name'])
            self.assertIsNone(self.client.findProperty(testProperty1['name']), 'failed to delete the test property1')
            self.assertIsNone(self.client.findProperty(testProperty2['name']), 'failed to delete the test property1')

    def testSetRemoveProperty2Channel(self):
        '''
        Set Property to channel removing it from all other channels
        for non destructive operation check TestUpdateAppend
        '''
        testProperty = {'name':'setTestProp', 'owner':self.propOwner}
        try:
            result = self.clientProp.set(property=testProperty)
            ch0 = self.testChannels[0]
            ch0['properties'] = [ {'name':'setTestProp', 'owner':self.propOwner, 'value':'testValue1'} ]
            testProperty['channels'] = [ch0]
            self.client.set(property=testProperty)
            self.assertTrue(checkPropertyOnChannel(self.client, ch0[u'name'], testProperty) , \
                            'Error: Property - setTestProp not added to the channel-pyTestChannel1')

            ch1 = self.testChannels[1]
            ch1['properties'] = [ {'name':'setTestProp', 'owner':self.propOwner, 'value':'testValue2'} ]
            testProperty['channels'] = [ch1]
            self.client.set(property=testProperty)
            '''check if the property has been added to the new channel and removed from the old channel'''
            self.assertTrue(checkPropertyOnChannel(self.client, ch1[u'name'], testProperty) and
                            not checkPropertyOnChannel(self.client, ch0[u'name'], testProperty), \
                            'Error: Tag-pySetTag not added to the channel-pyTestChannel2')
        finally:  # Delete operation causes an error if performed twice, IE: the first delete succeeded
            '''delete the property and ensure it is removed from the associated channel'''
            self.client.delete(propertyName=testProperty[u'name'])
            self.assertTrue(not checkPropertyOnChannel(self.client, ch0[u'name'], testProperty) and \
                            not checkPropertyOnChannel(self.client, ch1[u'name'], testProperty), \
                            'Error: Failed to delete the tag-pySetTag from channel-pyTestChannel1')

    def testGetAllPropperties(self):
        '''Test setting multiple properties and listing all tags'''
        testProps = []
        testProps.append({u'name':u'pyTestProp1', u'owner':self.propOwner})
        testProps.append({u'name':u'pyTestProp2', u'owner':self.propOwner})
        testProps.append({u'name':u'pyTestProp3', u'owner':self.propOwner})
        try:
            self.client.set(properties=testProps)
            allProperties = self.client.getAllProperties()
            self.assertTrue(checkPropInList(allProperties, testProps), 'failed at set a list of properties')
        finally:
            # delete the Tags
            for prop in testProps:
                self.client.delete(propertyName=prop[u'name'])
            # Check all the tags were correctly removed
            for prop in testProps:
                self.assertEqual(self.client.findProperty(propertyName=prop[u'name']), None, \
                                 'Error: property ' + prop[u'name'] + ' was not removed')
#===============================================================================
#
#===============================================================================
class OperationChannelTest(unittest.TestCase):

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
        Set and Delete a simple channel with no properties or tags
        '''
        try:
            testChannel = {u'name':u'pyTestChannelName', u'owner': self.channelOwner}
            self.clientCh.set(channel=testChannel)
            result = self.client.find(name=u'pyTestChannelName')
            self.assertTrue(len(result) == 1, 'incorrect number of channels returned')
            self.assertTrue(result[0][u'name'] == u'pyTestChannelName', 'incorrect channel returned')
        finally:
            self.clientCh.delete(channelName=testChannel[u'name'])
            result = self.client.find(name=u'pyTestChannelName')
            self.assertFalse(result, 'incorrect number of channels returned')

    def testSetDeleteChannelWithPropertiesAndTags(self):
        '''
        Set and Delete a simple channel with properties or tags
        '''
        try:
            testProp = {u'name':u'pyTestProp', u'owner':self.propOwner, u'value':u'testVal'}
            self.client.set(property=testProp)
            testTag = {u'name':u'pyTestTag', u'owner':self.tagOwner}
            self.client.set(tag=testTag)

            testChannel = {u'name':u'pyTestChannelName', u'owner': self.channelOwner, u'properties':[testProp], u'tags':[testTag]}
            self.clientCh.set(channel=testChannel)

            result = self.client.find(name=u'pyTestChannelName')
            self.assertTrue(len(result) == 1, 'incorrect number of channels returned')
            self.assertTrue(result[0][u'name'] == u'pyTestChannelName', 'incorrect channel returned')
        finally:
            '''Cleanup'''
            self.clientCh.delete(channelName=testChannel[u'name'])
            self.client.delete(tagName=testTag[u'name'])
            self.client.delete(propertyName=testProp[u'name'])
            result = self.client.find(name=u'pyTestChannelName')
            self.assertFalse(result, 'incorrect number of channels returned')

    def testSetRemoveChannels(self):
        '''
        Test Set and Delete on a list of channels with no propties or tags
        '''
        testChannels = [{u'name' : u'pyTestChannel1', u'owner' : self.channelOwner}, \
                        {u'name' : u'pyTestChannel2', u'owner' : self.channelOwner}, \
                        {u'name' : u'pyTestChannel3', u'owner' : self.channelOwner}]
        try:
            self.clientCh.set(channels=testChannels)
            r = self.client.find(name='pyTestChannel*')
            self.assertTrue(len(r) == 3, \
                            'ERROR: # of channels returned expected ' + str(len(r)) + ' expected 3')
        finally:
            # delete each individually
            for ch in testChannels:
                self.clientCh.delete(channelName=str(ch[u'name']))

    def testSetChannelsWithProperties(self):
        '''
        This method creates a set of channels and then updates the property values
        using the set method with the channels parameter.
        '''
        prop1 = {u'name':u'originalProp1', u'owner':self.propOwner, u'value':u'originalVal'}
        prop2 = {u'name':u'originalProp2', u'owner':self.propOwner, u'value':u'originalVal'}
        ch1 = {u'name':u'orgChannel1', u'owner':self.channelOwner, u'properties':[prop1, prop2]}
        ch2 = {u'name':u'orgChannel2', u'owner':self.channelOwner, u'properties':[prop1, prop2]}
        ch3 = {u'name':u'orgChannel3', u'owner':self.channelOwner, u'properties':[prop1]}
        channels = [ch1, ch2, ch3]

        self.client.set(property=prop1)
        self.client.set(property=prop2)

        self.client.set(channels=channels)
        chs = self.client.find(property=[(u'originalProp1', u'originalVal'), \
                                         (u'originalProp2', u'originalVal')])
        self.assertTrue(len(chs) == 2)
        for ch in chs:
            if (ch[u'properties'][0])[u'name'] == 'originalProp1':
                (ch[u'properties'][0])[u'value'] = 'newVal'
        self.client.set(channels=chs)
        self.assertTrue(len(self.client.find(property=[('originalProp1', 'newVal')])) == 2, \
                        'failed to update prop value')
        ''' clean up '''
        for ch in channels:
            self.client.delete(channelName=ch[u'name'])
        self.client.delete(propertyName=prop1[u'name'])
        self.client.delete(propertyName=prop2[u'name'])
        pass

    def testDestructiveSetRemoveChannels(self):
        '''
        This test will check that a POST in the channels resources is destructive
        '''
        testProp = {u'name':u'testProp', u'owner' : self.propOwner}
        try:
            self.clientProp.set(property=testProp)
            testProp[u'value'] = 'original'
            testChannels = [{u'name':u'pyChannel1', u'owner':self.channelOwner, u'properties':[testProp]}, \
                            {u'name':u'pyChannel2', u'owner':self.channelOwner}, \
                            {u'name':u'pyChannel3', u'owner':self.channelOwner}]
            self.clientCh.set(channel=testChannels[0])

            self.assertEqual(len(self.client.find(name=u'pyChannel*')), 1, \
                             'Failed to set a single channel correctly')
            result = self.client.find(name=u'pyChannel1')[0]
            self.assertTrue(checkPropWithValueInList( result['properties'], [testProp] ), \
                            'Failed to add pychannel1 correctly')
            testChannels[0] = {u'name':u'pyChannel1', u'owner':self.channelOwner}
            self.clientCh.set(channels=testChannels)
            self.assertEqual(len(self.client.find(name=u'pyChannel*')), 3, \
                             'Failed to set a list of channels correctly')
            self.assertTrue(not self.client.find(name=u'pyChannel1')[0][u'properties'] or \
                            testProp not in self.client.find(name=u'pyChannel1')[0][u'properties'], \
                            'Failed to set pychannel1 correctly')
        finally:
            for ch in testChannels:
                self.clientCh.delete(channelName=ch[u'name'])
            self.clientProp.delete(propertyName=testProp[u'name'])

    def testSetRemoveSpecialChar(self):
        spChannel = {u'name':u'special{}<chName:->*', u'owner':self.channelOwner}
        spProperty = {u'name':u'special{}<propName:->*', u'owner':self.propOwner, u'value':'sp<Val:->*'}
        spTag = {u'name':u'special{}<tagName:->*', u'owner':self.tagOwner}
        spChannel[u'properties'] = [spProperty]
        spChannel[u'tags'] = [spTag]

        try:
            self.client.set(tag=spTag)
            self.assertNotEqual(self.client.findTag(spTag[u'name']), None, 'failed to set Tag with special chars')
            self.client.set(property=spProperty)
            self.assertNotEqual(self.client.findProperty(spProperty[u'name']), None, 'failed to set Property with special chars')
            self.client.set(channel=spChannel)
            foundChannels = self.client.find(name=spChannel[u'name'])
            self.assertNotEqual(foundChannels[0], None, 'failed to set channel with special chars')
            self.assertTrue(foundChannels[0][u'name'] == spChannel[u'name'] and \
                            checkTagInList(foundChannels[0][u'tags'], [spTag]) and \
                            checkPropWithValueInList(foundChannels[0][u'properties'], [spProperty]), \
                            'Returned channel missing required properties and/or tags')
        finally:
            '''Cleanup'''
            self.client.delete(channelName=spChannel[u'name'])
            self.assertFalse(self.client.find(name=spChannel[u'name']), 'failed to delete channel with special char')
            self.client.delete(tagName=spTag[u'name'])
            self.assertTrue(self.client.findTag(spTag[u'name']) == None)
            self.client.delete(propertyName=spProperty[u'name'])
            self.assertTrue(self.client.findProperty(spProperty[u'name']) == None)

    def testQuotes(self):
        spChannel = {u'name':u'\'"Name', u'owner':self.channelOwner}
        self.client.set(channel=spChannel)
        self.assertTrue(len(self.client.find(name=u'\'"Name')) == 1)
        self.client.delete(channelName=u'\'"Name')
#===============================================================================
# Update Operation Tests
#===============================================================================

    def testUpdateChannel(self):
        '''
        Test the updating of a channel by adding tags and properties
        '''
        try:
            testProp1 = {u'name':u'pyTestProp1', u'owner':self.propOwner, u'value':u'testVal1'}
            self.client.set(property=testProp1)
            testTag1 = {u'name':u'pyTestTag1', u'owner':self.tagOwner}
            self.client.set(tag=testTag1)

            testChannel = {u'name':u'pyTestChannelName1', u'owner': self.channelOwner, u'properties':[testProp1], u'tags':[testTag1]}
            self.clientCh.set(channel=testChannel)

            testProp2 = {u'name':u'pyTestProp2', u'owner':self.propOwner, u'value':u'testVal2'}
            self.client.set(property=testProp2)
            testTag2 = {u'name':u'pyTestTag2', u'owner':self.tagOwner}
            self.client.set(tag=testTag2)
            testChannel = {u'name':u'pyTestChannelName1', u'owner': self.channelOwner, u'properties':[testProp2], u'tags':[testTag2]}
            self.clientCh.update(channel=testChannel)

            result = self.client.find(name=u'pyTestChannelName1')
            self.assertTrue(len(result) == 1, 'incorrect number of channels returned')
            self.assertTrue(result[0][u'name'] == u'pyTestChannelName1', 'incorrect channel returned')
            self.assertTrue(checkTagInList(result[0]['tags'], [testTag1, testTag2]), 'Failed to update the tags')
            self.assertTrue(checkPropWithValueInList(result[0]['properties'], [testProp1, testProp2]), 'Failed to update the properties')
        finally:
            '''Cleanup'''
            self.client.delete(tagName=testTag1[u'name'])
            self.client.delete(propertyName=testProp1[u'name'])
            self.client.delete(tagName=testTag2[u'name'])
            self.client.delete(propertyName=testProp2[u'name'])
            self.clientCh.delete(channelName=testChannel[u'name'])
            result = self.client.find(name=u'pyTestChannelName')
            self.assertFalse(result, 'incorrect number of channels returned')
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
        self.orgTag = {u'name':u'originalTag', u'owner': self.tagOwner}
        self.orgProp = {u'name':u'originalProp', u'owner':self.propOwner, u'value':u'originalValue'}

        self.clientTag.set(tag=self.orgTag)
        self.clientProp.set(property=self.orgProp)

        self.clientCh.set(channel={u'name':u'originalChannelName', \
                                          u'owner':self.channelOwner, \
                                          u'properties':[self.orgProp], \
                                          u'tags':[self.orgTag]})
        ch = self.client.find(name=u'originalChannelName')
        self.assertTrue(len(ch) == 1 and
                        self.orgProp in ch[0][u'properties'] and \
                        self.orgTag in ch[0][u'tags']);
        pass

    def UpdateTagName(self):
        newTagName = 'updatedTag'
        self.assertTrue(self.client.findTag(self.orgTag[u'name']) != None)
        self.clientTag.update(tag={u'name':newTagName, u'owner': self.tagOwner}, \
                           originalTagName=self.orgTag[u'name'])
        self.assertTrue(self.client.findTag(self.orgTag[u'name']) == None and \
                        self.client.findTag(newTagName) != None)
        # check that renaming the Tag does not remove it from any channel
        channelTags = self.client.find(name=u'originalChannelName')[0][u'tags']
        self.assertTrue(self.orgTag not in channelTags and \
                        {u'name':newTagName, u'owner':self.tagOwner} in channelTags)
        self.clientTag.update(tag=self.orgTag, originalTagName=newTagName)

    def testUpdateTagOwner(self):
        '''Test implemented in testUpdateTag'''
        pass

    # removed test till bug in the sevice is fixed - channelfinder needs to check for the existance of oldname not name
    def UpdatePropName(self):
        newPropName = u'updatedProperty'
        self.assertTrue(self.client.findProperty(self.orgProp[u'name']) != None)
        self.clientProp.update(property={u'name':newPropName, u'owner':self.propOwner}, \
                                         originalPropertyName=self.orgProp[u'name'])
        self.assertTrue(self.client.findProperty(self.orgProp[u'name']) == None and \
                        self.client.findProperty(newPropName) != None)
        # check to ensure that the Property is renamed and not removed from any channels
        channelProperties = self.client.find(name=u'originalChannelName')[0].getProperties()
        self.assertTrue(self.orgProp[u'name'] not in channelProperties.keys() and \
                        newPropName in channelProperties.keys())
        self.clientProp.update(property=self.orgProp, originalPropertyName=newPropName)


    def testUpdatePropOwner(self):
        pass

    def testUpdateChannelName(self):
        ch = self.client.find(name=u'originalChannelName')[0]
        newChannel = {u'name':u'updatedChannelName', u'owner': ch[u'owner'], u'properties': ch[u'properties'], u'tags': ch[u'tags']}
        self.clientCh.update(originalChannelName=u'originalChannelName', \
                           channel=newChannel)
        self.assertTrue(self.client.find(name=u'originalChannelName') == [])
        self.assertTrue(len(self.client.find(name=u'updatedChannelName')) == 1)
        # reset the channel back
        self.clientCh.update(originalChannelName=u'updatedChannelName', \
                           channel=ch)
        self.assertTrue(len(self.client.find(name=u'originalChannelName')) == 1)
        self.assertTrue(self.client.find(name=u'updatedChannelName') == [])

    def UpdateChannelOwner(self):
        ch = self.client.find(name='originalChannelName')[0]
        newChannel = {u'name':ch[u'name'], u'owner':self.tagOwner, u'properties': ch[u'properties'], u'tags':ch[u'tags']}
        self.clientCh.update(originalChannelName=u'originalChannelName', \
                           channel=newChannel)
        self.assertTrue(self.client.find(name=u'originalChannelName')[0][u'owner'] == self.tagOwner)
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
        ch = self.client.find(name=u'originalChannelName')[0]
        updatedProp = {u'name':u'originalProp', u'owner':self.propOwner, u'value':u'updatedValue'}
        newTag = {u'name':u'updatedTag', u'owner':self.tagOwner}
        newProp = {u'name':u'newProp', u'owner':self.propOwner, u'value':u'newValue'}
        try:
            self.clientTag.set(tag=newTag)
            self.clientProp.set(property=newProp)
            newChannel = {u'name':u'updatedChannelName', u'owner':self.channelOwner, \
                                 u'properties':[updatedProp, newProp], \
                                 u'tags':[newTag]}
            self.clientCh.update(originalChannelName=u'originalChannelName', \
                               channel=newChannel)
            foundChannel = self.client.find(name=u'updatedChannelName')[0]
            self.assertTrue(foundChannel[u'name'] == u'updatedChannelName' and
                            foundChannel[u'owner'] == self.channelOwner and \
                            updatedProp in foundChannel[u'properties'] and\
                            newProp in foundChannel[u'properties'] and \
                            newTag in foundChannel[u'tags'] and \
                            self.orgTag in foundChannel[u'tags'])

        finally:
            #reset
            self.clientCh.update(originalChannelName='updatedChannelName', \
                               channel=ch)
            self.assertTrue(len(self.client.find(name='originalChannelName')), \
                            'failed to reset the updated channels')
            if self.clientTag.findTag(newTag[u'name']):
                self.clientTag.delete(tagName=newTag[u'name'])
            if self.clientProp.findProperty(newProp[u'name']):
                self.clientProp.delete(propertyName=newProp[u'name'])

    def testUpdateChannel2(self):
        '''
        Update a channels using update(channel=updatedChannel)
        '''
        ch = self.client.find(name=u'originalChannelName')
        self.assertTrue(len(ch) == 1 and
                        self.orgProp in ch[0][u'properties'] and
                        self.orgTag in ch[0][u'tags'])
        updated_prop = {u'name': u'originalProp',
                        u'owner': self.propOwner,
                        u'value': u'newPropValue'}
        self.clientCh.update(channel={u'name': u'originalChannelName',
                                      u'owner': u'newOwner',
                                      u'properties': [updated_prop],
                                      u'tags': []})
        ch = self.client.find(name=u'originalChannelName')
        self.assertTrue(len(ch) == 1 and
                        updated_prop in ch[0][u'properties'] and
                        self.orgTag in ch[0][u'tags'] and
                        ch[0][u'owner'] == u'newOwner')


    def testUpdateProperty(self):
        '''
        Update a single property using update(property=updatedProperty)
        Updates existing channels with new property owner, without altering original value.
        '''
        prop = self.client.findProperty(propertyName=u'originalProp')
        self.assertDictEqual(prop, {u'owner': u'cf-update',
                                    u'channels': [],
                                    u'name': u'originalProp',
                                    u'value': None})

        updatedProperty = dict(prop)
        updatedProperty[u'owner'] = u'newOwner'
        self.clientProp.update(property=updatedProperty)
        '''Check property owner'''
        prop = self.client.findProperty(propertyName=u'originalProp')
        self.assertDictEqual(prop, {u'owner': u'newOwner',
                                    u'channels': [],
                                    u'name': u'originalProp',
                                    u'value': None})
        '''Check existing channel'''
        ch = self.client.find(name=u'originalChannelName')
        self.assertTrue({u'owner': u'newOwner',
                         u'name': u'originalProp',
                         u'value': u'originalValue'} in ch[0][u'properties'])

    def testUpdateTag(self):
        '''
        Update a single tag using update(tag=updatedTag)
        Updates owner in all associated channels.
        '''
        tag = self.client.findTag(tagName=u'originalTag')
        self.assertDictEqual(tag, {u'owner': u'cf-update', u'channels': [], u'name': u'originalTag'})

        updatedTag = dict(tag)
        updatedTag[u'owner'] = u'newOwner'
        self.clientTag.update(tag=updatedTag)
        '''Check tag owner'''
        tag = self.client.findTag(tagName=u'originalTag')
        self.assertDictEqual(tag, {u'owner': u'newOwner', u'channels': [], u'name': u'originalTag'})
        '''Checks existing channel'''
        ch = self.client.find(name=u'originalChannelName')
        self.assertTrue({u'owner': u'newOwner',
                         u'name': u'originalTag'} in ch[0][u'tags'])

    def tearDown(self):
        self.clientCh.delete(channelName=u'originalChannelName')
        self.clientTag.delete(tagName=u'originalTag')
        self.clientProp.delete(propertyName=u'originalProp')
        pass
'''
#===============================================================================
# Update operations to append tags and properties
#===============================================================================
'''
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

        self.Tag1 = {u'name':u'tag1', u'owner':self.tagOwner}
        self.Tag2 = {u'name':u'tag2', u'owner':self.tagOwner}
        self.Prop1 = {u'name':u'prop1', u'owner':self.propOwner, u'value':u'initialVal'}
        self.Prop2 = {u'name':u'prop2', u'owner':self.propOwner, u'value':u'initialVal'}
        self.ch1 = {u'name':u'orgChannel1', u'owner':self.ChannelOwner, u'tags':[self.Tag1, self.Tag2]}
        self.ch2 = {u'name':u'orgChannel2', u'owner':self.ChannelOwner, u'tags':[self.Tag2]}
        self.ch3 = {u'name':u'orgChannel3', u'owner':self.ChannelOwner}
        self.channels = [self.ch1, self.ch2, self.ch3]
        self.clientTag.set(tags=[self.Tag1, self.Tag2])
        self.clientProp.set(properties=[self.Prop1, self.Prop2])
        self.client.set(channels=self.channels)
        # originally 1 channel has tag Tag1 and 2 channels have tag Tag2
        self.assertTrue(len(self.client.find(tagName=self.Tag1[u'name'])) == 1)
        self.assertTrue(len(self.client.find(tagName=self.Tag2[u'name'])) == 2)
        pass

    def tearDown(self):
        self.clientTag.delete(tagName=self.Tag1[u'name'])
        self.clientTag.delete(tagName=self.Tag2[u'name'])
        self.clientProp.delete(propertyName=self.Prop1[u'name'])
        self.clientProp.delete(propertyName=self.Prop2[u'name'])
        for channel in self.channels:
            self.client.delete(channelName=channel[u'name'])
        self.assertTrue(self.client.find(name=u'orgChannel?') == [])
        pass

    def testUpdateAppendTag2Channel(self):
        '''
        Add tag to channel3 without removing it from the first 2 channels
        '''
        self.clientTag.update(tag=self.Tag2, channelName=self.ch3[u'name'])
        self.assertTrue(len(self.client.find(tagName=self.Tag2[u'name'])) == 3)

    def testUpdateAppendTag2Channels(self):
        '''
        Add tag to channels 2-3 without removing it from channel 1
        '''
        channelNames = [channel[u'name'] for channel in self.channels]
        self.clientTag.update(tag=self.Tag1, channelNames=channelNames)
        self.assertTrue(len(self.client.find(tagName=self.Tag1[u'name'])) == 3)

    def testUpdateAppendProperty2Channel(self):
        '''
        Test to update a channel with a property
        '''
        self.assertTrue(len(self.client.find(name=self.ch3[u'name'])) == 1 and
                         self.client.find(name=self.ch3[u'name'])[0][u'properties'] == [],
                         'the channel already has properties')
        self.clientProp.update(property=self.Prop1, channelName=self.ch3[u'name'])
        self.assertTrue(len(self.client.find(name=self.ch3[u'name'])) == 1 and
                        self.Prop1 in self.client.find(name=self.ch3[u'name'])[0][u'properties'],
                            'failed to update the channel with a new property')
        '''Check that Value of the property is correctly added'''
        self.Prop2[u'value'] = 'val'
        self.clientProp.update(property=self.Prop2, channelName=self.ch3[u'name'])
        chs = self.client.find(name=self.ch3[u'name'])
        self.assertTrue(len(chs) == 1 and
                        self.Prop1 in chs[0][u'properties'] and
                        self.Prop2 in chs[0][u'properties'],
                        'Failed to update the channel with a new property without disturbing the old one')
        self.client.set(channel=self.ch3)

    def testUpdateAppendProperty2Channels(self):
        '''
        Update a channels with a property
        '''
        self.assertTrue(len(self.client.find(name=self.ch2[u'name'])) == 1 and
                         self.client.find(name=self.ch2[u'name'])[0][u'properties'] == [],
                         'the channel already has properties')
        self.assertTrue(len(self.client.find(name=self.ch3[u'name'])) == 1 and
                         self.client.find(name=self.ch3[u'name'])[0][u'properties'] == [],
                         'the channel already has properties')
        self.Prop1[u'value'] = 'testVal'
        self.clientProp.update(property=self.Prop1, channelNames=[self.ch2[u'name'], self.ch3[u'name']])
        self.assertTrue(len(self.client.find(name=self.ch2[u'name'])) == 1 and
                        self.Prop1 in self.client.find(name=self.ch2[u'name'])[0][u'properties'],
                            'failed to update the channel with a new property')
        self.assertTrue(len(self.client.find(name=self.ch3[u'name'])) == 1 and
                        self.Prop1 in self.client.find(name=self.ch3[u'name'])[0][u'properties'],
                            'failed to update the channel with a new property')

    @unittest.skip("Skipping test for unimplemented functionality.")
    def testUpdateRemoveProperty2Channel(self):
        '''
        Updating a single channel with a property value = empty string is interpreted as a delete property
        '''
        try:
            self.client.set(channel={u'name':u'testChannel', u'owner':self.ChannelOwner, u'properties':[self.Prop1]})
            channel = self.client.find(name=u'testChannel')
            self.assertTrue(len(channel) == 1 and self.Prop1 in channel[0][u'properties'],
                            'Failed to create a test channel with property prop1')
            self.Prop1[u'value'] = ''
            channel[0][u'properties'] = [self.Prop1]
            self.client.update(channel=channel[0])
            self.assertFalse(self.client.find(name=u'testChannel')[0][u'properties'],
                             'Failed to deleted property prop1 form channel testChannel')
        finally:
            self.client.delete(channelName=u'testChannel')

    def UserOwnerCheck(self):
        '''
        the _user_ belonging to cf-properties and another group(cf-asd) sets the owner = group
        but should still be able to update the property
        '''
        try:
            self.clientProp.set(property={u'name':u'testProperty', u'owner':'cf-asd'})
            self.assertTrue({u'name':u'testProperty', u'owner':u'cf-asd'} in self.client.getAllProperties(), \
                            'failed to add testProperty')
            self.client.set(channel={u'name':u'testChannel', u'owner':u'cf-channels'})
            self.clientProp.update(property={u'name':u'testProperty', u'owner':u'cf-asd', u'value':u'val'}, channelName=u'testChannel')
            self.assertEqual(len(self.client.find(property=[(u'testProperty', '*')])), 1,
                                 'Failed to update testChannel with testProperty')
        finally:
            self.clientProp.delete(propertyName=u'testProperty')
            self.client.delete(channelName=u'testChannel')


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

    def testEmptyReturn(self):
        '''
        find for non existing entities should return None instead of a 404
        '''
        self.assertEquals(len(self.client.find(name=u'NonExistingChannelName')), 0,\
                        'Failed to return None when searching for a non existing channel')

    def MultiValueQuery(self):
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
        tagA = {u'name':u'tagA', u'owner':self.tagOwner}
        tagB = {u'name':u'tagB', u'owner':self.tagOwner}
        self.client.set(tag=tagA)
        self.client.set(tag=tagB)
        propA = {u'name':u'propA', u'owner':self.propOwner}
        propB = {u'name':u'propB', u'owner':self.propOwner}
        self.client.set(property=propA)
        self.client.set(property=propB)
        self.client.set(channel={u'name':u'pyTestChannelA', \
                                          u'owner':self.ChannelOwner, \
                                          u'tags':[tagA], \
                                          u'properties':[{u'name':u'propA', u'owner':self.propOwner, u'value':u'1'}]})
        self.client.set(channel={u'name':u'pyTestChannelB', \
                                          u'owner':self.ChannelOwner, \
                                          u'tags':[tagB], \
                                          u'properties':[{u'name':u'propB', u'owner':self.propOwner, u'value':u'2'}]})
        self.client.set(channel={u'name':u'pyTestChannelAB', \
                                          u'owner':self.ChannelOwner, \
                                          u'tags':[tagA, tagB], \
                                          u'properties':[{u'name':u'propA', u'owner':self.propOwner, u'value':u'a'}, \
                                                        {u'name':u'propB', u'owner':self.propOwner, u'value':u'b'}]})
        '''Tag Queries'''
        self.assertEqual(len(self.client.find(tagName=u'tagA')), 2, \
                         'failed to successfully complete a query for tagA')
        self.assertEqual(len(self.client.find(tagName=u'tagB')), 2, \
                         'failed to successfully complete a query for tagB')
        self.assertEqual(len(self.client.find(tagName=u'tagA,tagB')), 1, \
                         'failed to complete a query with ORed tagNames')
        '''Property Queries'''
        chs = self.client.find(property=[(u'propA', '*')])
        self.assertEqual(len(chs), 2, \
                         'Failed of query propA expected 2 found ' + str(len(chs)))
        chs = self.client.find(property=[(u'propA', '1')])
        self.assertEqual(len(chs), 1, \
                         'Failed of query propA expected 1 found ' + str(len(chs)))
        '''conditions AND'ed'''
        '''channels which have both propA and propB'''
        chs = self.client.find(property=[(u'propA', '*'), (u'propB', '*')])
        self.assertEqual(len(chs), 1, \
                         'Failed of query propA expected 1 found ' + str(len(chs)))
        '''conditions OR'ed'''
        '''channels which have propA = pattern1 OR pattern2'''
        chs = self.client.find(property=[(u'propA', '1'), (u'propA', 'a')])
        self.assertEqual(len(chs), 2, \
                         'Failed of query propA expected 2 found ' + str(len(chs)))

        ''' Check Find with multiple parameters '''
        chs = self.client.find(name=u'pyTestChannel*', \
                               tagName=tagA[u'name'], \
                               property=[(u'propA', '*')])
        self.assertEqual(len(chs), 2, 'expected 2 found ' + str(len(chs)))
        chs = self.client.find(name=u'pyTestChannel*', \
                               tagName=tagA[u'name'], \
                               property=[('propA', 'a')])
        self.assertEqual(len(chs), 1, u'expected 1 found ' + str(len(chs)))

        self.client.delete(channelName=u'pyTestChannelA')
        self.client.delete(channelName=u'pyTestChannelB')
        self.client.delete(channelName=u'pyTestChannelAB')

        self.client.delete(tagName=tagA[u'name'])
        self.client.delete(tagName=tagB[u'name'])
        self.client.delete(propertyName=propA[u'name'])
        self.client.delete(propertyName=propB[u'name'])



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

        self.client.set(property={u'name':'existingProperty',u'owner': self.propOwner})

    def tearDown(self):
        self.client.delete(propertyName='existingProperty')

    def testSetChannelWithNonExistingProp(self):
        self.assertRaises(Exception, \
                          self.client.set, \
                          channel={u'name':u'channelName', \
                                            u'owner':self.ChannelOwner, \
                                            u'properties':[{u'name':u'nonExisitngProperty', u'owner':u'owner'}]})

    def testSetChannelWithNonExistingTag(self):
        self.assertRaises(Exception, \
                          self.client.set, \
                          channel={u'name':'channelName', \
                                          u'owner':self.ChannelOwner, \
                                          u'tags':[{u'name':u'nonExisitngTag', u'owner':u'owner'}]})

    def testUpdateChannelWithNonExistingProp(self):
        self.assertRaises(Exception, \
                          self.client.update, \
                          channel={u'name':u'channelName', \
                                          u'owner':self.ChannelOwner, \
                                          u'properties':[{u'name':u'nonExisitngProperty', u'owner':u'owner'}]})

    def testUpdateChannelWithNonExistingTag(self):
        self.assertRaises(Exception,
                          self.client.update,
                          channel={u'name':u'channelName', \
                                          u'owner':self.ChannelOwner, \
                                          u'tags':[{u'name':'nonExisitngTag', u'owner':u'owner'}]})

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
                          channel={u'name':u'channelName', \
                                            u'owner':self.ChannelOwner, \
                                            u'properties':[{u'name':u'existingProperty', u'owner':self.propOwner}]})
        self.assertFalse(self.client.find(name=u'channelName'), \
                         'Failed: should not be able to create a channel with a property with value null')

    def testUpdateChannelWithNullPropertyValue(self):
        self.client.set(channel={u'name':u'channelName', \
                                            u'owner':self.ChannelOwner})
        try:
            self.assertRaises(Exception, \
                              self.client.update, \
                              channel={u'name':u'channelName', \
                                              u'owner':self.ChannelOwner, \
                                              u'properties':[{u'name':u'existingProperty', u'owner':self.propOwner}]})
            print "client: " + str(self.client.find(name='channelName')[0])
            #should this \/ be if client.find... == None ???
            self.assertFalse('existingProperty' in self.client.find(name=u'channelName')[0][u'properties'], \
                             'Failed: should not be able to update a channel with a property with value null')
        finally:
            self.client.delete(channelName=u'channelName')

    def testCreateChannelWithEmptyPropertyValue(self):
        self.assertRaises(Exception, \
                          self.client.set, \
                          channel={u'name':u'channelName', \
                                            u'owner':self.ChannelOwner, \
                                            u'properties':[{u'name':u'existingProperty', u'owner':self.propOwner, u'value':''}]})
        self.assertFalse(self.client.find(name=u'channelName'), \
                         'Failed: should not be able to create a channel with a property with empty value string')

    def UpdateChannelWithEmptyPropertyValue(self):
        self.client.set(channel={u'name':u'channelName', \
                                            u'owner':self.ChannelOwner})
        try:
            self.assertRaises(Exception, \
                              self.client.update, \
                              channel={u'name':u'channelName', \
                                              u'owner':self.ChannelOwner, \
                                              u'properties':[{u'name':u'existingProperty', u'owner':self.propOwner, u'value':u''}]})
            self.assertFalse(u'existingProperty' in ChannelUtil.getAllProperties(self.client.find(name=u'channelName')), \
                             'Failed: should not be able to update a channel with a property with empty value string')
        finally:
            self.client.delete(channelName=u'channelName')

def checkTagInList(allTags, tags):
    '''
    will check is all tags are present in allTags
    '''
    found = []
    for tag in tags:
        [ found.append(tag) for t in allTags if t['name'] == tag['name'] and t['owner'] == tag['owner'] ]
    return tags == found

def checkPropWithValueInList(allProps, props):
    '''
    will check is all props are present in allProps (checks that the values match too)
    '''
    found = []
    for prop in props:
        [ found.append(prop) for p in allProps if p['name'] == prop['name'] and p['owner'] == prop['owner'] and p['value'] == prop['value']]
    return props == found

def checkPropInList(allProps, props):
    '''
    will check is all props are present in allProps (only checks name and owner)
    '''
    found = []
    for prop in props:
        [ found.append(prop) for p in allProps if p['name'] == prop['name'] and p['owner'] == prop['owner'] ]
    return props == found

def checkTagOnChannel(client, channelName, tag):
    '''
    utility method which return true is channelName contains tag
    '''
    ch = client.find(name=channelName)[0]
    if ch[u'tags'] != None and checkTagInList(ch[u'tags'], [tag]):
        return True
    else:
        return False
    
def checkPropertyOnChannel(client, channelName, property):
    '''
    utility method which return true is channelName contains property
    '''
    ch = client.find(name=channelName)[0]
    if ch[u'properties'] != None and checkPropInList(ch[u'properties'], [property]):
        return True
    else:
        return False

def getDefaultTestConfig(arg):
    if _testConf.has_option('DEFAULT', arg):
        return _testConf.get('DEFAULT', arg)
    else:
        return None
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testConnection']
  #  suite = unittest.TestLoader().loadTestsFromTestCase(ErrorTest)
  #  unittest.TextTestRunner(verbosity=2).run(suite)
    
#    print sys.path
    
    unittest.main()
