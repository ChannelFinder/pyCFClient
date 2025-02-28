"""
Copyright (c) 2010 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on May 11, 2011

@author: shroffk
"""

from .Validators import PropertyValidator, TagValidator


class ChannelUtil(object):
    """
    Utiltity class
    """

    def __init__(self):
        """
        Constructor
        """

    @classmethod
    def getAllTags(cls, channels):
        """
        getAllTags([Channel]) -> [String]
        returns a list of the tagNames of all the tags present on this set of channels
        """
        if isinstance(channels, list):
            allTags = []
            for channel in channels:
                for tag in channel.getTags():
                    allTags.append(tag)
            uniqueNames = frozenset(allTags)
            return list(uniqueNames)
        else:
            return None

    @classmethod
    def getAllProperties(cls, channels):
        """
        getAllProperties([Channel]) -> [String]
        returns a list of the propertyNames of all the properties on the set of channels
        """
        if isinstance(channels, list):
            allProperties = []
            for channel in channels:
                if channel.getProperties():
                    for propertyName in channel.getProperties().keys():
                        allProperties.append(propertyName)
            uniqueNames = frozenset(allProperties)
            return list(uniqueNames)
        else:
            return None

    @classmethod
    def getAllPropValues(cls, channels, propertyName, key=None):
        """
        given the list of channels return a list of all values
        """
        ret = []
        for ch in channels:
            if ch.Properties:
                match = [
                    property
                    for property in ch.Properties
                    if property.Name == propertyName
                ]
                ret.append(match[0].Value)
        return sorted(ret, key=key)

    @classmethod
    def validateChannelsWithTag(cls, channels, tag):
        """
        Utility method to validate a group of channel to ensure they all have the tag 'tag'
        e.g.
        ChannelUtil.validateChannelsWithTag(client.find(name=*), Tag('goldenOrbit','tagOwner'))
        this will return True is all channels with any name have the tag 'goldenOrbit'
        and false if anyone channel does not have that tag
        """
        return cls.channelsValidityCheck(channels, TagValidator(tag))

    @classmethod
    def validateChannelWithProperty(cls, channels, prop):
        """
        Utility method to validate a group of channels to ensure they all have the property 'prop'
        e.g.
        ChannelUtil.validateChannelWithProperty(client.find(ElemName='The Magnet'), Property('length','propOwner','0.3'))

        This will return True if all channels with property ElemName with value 'The Magnet' also have the
        property length with value 0.3
        """
        return cls.channelsValidityCheck(channels, PropertyValidator(prop))

    @classmethod
    def channelsValidityCheck(cls, channels, validator):
        """
        A generic method to validate a set of channels based on a given validator.
        The validator needs to provide the logic on how to validate a channel in a validate method.
        """
        for ch in channels:
            if not validator.validate(ch):
                return False
        return True
