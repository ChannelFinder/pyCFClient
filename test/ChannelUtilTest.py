'''
Copyright (c) 2010 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on May 10, 2011

@author: shroffk
'''
import unittest
from channelfinder import Channel, Property, Tag
from channelfinder.util import ChannelUtil

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
    
    def testGetAllPropValues(self):
        ch1 = Channel('ch1', 'chOwner',
                          properties=[Property('location', 'propOwner', '234'),
                                      Property('prop1', 'propOwner', 'propVal')])
        ch2 = Channel('ch2', 'chOwner',
                          properties=[Property('location', 'propOwner', 'SR'),
                                      Property('prop2', 'propOwner', 'propVal')])
        ch3 = Channel('ch3', 'chOwner',
                          properties=[Property('location', 'propOwner', 'SR:234'),
                                      Property('prop2', 'propOwner', 'propVal')])
        chs = [ch1, ch2, ch3]
        values = ChannelUtil.getAllPropValues(chs, propertyName='location')
        self.assertTrue((ch1.Name+'(location)', '234') in values, \
                        'Failed to find property(location), value 234 for ch1')
        self.assertTrue((ch2.Name+'(location)', 'SR') in values, \
                        'Failed to find property(location), value SR for ch2')
        self.assertTrue((ch3.Name+'(location)', 'SR:234') in values, \
                        'Failed to find property(location), value SR:234 for ch3')
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testChannelUtil']
    unittest.main()
