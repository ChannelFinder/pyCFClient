'''
Created on Feb 11, 2011

@author: shroffk
'''
from Dictionary import Dictionary

class Channel(object):
    '''
    classdocs
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

