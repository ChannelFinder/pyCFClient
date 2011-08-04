'''
Copyright (c) 2010 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on Feb 11, 2011

@author: shroffk
'''

class Channel(object):
    '''
    A Channel object consists of a unique name, an owner and an optional list
    of Tags and Properties 
    '''
    # TODO
    # updated the properties datastructure by splitting it into 2 dict 

    
    def __init__(self, name, owner, properties=None, tags=None):
        '''
        Constructor
        name = channel name
        owner = channel owner
        properties = list of properties of type Property
        tags = list of tags of type Tag
        '''
        self.__Name = name.strip();
        self.__Owner = owner.strip();
        self.Properties = properties
        self.Tags = tags
    
    ## All the attributes are private and read only in an attempt to make the channel object immutable
    Name = property(lambda self:self.__Name)
    Owner = property(lambda self:self.__Owner)
#    Properties = property(lambda self:self.Properties)
#    Tags = property(lambda self:self.Tags)
        
    ## TODO don't recreate the dictionary with every get, 
    def getProperties(self):
        '''
        getProperties returns a dictionary containing all properties associated with calling channel.
        the key= propertyName and the value=propertyValue
        '''
        propDictionary = {}
        if self.Properties == None:
            return None
        for property in self.Properties:
            propDictionary[property.Name] = property.Value
        return propDictionary

#    properties = property(getProperties)
    
    ## TODO don't recreate the list with each get call
    def getTags(self):
        '''
        get tags returns a list of tagNames for the tags associated with this channel
        '''
        if self.Tags == None:
            return None
        else:
            return set([ tag.Name for tag in self.Tags])
    
#    tags = property(getTags)

class Property(object):
    '''
    Property consists of a name, an owner and a value  
    '''
    
    def __init__(self, name, owner, value=None):
        self.Name = name.strip()
        self.Owner = owner.strip()
        self.Value = value.strip()
    
    def __cmp__(self, *arg, **kwargs):  
        if arg[0] == None:
            return 1      
        return cmp((self.Name, self.Value), (arg[0].Name, arg[0].Value))
        
class Tag(object):
    '''
    Tag object consists on a name and an owner
    '''
    
    def __init__(self, name, owner):
        self.Name = name.strip()
        self.Owner = owner.strip()
    
    def __cmp__(self, *arg, **kwargs):
        if arg[0] == None:
            return 1
        return cmp(self.Name, arg[0].Name)
