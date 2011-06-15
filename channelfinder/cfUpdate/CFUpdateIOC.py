'''
Created on Apr 1, 2011

@author: shroffk
'''
import os
import re
from optparse import OptionParser
from getpass import getpass
from channelfinder.core.Channel import Channel, Property
from channelfinder.core.ChannelFinderClient import ChannelFinderClient
from glob import glob

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

def getPVNames(completeFilePath):
    try:
        f = open(completeFilePath)
        pvNames = f.read().splitlines()
        pvNames=map(lambda x: x.strip(), pvNames)
        pvNames=filter(lambda x: len(x)>0, pvNames)
        return pvNames
    except IOError:
        return None

def updateChannelFinder(pvNames, hostName, iocName, \
                        service=None, username=None, password=None):
    '''
    pvNames = list of pvNames 
    (None permitted will effectively remove the hostname, iocname from all channels)
    hostName = pv hostName (None not permitted)
    iocName = pv iocName (None not permitted)
    [optional] if not specified the default values are used by the 
    channelfinderapi lib
    service = channelfinder service URL
    username = channelfinder username
    password = channelfinder password
    '''
    if hostName == None or iocName == None:
        raise Exception, 'missing hostName or iocName'
    channels = []
    client = ChannelFinderClient(BaseURL=service, username=username, password=password)
    checkPropertiesExist(client, username)
    previousChannelsList = client.find(property=[('hostName', hostName), ('iocName', iocName)])
    if previousChannelsList != None:
        for ch in previousChannelsList:
            if pvNames != None and ch.Name in pvNames:
                channels.append(updateChannel(ch, \
                                              hostName=hostName, \
                                              iocName=iocName))
                pvNames.remove(ch.Name)
            elif pvNames == None or ch.Name not in pvNames:
                #  orphan the channel
                channels.append(updateChannel(ch))
    # now pvNames contains a list of pv's new on this host/ioc
    for pv in pvNames:
        ch = client.find(name=pv)
        if ch == None:
            # New channel
            channels.append(createChannel(pv, username, \
                                          hostName=hostName, \
                                          iocName=iocName))
        elif ch[0] != None:
            # update existing channel
            channels.append(updateChannel(ch[0], username, \
                                          hostName=hostName, \
                                          iocName=iocName))
    client.set(channels=channels)

def updateChannel(channel, username, hostName=None, iocName=None):
    '''
    Helper to update a channel object so as to not affect the existing properties
    '''
    if isinstance(channel, Channel):
        # properties list devoid of hostName and iocName properties
        properties = [property for property in channel.Properties \
                      if property.Name != 'hostName' and property.Name != 'iocName']
        if hostName != None:
            properties.append(Property('hostName', username, hostName))
        if iocName != None:
            properties.append(Property('iocName', username, iocName))
        channel.Properties = properties
        return channel

def createChannel(chName, chOwner, hostName=None, iocName=None):
    '''
    Helper to create a channel object with the required properties
    '''
    ch = Channel(chName, chOwner)
    ch.Properties = []
    if hostName != None:
        ch.Properties.append(Property('hostName', chOwner, hostName))
    if iocName != None:
        ch.Properties.append(Property('iocName', chOwner, iocName))
    return ch

def checkPropertiesExist(client, username):
    '''
    Checks if the properties used by dbUpdate are present if not it creates them
    '''
    requiredProperties = ['hostName', 'iocName']
    for propName in requiredProperties:
        if client.findProperty(propName) == None:
            client.set(property=Property(propName, username))                

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
                updateChannelFinder(getPVNames(completeFilePath), \
                            ifNoneReturnDefault(opts.hostName, fHostName), \
                            ifNoneReturnDefault(opts.iocName, fIocName), \
                            service=opts.serviceURL, username=opts.username, password=opts.password)
        else:
            completeFilePath = os.path.abspath(filename)
            fHostName, fIocName = getArgsFromFilename(completeFilePath)
            updateChannelFinder(getPVNames(completeFilePath), \
                            ifNoneReturnDefault(opts.hostName, fHostName), \
                            ifNoneReturnDefault(opts.iocName, fIocName), \
                            service=opts.serviceURL, username=opts.username, password=opts.password)
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
    parser.add_option('-u', '--username', \
                      action='store', type='string', dest='username', \
                      help='username')
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
