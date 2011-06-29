'''
Created on Feb 11, 2011

@author: shroffk
'''
import unittest

from channelfinder.core.Channel import Channel, Property, Tag

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass
    
    def testChannelCreation(self):
        channel = Channel('ChannelName', 'ChannelOwner')
        self.assertEqual(channel.Name, 'ChannelName')
        pass
    
    def testAddProperty(self):
        properties = [Property('prop1', 'propOwner', 'val1'),
                      Property('prop2', 'propOwner', 'val2')]        
        channel = Channel('ChannelName', 'ChannelOwner', properties=properties)
        self.assertEqual(properties, channel.Properties)
        pass
    
    def testAddTag(self):
        tags = [Tag('tag1', 'tagOwner'), Tag('tag2', 'tagOwner')]
        channel = Channel('ChannelName', 'ChannelOwner', tags=tags)
        self.assertEqual(tags, channel.Tags)
        pass
       
    def Immutability(self):
        '''
        removed test cause the ability to add property and tag list is required.
        '''
        channel = Channel('ChannelName', 'ChannelOwner')
        self.assertRaises(AttributeError, channel.Properties, [])
        self.assertRaises(AttributeError, channel.Tags, [])
   
class ErrorTest(unittest.TestCase):   
    
    def setUp(self):
        self.testChannel = Channel('ChannelName', 'ChannelOwner', properties=[], tags=[])     
        pass

    def tearDown(self):
        pass
    
    def testInvalidCreation(self):
        try:
            ch = Channel('chName', 'chOwner', properties='invalidProperty')
        except:
            pass
        try:
            ch = Channel('chName', 'chOwner', tags='invalidProperty')
        except:
            pass
        
    def testAddInvalidPropertyType(self):        
        self.assertRaises(Exception, self.testChannel.Properties.__setitem__, 'name', 'string')
        pass
    
    def testaddInvalidTagType(self):        
        self.assertRaises(Exception, self.testChannel.Tags.__setitem__, 'name', 1234)
        pass
    
    def testDuplicateProperties(self):
        pass
    
    def testnoDuplicateTags(self):
        pass
    
class TagTest(unittest.TestCase):
    
    def testCmpOperation(self):
        tagList = [Tag('tagA', 'tagOwner'), Tag('tagB', 'tagOwner'), Tag('tagC', 'tagOwner')]
        self.assertTrue(Tag('tagA', 'tagOwner') in tagList, 'failed to find tag in list')
        self.assertTrue(Tag('tagA', 'tagOwner2') in tagList, 'failed to find tag in list')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
