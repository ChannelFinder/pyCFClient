# -*- coding: utf-8 -*-

"""
Copyright (c) 2010 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on Feb 11, 2011

@author: shroffk
"""

from ._conf import PYTHON3

if PYTHON3:
    # cmp function is gone in Python 3.
    # Define for backward compatibility
    def cmp(a, b):
        return (a > b) - (a < b)


class Channel(object):
    # TODO
    # updated the properties data structure by splitting it into 2 dict

    # All the attributes are private and read only in an attempt to make the channel object immutable
    Name = property(lambda self: self.__Name)
    Owner = property(lambda self: self.__Owner)

    def __init__(self, name, owner, properties=None, tags=None):
        """
        Channel object constructor.
        A Channel object consists of a unique name, an owner and an optional list
        of Tags and Properties

        :param name: channel name
        :param owner: channel owner
        :param properties: list of properties of type Property
        :param tags: list of tags of type Tag
        """
        self.__Name = str(name).strip()
        self.__Owner = str(owner).strip()
        self.Properties = properties
        self.Tags = tags

    ## TODO don't recreate the dictionary with every get
    def getProperties(self):
        """
        Get all properties associated with calling channel.
        It returns a dictionary with format:
            {"property name":  "property value",
                ...
            }

        :return: dictionary of properties, or None if property is empty
        """
        propDictionary = {}
        if self.Properties is None:
            return None
        for prop in self.Properties:
            propDictionary[prop.Name] = prop.Value
        return propDictionary

    def getTags(self):
        """
        Get all tags associated with calling channel.
        All names in the results are unique, and duplicated name are removed.
        It returns a list of tag names with format ['tag 1', 'tag 2', ...]

        :return: list of tags, or None if tag is empty
        """
        if self.Tags is None:
            return None
        else:
            return set([tag.Name for tag in self.Tags])


class Property(object):
    def __init__(self, name, owner, value=None):
        """
        Property consists of a name, an owner and a value
        """
        self.Name = str(name).strip()
        self.Owner = str(owner).strip()
        self.Value = value
        if self.Value:
            str(value).strip()

    def __cmp__(self, *arg, **kwargs):
        if arg[0] is None:
            return 1
        return cmp((self.Name, self.Value), (arg[0].Name, arg[0].Value))


class Tag(object):
    def __init__(self, name, owner):
        """
        Tag object consists on a name and an owner
        """
        self.Name = str(name).strip()
        self.Owner = str(owner).strip()

    def __cmp__(self, *arg, **kwargs):
        if arg[0] is None:
            return 1
        return cmp(self.Name, arg[0].Name)
