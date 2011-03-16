"""
This module is a client which provides a interface to access channel finder service to get channel information.
The Channel Finder service uses a web service, and http protocol to provide EPICS channel name, and its related
properties, tags. The properties supported so far are, which is developed against NSLS II storage ring.: 
    'elem_type':   element type
    'elem_name':   element name
    'length':      element length
    's_position':  s position along beam trajectory
    'ordinal':     index in simulation code (for NSLS II storage ring, tracy)
    'system':      system, for example, storage ring
    'cell':        cell information
    'girder':      girder information
    'handle':      handle, either setpoint or readback
    'symmetry':    symmetry (A or B for NSLS II storage ring, following the naming convention)
    
  

Created on Mar 14, 2011
         National Synchrotron Radiation Facility II
         Brookhaven National Laboratory
         PO Box 5000, Upton, New York, 11973-5000

@author: G. Shen
"""

import sys
import time

from ChannelFinderClient import ChannelFinderClient
from Channel import Channel
from Channel import Property

def addProps(cf):
    # every property has to be added first before using it.
    properties = []
    
    # connect to server is time-consuming
    # A bad example to add multiple properties
#    beg = time.time()
#    if cf.findProperty('dev_type') == None:
#        properties.append(Property('dev_type', 'vioc'))
#    if cf.findProperty('elem_name') == None:
#        properties.append(Property('elem_name', 'vioc'))
#    if cf.findProperty('length') == None:
#        properties.append(Property('length', 'vioc'))
#    if cf.findProperty('s_position') == None:
#        properties.append(Property('s_position', 'vioc'))
#    if cf.findProperty('ordinal') == None:
#        properties.append(Property('ordinal', 'vioc'))
#    if cf.findProperty('system') == None:
#        properties.append(Property('system', 'vioc'))
#    if cf.findProperty('cell') == None:
#        properties.append(Property('cell', 'vioc'))
#    if cf.findProperty('girder') == None:
#        properties.append(Property('girder', 'vioc'))
#    if cf.findProperty('ch_type') == None:
#        properties.append(Property('ch_type', 'vioc'))
#    end = time.time()
#    print ('%.6f' % (end - beg))

    # This method works better
#    beg1 = time.time()
    propDict = {'elem_type': 'vioc', \
                'elem_name': 'vioc', \
                'length': 'vioc', \
                's_position': 'vioc', \
                'ordinal': 'vioc', \
                'system': 'vioc', \
                'cell': 'vioc', \
                'girder': 'vioc', \
                'handle': 'vioc', \
                'symmetry': 'vioc'
                }

    properties1 = cf.getAllProperties()
    for prop in properties1:
        try:
            del propDict[prop.Name]
        except KeyError:
            pass
    if len(propDict) > 0:
        for key in propDict.iterkeys():
            properties.append(Property(key, propDict[key]))
#    end1 = time.time()
#    print ('%.6f' % (end1 - beg1))

    if len(properties) > 0:
        cf.add(properties=properties)
    else:
        print 'all properties are in database already.'

def buildProps(results, channame, chtype):
    properties = [Property('elem_type', 'vioc', results[6]),
                  Property('elem_name', 'vioc', results[3]),
                  Property('length', 'vioc', results[4]),
                  Property('s_position', 'vioc', results[5]),
                  Property('ordinal', 'vioc', results[0])]

    # SR stands for storage ring
    if channame.startswith('SR'):
        properties.append(Property('system', 'vioc', 'storage ring'))

    # C00 stands for global pv                
    if channame.find('C00') == -1:
        tmp = channame.split(':')
        properties.append(Property('cell', 'vioc', tmp[1][1:3]))
        properties.append(Property('girder', 'vioc', tmp[2][1:3]))
        properties.append(Property('symmetry', 'vioc', tmp[2][3:4]))

    properties.append(Property('handle', 'vioc', chtype))
    return properties

if __name__ == '__main__':
    baseurl = 'http://channelfinder.nsls2.bnl.gov:8080/ChannelFinder'
    client = ChannelFinderClient(BaseURL=baseurl, username='boss', password='1234')
    # you can use browser to view results
    # http://channelfinder.nsls2.bnl.gov:8080/ChannelFinder/resources/channels?~name=SR*
    
    addProps(client)

    try:
        # the file has the following attributes:
        #index, read back, set point, phys name, len[m], s[m], type
        f = open('lat_conf_table.txt', 'r')
        lines = f.readlines()
        channels = []
        for line in lines:
            if not (line.startswith('#') or line.startswith('!') or not line.strip()):
                results = line.split()
                if len(results) < 7:
                    # input file format problem
                    raise
                
                if results[1] != 'NULL':
                    channels.append(Channel((u'%s' %results[1]), 'vioc', properties=buildProps(results, results[1], 'readback')))
                    #name = u'%s' % result[1]
                    #channels.append(Channel(name, 'vioc', properties=buildProps(results, results[1], 'readback')))
                    #client.add(channel = Channel((u'%s' %results[1]), 'vioc', properties=buildProps(results, results[1], 'readback')))
                if results[2] != 'NULL':
                    channels.append(Channel((u'%s' %results[2]), 'vioc', properties=buildProps(results, results[2], 'readback')))
                    #name = u'%s' % result[2]
                    #channels.append(Channel(name, 'vioc', properties=buildProps(results, results[2], 'readback')))
                    #client.add(channel = Channel((u'%s' %results[2]), 'vioc', properties=buildProps(results, results[2], 'setpoint')))
        beg = time.time()
        client.add(channels=channels)
        end = time.time()
        print ('%.6f' % (end-beg))
    finally:
        f.close()
    
#    channels = client.getAllChannels()
    channels = client.find(name='SR*')
    print len(channels)
#    beg = time.time()
    for channel in channels:
        print channel.Name
#        client.remove(channelName=(u'%s' % channel.Name))
    end = time.time()
#    print ('%.6f' % (end-beg))
