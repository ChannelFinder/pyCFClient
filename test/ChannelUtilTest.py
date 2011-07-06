'''
Created on May 10, 2011

@author: shroffk
'''
import unittest
from channelfinder.core.Channel import Channel, Property, Tag
from channelfinder.util.ChannelUtil import ChannelUtil

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def testChannelUtil(self):
        channel1 = Channel('chName1', 'chOwner',
                          properties=[Property('location', 'propOwner', 'propVal'),
                                      Property('prop1', 'propOwner', 'propVal')],
                          tags=[Tag('myTag', 'tagOwner')])
        channel2 = Channel('chName2', 'chOwner',
                          properties=[Property('location', 'propOwner', 'propVal'),
                                      Property('prop2', 'propOwner', 'propVal')],
                          tags=[Tag('myTag', 'tagOwner'),
                                Tag('goldenOrbit', 'tagOwner')])
        channels = [channel1, channel2]
        allTags = ChannelUtil.getAllTags(channels)
        self.assertTrue(len(allTags) == 2, \
                        'expected 2 tags found ' +  str(len(allTags)))
        allPropertyNames = ChannelUtil.getAllProperties(channels)
        self.assertTrue(len(allPropertyNames) == 3, \
                        'expected 3 unique properties but found ' + str(len(allPropertyNames)))
       
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testChannelUtil']
    unittest.main()
