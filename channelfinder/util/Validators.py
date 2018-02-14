'''
Created on Mar 13, 2012

@author: shroffk
'''

class TagValidator(object):
    '''
    A simple Validator that ensures that a particular Tag is present on the channel
    '''


    def __init__(self, tag):
        '''
        Constructor
        '''
        self.tag = tag

    def validate(self, channel):
        tags = [t.Name for t in channel.Tags]
        return self.tag.Name in tags

class PropertyValidator(object):
    '''
    A simple Validator that ensures that a particular Property is present on the channel
    '''

    def __init__(self, prop):
        '''
        Constructor
        '''
        self.property = prop
    
    def validate(self, channel):
        props = [p.Name for p in channel.Properties]
        # for p in channel.Properties:
        #     props.append(p.Name)
        return self.property.Name in props
