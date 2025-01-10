"""
Copyright (c) 2010 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on Feb 15, 2011

@author: shroffk
"""

import unittest

from channelfinder import ChannelFinderClient
from channelfinder.util import ChannelUtil
from _testConf import _testConf, ChannelFinderClientTestCase

import urllib3

urllib3.disable_warnings()


class ConnectionTest(ChannelFinderClientTestCase):
    def testConnection(self):
        testUrl = getDefaultTestConfig("BaseURL")
        self.assertNotEqual(
            ChannelFinderClient(
                BaseURL=testUrl,
                username=getDefaultTestConfig("username"),
                password=getDefaultTestConfig("password"),
            ),
            None,
            "failed to create client",
        )
        badBaseurl = ["", "noSuchURL"]
        for url in badBaseurl:
            self.assertRaises(
                Exception, ChannelFinderClient, BaseURL=url, msg="message"
            )


# ===============================================================================
# Test JSON Parsing
# ===============================================================================
"""
class JSONparserTest(ChannelFinderClientTestCase):

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
                                                            [{u'name':u'Test_first:a<000>:0:0', u'owner':u'shroffk',
                                                             u'properties':[{u'name':u'Test_PropA', u'owner':u'shroffk', u'value':u'0'},
                                                                      {u'name':u'Test_PropB', u'owner':u'shroffk', u'value':u'19'},
                                                                      {u'name':u'Test_PropC', u'owner':u'shroffk', u'value':u'ALL'}],
                                                                      u'tags':[{u'name':u'Test_TagA', u'owner':u'shroffk'},
                                                                       {u'name':u'Test_TagB', u'owner':u'shroffk'}]}])
#        print encodedChannel[u'channels'][u'channel']
        print "TEST "+ str(encodedChannel[u'channels'][u'channel']) + "  ==  " + str(self.channel)
        self.assertTrue(encodedChannel[u'channels'][u'channel'] == self.channel)

    def testEncodeChannels(self):
        self.assertTrue(self.multiChannels ==
                        ChannelFinderClient()._ChannelFinderClient__encodeChannels(ChannelFinderClient()._ChannelFinderClient__decodeChannels(self.multiChannels)))
"""


# ===============================================================================
# Test all the tag operations
# ===============================================================================
class OperationTagTest(ChannelFinderClientTestCase):
    def setUp(self):
        """Default Owners"""
        self.channelOwner = _testConf.get("DEFAULT", "channelOwner")
        self.tagOwner = _testConf.get("DEFAULT", "tagOwner")
        """Default Clients"""
        self.client = ChannelFinderClient(
            BaseURL=_testConf.get("DEFAULT", "BaseURL"),
            username=_testConf.get("DEFAULT", "username"),
            password=_testConf.get("DEFAULT", "password"),
        )
        self.clientTag = ChannelFinderClient(
            BaseURL=_testConf.get("DEFAULT", "BaseURL"),
            username=_testConf.get("DEFAULT", "tagUsername"),
            password=_testConf.get("DEFAULT", "tagPassword"),
        )
        self.testChannels = [
            {"name": "pyTestChannel1", "owner": self.channelOwner},
            {"name": "pyTestChannel2", "owner": self.channelOwner},
            {"name": "pyTestChannel3", "owner": self.channelOwner},
        ]
        self.client.set(channels=self.testChannels)
        self.assertTrue(
            len(self.client.find(name="pyTestChannel*")) == 3,
            "Error: Failed to set channel",
        )

    def tearDown(self):
        for ch in self.testChannels:
            self.client.delete(channelName=ch["name"])

    def testCreateAndDeleteTag(self):
        testTag = {"name": "setTestTag", "owner": self.tagOwner}
        try:
            self.clientTag.set(tag=testTag)
            foundtag = self.client.findTag(testTag["name"])
            self.assertIsNotNone(foundtag, "failed to create a test tag")
            self.assertTrue(
                checkTagInList([foundtag], [testTag]), "tag not created correctly"
            )
        finally:
            self.clientTag.delete(tagName=testTag["name"])
            foundtag = self.client.findTag(testTag["name"])
            self.assertIsNone(foundtag, "failed to delete the test tag")

    def testCreateAndDeleteTagWithChannel(self):
        testTag = {
            "name": "setTestTag",
            "owner": self.tagOwner,
            "channels": [self.testChannels[0]],
        }
        try:
            result = self.clientTag.set(tag=testTag)
            foundtag = self.client.findTag(testTag["name"])
            self.assertIsNotNone(foundtag, "failed to create a test tag")
            self.assertTrue(
                checkTagInList([foundtag], [testTag]), "tag not created correctly"
            )
            """check the created tag was added to the channel"""
            self.assertTrue(
                checkTagOnChannel(self.client, self.testChannels[0]["name"], foundtag),
                "Failed to correctly set the created tag to the appropriate channel",
            )
        finally:
            self.clientTag.delete(tagName=testTag["name"])
            foundtag = self.client.findTag(testTag["name"])
            self.assertIsNone(foundtag, "failed to delete the test tag")

    def testCreateAndDeleteTags(self):
        testTags = [
            {"name": "pyTag1", "owner": self.tagOwner},
            {"name": "pyTag2", "owner": self.tagOwner},
            {"name": "pyTag3", "owner": self.tagOwner},
        ]
        try:
            self.clientTag.set(tags=testTags)
            """Check if all the tags were correctly Added """
            for tag in testTags:
                self.assertTrue(
                    self.client.findTag(tagname=tag["name"]),
                    "Error: tag " + tag["name"] + " was not added",
                )
        finally:
            """delete the Tags """
            for tag in testTags:
                self.clientTag.delete(tagName=tag["name"])
            """Check all the tags were correctly removed """
            for tag in testTags:
                self.assertEqual(
                    self.client.findTag(tagname="pyTag1"),
                    None,
                    "Error: tag " + tag["name"] + " was not removed",
                )

    def testSetRemoveTag2Channel(self):
        """
        Set Tag to channel removing it from all other channels
        for non destructive operation check TestUpdateAppend
        """
        testTag = {"name": "pySetTag", "owner": self.tagOwner}
        try:
            self.client.set(tag=testTag)
            self.client.set(tag=testTag, channelName=self.testChannels[0]["name"])

            self.assertTrue(
                checkTagOnChannel(self.client, "pyTestChannel1", testTag),
                "Error: Tag-pySetTag not added to the channel-pyTestChannel1",
            )

            self.client.set(tag=testTag, channelName=self.testChannels[1]["name"])
            # check if the tag has been added to the new channel and removed from the old channel
            self.assertTrue(
                checkTagOnChannel(self.client, self.testChannels[1]["name"], testTag)
                and not checkTagOnChannel(
                    self.client, self.testChannels[0]["name"], testTag
                ),
                "Error: Tag-pySetTag not added to the channel-pyTestChannel2",
            )

            self.client.delete(tag=testTag, channelName=self.testChannels[1]["name"])
            self.assertTrue(
                not checkTagOnChannel(
                    self.client, self.testChannels[1]["name"], testTag
                ),
                "Error: Failed to delete the tag-pySetTag from channel-pyTestChannel1",
            )
        finally:
            self.client.delete(tagName=testTag["name"])

    # TODO set a check for removing the tag from a subset of channels which have that tag

    def testSetRemoveTag2Channels(self):
        """
        Set tags to a set of channels and remove it from all other channels
        """
        testTag = {"name": "pySetTag", "owner": self.tagOwner}
        # the list comprehension is used to construct a list of all the channel names
        channelNames = [channel["name"] for channel in self.testChannels]
        try:
            self.client.set(tag=testTag, channelNames=channelNames)
            responseChannelNames = [
                channel["name"] for channel in self.client.find(tagName=testTag["name"])
            ]
            for ch in channelNames:
                self.assertTrue(
                    ch in responseChannelNames,
                    "Error: tag-pySetTag not added to channel " + ch,
                )
            self.client.delete(tag=testTag, channelNames=channelNames)
            response = self.client.find(tagName=testTag["name"])
            if response:
                responseChannelNames = [channel["name"] for channel in response]
                for ch in channelNames:
                    self.assertFalse(
                        ch in responseChannelNames,
                        "Error: tag-pySetTag not removed from channel " + ch,
                    )
        finally:
            self.client.delete(tagName=testTag["name"])

    def testUpdateTag(self):
        """
        Add a tag to a group of channels without removing it from existing channels
        """
        tag = {
            "name": "initialTestTag",
            "owner": self.tagOwner,
            "channels": [self.testChannels[0]],
        }
        try:
            """Create initial tag"""
            self.clientTag.set(tag=tag)
            self.assertIsNotNone(
                self.client.findTag(tag["name"]), "failed to create a test tag"
            )
            """Update tag with new channels"""
            tag["channels"] = [self.testChannels[1], self.testChannels[2]]
            self.clientTag.update(tag=tag)

            for channel in self.testChannels:
                self.assertTrue(
                    checkTagOnChannel(self.client, channel["name"], tag),
                    "Failed to updated tag",
                )
        finally:
            """cleanup"""
            self.client.delete(tagName=tag["name"])
            self.assertIsNone(
                self.client.findTag(tag["name"]),
                "failed to delete the test tag:" + tag["name"],
            )

    def testUpdateTags(self):
        """
        Add tags to a group of channels without removing it from existing channels
        """
        tag1 = {
            "name": "pyTestTag1",
            "owner": self.tagOwner,
            "channels": [self.testChannels[0]],
        }
        tag2 = {
            "name": "pyTestTag2",
            "owner": self.tagOwner,
            "channels": [self.testChannels[0]],
        }

        try:
            """Create initial tags which are set on the pyTestChannel1"""
            self.clientTag.set(tags=[tag1, tag2])
            self.assertIsNotNone(
                self.client.findTag(tag1["name"]),
                "failed to create a test tag: pyTestTag1",
            )
            self.assertIsNotNone(
                self.client.findTag(tag1["name"]),
                "failed to create a test tag: pyTestTag2",
            )
            """Update tags with new channels"""
            tag1["channels"] = [self.testChannels[1], self.testChannels[2]]
            tag2["channels"] = [self.testChannels[1], self.testChannels[2]]
            self.clientTag.update(tags=[tag1, tag2])
            """Check that the all channels have been updated with the tags"""
            for channel in self.testChannels:
                self.assertTrue(
                    checkTagOnChannel(self.client, channel["name"], tag1)
                    and checkTagOnChannel(self.client, channel["name"], tag2),
                    "Failed to updated tags",
                )
        finally:
            """cleanup"""
            self.client.delete(tagName=tag1["name"])
            self.client.delete(tagName=tag2["name"])
            self.assertIsNone(
                self.client.findTag(tag1["name"]),
                "failed to delete the test tag:" + tag1["name"],
            )
            self.assertIsNone(
                self.client.findTag(tag2["name"]),
                "failed to delete the test tag:" + tag2["name"],
            )

    def testGetAllTags(self):
        """Test setting multiple tags and listing all tags"""
        testTags = [
            {"name": "testTag1", "owner": self.tagOwner},
            {"name": "testTag2", "owner": self.tagOwner},
            {"name": "testTag3", "owner": self.tagOwner},
        ]
        try:
            self.client.set(tags=testTags)
            allTags = self.client.getAllTags()
            self.assertTrue(
                checkTagInList(allTags, testTags), "Failed to create multiple tags"
            )
        finally:
            # delete the Tags
            for tag in testTags:
                self.client.delete(tagName=tag["name"])
            # Check all the tags were correctly removed
            for tag in testTags:
                self.assertEqual(
                    self.client.findTag(tagname=tag["name"]),
                    None,
                    "Error: property " + tag["name"] + " was not removed",
                )


# ===============================================================================
# Test all the property operations
# ===============================================================================


class OperationPropertyTest(ChannelFinderClientTestCase):
    def setUp(self):
        """Default Owners"""
        self.channelOwner = _testConf.get("DEFAULT", "channelOwner")
        self.propOwner = _testConf.get("DEFAULT", "propOwner")
        """Default Clients"""
        self.client = ChannelFinderClient(
            BaseURL=_testConf.get("DEFAULT", "BaseURL"),
            username=_testConf.get("DEFAULT", "username"),
            password=_testConf.get("DEFAULT", "password"),
        )
        self.clientProp = ChannelFinderClient(
            BaseURL=_testConf.get("DEFAULT", "BaseURL"),
            username=_testConf.get("DEFAULT", "propUsername"),
            password=_testConf.get("DEFAULT", "propPassword"),
        )
        self.testChannels = [
            {"name": "pyTestChannel1", "owner": self.channelOwner},
            {"name": "pyTestChannel2", "owner": self.channelOwner},
            {"name": "pyTestChannel3", "owner": self.channelOwner},
        ]
        self.client.set(channels=self.testChannels)
        self.assertTrue(
            len(self.client.find(name="pyTestChannel*")) == 3,
            "Error: Failed to set channel",
        )
        pass

    def tearDown(self):
        for ch in self.testChannels:
            self.client.delete(channelName=ch["name"])
        pass

    def testCreateAndDeleteProperty(self):
        """
        Create and delete a single property
        """
        testProperty = {"name": "setTestProp", "owner": self.propOwner}
        try:
            result = self.clientProp.set(property=testProperty)
            foundProperty = self.client.findProperty(testProperty["name"])
            self.assertIsNotNone(foundProperty, "failed to create a test property")
            self.assertTrue(
                checkPropInList([foundProperty], [testProperty]),
                "property not created correctly",
            )
        finally:
            self.client.delete(propertyName=testProperty["name"])
            foundProperty = self.client.findProperty(testProperty["name"])
            self.assertIsNone(foundProperty, "failed to delete the test property")

    def testCreateAndDeletePropertyWithChannel(self):
        """
        Create and delete a single property
        """
        ch = self.testChannels[0]
        ch["properties"] = [
            {"name": "setTestProp", "owner": self.propOwner, "value": "testValue1"}
        ]
        testProperty = {
            "name": "setTestProp",
            "owner": self.propOwner,
            "channels": [ch],
        }
        try:
            result = self.clientProp.set(property=testProperty)
            foundProperty = self.client.findProperty(testProperty["name"])
            self.assertIsNotNone(foundProperty, "failed to create a test property")
            self.assertTrue(
                checkPropInList([foundProperty], [testProperty]),
                "property not created correctly",
            )
            """check the created property was added to the channel"""
            self.assertTrue(
                checkPropertyOnChannel(
                    self.client, self.testChannels[0]["name"], foundProperty
                ),
                "Failed to correctly set the created property to the appropriate channel",
            )
        finally:
            self.client.delete(propertyName=testProperty["name"])
            foundProperty = self.client.findProperty(testProperty["name"])
            self.assertIsNone(foundProperty, "failed to delete the test property")

    def testCreateAndDeletePropertyWithChannels(self):
        """
        Create and delete a single property
        """
        ch1 = self.testChannels[0]
        ch1["properties"] = [
            {"name": "setTestProp", "owner": self.propOwner, "value": "testValue1"}
        ]
        ch2 = self.testChannels[1]
        ch2["properties"] = [
            {"name": "setTestProp", "owner": self.propOwner, "value": "testValue2"}
        ]
        testProperty = {
            "name": "setTestProp",
            "owner": self.propOwner,
            "channels": [ch1, ch2],
        }
        try:
            self.clientProp.set(property=testProperty)
            foundProperty = self.client.findProperty(testProperty["name"])
            self.assertIsNotNone(foundProperty, "failed to create a test property")
            self.assertTrue(
                checkPropInList([foundProperty], [testProperty]),
                "property not created correctly",
            )
            """check the created property was added to the channel"""
            self.assertTrue(
                checkPropertyOnChannel(
                    self.client, self.testChannels[0]["name"], foundProperty
                ),
                "Failed to correctly set the created property to the appropriate channel",
            )
            self.assertTrue(
                checkPropertyOnChannel(
                    self.client, self.testChannels[1]["name"], foundProperty
                ),
                "Failed to correctly set the created property to the appropriate channel",
            )
        finally:
            self.client.delete(propertyName=testProperty["name"])
            foundProperty = self.client.findProperty(testProperty["name"])
            self.assertIsNone(foundProperty, "failed to delete the test property")

    def testCreateAndDeleteProperties(self):
        """
        Create and delete a set of properties
        """
        testProperty1 = {"name": "pyTestProp1", "owner": self.propOwner}
        testProperty2 = {"name": "pyTestProp2", "owner": self.propOwner}
        try:
            self.clientProp.set(properties=[testProperty1, testProperty2])
            self.assertTrue(
                checkPropInList(
                    self.clientProp.getAllProperties(), [testProperty1, testProperty2]
                ),
                "property not created correctly",
            )
        finally:
            self.client.delete(propertyName=testProperty1["name"])
            self.client.delete(propertyName=testProperty2["name"])
            self.assertIsNone(
                self.client.findProperty(testProperty1["name"]),
                "failed to delete the test property1",
            )
            self.assertIsNone(
                self.client.findProperty(testProperty2["name"]),
                "failed to delete the test property1",
            )

    def testSetRemoveProperty2Channel(self):
        """
        Set Property to channel removing it from all other channels
        for non destructive operation check TestUpdateAppend
        """
        testProperty = {"name": "setTestProp", "owner": self.propOwner}
        try:
            self.clientProp.set(property=testProperty)
            ch0 = self.testChannels[0]
            ch0["properties"] = [
                {"name": "setTestProp", "owner": self.propOwner, "value": "testValue1"}
            ]
            testProperty["channels"] = [ch0]
            self.client.set(property=testProperty)
            self.assertTrue(
                checkPropertyOnChannel(self.client, ch0["name"], testProperty),
                "Error: Property - setTestProp not added to the channel-pyTestChannel1",
            )

            ch1 = self.testChannels[1]
            ch1["properties"] = [
                {"name": "setTestProp", "owner": self.propOwner, "value": "testValue2"}
            ]
            testProperty["channels"] = [ch1]
            self.client.set(property=testProperty)
            """check if the property has been added to the new channel and removed from the old channel"""
            self.assertTrue(
                checkPropertyOnChannel(self.client, ch1["name"], testProperty)
                and not checkPropertyOnChannel(self.client, ch0["name"], testProperty),
                "Error: Tag-pySetTag not added to the channel-pyTestChannel2",
            )
        finally:  # Delete operation causes an error if performed twice, IE: the first delete succeeded
            """delete the property and ensure it is removed from the associated channel"""
            self.client.delete(propertyName=testProperty["name"])
            self.assertTrue(
                not checkPropertyOnChannel(self.client, ch0["name"], testProperty)
                and not checkPropertyOnChannel(self.client, ch1["name"], testProperty),
                "Error: Failed to delete the tag-pySetTag from channel-pyTestChannel1",
            )

    def testGetAllPropperties(self):
        """Test setting multiple properties and listing all tags"""
        testProps = [
            {"name": "pyTestProp1", "owner": self.propOwner},
            {"name": "pyTestProp2", "owner": self.propOwner},
            {"name": "pyTestProp3", "owner": self.propOwner},
        ]
        try:
            self.client.set(properties=testProps)
            allProperties = self.client.getAllProperties()
            self.assertTrue(
                checkPropInList(allProperties, testProps),
                "failed at set a list of properties",
            )
        finally:
            # delete the Tags
            for prop in testProps:
                self.client.delete(propertyName=prop["name"])
            # Check all the tags were correctly removed
            for prop in testProps:
                self.assertEqual(
                    self.client.findProperty(propertyname=prop["name"]),
                    None,
                    "Error: property " + prop["name"] + " was not removed",
                )


# ===============================================================================
#
# ===============================================================================
class OperationChannelTest(ChannelFinderClientTestCase):
    def setUp(self):
        """Default Owners"""
        self.channelOwner = _testConf.get("DEFAULT", "channelOwner")
        self.propOwner = _testConf.get("DEFAULT", "propOwner")
        self.tagOwner = _testConf.get("DEFAULT", "tagOwner")
        """Default Clients"""
        self.client = ChannelFinderClient(
            BaseURL=_testConf.get("DEFAULT", "BaseURL"),
            username=_testConf.get("DEFAULT", "username"),
            password=_testConf.get("DEFAULT", "password"),
        )
        self.clientCh = ChannelFinderClient(
            BaseURL=_testConf.get("DEFAULT", "BaseURL"),
            username=_testConf.get("DEFAULT", "channelUsername"),
            password=_testConf.get("DEFAULT", "channelPassword"),
        )
        self.clientProp = ChannelFinderClient(
            BaseURL=_testConf.get("DEFAULT", "BaseURL"),
            username=_testConf.get("DEFAULT", "propUsername"),
            password=_testConf.get("DEFAULT", "propPassword"),
        )
        self.clientTag = ChannelFinderClient(
            BaseURL=_testConf.get("DEFAULT", "BaseURL"),
            username=_testConf.get("DEFAULT", "tagUsername"),
            password=_testConf.get("DEFAULT", "tagPassword"),
        )

    def testSetDeleteChannel(self):
        """
        Set and Delete a simple channel with no properties or tags
        """
        try:
            testChannel = {"name": "pyTestChannelName", "owner": self.channelOwner}
            self.clientCh.set(channel=testChannel)
            result = self.client.find(name="pyTestChannelName")
            self.assertTrue(len(result) == 1, "incorrect number of channels returned")
            self.assertTrue(
                result[0]["name"] == "pyTestChannelName", "incorrect channel returned"
            )
        finally:
            self.clientCh.delete(channelName=testChannel["name"])
            result = self.client.find(name="pyTestChannelName")
            self.assertFalse(result, "incorrect number of channels returned")

    def testSetDeleteChannelWithPropertiesAndTags(self):
        """
        Set and Delete a simple channel with properties or tags
        """
        try:
            testProp = {
                "name": "pyTestProp",
                "owner": self.propOwner,
                "value": "testVal",
            }
            self.client.set(property=testProp)
            testTag = {"name": "pyTestTag", "owner": self.tagOwner}
            self.client.set(tag=testTag)

            testChannel = {
                "name": "pyTestChannelName",
                "owner": self.channelOwner,
                "properties": [testProp],
                "tags": [testTag],
            }
            self.clientCh.set(channel=testChannel)

            result = self.client.find(name="pyTestChannelName")
            self.assertTrue(len(result) == 1, "incorrect number of channels returned")
            self.assertTrue(
                result[0]["name"] == "pyTestChannelName", "incorrect channel returned"
            )
        finally:
            """Cleanup"""
            self.clientCh.delete(channelName=testChannel["name"])
            self.client.delete(tagName=testTag["name"])
            self.client.delete(propertyName=testProp["name"])
            result = self.client.find(name="pyTestChannelName")
            self.assertFalse(result, "incorrect number of channels returned")

    def testSetRemoveChannels(self):
        """
        Test Set and Delete on a list of channels with no propties or tags
        """
        testChannels = [
            {"name": "pyTestChannel1", "owner": self.channelOwner},
            {"name": "pyTestChannel2", "owner": self.channelOwner},
            {"name": "pyTestChannel3", "owner": self.channelOwner},
        ]
        try:
            self.clientCh.set(channels=testChannels)
            r = self.client.find(name="pyTestChannel*")
            self.assertTrue(
                len(r) == 3,
                "ERROR: # of channels returned expected " + str(len(r)) + " expected 3",
            )
        finally:
            # delete each individually
            for ch in testChannels:
                self.clientCh.delete(channelName=str(ch["name"]))

    def testSetChannelsWithProperties(self):
        """
        This method creates a set of channels and then updates the property values
        using the set method with the channels parameter.
        """
        prop1 = {
            "name": "originalProp1",
            "owner": self.propOwner,
            "value": "originalVal",
        }
        prop2 = {
            "name": "originalProp2",
            "owner": self.propOwner,
            "value": "originalVal",
        }
        ch1 = {
            "name": "orgChannel1",
            "owner": self.channelOwner,
            "properties": [prop1, prop2],
        }
        ch2 = {
            "name": "orgChannel2",
            "owner": self.channelOwner,
            "properties": [prop1, prop2],
        }
        ch3 = {"name": "orgChannel3", "owner": self.channelOwner, "properties": [prop1]}
        channels = [ch1, ch2, ch3]

        self.client.set(property=prop1)
        self.client.set(property=prop2)

        self.client.set(channels=channels)
        chs = self.client.find(
            property=[
                ("originalProp1", "originalVal"),
                ("originalProp2", "originalVal"),
            ]
        )
        self.assertTrue(len(chs) == 2)
        for ch in chs:
            if (ch["properties"][0])["name"] == "originalProp1":
                (ch["properties"][0])["value"] = "newVal"
        self.client.set(channels=chs)
        self.assertTrue(
            len(self.client.find(property=[("originalProp1", "newVal")])) == 2,
            "failed to update prop value",
        )
        """ clean up """
        for ch in channels:
            self.client.delete(channelName=ch["name"])
        self.client.delete(propertyName=prop1["name"])
        self.client.delete(propertyName=prop2["name"])
        pass

    def testDestructiveSetRemoveChannels(self):
        """
        This test will check that a POST in the channels resources is destructive
        """
        testProp = {"name": "testProp", "owner": self.propOwner}
        try:
            self.clientProp.set(property=testProp)
            testProp["value"] = "original"
            testChannels = [
                {
                    "name": "pyChannel1",
                    "owner": self.channelOwner,
                    "properties": [testProp],
                },
                {"name": "pyChannel2", "owner": self.channelOwner},
                {"name": "pyChannel3", "owner": self.channelOwner},
            ]
            self.clientCh.set(channel=testChannels[0])

            self.assertEqual(
                len(self.client.find(name="pyChannel*")),
                1,
                "Failed to set a single channel correctly",
            )
            result = self.client.find(name="pyChannel1")[0]
            self.assertTrue(
                checkPropWithValueInList(result["properties"], [testProp]),
                "Failed to add pychannel1 correctly",
            )
            testChannels[0] = {"name": "pyChannel1", "owner": self.channelOwner}
            self.clientCh.set(channels=testChannels)
            self.assertEqual(
                len(self.client.find(name="pyChannel*")),
                3,
                "Failed to set a list of channels correctly",
            )
            self.assertTrue(
                not self.client.find(name="pyChannel1")[0]["properties"]
                or testProp not in self.client.find(name="pyChannel1")[0]["properties"],
                "Failed to set pychannel1 correctly",
            )
        finally:
            for ch in testChannels:
                self.clientCh.delete(channelName=ch["name"])
            self.clientProp.delete(propertyName=testProp["name"])

    def testSetRemoveSpecialChar(self):
        spChannel = {"name": "special{}<chName:->*", "owner": self.channelOwner}
        spProperty = {
            "name": "special{}<propName:->*",
            "owner": self.propOwner,
            "value": "sp<Val:->*",
        }
        spTag = {"name": "special{}<tagName:->*", "owner": self.tagOwner}
        spChannel["properties"] = [spProperty]
        spChannel["tags"] = [spTag]

        try:
            self.client.set(tag=spTag)
            self.assertNotEqual(
                self.client.findTag(spTag["name"]),
                None,
                "failed to set Tag with special chars",
            )
            self.client.set(property=spProperty)
            self.assertNotEqual(
                self.client.findProperty(spProperty["name"]),
                None,
                "failed to set Property with special chars",
            )
            self.client.set(channel=spChannel)
            foundChannels = self.client.find(name=spChannel["name"])
            self.assertNotEqual(
                foundChannels[0], None, "failed to set channel with special chars"
            )
            self.assertTrue(
                foundChannels[0]["name"] == spChannel["name"]
                and checkTagInList(foundChannels[0]["tags"], [spTag])
                and checkPropWithValueInList(
                    foundChannels[0]["properties"], [spProperty]
                ),
                "Returned channel missing required properties and/or tags",
            )
        finally:
            """Cleanup"""
            self.client.delete(channelName=spChannel["name"])
            self.assertFalse(
                self.client.find(name=spChannel["name"]),
                "failed to delete channel with special char",
            )
            self.client.delete(tagName=spTag["name"])
            self.assertTrue(self.client.findTag(spTag["name"]) == None)
            self.client.delete(propertyName=spProperty["name"])
            self.assertTrue(self.client.findProperty(spProperty["name"]) == None)

    def testQuotes(self):
        spChannel = {"name": "'\"Name", "owner": self.channelOwner}
        self.client.set(channel=spChannel)
        self.assertTrue(len(self.client.find(name="'\"Name")) == 1)
        self.client.delete(channelName="'\"Name")

        # ===============================================================================

    # Update Operation Tests
    # ===============================================================================

    def testUpdateChannel(self):
        """
        Test the updating of a channel by adding tags and properties
        """
        try:
            testProp1 = {
                "name": "pyTestProp1",
                "owner": self.propOwner,
                "value": "testVal1",
            }
            self.client.set(property=testProp1)
            testTag1 = {"name": "pyTestTag1", "owner": self.tagOwner}
            self.client.set(tag=testTag1)

            testChannel = {
                "name": "pyTestChannelName1",
                "owner": self.channelOwner,
                "properties": [testProp1],
                "tags": [testTag1],
            }
            self.clientCh.set(channel=testChannel)

            testProp2 = {
                "name": "pyTestProp2",
                "owner": self.propOwner,
                "value": "testVal2",
            }
            self.client.set(property=testProp2)
            testTag2 = {"name": "pyTestTag2", "owner": self.tagOwner}
            self.client.set(tag=testTag2)
            testChannel = {
                "name": "pyTestChannelName1",
                "owner": self.channelOwner,
                "properties": [testProp2],
                "tags": [testTag2],
            }
            self.clientCh.update(channel=testChannel)

            result = self.client.find(name="pyTestChannelName1")
            self.assertTrue(len(result) == 1, "incorrect number of channels returned")
            self.assertTrue(
                result[0]["name"] == "pyTestChannelName1", "incorrect channel returned"
            )
            self.assertTrue(
                checkTagInList(result[0]["tags"], [testTag1, testTag2]),
                "Failed to update the tags",
            )
            self.assertTrue(
                checkPropWithValueInList(
                    result[0]["properties"], [testProp1, testProp2]
                ),
                "Failed to update the properties",
            )
        finally:
            """Cleanup"""
            self.client.delete(tagName=testTag1["name"])
            self.client.delete(propertyName=testProp1["name"])
            self.client.delete(tagName=testTag2["name"])
            self.client.delete(propertyName=testProp2["name"])
            self.clientCh.delete(channelName=testChannel["name"])
            result = self.client.find(name="pyTestChannelName")
            self.assertFalse(result, "incorrect number of channels returned")


# ===============================================================================
# Update Opertation Tests
# ===============================================================================


class UpdateOperationTest(ChannelFinderClientTestCase):
    def setUp(self):
        """Default set of Owners"""
        self.channelOwner = _testConf.get("DEFAULT", "channelOwner")
        self.propOwner = _testConf.get("DEFAULT", "propOwner")
        self.tagOwner = _testConf.get("DEFAULT", "tagOwner")
        """Default set of clients"""
        self.client = ChannelFinderClient()
        self.clientCh = ChannelFinderClient(
            BaseURL=_testConf.get("DEFAULT", "BaseURL"),
            username=_testConf.get("DEFAULT", "channelUsername"),
            password=_testConf.get("DEFAULT", "channelPassword"),
        )
        self.clientProp = ChannelFinderClient(
            BaseURL=_testConf.get("DEFAULT", "BaseURL"),
            username=_testConf.get("DEFAULT", "propUsername"),
            password=_testConf.get("DEFAULT", "propPassword"),
        )
        self.clientTag = ChannelFinderClient(
            BaseURL=_testConf.get("DEFAULT", "BaseURL"),
            username=_testConf.get("DEFAULT", "tagUsername"),
            password=_testConf.get("DEFAULT", "tagPassword"),
        )
        """ Test Properties and Tags """
        self.orgTag = {"name": "originalTag", "owner": self.tagOwner}
        self.orgProp = {
            "name": "originalProp",
            "owner": self.propOwner,
            "value": "originalValue",
        }
        self.orgTagResponse = {
            "name": "originalTag",
            "owner": self.tagOwner,
            "channels": [],
        }
        self.orgPropResponse = {
            "name": "originalProp",
            "owner": self.propOwner,
            "value": "originalValue",
            "channels": [],
        }

        self.clientTag.set(tag=self.orgTag)
        self.clientProp.set(property=self.orgProp)

        self.clientCh.set(
            channel={
                "name": "originalChannelName",
                "owner": self.channelOwner,
                "properties": [self.orgProp],
                "tags": [self.orgTag],
            }
        )
        ch = self.client.find(name="originalChannelName")
        self.assertTrue(
            len(ch) == 1
            and self.orgPropResponse in ch[0]["properties"]
            and self.orgTagResponse in ch[0]["tags"]
        )

    def UpdateTagName(self):
        newTagName = "updatedTag"
        self.assertTrue(self.client.findTag(self.orgTag["name"]) is not None)
        self.clientTag.update(
            tag={"name": newTagName, "owner": self.tagOwner},
            originalTagName=self.orgTag["name"],
        )
        self.assertTrue(
            self.client.findTag(self.orgTag["name"]) is None
            and self.client.findTag(newTagName) is not None
        )
        # check that renaming the Tag does not remove it from any channel
        channelTags = self.client.find(name="originalChannelName")[0]["tags"]
        self.assertTrue(
            self.orgTagResponse not in channelTags
            and {"name": newTagName, "owner": self.tagOwner, "channels": []}
            in channelTags
        )
        self.clientTag.update(tag=self.orgTag, originalTagName=newTagName)

    def testUpdateTagOwner(self):
        """Test implemented in testUpdateTag"""
        self.assertTrue(True)

    # removed test till bug in the sevice is fixed - channelfinder needs to check for the existance of oldname not name
    def UpdatePropName(self):
        newPropName = "updatedProperty"
        self.assertTrue(self.client.findProperty(self.orgProp["name"]) is not None)
        self.clientProp.update(
            property={"name": newPropName, "owner": self.propOwner},
            originalPropertyName=self.orgProp["name"],
        )
        self.assertTrue(
            self.client.findProperty(self.orgProp["name"]) is None
            and self.client.findProperty(newPropName) is not None
        )
        # check to ensure that the Property is renamed and not removed from any channels
        channelProperties = self.client.find(name="originalChannelName")[
            0
        ].getProperties()
        self.assertTrue(
            self.orgProp["name"] not in channelProperties.keys()
            and newPropName in channelProperties.keys()
        )
        self.clientProp.update(property=self.orgProp, originalPropertyName=newPropName)

    def testUpdatePropOwner(self):
        self.assertTrue(True)

    def testUpdateChannelName(self):
        ch = self.client.find(name="originalChannelName")[0]
        newChannel = {
            "name": "updatedChannelName",
            "owner": ch["owner"],
            "properties": ch["properties"],
            "tags": ch["tags"],
        }
        self.clientCh.update(
            originalChannelName="originalChannelName", channel=newChannel
        )
        self.assertTrue(self.client.find(name="originalChannelName") == [])
        self.assertTrue(len(self.client.find(name="updatedChannelName")) == 1)
        # reset the channel back
        self.clientCh.update(originalChannelName="updatedChannelName", channel=ch)
        self.assertTrue(len(self.client.find(name="originalChannelName")) == 1)
        self.assertTrue(self.client.find(name="updatedChannelName") == [])

    def UpdateChannelOwner(self):
        ch = self.client.find(name="originalChannelName")[0]
        newChannel = {
            "name": ch["name"],
            "owner": self.tagOwner,
            "properties": ch["properties"],
            "tags": ch["tags"],
        }
        self.clientCh.update(
            originalChannelName="originalChannelName", channel=newChannel
        )
        self.assertTrue(
            self.client.find(name="originalChannelName")[0]["owner"] == self.tagOwner
        )

    def testUpdateChannel(self):
        """
        the test updates the channel name and owner
        it also updates an existing property
        and adds a new property and tag
        leaving an existing tag untouched

        TODO
        using the lowest lever _tagOwner_ as the newOwner
        """
        ch = self.client.find(name="originalChannelName")[0]
        updatedProp = {
            "name": "originalProp",
            "owner": self.propOwner,
            "value": "updatedValue",
        }
        newTag = {"name": "updatedTag", "owner": self.tagOwner}
        newProp = {"name": "newProp", "owner": self.propOwner, "value": "newValue"}
        updatedPropResponse = {
            "name": "originalProp",
            "owner": self.propOwner,
            "value": "updatedValue",
            "channels": [],
        }
        newTagResponse = {"name": "updatedTag", "owner": self.tagOwner, "channels": []}
        newPropResponse = {
            "name": "newProp",
            "owner": self.propOwner,
            "value": "newValue",
            "channels": [],
        }
        try:
            self.clientTag.set(tag=newTag)
            self.clientProp.set(property=newProp)
            newChannel = {
                "name": "updatedChannelName",
                "owner": self.channelOwner,
                "properties": [updatedProp, newProp],
                "tags": [newTag],
            }
            self.clientCh.update(
                originalChannelName="originalChannelName", channel=newChannel
            )
            foundChannel = self.client.find(name="updatedChannelName")[0]
            self.assertTrue(foundChannel["name"] == "updatedChannelName")
            self.assertTrue(foundChannel["owner"] == self.channelOwner)
            self.assertTrue(updatedPropResponse in foundChannel["properties"])
            self.assertTrue(newPropResponse in foundChannel["properties"])
            self.assertTrue(newTagResponse in foundChannel["tags"])
            self.assertTrue(self.orgTagResponse in foundChannel["tags"])

        finally:
            # reset
            self.clientCh.update(originalChannelName="updatedChannelName", channel=ch)
            self.assertTrue(
                len(self.client.find(name="originalChannelName")),
                "failed to reset the updated channels",
            )
            if self.clientTag.findTag(newTag["name"]):
                self.clientTag.delete(tagName=newTag["name"])
            if self.clientProp.findProperty(newProp["name"]):
                self.clientProp.delete(propertyName=newProp["name"])

    def testUpdateChannel2(self):
        """
        Update a channels using update(channel=updatedChannel)
        """
        ch = self.client.find(name="originalChannelName")
        self.assertTrue(
            len(ch) == 1
            and self.orgPropResponse in ch[0]["properties"]
            and self.orgTagResponse in ch[0]["tags"]
        )
        updatedProp = {
            "name": "originalProp",
            "owner": self.propOwner,
            "value": "newPropValue",
        }
        self.clientCh.update(
            channel={
                "name": "originalChannelName",
                "owner": "newOwner",
                "properties": [updatedProp],
                "tags": [],
            }
        )
        ch = self.client.find(name="originalChannelName")
        updatedPropResponse = {
            "name": "originalProp",
            "owner": self.propOwner,
            "value": "newPropValue",
            "channels": [],
        }
        self.assertTrue(len(ch) == 1)
        self.assertTrue(updatedPropResponse in ch[0]["properties"])
        self.assertTrue(self.orgTagResponse in ch[0]["tags"])
        self.assertTrue(ch[0]["owner"] == "newOwner")

    def testUpdateProperty(self):
        """
        Update a single property using update(property=updatedProperty)
        Updates existing channels with new property owner, without altering original value.
        """
        prop = self.client.findProperty(propertyname="originalProp")
        prop["channels"] = []
        self.assertDictEqual(
            prop,
            {
                "owner": self.propOwner,
                "channels": [],
                "name": "originalProp",
                "value": None,
            },
        )

        updatedProperty = dict(prop)
        updatedProperty["owner"] = "newOwner"
        self.clientProp.update(property=updatedProperty)
        """Check property owner"""
        prop = self.client.findProperty(propertyname="originalProp")
        prop["channels"] = []
        self.assertDictEqual(
            prop,
            {
                "owner": "newOwner",
                "channels": [],
                "name": "originalProp",
                "value": None,
            },
        )
        """Check existing channel"""
        ch = self.client.find(name="originalChannelName")
        self.assertTrue(
            {
                "owner": "newOwner",
                "name": "originalProp",
                "value": "originalValue",
                "channels": [],
            }
            in ch[0]["properties"]
        )

    def testUpdateTag(self):
        """
        Update a single tag using update(tag=updatedTag)
        Updates owner in all associated channels.
        """
        tag = self.client.findTag(tagname="originalTag")
        tag["channels"] = []
        self.assertDictEqual(
            tag, {"owner": self.tagOwner, "channels": [], "name": "originalTag"}
        )

        updatedTag = dict(tag)
        updatedTag["owner"] = "newOwner"
        self.clientTag.update(tag=updatedTag)
        """Check tag owner"""
        tag = self.client.findTag(tagname="originalTag")
        tag["channels"] = []
        self.assertDictEqual(
            tag, {"owner": "newOwner", "channels": [], "name": "originalTag"}
        )
        """Checks existing channel"""
        ch = self.client.find(name="originalChannelName")
        self.assertTrue(
            {"owner": "newOwner", "name": "originalTag", "channels": []}
            in ch[0]["tags"]
        )

    def tearDown(self):
        self.clientCh.delete(channelName="originalChannelName")
        self.clientTag.delete(tagName="originalTag")
        self.clientProp.delete(propertyName="originalProp")


"""
#===============================================================================
# Update operations to append tags and properties
#===============================================================================
"""


class UpdateAppendTest(ChannelFinderClientTestCase):
    def setUp(self):
        """Default Owners"""
        self.ChannelOwner = _testConf.get("DEFAULT", "channelOwner")
        self.propOwner = _testConf.get("DEFAULT", "propOwner")
        self.tagOwner = _testConf.get("DEFAULT", "tagOwner")
        """Default Client"""
        self.client = ChannelFinderClient(
            BaseURL=_testConf.get("DEFAULT", "BaseURL"),
            username=_testConf.get("DEFAULT", "username"),
            password=_testConf.get("DEFAULT", "password"),
        )
        self.clientProp = ChannelFinderClient(
            BaseURL=_testConf.get("DEFAULT", "BaseURL"),
            username=_testConf.get("DEFAULT", "propUsername"),
            password=_testConf.get("DEFAULT", "propPassword"),
        )
        self.clientTag = ChannelFinderClient(
            BaseURL=_testConf.get("DEFAULT", "BaseURL"),
            username=_testConf.get("DEFAULT", "tagUsername"),
            password=_testConf.get("DEFAULT", "tagPassword"),
        )

        self.Tag1 = {"name": "tag1", "owner": self.tagOwner}
        self.Tag2 = {"name": "tag2", "owner": self.tagOwner}
        self.Prop1 = {"name": "prop1", "owner": self.propOwner, "value": "initialVal"}
        self.Prop2 = {"name": "prop2", "owner": self.propOwner, "value": "initialVal"}
        self.Prop1Response = self.Prop1.copy()
        self.Prop1Response["channels"] = []
        self.Prop2Response = {
            "name": "prop2",
            "owner": self.propOwner,
            "value": "initialVal",
        }
        self.Prop2Response = self.Prop2.copy()
        self.Prop2Response["channels"] = []
        self.ch1 = {
            "name": "orgChannel1",
            "owner": self.ChannelOwner,
            "tags": [self.Tag1, self.Tag2],
        }
        self.ch2 = {
            "name": "orgChannel2",
            "owner": self.ChannelOwner,
            "tags": [self.Tag2],
        }
        self.ch3 = {"name": "orgChannel3", "owner": self.ChannelOwner}
        self.channels = [self.ch1, self.ch2, self.ch3]
        self.clientTag.set(tags=[self.Tag1, self.Tag2])
        self.clientProp.set(properties=[self.Prop1, self.Prop2])
        self.client.set(channels=self.channels)
        # originally 1 channel has tag Tag1 and 2 channels have tag Tag2
        self.assertTrue(len(self.client.find(tagName=self.Tag1["name"])) == 1)
        self.assertTrue(len(self.client.find(tagName=self.Tag2["name"])) == 2)
        pass

    def tearDown(self):
        self.clientTag.delete(tagName=self.Tag1["name"])
        self.clientTag.delete(tagName=self.Tag2["name"])
        self.clientProp.delete(propertyName=self.Prop1["name"])
        self.clientProp.delete(propertyName=self.Prop2["name"])
        for channel in self.channels:
            self.client.delete(channelName=channel["name"])
        self.assertTrue(self.client.find(name="orgChannel?") == [])
        pass

    def testUpdateAppendTag2Channel(self):
        """
        Add tag to channel3 without removing it from the first 2 channels
        """
        self.clientTag.update(tag=self.Tag2, channelName=self.ch3["name"])
        self.assertTrue(len(self.client.find(tagName=self.Tag2["name"])) == 3)

    def testUpdateAppendTag2Channels(self):
        """
        Add tag to channels 2-3 without removing it from channel 1
        """
        channelNames = [channel["name"] for channel in self.channels]
        self.clientTag.update(tag=self.Tag1, channelNames=channelNames)
        self.assertTrue(len(self.client.find(tagName=self.Tag1["name"])) == 3)

    def testUpdateAppendProperty2Channel(self):
        """
        Test to update a channel with a property
        """
        self.assertEqual(len(self.client.find(name=self.ch3["name"])), 1)
        self.assertEqual(
            self.client.find(name=self.ch3["name"])[0]["properties"],
            [],
            "the channel already has properties",
        )
        self.clientProp.update(property=self.Prop1, channelName=self.ch3["name"])
        self.assertEqual(len(self.client.find(name=self.ch3["name"])), 1)
        ch3 = self.client.find(name=self.ch3["name"])
        self.assertTrue(
            self.Prop1Response in ch3[0]["properties"],
            "failed to update the channel with a new property",
        )
        """Check that Value of the property is correctly added"""
        self.Prop2["value"] = "val"
        self.Prop2Response["value"] = "val"
        self.clientProp.update(property=self.Prop2, channelName=self.ch3["name"])
        chs = self.client.find(name=self.ch3["name"])
        self.assertTrue(
            len(chs) == 1
            and self.Prop1Response in chs[0]["properties"]
            and self.Prop2Response in chs[0]["properties"],
            "Failed to update the channel with a new property without disturbing the old one",
        )
        self.client.set(channel=self.ch3)

    def testUpdateAppendProperty2Channels(self):
        """
        Update a channels with a property
        """
        self.assertTrue(
            len(self.client.find(name=self.ch2["name"])) == 1
            and self.client.find(name=self.ch2["name"])[0]["properties"] == [],
            "the channel already has properties",
        )
        self.assertTrue(
            len(self.client.find(name=self.ch3["name"])) == 1
            and self.client.find(name=self.ch3["name"])[0]["properties"] == [],
            "the channel already has properties",
        )
        self.Prop1["value"] = "testVal"
        self.Prop1Response["value"] = "testVal"
        self.clientProp.update(
            property=self.Prop1, channelNames=[self.ch2["name"], self.ch3["name"]]
        )
        self.assertTrue(
            len(self.client.find(name=self.ch2["name"])) == 1
            and self.Prop1Response
            in self.client.find(name=self.ch2["name"])[0]["properties"],
            "failed to update the channel with a new property",
        )
        self.assertTrue(
            len(self.client.find(name=self.ch3["name"])) == 1
            and self.Prop1Response
            in self.client.find(name=self.ch3["name"])[0]["properties"],
            "failed to update the channel with a new property",
        )

    @unittest.skip("Skipping test for unimplemented functionality.")
    def testUpdateRemoveProperty2Channel(self):
        """
        Updating a single channel with a property value = empty string is interpreted as a delete property
        """
        try:
            self.client.set(
                channel={
                    "name": "testChannel",
                    "owner": self.ChannelOwner,
                    "properties": [self.Prop1],
                }
            )
            channel = self.client.find(name="testChannel")
            self.assertTrue(
                len(channel) == 1 and self.Prop1Response in channel[0]["properties"],
                "Failed to create a test channel with property prop1",
            )
            self.Prop1["value"] = ""
            channel[0]["properties"] = [self.Prop1]
            self.client.update(channel=channel[0])
            self.assertFalse(
                self.client.find(name="testChannel")[0]["properties"],
                "Failed to deleted property prop1 form channel testChannel",
            )
        finally:
            self.client.delete(channelName="testChannel")

    def UserOwnerCheck(self):
        """
        the _user_ belonging to cf-properties and another group(cf-asd) sets the owner = group
        but should still be able to update the property
        """
        try:
            self.clientProp.set(property={"name": "testProperty", "owner": "cf-asd"})
            self.assertTrue(
                {"name": "testProperty", "owner": "cf-asd"}
                in self.client.getAllProperties(),
                "failed to add testProperty",
            )
            self.client.set(channel={"name": "testChannel", "owner": "cf-channels"})
            self.clientProp.update(
                property={"name": "testProperty", "owner": "cf-asd", "value": "val"},
                channelName="testChannel",
            )
            self.assertEqual(
                len(self.client.find(property=[("testProperty", "*")])),
                1,
                "Failed to update testChannel with testProperty",
            )
        finally:
            self.clientProp.delete(propertyName="testProperty")
            self.client.delete(channelName="testChannel")


# ===========================================================================
# Query Tests
# ===========================================================================


class QueryTest(ChannelFinderClientTestCase):
    def setUp(self):
        """Default Owners"""
        self.ChannelOwner = _testConf.get("DEFAULT", "channelOwner")
        self.propOwner = _testConf.get("DEFAULT", "propOwner")
        self.tagOwner = _testConf.get("DEFAULT", "tagOwner")
        """Default Client"""
        self.client = ChannelFinderClient(
            BaseURL=_testConf.get("DEFAULT", "BaseURL"),
            username=_testConf.get("DEFAULT", "username"),
            password=_testConf.get("DEFAULT", "password"),
        )
        pass

    def tearDown(self):
        pass

    def testQueryChannel(self):
        pass

    def testEmptyReturn(self):
        """
        find for non existing entities should return None instead of a 404
        """
        self.assertEqual(
            len(self.client.find(name="NonExistingChannelName")),
            0,
            "Failed to return None when searching for a non existing channel",
        )

    def MultiValueQuery(self):
        """
        add multiple search values for the same parameter
        Expected behaviour

        Logically OR'ed
        name=pattern1,pattern2 => return channels with name matching pattern1 OR pattern2
        propName=valPattern1, valPattern2 => return channels with property 'propName'
                                             with values matching valPattern1 OR valPattern2

        Logically AND'ed
        tagName=pattern1, pattern2 => return channels with tags matching pattern1 AND pattern2
        """
        tagA = {"name": "tagA", "owner": self.tagOwner}
        tagB = {"name": "tagB", "owner": self.tagOwner}
        self.client.set(tag=tagA)
        self.client.set(tag=tagB)
        propA = {"name": "propA", "owner": self.propOwner}
        propB = {"name": "propB", "owner": self.propOwner}
        self.client.set(property=propA)
        self.client.set(property=propB)
        self.client.set(
            channel={
                "name": "pyTestChannelA",
                "owner": self.ChannelOwner,
                "tags": [tagA],
                "properties": [
                    {"name": "propA", "owner": self.propOwner, "value": "1"}
                ],
            }
        )
        self.client.set(
            channel={
                "name": "pyTestChannelB",
                "owner": self.ChannelOwner,
                "tags": [tagB],
                "properties": [
                    {"name": "propB", "owner": self.propOwner, "value": "2"}
                ],
            }
        )
        self.client.set(
            channel={
                "name": "pyTestChannelAB",
                "owner": self.ChannelOwner,
                "tags": [tagA, tagB],
                "properties": [
                    {"name": "propA", "owner": self.propOwner, "value": "a"},
                    {"name": "propB", "owner": self.propOwner, "value": "b"},
                ],
            }
        )
        """Tag Queries"""
        self.assertEqual(
            len(self.client.find(tagName="tagA")),
            2,
            "failed to successfully complete a query for tagA",
        )
        self.assertEqual(
            len(self.client.find(tagName="tagB")),
            2,
            "failed to successfully complete a query for tagB",
        )
        self.assertEqual(
            len(self.client.find(tagName="tagA,tagB")),
            1,
            "failed to complete a query with ORed tagNames",
        )
        """Property Queries"""
        chs = self.client.find(property=[("propA", "*")])
        self.assertEqual(
            len(chs), 2, "Failed of query propA expected 2 found " + str(len(chs))
        )
        chs = self.client.find(property=[("propA", "1")])
        self.assertEqual(
            len(chs), 1, "Failed of query propA expected 1 found " + str(len(chs))
        )
        """conditions AND'ed"""
        """channels which have both propA and propB"""
        chs = self.client.find(property=[("propA", "*"), ("propB", "*")])
        self.assertEqual(
            len(chs), 1, "Failed of query propA expected 1 found " + str(len(chs))
        )
        """conditions OR'ed"""
        """channels which have propA = pattern1 OR pattern2"""
        chs = self.client.find(property=[("propA", "1"), ("propA", "a")])
        self.assertEqual(
            len(chs), 2, "Failed of query propA expected 2 found " + str(len(chs))
        )

        """ Check Find with multiple parameters """
        chs = self.client.find(
            name="pyTestChannel*", tagName=tagA["name"], property=[("propA", "*")]
        )
        self.assertEqual(len(chs), 2, "expected 2 found " + str(len(chs)))
        chs = self.client.find(
            name="pyTestChannel*", tagName=tagA["name"], property=[("propA", "a")]
        )
        self.assertEqual(len(chs), 1, "expected 1 found " + str(len(chs)))

        self.client.delete(channelName="pyTestChannelA")
        self.client.delete(channelName="pyTestChannelB")
        self.client.delete(channelName="pyTestChannelAB")

        self.client.delete(tagName=tagA["name"])
        self.client.delete(tagName=tagB["name"])
        self.client.delete(propertyName=propA["name"])
        self.client.delete(propertyName=propB["name"])


# ===============================================================================
#  ERROR tests
# ===============================================================================
class ErrorTest(ChannelFinderClientTestCase):
    def setUp(self):
        """Default Owners"""
        self.ChannelOwner = _testConf.get("DEFAULT", "channelOwner")
        self.propOwner = _testConf.get("DEFAULT", "propOwner")
        self.tagOwner = _testConf.get("DEFAULT", "tagOwner")
        """Default Client"""
        self.client = ChannelFinderClient(
            BaseURL=_testConf.get("DEFAULT", "BaseURL"),
            username=_testConf.get("DEFAULT", "username"),
            password=_testConf.get("DEFAULT", "password"),
        )

        self.client.set(property={"name": "existingProperty", "owner": self.propOwner})

    def tearDown(self):
        self.client.delete(propertyName="existingProperty")

    def testSetChannelWithNonExistingProp(self):
        self.assertRaises(
            Exception,
            self.client.set,
            channel={
                "name": "channelName",
                "owner": self.ChannelOwner,
                "properties": [{"name": "nonExisitngProperty", "owner": "owner"}],
            },
        )

    def testSetChannelWithNonExistingTag(self):
        self.assertRaises(
            Exception,
            self.client.set,
            channel={
                "name": "channelName",
                "owner": self.ChannelOwner,
                "tags": [{"name": "nonExisitngTag", "owner": "owner"}],
            },
        )

    def testUpdateChannelWithNonExistingProp(self):
        self.assertRaises(
            Exception,
            self.client.update,
            channel={
                "name": "channelName",
                "owner": self.ChannelOwner,
                "properties": [{"name": "nonExisitngProperty", "owner": "owner"}],
            },
        )

    def testUpdateChannelWithNonExistingTag(self):
        self.assertRaises(
            Exception,
            self.client.update,
            channel={
                "name": "channelName",
                "owner": self.ChannelOwner,
                "tags": [{"name": "nonExisitngTag", "owner": "owner"}],
            },
        )

    def testUpdateNonExistingChannel(self):
        pass

    def testUpdateNonExistingProperty(self):
        pass

    def testUpdateNoneExistingTag(self):
        pass

    def testIncorrectFindArguments(self):
        self.assertRaises(Exception, self.client.find, processVariable="zzz")
        self.assertRaises(Exception, self.client.find, properties="zzz")
        self.assertRaises(Exception, self.client.find, tag="zzz")

    def testCreateChannelWithNullPropertyValue(self):
        self.assertRaises(
            Exception,
            self.client.set,
            channel={
                "name": "channelName",
                "owner": self.ChannelOwner,
                "properties": [{"name": "existingProperty", "owner": self.propOwner}],
            },
        )
        self.assertFalse(
            self.client.find(name="channelName"),
            "Failed: should not be able to create a channel with a property with value null",
        )

    def testUpdateChannelWithNullPropertyValue(self):
        self.client.set(channel={"name": "channelName", "owner": self.ChannelOwner})
        try:
            self.assertRaises(
                Exception,
                self.client.update,
                channel={
                    "name": "channelName",
                    "owner": self.ChannelOwner,
                    "properties": [
                        {"name": "existingProperty", "owner": self.propOwner}
                    ],
                },
            )
            print("client: " + str(self.client.find(name="channelName")[0]))
            # should this/ be if client.find... == None ???
            self.assertFalse(
                "existingProperty"
                in self.client.find(name="channelName")[0]["properties"],
                "Failed: should not be able to update a channel with a property with value null",
            )
        finally:
            self.client.delete(channelName="channelName")

    def testCreateChannelWithEmptyPropertyValue(self):
        self.assertRaises(
            Exception,
            self.client.set,
            channel={
                "name": "channelName",
                "owner": self.ChannelOwner,
                "properties": [
                    {"name": "existingProperty", "owner": self.propOwner, "value": ""}
                ],
            },
        )
        self.assertFalse(
            self.client.find(name="channelName"),
            "Failed: should not be able to create a channel with a property with empty value string",
        )

    def UpdateChannelWithEmptyPropertyValue(self):
        self.client.set(channel={"name": "channelName", "owner": self.ChannelOwner})
        try:
            self.assertRaises(
                Exception,
                self.client.update,
                channel={
                    "name": "channelName",
                    "owner": self.ChannelOwner,
                    "properties": [
                        {
                            "name": "existingProperty",
                            "owner": self.propOwner,
                            "value": "",
                        }
                    ],
                },
            )
            self.assertFalse(
                "existingProperty"
                in ChannelUtil.getAllProperties(self.client.find(name="channelName")),
                "Failed: should not be able to update a channel with a property with empty value string",
            )
        finally:
            self.client.delete(channelName="channelName")


def checkTagInList(allTags, tags):
    """
    will check is all tags are present in allTags
    """
    found = []
    for tag in tags:
        [
            found.append(tag)
            for t in allTags
            if t["name"] == tag["name"] and t["owner"] == tag["owner"]
        ]
    return tags == found


def checkPropWithValueInList(allProps, props):
    """
    will check is all props are present in allProps (checks that the values match too)
    """
    found = []
    for prop in props:
        [
            found.append(prop)
            for p in allProps
            if p["name"] == prop["name"]
            and p["owner"] == prop["owner"]
            and p["value"] == prop["value"]
        ]
    return props == found


def checkPropInList(allProps, props):
    """
    will check is all props are present in allProps (only checks name and owner)
    """
    found = []
    for prop in props:
        [
            found.append(prop)
            for p in allProps
            if p["name"] == prop["name"] and p["owner"] == prop["owner"]
        ]
    return props == found


def checkTagOnChannel(client, channelName, tag):
    """
    utility method which return true is channelName contains tag
    """
    ch = client.find(name=channelName)[0]
    if ch["tags"] != None and checkTagInList(ch["tags"], [tag]):
        return True
    else:
        return False


def checkPropertyOnChannel(client, channelName, property):
    """
    utility method which return true is channelName contains property
    """
    ch = client.find(name=channelName)[0]
    if ch["properties"] != None and checkPropInList(ch["properties"], [property]):
        return True
    else:
        return False


def getDefaultTestConfig(arg):
    if _testConf.has_option("DEFAULT", arg):
        return _testConf.get("DEFAULT", arg)
    else:
        return None


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testConnection']
    #  suite = unittest.TestLoader().loadTestsFromTestCase(ErrorTest)
    #  unittest.TextTestRunner(verbosity=2).run(suite)

    #    print sys.path

    unittest.main()
