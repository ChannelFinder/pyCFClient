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

from channelfinder.ChannelFinderClient import ChannelFinderClient
from channelfinder.Channel import Tag

if __name__ == '__main__':
    cf = ChannelFinderClient(BaseURL = 'http://channelfinder.nsls2.bnl.gov:8080/ChannelFinder', username='boss', password='1234')
    
    # set one tag
    tag = Tag('example1', 'vioc')
    cf.set(tag=tag)
    
    # set a set of tags
    tags = [Tag('example2', 'vioc'), Tag('example3', 'vioc'), Tag('example4', 'vioc'), Tag('example5', 'vioc')]
    cf.set(tags=tags)
    
    channels = cf.find(name='SR*')
    channelNames = [channel.Name for channel in channels]
    
    # set a tag to many channels
    cf.set(tag=tag, channelNames=channelNames)
    
    # set tags to many channels
    for tag in tags:
        cf.set(tag=tag, channelNames=channelNames)

    # retrieve channel, properties, and tags
#    channels = cf.find(name='SR*')
#    for channel in channels:
#        print channel.Name
#        # get tags for each channel
#        tmp_tags = channel.getTags()
#        if tmp_tags != None:
#            for tmp_tag in tmp_tags:
#                print tmp_tag
        
    # remove one tag
#    cf.remove(tagName='example1')
#    cf.remove(tagName='example2')
#    cf.remove(tagName='example3')
#    cf.remove(tagName='example4')
#    cf.remove(tagName='example5')
    
#    print len(channels)
