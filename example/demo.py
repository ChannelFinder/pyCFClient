"""
This module is a demo which provides a interface to access channel finder service to get channel information.
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

from channelfinder import ChannelFinderClient

import urllib3
urllib3.disable_warnings()


def prop_demo(cf):
    """
    Demo routine to operate property

    :param cf:
    :return:
    """
    # every property has to be added first before using it.
    properties = []
    propDict = {'elem_type': 'cf-update', \
                'elem_name': 'cf-update', \
                'dev_name': 'cf-update', \
                'length': 'cf-update', \
                's_position': 'cf-update', \
                'ordinal': 'cf-update', \
                'system': 'cf-update', \
                'cell': 'cf-update', \
                'girder': 'cf-update', \
                'handle': 'cf-update', \
                'symmetry': 'cf-update'
                }

    properties1 = cf.getAllProperties()
    print(properties1)
    for prop in properties1:
        try:
            del propDict[prop['name']]
        except KeyError:
            pass
    if len(propDict) > 0:
        for k, v in propDict.items():
            properties.append({u'name': k, u'owner': v})
        if len(propDict) == 1:
            cf.set(property=properties)
        else:
            cf.set(properties=properties)
        properties2 = cf.getAllProperties()
        print(properties2)
    else:
        print('all properties are in database already.')


def channel_demo(cf):
    """
    Demo routine to operate channel

    :param cf:
    :return:
    """
    try:
        # the file has the following attributes:
        # index, read back, set point, phys name, len[m], s[m], type
        f = open('lat_conf_table.txt', 'r')
        lines = f.readlines()
        channels = []

        for line in lines:
            if not (line.startswith('#') or line.startswith('!') or not line.strip()):
                results = line.split()
                if len(results) < 7:
                    # input file format problem
                    raise
                props = [{'name': u'elem_type', 'value': results[6]},
                         {'name': u'elem_name', 'value': results[3]},
                         {'name': u'length', 'value': results[4]},
                         {'name': u's_position', 'value': results[5]},
                         {'name': u'ordinal', 'value': results[0]},
                         {'name': u'system', 'value': u'SR'}
                         ]

                if results[1] != 'NULL':
                    props.append({'name': u'handle', 'value': u'readback'})
                    channels.append({u'name': results[1], u'owner': u'cf-update', u'properties': props})
                if results[2] != 'NULL':
                    props.append({'name': u'handle', 'value': u'setpoint'})
                    channels.append({u'name': results[2], u'owner': u'cf-update', u'properties': props})
        cf.set(channels=channels)
    finally:
        f.close()

    channels = cf.find(name='SR*')
    print(len(channels))
    for channel in channels:
        print(channel)


def tag_demo(cf):
    """
    Demo routine to operate tag
    :param cf:
    :return:
    """
    # set one tag
    tag = {'name': 'example1', 'owner': 'cf-update'}
    cf.set(tag=tag)
    
    # set a set of tags
    tags = [{'name': 'example2', 'owner': 'cf-update'},
            {'name': 'example3', 'owner': 'cf-update'},
            {'name': 'example4', 'owner': 'cf-update'},
            {'name': 'example5', 'owner': 'cf-update'}]
    cf.set(tags=tags)

    channels = cf.find(name='SR*')
    channelNames = [channel['name'] for channel in channels]
    
    # set a tag to many channels
    cf.set(tag=tag, channelNames=channelNames)
    
    # set tags to many channels
    for tag in tags:
        cf.set(tag=tag, channelNames=channelNames)


if __name__ == '__main__':
    cf = ChannelFinderClient(BaseURL='https://barkeria-vm:8181/ChannelFinder', username='channel', password='1234')
    # you can use browser to view results
    # http://localhost:8080/ChannelFinder/resources/channels?~name=SR*

    tag_demo(cf)
    prop_demo(cf)
    channel_demo(cf)
