'''
Created on Apr 5, 2011

@author: shroffk
'''
import unittest
import os
from channelfinder.core.Channel import Channel, Property
from channelfinder.core.ChannelFinderClient import ChannelFinderClient
from channelfinder.cfUpdate.CFUpdateIOC import getArgsFromFilename, updateChannelFinder, ifNoneReturnDefault
from time import time
from tempfile import NamedTemporaryFile
from channelfinder.cfUpdate.CFUpdateIOC import getPVNames
from copy import copy

class Test(unittest.TestCase):
    baseURL = 'https://localhost:8181/ChannelFinder'
    
    def setUp(self):
        pass


    def tearDown(self):
        pass

    def testParameterParsing(self):
#        scrap.mainRun(mockOpt('mockhostname', 'mockiocname'), [])
        pass
    
    def testGetArgsFromFilename(self):
        #parse just file name
        hostname, iocname = getArgsFromFilename('aaa.bbb.ccc')
        self.assertTrue(hostname == 'aaa' and iocname == 'bbb', 'failed to parse the file name correctly')
        # parse file name from complete path
        hostname, iocname = getArgsFromFilename('complete/path/to/file/aaa.bbb.ccc')
        self.assertTrue(hostname == 'aaa' and iocname == 'bbb', 'failed to parse the file path correctly')
        # parse file which does not fit the format
        hostname, iocname = getArgsFromFilename('complete/path/to/file/somefilename')
        self.assertTrue(hostname == None and iocname == None, 'failed to parse the file path correctly')
        # file with only hostName
        hostname, iocname = getArgsFromFilename('complete/path/to/file/aaa.somefilename')
        self.assertTrue(hostname == 'aaa' and iocname == None, 'failed to parse the file correctly')
        # parse the hostname/iocname from 1st and 2nd positions seperated by .
        hostname, iocname = getArgsFromFilename('complete/path/to/file/aaa.bbb.ccc.ddd')
        self.assertTrue(hostname == 'aaa' and iocname == 'bbb', 'failed to parse the file correctly')             
        pass

    def testAddUpdateChannels(self):
        # Check the method finds the error conditions and raises exceptions
        self.assertRaises(Exception, updateChannelFinder, [[], None, None])
        self.assertRaises(Exception, updateChannelFinder, [[], None, 'iocname'])
        self.assertRaises(Exception, updateChannelFinder, [[], 'hostName', None])
        # create default client
        client = ChannelFinderClient()
        
        # add new pv's
        t1 = str(time())
        hostName1 = 'update-test-hostname' + t1
        iocName1 = 'update-test-iocName' + t1
        channels = client.find(property=[('hostName', hostName1), ('iocName', iocName1)])
        self.assertTrue(channels == None or len(channels) == 0, 'channels already present')
        # New Channels added
        updateChannelFinder(['cf-update-pv1', 'cf-update-pv2'], \
                            hostName1, \
                            iocName1, \
                            owner = 'cf-update', \
                            service = self.baseURL ,\
                            username='cf-update', \
                            password='1234')
        channels = client.find(property=[('hostName', hostName1), ('iocName', iocName1)])
        self.assertTrue(len(channels) == 2, 'failed to create the channels with appropriate properties')
        t2 = str(time())
        hostName2 = 'update-test-hostname' + t2
        iocName2 = 'update-test-iocName' + t2
        # Existing channels are updated
        updateChannelFinder(['cf-update-pv1', 'cf-update-pv2'], \
                            hostName2, \
                            iocName2, \
                            owner = 'cf-update', \
                            service = self.baseURL ,\
                            username='cf-update', \
                            password='1234')
        # no channels should have the old proerty values 
        self.assertTrue(client.find(property=[('hostName', hostName1), ('iocName', iocName1)]) == None, \
                        'failed to update the channels with appropriate properties, old values found')
        # channels should be updated to the new values
        self.assertTrue(len(client.find(property=[('hostName', hostName2), ('iocName', iocName2)])) == 2, \
                        'failed to update the channels with appropriate properties')
        # Cleanup
        client = ChannelFinderClient(BaseURL=self.baseURL, username='cf-update', password='1234')
        client.delete(channelName='cf-update-pv1')
        client.delete(channelName='cf-update-pv2')
        pass
    
    def testAddUpdateChannelsWithProperties(self):
        '''
        This is to check that existing properties of channels are not affected.
        '''
        unaffectedProperty = Property('unaffectedProperty', 'cf-properties', 'unchanged')
        # create default client
        client = ChannelFinderClient(BaseURL=self.baseURL, username='property', password='1234')
        client.set(property=unaffectedProperty)
        
        # add new pv's
        t1 = str(time())
        hostName1 = 'update-test-hostname' + t1
        iocName1 = 'update-test-iocName' + t1
        # New Channels added
        client = ChannelFinderClient(BaseURL=self.baseURL, username='cf-update', password='1234');
        client.set(channel=Channel('cf-update-pv1', 'cf-update', properties=[unaffectedProperty]))
        updateChannelFinder(['cf-update-pv1', 'cf-update-pv2'], \
                            hostName1, \
                            iocName1, \
                            'cf-update', \
                            service = self.baseURL ,\
                            username='cf-update', \
                            password='1234')
        channels = client.find(property=[('hostName', hostName1), ('iocName', iocName1)])
        self.assertTrue(len(channels) == 2, 'failed to create the channels with appropriate properties')
        channels = client.find(name='cf-update-pv1')
        self.assertTrue(len(channels) == 1)
        self.assertTrue(len(channels[0].Properties) == 3)
        # Cleanup
        client.delete(channelName='cf-update-pv1')
        client.delete(channelName='cf-update-pv2')
        
        
    def testNoneCheck(self):
        self.assertTrue(ifNoneReturnDefault('Value', 'default') == 'Value')
        self.assertTrue(ifNoneReturnDefault(None, 'default') == 'default')
        self.assertTrue(ifNoneReturnDefault(None, None) == None)
        self.assertTrue(ifNoneReturnDefault('', 'default') == '')
        
    def testPVUpdate(self):
        '''
        Test condition 
        IOC turned on with ch1, ch2
        IOC turned on with ch1 only
        IOC turned on with ch1, ch2
        '''
        try:
            updateChannelFinder(['ch1', 'ch2'], 'testHost', 'testIOC', owner='cf-update', service=self.baseURL ,username='cf-update',password='1234')
            client = ChannelFinderClient(BaseURL=self.baseURL, username='cf-update',password='1234')
            chs = client.find(property=[('hostName','testHost'),('iocName','testIOC')])
            self.assertEqual(len(chs), 2, 'Expected 2 positive matches but found '+str(len(chs)))
            updateChannelFinder(['ch1'],'testHost','testIOC', owner='cf-update', service=self.baseURL ,username='cf-update',password='1234')
            chs = client.find(property=[('hostName','testHost'),('iocName','testIOC')])
            self.assertEqual(len(chs), 1, 'Expected 1 positive matches but found '+str(len(chs)))
            self.assertTrue(chs[0].Name == 'ch1', 'channel with name ch1 not found')
            updateChannelFinder(['ch1', 'ch2'], 'testHost', 'testIOC', owner='cf-update', service=self.baseURL ,username='cf-update',password='1234')
            chs = client.find(property=[('hostName','testHost'),('iocName','testIOC')])
            self.assertEqual(len(chs), 2, 'Expected 2 positive matches but found '+str(len(chs)))
        finally:
            client.delete(channelName ='ch1')
            client.delete(channelName ='ch2')
    
    def testPVMove(self):
        '''
        ch1, ch2 on host1, ioc1
        ch1 on host1, ioc1; ch2 on host1, ioc2 (case1)
        ch1, ch2 on host1, ioc1 (reset)
        ch1 on host1, ioc1; ch2 on host2, ioc2 (case2)
        ch1, ch2 on host1, ioc1 (reset)
        '''
        try:
            updateChannelFinder(['ch1', 'ch2'], 'host1', 'ioc1', owner='cf-update', service=self.baseURL ,username='cf-update',password='1234')
            client = ChannelFinderClient(BaseURL=self.baseURL, username='cf-update',password='1234')
            chs = client.find(property=[('hostName','host1'),('iocName','ioc1')])
            self.assertEqual(len(chs), 2, 'Expected 2 positive matches but found '+str(len(chs)))
            '''CASE1'''
            updateChannelFinder(['ch1'],'host1','ioc1', owner='cf-update', service=self.baseURL ,username='cf-update',password='1234')
            updateChannelFinder(['ch2'],'host1','ioc2', owner='cf-update', service=self.baseURL ,username='cf-update',password='1234')
            chs = client.find(property=[('hostName','host1')])
            self.assertEqual(len(chs), 2, 'Expected 1 positive matches but found '+str(len(chs)))
            self.assertEqual(client.find(property=[('hostName','host1'),('iocName','ioc1')])[0].Name, 'ch1', \
                             'Failed to find the expected channel _ch1_ with prop host1, ioc1')
            self.assertEqual(client.find(property=[('hostName','host1'),('iocName','ioc2')])[0].Name, 'ch2', \
                             'Failed to find the expected channel _ch2_ with prop host1, ioc2')
            '''RESET'''
            updateChannelFinder(['ch1', 'ch2'], 'host1', 'ioc1', owner='cf-update', service=self.baseURL ,username='cf-update',password='1234')
            self.assertEqual(len(client.find(property=[('hostName','host1'),('iocName','ioc1')])), 2, \
                             'Failed to reset the channels' )            
            '''CASE2'''
            updateChannelFinder(['ch1'],'host1','ioc1', owner='cf-update', service=self.baseURL ,username='cf-update',password='1234')
            updateChannelFinder(['ch2'],'host2','ioc2', owner='cf-update', service=self.baseURL ,username='cf-update',password='1234')
            self.assertEqual(client.find(property=[('hostName','host1'),('iocName','ioc1')])[0].Name, 'ch1', \
                             'Failed to find the expected channel _ch1_ with prop host1, ioc1')
            self.assertEqual(client.find(property=[('hostName','host2'),('iocName','ioc2')])[0].Name, 'ch2', \
                             'Failed to find the expected channel _ch2_ with prop host1, ioc2')
            '''RESET'''
            updateChannelFinder(['ch1', 'ch2'], 'host1', 'ioc1', owner='cf-update', service=self.baseURL ,username='cf-update',password='1234')
            self.assertEqual(len(client.find(property=[('hostName','host1'),('iocName','ioc1')])), 2, \
                             'Failed to reset the channels' )
        finally:
            client.delete(channelName ='ch1')
            client.delete(channelName ='ch2')
    
    def testRegularExperssion(self):
        tempFile = NamedTemporaryFile(delete=False)
        publicPVs = ['publicPV1', 'publicPV2', 'publicPV3']
        privatePVS = ['_privatePV1', '_privatePV2']
        allPVs = copy(publicPVs);
        allPVs.extend(privatePVS)
        for pv in allPVs:
            tempFile.write(pv+'\n')
        tempFile.close();        
        try:
            pvNames = getPVNames(tempFile.name)
            self.assertEqual(len(pvNames), len(allPVs), \
                             'expected '+str(len(allPVs))+ ' but got '+str(len(pvNames)))
            pvNames = getPVNames(tempFile.name, pattern='[^_]+')
            self.assertEqual(len(pvNames), len(publicPVs), \
                             'expected '+str(len(allPVs))+ ' but got '+str(len(publicPVs)))
            self.assertTrue(frozenset(pvNames).issuperset(frozenset(publicPVs)), \
                            'resulting pvNames contains invalid non public pvs')
            self.assertTrue(frozenset(pvNames).isdisjoint(frozenset(privatePVS)), \
                            'result pvNames contains invalid private pvs')            
            pass
        finally:
            os.remove(tempFile.name)
        pass
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
class mockOpt():
    def __init__(self, hostname, iocname, service=None):
        self.hostname = hostname
        self.iocname = iocname
        self.service = service
    
