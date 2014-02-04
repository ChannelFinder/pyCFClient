'''
Copyright (c) 2010 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on Apr 1, 2011

@author: shroffk

CFUpdateIOC provides a command like client to update channelfinder
with a list of process variables (usually the output of the dbl command).
'''
import os
import re
from optparse import OptionParser
from getpass import getpass
from channelfinder import Channel, Property
from channelfinder import ChannelFinderClient
from glob import glob
from channelfinder._conf import _conf

def getArgsFromFilename(completeFilePath):
    fileName = os.path.split(os.path.normpath(completeFilePath))[1]
    pattern4Hostname = '(\S+?)\.\S+'
    match = re.search(pattern4Hostname, fileName)
    if match:
        hostName = match.group(1)
    else:
        hostName = None
    pattern4Iocname = '\S+?\.(\S+?)\.\S+'
    match = re.search(pattern4Iocname, fileName)
    if match:
        iocName = match.group(1)
    else:
        iocName = None
    return hostName, iocName

def getPVNames(completeFilePath, pattern=None):
    try:
        f = open(completeFilePath)
        pvNames = f.read().splitlines()
        pvNames=map(lambda x: x.strip(), pvNames)
        pvNames=filter(lambda x: len(x)>0, pvNames)
        if pattern:
            pvNames=[ re.match(pattern,pvName).group() for pvName in pvNames if re.match(pattern, pvName) ]
        return pvNames
    except IOError:
        return None
    finally:
        if f:
            f.close()

def updateChannelFinder(pvNames, hostName, iocName, time, owner, \
                        service=None, username=None, password=None):
    '''
    pvNames = list of pvNames 
    ([] permitted will effectively remove the hostname, iocname from all channels)
    hostName = pv hostName (None not permitted)
    iocName = pv iocName (None not permitted)
    owner = the owner of the channels and properties being added, this can be different from the user
    e.g. user = abc might create a channel with owner = group-abc
    time = the time at which these channels are being created/modified
    [optional] if not specified the default values are used by the 
    channelfinderapi lib
    service = channelfinder service URL
    username = channelfinder username
    password = channelfinder password
    '''
    if hostName == None or iocName == None:
        raise Exception, 'missing hostName or iocName'
    channels = []
    try:
        client = ChannelFinderClient(BaseURL=service, username=username, password=password)
    except:
        raise Exception, 'Unable to create a valid webResourceClient'
    checkPropertiesExist(client, owner)
    previousChannelsList = client.findByArgs([('hostName', hostName), ('iocName', iocName)])
    if previousChannelsList != None:
        for ch in previousChannelsList:
            if pvNames != None and ch.Name in pvNames:
                ''''''
                channels.append(updateChannel(ch,\
                                              owner=owner, \
                                              hostName=hostName, \
                                              iocName=iocName, \
                                              pvStatus='Active', \
                                              time=time))
                pvNames.remove(ch.Name)
            elif pvNames == None or ch.Name not in pvNames:
                '''Orphan the channel : mark as inactive, keep the old hostName and iocName'''
                channels.append(updateChannel(ch, \
                                              owner=owner, \
                                              hostName=ch.getProperties()['hostName'], \
                                              iocName=ch.getProperties()['iocName'], \
                                              pvStatus='InActive', \
                                              time=ch.getProperties()['time']))
    # now pvNames contains a list of pv's new on this host/ioc
    for pv in pvNames:
        ch = client.findByArgs([('~name',pv)])
        if ch == None:
            '''New channel'''
            channels.append(createChannel(pv, \
                                          chOwner=owner, \
                                          hostName=hostName, \
                                          iocName=iocName, \
                                          pvStatus='Active', \
                                          time=time))
        elif ch[0] != None:
            '''update existing channel: exists but with a different hostName and/or iocName'''
            channels.append(updateChannel(ch[0], \
                                          owner=owner, \
                                          hostName=hostName, \
                                          iocName=iocName, \
                                          pvStatus='Active', \
                                          time=time))
    client.set(channels=channels)

def updateChannel(channel, owner, hostName=None, iocName=None, pvStatus='InActive', time=None):
    '''
    Helper to update a channel object so as to not affect the existing properties
    '''
    if isinstance(channel, Channel):
        # properties list devoid of hostName and iocName properties
        if channel.Properties:
            properties = [property for property in channel.Properties \
                          if property.Name != 'hostName' and property.Name != 'iocName' and property.Name != 'pvStatus']
        else:
            properties = []
        if hostName != None:
            properties.append(Property('hostName', owner, hostName))
        if iocName != None:
            properties.append(Property('iocName', owner, iocName))
        if pvStatus:
            properties.append(Property('pvStatus', owner, pvStatus))
        if time:
            properties.append(Property('time', owner, time)) 
        channel.Properties = properties
        return channel

def createChannel(chName, chOwner, hostName=None, iocName=None, pvStatus='InActive', time=None):
    '''
    Helper to create a channel object with the required properties
    '''
    ch = Channel(chName, chOwner)
    ch.Properties = []
    if hostName != None:
        ch.Properties.append(Property('hostName', chOwner, hostName))
    if iocName != None:
        ch.Properties.append(Property('iocName', chOwner, iocName))
    if pvStatus:
        ch.Properties.append(Property('pvStatus', chOwner, pvStatus))
    if time:
        ch.Properties.append(Property('time', chOwner, time))
    return ch

def checkPropertiesExist(client, propOwner):
    '''
    Checks if the properties used by dbUpdate are present if not it creates them
    '''
    requiredProperties = ['hostName', 'iocName', 'pvStatus', 'time']
    for propName in requiredProperties:
        if client.findProperty(propName) == None:
            try:
                client.set(property=Property(propName, propOwner))
            except Exception as e:
                print 'Failed to create the property',propName
                print 'CAUSE:',e.message

def ifNoneReturnDefault(object, default):
    '''
    if the object is None or empty string then this function returns the default value
    '''
    if object == None and object != '':
        return default
    else:
        return object

def mainRun(opts, args):
    '''
    the main is broken so that the unit test can use mock opt objects for testing
    '''
    for filename in args:
        if('*' in filename or '?' in filename):
            matchingFiles = glob(filename)
            for eachMatchingFile in matchingFiles:
                completeFilePath = os.path.abspath(eachMatchingFile)
                fHostName, fIocName = getArgsFromFilename(completeFilePath)
                ftime = os.path.getctime(completeFilePath)
                pattern = __getDefaultConfig('pattern', opts.pattern)
                updateChannelFinder(getPVNames(completeFilePath, pattern=pattern), \
                            ifNoneReturnDefault(opts.hostName, fHostName), \
                            ifNoneReturnDefault(opts.iocName, fIocName), \
                            ifNoneReturnDefault(opts.time, ftime), \
                            ifNoneReturnDefault(opts.owner,__getDefaultConfig('username', opts.username)), \
                            service=__getDefaultConfig('BaseURL',opts.serviceURL), \
                            username=__getDefaultConfig('username',opts.username), \
                            password=__getDefaultConfig('password',opts.password))
        else:
            completeFilePath = os.path.abspath(filename)
            fHostName, fIocName = getArgsFromFilename(completeFilePath)
            ftime = os.path.getctime(completeFilePath)
            pattern = __getDefaultConfig('pattern', opts.pattern)
            updateChannelFinder(getPVNames(completeFilePath, pattern=pattern), \
                            ifNoneReturnDefault(opts.hostName, fHostName), \
                            ifNoneReturnDefault(opts.iocName, fIocName), \
                            ifNoneReturnDefault(opts.time, ftime), \
                            ifNoneReturnDefault(opts.owner,__getDefaultConfig('username', opts.username)), \
                            service=__getDefaultConfig('BaseURL',opts.serviceURL), \
                            username=__getDefaultConfig('username',opts.username), \
                            password=__getDefaultConfig('password',opts.password))
            
def __getDefaultConfig(arg, value):
        if value == None:
            try:
                return _conf.get('DEFAULT', arg)
            except:
                return None
        else:
            return value
        
def main():
    usage = "usage: %prog [options] filename"
    parser = OptionParser(usage=usage)
    parser.add_option('-H', '--hostname', \
                      action='store', type='string', dest='hostName', \
                      help='the hostname')
    parser.add_option('-i', '--iocname', \
                      action='store', type='string', dest='iocName', \
                      help='the iocname')
    parser.add_option('-s', '--service', \
                      action='store', type='string', dest='serviceURL', \
                      help='the service URL')
    parser.add_option('-o', '--owner', \
                      action='store', type='string', dest='owner', \
                      help='owner if not specified username will default as owner')
    parser.add_option('-r', '--pattern', \
                      action='store', type='string', dest='pattern', \
                      help='pattern to match valid channel names')
    parser.add_option('-u', '--username', \
                      action='store', type='string', dest='username', \
                      help='username')
    parser.add_option('-t', '--time', \
                      action='store', type='string', dest='time', \
                      help='time')
    parser.add_option('-p', '--password', \
                      action='callback', callback=getPassword, \
                      dest='password', \
                      help='prompt user for password')
    opts, args = parser.parse_args()
    if len(args) == 0 or args == None:
        parser.error('Please specify a file')
    mainRun(opts, args)

def getPassword(option, opt_str, value, parser):
    '''
    Simple method to prompt user for password
    TODO do not show the password.
    '''
    parser.values.password = getpass()        
            
if __name__ == '__main__':
    main()
    pass
