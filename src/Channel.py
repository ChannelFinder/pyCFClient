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
        self.__Name = name;
        self.__Owner = owner;
        self.__Properties = properties
        self.__Tags = tags
    
    ## All the attributes are private and read only in an attempt to make the channel object immutable
    Name = property(lambda self:self.__Name)
    Owner = property(lambda self:self.__Owner)
    Properties = property(lambda self:self.__Properties)
    Tags = property(lambda self:self.__Tags)
        
    ## TODO don't recreate the dictionary with every get, 
    def getProperties(self):
        '''getProperties returns a dictionary containing all properties associated with calling channel.\
        the key= propertyName and the value=propertyValue'''
        propDictionary = {}
        for property in self.Properties:
            propDictionary[property.Name] = property.Value
        return propDictionary

#    properties = property(getProperties)
    
    ## TODO don't recreate the list with each get call
    def getTags(self):
        '''
        get tags returns a list of tagNames for the tags associated with this channel
        '''
        return set([ tag.Name for tag in self.Tags])
    
#    tags = property(getTags)

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
