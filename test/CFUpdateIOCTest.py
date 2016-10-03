'''
Copyright (c) 2010 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on Apr 5, 2011

@author: shroffk
'''
import unittest
import os
from channelfinder import ChannelFinderClient
from _testConf import _testConf
from channelfinder.cfUpdate.CFUpdateIOC import getPVNames, getArgsFromFilename, updateChannelFinder, ifNoneReturnDefault
from time import time
from tempfile import NamedTemporaryFile
from copy import copy

class Test(unittest.TestCase):
    
    def setUp(self):
        if _testConf.has_option('DEFAULT', 'BaseURL'):
            self.baseURL = _testConf.get('DEFAULT', 'BaseURL')
        if _testConf.has_option('DEFAULT', 'username'):
            self.username = _testConf.get('DEFAULT', 'username')
        if _testConf.has_option('DEFAULT', 'password'):
            self.password = _testConf.get('DEFAULT', 'password')
        if _testConf.has_option('DEFAULT', 'owner'):
            self.owner = _testConf.get('DEFAULT', 'owner')
            
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
                            owner=self.owner, \
                            time=t1, \
                            service=self.baseURL , \
                            username=self.username, \
                            password=self.password)
        channels = client.find(property=[('hostName', hostName1), ('iocName', iocName1), ('time', t1)])
        self.assertTrue(len(channels) == 2, 'failed to create the channels with appropriate properties')
        t2 = str(time())
        hostName2 = 'update-test-hostname' + t2
        iocName2 = 'update-test-iocName' + t2
        # Existing channels are updated
        updateChannelFinder(['cf-update-pv1', 'cf-update-pv2'], \
                            hostName2, \
                            iocName2, \
                            owner=self.owner, \
                            time=t2, \
                            service=self.baseURL , \
                            username=self.username, \
                            password=self.password)
        # no channels should have the old proerty values 
        self.assertTrue(not client.find(property=[('hostName', hostName1), ('iocName', iocName1), ('time', t1)]), \
                        'failed to update the channels with appropriate properties, old values found')
        # channels should be updated to the new values
        self.assertTrue(len(client.find(property=[('hostName', hostName2), ('iocName', iocName2), ('time', t2)])) == 2, \
                        'failed to update the channels with appropriate properties')
        # Cleanup
        client = ChannelFinderClient(BaseURL=self.baseURL, username=self.username, password=self.password)
        client.delete(channelName='cf-update-pv1')
        client.delete(channelName='cf-update-pv2')
        pass
    
    def testAddUpdateChannelsWithProperties(self):
        '''
        This is to check that existing properties of channels are not affected.
        '''
        unaffectedProperty = {u'name':u'unaffectedProperty', u'owner':self.owner, u'value':u'unchanged'}
        # create default client
        client = ChannelFinderClient(BaseURL=self.baseURL, username=self.username, password=self.password)
        client.set(property=unaffectedProperty)
        
        # add new pv's
        t1 = str(time())
        hostName1 = 'update-test-hostname' + t1
        iocName1 = 'update-test-iocName' + t1
        # New Channels added
        client = ChannelFinderClient(BaseURL=self.baseURL, username=self.username, password=self.password);
        client.set(channel={u'name':u'cf-update-pv1', u'owner':u'cf-update', u'properties':[unaffectedProperty]})
        updateChannelFinder(['cf-update-pv1', 'cf-update-pv2'], \
                            hostName1, \
                            iocName1, \
                            owner=self.owner, \
                            time=t1, \
                            service=self.baseURL , \
                            username=self.username, \
                            password=self.password)
        channels = client.find(property=[('hostName', hostName1), ('iocName', iocName1), ('time', t1)])
        self.assertTrue(len(channels) == 2, 'failed to create the channels with appropriate properties')
        channels = client.find(name='cf-update-pv1')
        self.assertTrue(len(channels) == 1)
        self.assertTrue(len(channels[0][u'properties']) == 5)
        # Cleanup
        client.delete(channelName='cf-update-pv1')
        client.delete(channelName='cf-update-pv2')
        client.delete(propertyName=unaffectedProperty[u'name'])

    def testPreservingOfAttributes(self):
        '''
        This test is to ensure that existing properties and tags are left untouched.
        Case1:
        first time the cf-update comes across these channels and adds hostName and iocName
        Case2:
        the hostName is changed
        Case3:
        the iocName is changed
        Case4:
        both hostName and iocName are changed
        Case5:
        the channel is removed
        in all cases the existing unaffected* property and tag should remain with the channel               
        '''
        unaffectedProperty = {u'name':u'unaffectedProperty', u'owner':self.owner, u'value':u'unchanged'}
        unaffectedTag = {u'name':u'unaffectedTag', u'owner':self.owner}
        # create default client
        client = ChannelFinderClient(BaseURL=self.baseURL, username=self.username, password=self.password)
        client.set(property=unaffectedProperty)
        client.set(tag=unaffectedTag)
        
        client.set(channel={u'name':u'cf-update-pv1', u'owner':u'cf-update', u'properties':[unaffectedProperty], u'tags':[unaffectedTag]})
        client.set(channel={u'name':u'cf-update-pv2', u'owner':u'cf-update', u'properties':[unaffectedProperty], u'tags':[unaffectedTag]})
        
        # Case1:
        hostName = 'initialHost'
        iocName = 'initialIoc'
        updateChannelFinder(['cf-update-pv1', 'cf-update-pv2'], \
                            hostName, \
                            iocName, \
                            owner=self.owner, \
                            time=time(), \
                            service=self.baseURL , \
                            username=self.username, \
                            password=self.password)
        channels = client.find(name='cf-update-pv*')
        for channel in channels:
            self.assertTrue(unaffectedProperty in channel['properties'] and unaffectedTag in channel['tags'])
            self.assertTrue(self.__check4properties({u'name':u'hostName', u'value':hostName}, channel['properties']) and 
                            self.__check4properties({u'name':u'iocName', u'value':iocName}, channel['properties']) and 
                            self.__check4properties({u'name':u'pvStatus', u'value':u'Active'}, channel['properties']),
                            'Failed to update channels with the correct hostName and/or iocName')
        # Case2:
        hostName = 'newHost'
        updateChannelFinder(['cf-update-pv1', 'cf-update-pv2'], \
                            hostName, \
                            iocName, \
                            owner=self.owner, \
                            time=time(), \
                            service=self.baseURL , \
                            username=self.username, \
                            password=self.password)
        channels = client.find(name='cf-update-pv*')
        for channel in channels:
            self.assertTrue(unaffectedProperty in channel['properties'] and unaffectedTag in channel['tags'])
            self.assertTrue(self.__check4properties({u'name':u'hostName', u'value':hostName}, channel['properties']) and 
                            self.__check4properties({u'name':u'iocName', u'value':iocName}, channel['properties']) and 
                            self.__check4properties({u'name':u'pvStatus', u'value':u'Active'}, channel['properties']),
                            'Failed to update channels with the correct hostName and/or iocName')
        self.assertTrue(not client.find(property=[('hostName', 'initialHost')]), 'Failed to cleanup old property')
        # Case 3:
        iocName = 'newIoc'
        updateChannelFinder(['cf-update-pv1', 'cf-update-pv2'], \
                            hostName, \
                            iocName, \
                            owner=self.owner, \
                            time=time(), \
                            service=self.baseURL , \
                            username=self.username, \
                            password=self.password)
        channels = client.find(name='cf-update-pv*')
        for channel in channels:
            self.assertTrue(unaffectedProperty in channel['properties'] and unaffectedTag in channel['tags'])
            self.assertTrue(self.__check4properties({u'name':u'hostName', u'value':hostName}, channel['properties']) and 
                            self.__check4properties({u'name':u'iocName', u'value':iocName}, channel['properties']) and 
                            self.__check4properties({u'name':u'pvStatus', u'value':u'Active'}, channel['properties']),
                            'Failed to update channels with the correct hostName and/or iocName')
        self.assertTrue(not client.find(property=[('hostName', 'initialHost')]), 'Failed to cleanup old property')
        self.assertTrue(not client.find(property=[('iocName', 'initialIoc')]), 'Failed to cleanup old property')
        # Case 4:
        updateChannelFinder([], \
                            hostName, \
                            iocName, \
                            owner=self.owner, \
                            time=time(), \
                            service=self.baseURL , \
                            username=self.username, \
                            password=self.password)
        channels = client.find(name='cf-update-pv*')
        for channel in channels:
            self.assertTrue(unaffectedProperty in channel['properties'] and unaffectedTag in channel['tags'])
            self.assertTrue(self.__check4properties({u'name':u'hostName', u'value':hostName}, channel['properties']) and 
                            self.__check4properties({u'name':u'iocName', u'value':iocName}, channel['properties']) and 
                            self.__check4properties({u'name':u'pvStatus', u'value':u'Inactive'}, channel['properties']),
                            'Failed to update channels with the correct hostName and/or iocName')
        self.assertTrue(not client.find(property=[('hostName', 'initialHost')]), 'Failed to cleanup old property')
        self.assertTrue(not client.find(property=[('iocName', 'initialIoc')]), 'Failed to cleanup old property')
        
        # Cleanup
        '''
        TODO this cleanup code should not be contingent to the successful completion of all checks...
        This could pollute CF 
        '''
        client.delete(channelName='cf-update-pv1')
        client.delete(channelName='cf-update-pv2')
        client.delete(propertyName=unaffectedProperty[u'name'])
        client.delete(tagName=unaffectedTag[u'name'])

    def __check4properties(self, prop, properties):
        '''
        check if property existing in a list of properties
        The equality test will be based on the name and the value while ignoring the owner 
        '''
        foundProp = [ p for p in properties if p[u'name'] == prop[u'name'] ]
        if len(foundProp) == 1 and foundProp[0][u'value'] == prop[u'value']:
            return True
        else:
            return False

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
        client = ChannelFinderClient(BaseURL=self.baseURL, username=self.username, password=self.password)
        try:
            updateChannelFinder(['ch1', 'ch2'], \
                                'testHost', \
                                'testIOC', \
                                owner=self.owner, \
                                time=time(), \
                                service=self.baseURL, \
                                username=self.username, password=self.password)
            chs = client.find(property=[('hostName', 'testHost'), ('iocName', 'testIOC'), ('pvStatus', 'Active')])
            self.assertEqual(len(chs), 2, 'Expected 2 positive matches but found ' + str(len(chs)))
            updateChannelFinder(['ch1'], \
                                'testHost', \
                                'testIOC', \
                                owner=self.owner, \
                                time=time(), \
                                service=self.baseURL, \
                                username=self.username, password=self.password)
            chs = client.find(property=[('hostName', 'testHost'), ('iocName', 'testIOC'), ('pvStatus', 'Active')])
            self.assertEqual(len(chs), 1, 'Expected 1 positive matches but found ' + str(len(chs)))
            self.assertTrue(chs[0][u'name'] == 'ch1', 'channel with name ch1 not found')
            chs = client.find(property=[('hostName', 'testHost'), ('iocName', 'testIOC'), ('pvStatus', 'Inactive')])
            self.assertEqual(len(chs), 1, 'Expected 1 positive matches but found ' + str(len(chs)))
            self.assertTrue(chs[0][u'name'] == 'ch2', 'channel with name ch2 not found')
            updateChannelFinder(['ch1', 'ch2'], \
                                'testHost', \
                                'testIOC', \
                                owner=self.owner, \
                                time=time(), \
                                service=self.baseURL, \
                                username=self.username, password=self.password)
            chs = client.find(property=[('hostName', 'testHost'), ('iocName', 'testIOC'), ('pvStatus', 'Active')])
            self.assertEqual(len(chs), 2, 'Expected 2 positive matches but found ' + str(len(chs)))
        finally:
            client.delete(channelName='ch1')
            client.delete(channelName='ch2')
    
    def testPVMove(self):
        '''
        ch1, ch2 on host1, ioc1
        ch1 on host1, ioc1; ch2 on host1, ioc2 (case1)
        ch1, ch2 on host1, ioc1 (reset)
        ch1 on host1, ioc1; ch2 on host2, ioc2 (case2)
        ch1, ch2 on host1, ioc1 (reset)
        '''
        client = ChannelFinderClient(BaseURL=self.baseURL, username=self.username, password=self.password)
        try:
            updateChannelFinder(['ch1', 'ch2'], \
                                'host1', \
                                'ioc1', \
                                owner=self.owner, \
                                time=time(),\
                                service=self.baseURL, \
                                username=self.username, password=self.password)
            chs = client.find(property=[('hostName', 'host1'), ('iocName', 'ioc1')])
            self.assertEqual(len(chs), 2, 'Expected 2 positive matches but found ' + str(len(chs)))
            '''CASE1'''
            updateChannelFinder(['ch1'], \
                                'host1', \
                                'ioc1', \
                                time=time(), \
                                owner=self.owner, service=self.baseURL, \
                                username=self.username, password=self.password)
            updateChannelFinder(['ch2'], \
                                'host1', \
                                'ioc2', \
                                time=time(), \
                                owner=self.owner, service=self.baseURL, \
                                username=self.username, password=self.password)
            chs = client.find(property=[('hostName', 'host1')])
            self.assertEqual(len(chs), 2, 'Expected 1 positive matches but found ' + str(len(chs)))
            self.assertEqual(client.find(property=[('hostName', 'host1'), ('iocName', 'ioc1')])[0][u'name'], 'ch1', \
                             'Failed to find the expected channel _ch1_ with prop host1, ioc1')
            self.assertEqual(client.find(property=[('hostName', 'host1'), ('iocName', 'ioc2')])[0][u'name'], 'ch2', \
                             'Failed to find the expected channel _ch2_ with prop host1, ioc2')
            '''RESET'''
            updateChannelFinder(['ch1', 'ch2'], \
                                'host1', \
                                'ioc1', \
                                time=time(), \
                                owner=self.owner, service=self.baseURL, \
                                username=self.username, password=self.password)
            self.assertEqual(len(client.find(property=[('hostName', 'host1'), ('iocName', 'ioc1')])), 2, \
                             'Failed to reset the channels')            
            '''CASE2'''
            updateChannelFinder(['ch1'], \
                                'host1', \
                                'ioc1', \
                                owner=self.owner, \
                                time=time(), \
                                service=self.baseURL, username=self.username, \
                                password=self.password)
            updateChannelFinder(['ch2'], \
                                'host2', \
                                'ioc2', \
                                owner=self.owner, service=self.baseURL, \
                                time=time(), \
                                username=self.username, password=self.password)
            self.assertEqual(client.find(property=[('hostName', 'host1'), ('iocName', 'ioc1')])[0][u'name'], 'ch1', \
                             'Failed to find the expected channel _ch1_ with prop host1, ioc1')
            self.assertEqual(client.find(property=[('hostName', 'host2'), ('iocName', 'ioc2')])[0][u'name'], 'ch2', \
                             'Failed to find the expected channel _ch2_ with prop host1, ioc2')
            '''RESET'''
            updateChannelFinder(['ch1', 'ch2'], \
                                'host1', \
                                'ioc1', \
                                owner=self.owner, \
                                time=time(), \
                                service=self.baseURL, \
                                username=self.username, password=self.password)
            self.assertEqual(len(client.find(property=[('hostName', 'host1'), ('iocName', 'ioc1')])), 2, \
                             'Failed to reset the channels')
        finally:
            client.delete(channelName='ch1')
            client.delete(channelName='ch2')
    
    def testRegularExperssion(self):
        tempFile = NamedTemporaryFile(delete=False)
        publicPVs = ['publicPV1', 'publicPV2', 'publicPV3']
        privatePVS = ['_privatePV1', '_privatePV2']
        allPVs = copy(publicPVs);
        allPVs.extend(privatePVS)
        for pv in allPVs:
            tempFile.write(pv + '\n')
        tempFile.close();        
        try:
            pvNames = getPVNames(tempFile.name)
            self.assertEqual(len(pvNames), len(allPVs), \
                             'expected ' + str(len(allPVs)) + ' but got ' + str(len(pvNames)))
            pvNames = getPVNames(tempFile.name, pattern='[^_]+')
            self.assertEqual(len(pvNames), len(publicPVs), \
                             'expected ' + str(len(allPVs)) + ' but got ' + str(len(publicPVs)))
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
    
