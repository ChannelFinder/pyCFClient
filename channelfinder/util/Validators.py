'''
Created on Mar 13, 2012

@author: shroffk
'''
from channelfinder import Channel, Property, Tag

class TagValidator(object):
    '''
    A simple Validator that ensures that a particular Tag is present on the channel
    '''
    

    def __init__(self, tag):
        '''
        Constructor
        '''
        self.tag = tag;
    
    def validate(self, channel):
        return self.tag in channel.Tags

class PropertyValidator(object):
    '''
    A simple Validator that ensures that a particular Tag is present on the channel
    '''

    def __init__(self, prop):
        '''
        Constructor
        '''
        self.property = prop
    
    def validate(self, channel):
        return self.property in channel.Properties
                