'''
Created on Apr 5, 2011

@author: shroffk
'''
import unittest
from channelfinder.core.Channel import Channel, Property
from channelfinder.core.ChannelFinderClient import ChannelFinderClient
from channelfinder.cfUpdate.CFUpdateIOC import getArgsFromFilename, updateChannelFinder, ifNoneReturnDefault
from time import time

class Test(unittest.TestCase):


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
                            iocName1)
        channels = client.find(property=[('hostName', hostName1), ('iocName', iocName1)])
        self.assertTrue(len(channels) == 2, 'failed to create the channels with appropriate properties')
        t2 = str(time())
        hostName2 = 'update-test-hostname' + t2
        iocName2 = 'update-test-iocName' + t2
        # Existing channels are updated
        updateChannelFinder(['cf-update-pv1', 'cf-update-pv2'], \
                            hostName2, \
                            iocName2)
        # no channels should have the old proerty values 
        self.assertTrue(client.find(property=[('hostName', hostName1), ('iocName', iocName1)]) == None, \
                        'failed to update the channels with appropriate properties, old values found')
        # channels should be updated to the new values
        self.assertTrue(len(client.find(property=[('hostName', hostName2), ('iocName', iocName2)])) == 2, \
                        'failed to update the channels with appropriate properties')
        # Cleanup
        client.delete(channelName='cf-update-pv1')
        client.delete(channelName='cf-update-pv2')
        pass
    
    def testAddUpdateChannelsWithProperties(self):
        '''
        This is to check that existing properties of channels are not affected.
        '''
        unaffectedProperty = Property('unaffectedProperty', 'boss', 'unchanged')
        # create default client
        client = ChannelFinderClient()
        client.set(property=unaffectedProperty)
        
        # add new pv's
        t1 = str(time())
        hostName1 = 'update-test-hostname' + t1
        iocName1 = 'update-test-iocName' + t1
        # New Channels added
        client.set(channel=Channel('cf-update-pv1', 'boss', properties=[unaffectedProperty]))
        updateChannelFinder(['cf-update-pv1', 'cf-update-pv2'], \
                            hostName1, \
                            iocName1)
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



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
class mockOpt():
    def __init__(self, hostname, iocname, service=None):
        self.hostname = hostname
        self.iocname = iocname
        self.service = service
    
