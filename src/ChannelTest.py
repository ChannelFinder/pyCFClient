'''
Created on Feb 11, 2011

@author: shroffk
'''
import unittest

from Channel import Channel

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass
    
    def testChannelCreation(self):
        channel = Channel('ChannelName','ChannelOwner')
        self.assertEqual(channel.Name, 'ChannelName')
        pass
    
    def testAddProperty(self):
        properties = {'prop1':('value1','owner1'),'prop2':('value2','owner2')}
        channel = Channel('ChannelName','ChannelOwner',properties=properties)
        self.assertEqual(properties, channel.Properties)
        pass
    
    def testAddTag(self):
        tags = {'tag1':'owner1','tag2':'owner2'}
        channel = Channel('ChannelName','ChannelOwner',tags=tags)
        self.assertEqual(tags, channel.Tags)
        pass
   
class ErrorTest(unittest.TestCase):   
    
    def setUp(self):
        self.testChannel = Channel('ChannelName','ChannelOwner')     
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
            print 'error'
        except:
            pass
        
    def testAddInvalidPropertyType(self):        
        self.assertRaises(Exception, self.testChannel.Properties.__setitem__, 'name','string')
        pass
    
    def testaddInvalidTagType(self):        
        self.assertRaises(Exception, self.testChannel.Tags.__setitem__, 'name',1234)
        pass
    
    def testDuplicateProperties(self):
        pass
    
    def testnoDuplicateTags(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()