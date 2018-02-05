'''
Copyright (c) 2010 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on May 10, 2011

@author: shroffk
'''
import unittest
from channelfinder import Channel, Property, Tag
from channelfinder.util import ChannelUtil

import requests
requests.packages.urllib3.disable_warnings()


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
                        'expected 2 tags found ' + str(len(allTags)))
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
        self.assertTrue('234' in values, \
                        'Failed to find property(location), value 234 for ch1')
        self.assertTrue('SR' in values, \
                        'Failed to find property(location), value SR for ch2')
        self.assertTrue('SR:234' in values, \
                        'Failed to find property(location), value SR:234 for ch3')
        pass
    
    def testValidateWithTag(self):   
        ch1 = Channel('chName1', 'chOwner',
                          properties=[Property('location', 'propOwner', 'propVal'),
                                      Property('prop1', 'propOwner', 'propVal')],
                          tags=[Tag('myTag', 'tagOwner')])
        ch2 = Channel('chName2', 'chOwner',
                          properties=[Property('location', 'propOwner', 'propVal'),
                                      Property('prop2', 'propOwner', 'propVal')],
                          tags=[Tag('myTag', 'tagOwner'),
                                Tag('goldenOrbit', 'tagOwner')])
        self.assertTrue(ChannelUtil.validateChannelsWithTag([ch1, ch2], Tag('myTag', 'someOwner')), \
                        'Failed to validate channels based on TagValidator')
        self.assertFalse(ChannelUtil.validateChannelsWithTag([ch1, ch2], Tag('goldenOrbit', 'someOwner')), \
                         'Failed to correctly validate channels based on a TagValidator')  
        pass
    
    def testValidateWithProperty(self):
        ch1 = Channel('ch1', 'chOwner',
                          properties=[Property('location', 'propOwner', '234'),
                                      Property('prop1', 'propOwner', 'propVal')])
        ch2 = Channel('ch2', 'chOwner',
                          properties=[Property('location', 'propOwner', 'SR'),
                                      Property('prop2', 'propOwner', 'propVal')])
        ch3 = Channel('ch3', 'chOwner',
                          properties=[Property('location', 'propOwner', 'SR:234'),
                                      Property('prop2', 'propOwner', 'propVal')])
        self.assertTrue(ChannelUtil.validateChannelWithProperty([ch2, ch3], Property('prop2', 'anyOwner', 'propVal')))
        self.assertFalse(ChannelUtil.validateChannelWithProperty([ch1, ch2, ch3], Property('prop2', 'anyOwner', 'propVal')), \
                         'Failed to correctly validate channels based on a PropertyValidator')
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testChannelUtil']
    unittest.main()
