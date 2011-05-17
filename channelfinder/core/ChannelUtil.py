'''
Created on May 11, 2011

@author: shroffk
'''
from sets import Set 

class ChannelUtil(object):
    '''
    Utiltity class
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
    
    @classmethod
    def getAllTags(cls, channels):
        '''
        getAllTags([Channel]) -> [String]
        returns a list of the tagNames of all the tags present on this set of channels
        '''
        if isinstance(channels, list):
            allTags = []
            for channel in channels:
                for tag in channel.getTags():
                    allTags.append(tag)
            uniqueNames = Set(allTags)
            return list(uniqueNames)
        else:
            return None
        
    @classmethod
    def getAllProperties(cls, channels):
        '''
        getAllProperties([Channel]) -> [String]
        returns a list of the propertyNames of all the properties on the set of channels
        '''      
        if isinstance(channels, list):
            allProperties = []
            for channel in channels:
                for propertyName in channel.getProperties().keys():
                    allProperties.append(propertyName)
            uniqueNames = Set(allProperties)
            return list(uniqueNames)
        else:
            return None