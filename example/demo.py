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

from ChannelFinderClient import ChannelFinderClient

if __name__ == '__main__':
    cf = ChannelFinderClient(BaseURL = 'http://channelfinder.nsls2.bnl.gov:8080/ChannelFinder')
    channels = cf.find(name='SR*')
    for channel in channels:
        print channel.Name
        props = channel.getProperties()
        for k, v in props.items():
            print k, v
#        client.remove(channelName=(u'%s' % channel.Name))
    print len(channels)
