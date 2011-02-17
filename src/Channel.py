'''
Created on Feb 11, 2011

@author: shroffk
'''
from Dictionary import Dictionary
from _abcoll import Set

class Channel(object):
    '''
    channel class 
    '''
    # TODO
    # updated the properties datastructure by splitting it into 2 dict 

    
    def __init__(self, name, owner, properties=None, tags=None):
        '''
        Constructor
        '''
        self.Name = name;
        self.Owner = owner;
        self.Properties = Dictionary(properties)
        self.Tags = Dictionary(tags)
        
    def getProperties(self):
        '''getProperties returns a dictionary containing all properties associated with calling channel.\
        the key= propertyName and the value=propertyValue'''
        propDictionary = {}
        for property in self.Properties:
            propDictionary[property.Name] = property.Value
    
    def getTags(self):
        '''
        get tags returns a list of tagNames for the tags associated with this channel
        '''
        return set([ tag.Name for tag in self.Tags])

class Property(object):
    '''
    Property consists of a name ,an owner and  
    '''
    
    def __init__(self, name, owner, value=None):
        self.Name = name
        self.Owner = owner
        self.Value = value
        
class Tag(object):
    '''
    Tag 
    '''
    
    def __init__(self, name, owner):
        self.Name = name
        self.Owner = owner
