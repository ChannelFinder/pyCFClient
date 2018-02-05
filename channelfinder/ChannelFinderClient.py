'''
Copyright (c) 2010 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on Feb 15, 2011

@author: shroffk

'''


import re
import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from requests import auth
from copy import copy
try:
    from json import JSONDecoder, JSONEncoder
except ImportError: 
    from simplejson import JSONDecoder, JSONEncoder

from ._conf import _conf

class ChannelFinderClient(object):
    '''
    The ChannelFinderClient provides a connection object to perform 
    set, update, delete and find operations.
    
    TODO: Fix pydocs
    '''

    __jsonheader = {'content-type':'application/json', 'accept':'application/json'}    
    __channelsResource = '/resources/channels'
    __propertiesResource = '/resources/properties'
    __tagsResource = '/resources/tags'
 
    def __init__(self, BaseURL=None, username=None, password=None):
        '''
        BaseURL = the url of the channelfinder service
        username = 
        '''
        try:            
            self.__baseURL = self.__getDefaultConfig('BaseURL', BaseURL)
            self.__userName = self.__getDefaultConfig('username', username)
            self.__password = self.__getDefaultConfig('password', password)
            if self.__userName and self.__password:
                self.__auth = auth.HTTPBasicAuth(self.__userName, self.__password)
            else:
                self.__auth = None
            self.__session = requests.Session()
            self.__session.mount(self.__baseURL, Ssl3HttpAdapter())
            #self.__session.get(self.__baseURL, verify=False, headers=copy(self.__jsonheader)).raise_for_status()
 
        except:
            raise RuntimeError('Failed to create client to ' + self.__baseURL)

    def __getDefaultConfig(self, arg, value):
        if value == None and _conf.has_option('DEFAULT', arg):
            return _conf.get('DEFAULT', arg)
        else:
            return value

    def set(self, **kwds):
        '''
        method to allow various types of set operations on one or many channels, tags or properties
        The operation creates a new entry if none exists and destructively replaces existing entries.
        set(channel = Channel)
        >>> set(channel={'name':'channelName', 'owner':'channelOwner'})
        >>> set(channel={'name':'channelName',
                         'owner':'channelOwner',
                         'tags':[{'name':'tagName1', 'owner':'tagOwner'}, ...],
                         'properties':[{'name':'propName1', 'owner':'propOwner', 'value':'propValue1'}, ...]})

        set(channels = [Channel])
        >>> set(channels=[{'name':'chName1','owner':'chOwner'},{'name':'chName2','owner':'chOwner'}])
        >>> set(channels=[{'name':'chName1','owner':'chOwner', 'tags':[...], 'properties':[...]}, {...}])
        
        set(tag = Tag)
        >>> set(tag={'name':'tagName','owner':'tagOwner'})
        
        set(tags = [Tag])
        >>> set(tags=[{'name':'tag1','tagOwner'},{'name':'tag2','owner':'tagOwner'}])
        
        set(property = Property )
        >>> set(property={'name':'propertyName','owner':'propertyOwner'})
        
        set(properties = [Property])
        >>> set(properties=[{'name':'prop1','owner':'propOwner'},'prop2','propOwner']) 
                   
        *** IMP NOTE: Following operation are destructive ***
        *** if you simply want to append a tag or property use the update operation***
        
        set(tag=Tag, channelName=String)
        >>> set(tag={'name':'tagName','owner':'tagOwner'}, channelName='chName')
        # will create/replace specified Tag
        # and add it to the channel with the name = channelName
        
        set(tag=Tag, channelNames=[String])
        >>> set (tag={'name':'tagName','owner':'tagOwner'}, channelNames=['ch1','ch2','ch3'])
        # will create/replace the specified Tag 
        # and add it to the channels with the names specified in channelNames
        # and delete it from all other channels
        
        set(property=Property, channelNames=[String])
        >>> set(property={'name':'propName','owner':'propOwner','value':'propValue'}, channels=[...])
        # will create/replace the specified Property
        # and add it to the channels with the names specified in channels
        # and delete it from all other channels
        
        '''
        if len(kwds) == 1:
            self.__handleSingleAddParameter(**kwds)
        elif len(kwds) == 2:
            self.__handleMultipleAddParameters(**kwds)
        else:
            raise RuntimeError('incorrect usage: ')
    
    def __handleSingleAddParameter(self, **kwds):
        if 'channel' in kwds :
            r = self.__session.put(self.__baseURL + self.__channelsResource + '/' + kwds['channel'][u'name'],
                             data=JSONEncoder().encode(kwds['channel']),
                             headers=copy(self.__jsonheader),
                             verify=False,
                             auth=self.__auth)
            r.raise_for_status()
        elif 'channels' in kwds :
            r = self.__session.put(self.__baseURL + self.__channelsResource,
                              data=JSONEncoder().encode(kwds['channels']),
                              headers=copy(self.__jsonheader),
                              verify=False,
                              auth=self.__auth)
            r.raise_for_status()
        elif 'tag' in kwds:
            r = self.__session.put(self.__baseURL + self.__tagsResource + '/' + kwds['tag'][u'name'],
                             data=JSONEncoder().encode(kwds['tag']),
                             headers=copy(self.__jsonheader),
                             verify=False,
                             auth=self.__auth)
            r.raise_for_status()
        elif 'tags' in kwds:
            data = JSONEncoder().encode(kwds['tags'])
            r = self.__session.put(self.__baseURL + self.__tagsResource,
                             data=data,
                             headers=copy(self.__jsonheader),
                             verify=False,
                             auth=self.__auth)
            r.raise_for_status()
        elif 'property' in kwds:
            r = self.__session.put(self.__baseURL + self.__propertiesResource + '/' + kwds['property'][u'name'],
                             data=JSONEncoder().encode(kwds['property']) ,
                             headers=copy(self.__jsonheader),
                             verify=False,
                             auth=self.__auth)
            r.raise_for_status()
        elif 'properties' in kwds: ############################ u'property' may be incorrect
            data = JSONEncoder().encode(kwds['properties'])
            r = self.__session.put(self.__baseURL + self.__propertiesResource,
                              data=data,
                              headers=copy(self.__jsonheader),
                              verify=False,
                              auth=self.__auth)
            r.raise_for_status()
        else:
            raise RuntimeError('Incorrect Usage: unknown key')

    def __handleMultipleAddParameters(self, **kwds):
        # set a tag to a channel
        if 'tag' in kwds and 'channelName' in kwds:
            channels = [{u'name':kwds['channelName'].strip(), u'owner':self.__userName}]
            kwds['tag']['channels'] = channels
            data = kwds['tag']
            self.__session.put(self.__baseURL + self.__tagsResource + '/' + kwds['tag'][u'name'],
                         data=JSONEncoder().encode(data),
                         headers=copy(self.__jsonheader),
                         verify=False,
                         auth=self.__auth).raise_for_status()
        elif 'tag' in kwds and 'channelNames' in kwds:
            channels = []
            for eachChannel in kwds['channelNames']:
                channels.append({u'name':eachChannel, u'owner':self.__userName})
            kwds['tag']['channels'] = channels
            data = kwds['tag']
            self.__session.put(self.__baseURL + self.__tagsResource + '/' + kwds['tag'][u'name'],
                         data=JSONEncoder().encode(data),
                         headers=copy(self.__jsonheader),
                         verify=False,
                         auth=self.__auth).raise_for_status()
        elif 'property' in kwds and 'channels' in kwds:
            data = kwds['property']
            data['property']['channels'] = kwds['channels']
            self.__session.put(self.__baseURL + self.__propertiesResource + '/' + kwds['property'][u'name'],
                         data=JSONEncoder().encode(data),
                         headers=copy(self.__jsonheader),
                         verify=False,
                         auth=self.__auth).raise_for_status()
        else:
            raise RuntimeError('Incorrect Usage: unknown keys')

    def __checkResponseState(self, r):
        '''
        simply checks the return status of the http response
        '''
        if not int(r[u'headers']['status']) <= 206:
            match = re.search(r'<b>description</b>([\S\s]*?)</p>', r[u'body'])
            msg = match.group(1)
            raise RuntimeError('HTTP Error status: ' + r[u'headers']['status'] + ' Cause: ' + msg)
        return r

    def find(self, **kwds):
        '''
        Method allows you to query for a channel/s based on name, properties, tags
        find(name = channelNamePattern)
        >>> find(name='*')
        >>> find(name='SR:C01*')

        find(tagName = tagNamePattern)
        >>> find(tagName = 'myTag')

        find(property = [(propertyName,propertyValuePattern)])
        >>> find(property=[('position','*')])
        >>> find(property=[('position','*'),('cell','')])

        returns a _list_ of matching Channels
        special pattern matching char
        * for multiple char
        ? for single char

        Searching with multiple parameters
        >>> find(name='SR:C01*', tagName = 'myTag', property=[('position','pattern1')])
        return all channels with name matching 'SR:C01*' AND
                            with tagName = 'mytag' AND
                            with property 'position' with value matching 'pattern1'


        For multiValued searches
        >>> find(name='pattern1|pattern2')
        will return all the channels which match either pattern1 OR pattern2
        >>> find(name='pattern1,pattern2')
        will return all the channels which match either pattern1 AND pattern2

        >>> find(property=[('propA','pattern1,pattern2')])
        will return all the channels which have the property propA  and
        whose values match pattern1 OR pattern2

        >>> find(property=[('propA', 'pattern1'),('propB', 'pattern2')])
        will return all the channels which have properties
        _propA_ with value matching _pattern1_ AND _propB_ with value matching _pattern2_

        >>> find(tagName='pattern1,pattern2')
        will return all the channels which have the tags matching pattern1 AND pattern2

        >>> find(size=5)
        will return the first 5 channels

        Basic rule for *size* and *ifrom* parameters:
        (n >= 1, m >= 0)
        >>> assert find(size=n, ifrom=m) == find(size=n+m)[-n:]

        To query for the existance of a tag or property use findTag and findProperty.
        '''
        if not self.__baseURL:
            raise RuntimeError('Connection not created')
        if not len(kwds) > 0:
            raise RuntimeError('Incorrect usage: atleast one parameter must be specified')
        args = []
        for key in kwds:
            if key == 'name':
                patterns = kwds[key].split(',')
                for eachPattern in patterns:
                    args.append(('~name', eachPattern.strip()))
            elif key == 'tagName':
                patterns = kwds[key].split(',')
                for eachPattern in patterns:
                    args.append(('~tag', eachPattern.strip()))
            elif key == 'property':
                for prop in kwds[key]:
                    patterns = prop[1].split(',')
                    for eachPattern in patterns:
                        args.append((prop[0], eachPattern.strip()))
            elif key == 'size':
                args.append(('~size', '{0:d}'.format(int(kwds[key]))))
            elif key == 'ifrom':
                args.append(('~from', '{0:d}'.format(int(kwds[key]))))
            else:
                raise RuntimeError('unknown find argument ' + key)
        return self.findByArgs(args)

    def findByArgs(self, args):
        url = self.__baseURL + self.__channelsResource
        r = self.__session.get(url,
                         params=args,
                         headers=copy(self.__jsonheader),
                         verify=False,
                         auth=self.__auth)
        try:
            r.raise_for_status()
            return r.json()
        except:
            if r.status_code == 404:
                return None
            else:
                r.raise_for_status()

    def findTag(self, tagName):
        '''
        Searches for the _exact_ tagName and returns a single Tag object if found
        '''
        url = self.__baseURL + self.__tagsResource + '/' + tagName
        r = self.__session.get(url,
                         headers=copy(self.__jsonheader),
                         verify=False,
                         auth=self.__auth)
        try:
            r.raise_for_status()
            return r.json()
        except:
            if r.status_code == 404:
                return None
            else:
                r.raise_for_status()

    def findProperty(self, propertyName):
        '''
        Searches for the _exact_ propertyName and return a single Property object if found
        '''
        url = self.__baseURL + self.__propertiesResource + '/' + propertyName
        r = self.__session.get(url, headers=copy(self.__jsonheader), verify=False)
        try:
            r.raise_for_status()
            return r.json()
        except:
            if r.status_code == 404:
                return None
            else:
                r.raise_for_status()

    def getAllTags(self):
        '''
        return a list of all the Tags present - even the ones not associated w/t any channel
        '''
        url = self.__baseURL + self.__tagsResource
        r = self.__session.get(url, headers=copy(self.__jsonheader), verify=False)
        try:
            r.raise_for_status()
            return r.json()
        except:
            if r.status_code == 404:
                return None
            else:
                r.raise_for_status()

    def getAllProperties(self):
        '''
        return a list of all the Properties present - even the ones not associated w/t any channel
        '''
        url = self.__baseURL + self.__propertiesResource
        r = self.__session.get(url, headers=copy(self.__jsonheader), verify=False)
        try:
            r.raise_for_status()
            return r.json()
        except:
            if r.status_code == 404:
                return None
            else:
                r.raise_for_status()

    def delete(self, **kwds):
        '''
        Method to delete a channel, property, tag
        delete(channelName = String)
        >>> delete(channelName = 'ch1')

        delete(tagName = String)
        >>> delete(tagName = 'myTag')
        # tagName = tag name of the tag to be removed from all channels

        delete(propertyName = String)
        >>> delete(propertyName = 'position')
        # propertyName = property name of property to be removed from all channels

        delete(tag = Tag ,channelName = String)
        >>> delete(tag={'name':'myTag','owner':'tagOwner'}, channelName = 'chName')
        # delete the tag from the specified channel _chName_

        delete(tag = Tag ,channelNames = [String])
        >>> delete(tag={'name':'myTag', 'owner':'tagOwner'}, channelNames=['ch1','ch2','ch3'])
        # delete the tag from all the channels specified in the channelNames list

        delete(property = Property ,channelName = String)
        >>> delete(property = {'name':'propName','propOwner':'propOwner'} ,channelName = 'chName')
        # delete the property from the specified channel

        delete(property = Property ,channelNames = [String])
        >>> delete(property = {'name':'propName','owner':'propOwner'} ,channelNames = ['ch1','ch2','ch3'])
        # delete the property from all the channels in the channelNames list
        '''
        if len(kwds) == 1:
            self.__handleSingleDeleteParameter(**kwds)
        elif len(kwds) == 2:
            self.__handleMultipleDeleteParameters(**kwds)
        else:
            raise RuntimeError('incorrect usage: Delete a single Channel/tag/property')

    def __handleSingleDeleteParameter(self, **kwds):
        if 'channelName' in kwds:
            url = self.__baseURL + self.__channelsResource + '/' + kwds['channelName'].strip()
            self.__session.delete(url,
                            headers=copy(self.__jsonheader),
                            verify=False,
                            auth=self.__auth).raise_for_status()
            pass
        elif 'tagName' in kwds:
            url = self.__baseURL + self.__tagsResource + '/' + kwds['tagName'].strip()
            self.__session.delete(url,
                            verify=False,
                            headers=copy(self.__jsonheader),
                            auth=self.__auth).raise_for_status()
            pass
        elif 'propertyName' in kwds:
            url = self.__baseURL + self.__propertiesResource + '/' + kwds['propertyName'].strip()
            self.__session.delete(url,
                            headers=copy(self.__jsonheader),
                            verify=False,
                            auth=self.__auth).raise_for_status()
            pass
        else:
            raise RuntimeError(' unkown key use channelName, tagName or proprtyName')

    def __handleMultipleDeleteParameters(self, **kwds):
        if 'tag' in kwds and 'channelName' in kwds:
            self.__session.delete(self.__baseURL + self.__tagsResource + '/' + kwds['tag'][u'name'] + '/' + kwds['channelName'].strip(),
                            headers=copy(self.__jsonheader),
                            verify=False,
                            auth=self.__auth).raise_for_status()
        elif 'tag' in kwds and 'channelNames' in kwds:
            # find channels with the tag
            channelsWithTag = self.find(tagName=kwds['tag'][u'name'])
            # delete channels from which tag is to be removed

            channelNames = [channel[u'name'] for channel in channelsWithTag if channel[u'name'] not in kwds['channelNames']]
            self.set(tag=kwds['tag'], channelNames=channelNames)
        elif 'property' in kwds and 'channelName' in kwds:
            self.__session.delete(self.__baseURL + self.__propertiesResource + '/' + kwds['property'][u'name'] + '/' + kwds['channelName'],
                            headers=copy(self.__jsonheader),
                            verify=False,
                            auth=self.__auth).raise_for_status()
        elif 'property' in kwds and 'channelNames' in kwds:
            channelsWithProp = self.find(property=[(kwds['property'][u'name'], '*')])
            channels = [channel for channel in channelsWithProp if channel[u'name'] not in kwds['channelNames']]
            self.set(property=kwds['property'], channels=channels)
        else:
            raise RuntimeError(' unkown keys')

#===============================================================================
# Update methods
#===============================================================================
    def update(self, **kwds):
        '''
        update(channel = Channel)
        >>> update(channel = {'name':'existingCh',
                                     'owner':'chOwner',
                                     'properties':'[
                                        {'name':'newProp','owner':'propOwner','value':'Val'},
                                        {'name':'existingProp','owner':'propOwner','value':'newVal'}],
                                     tags=[{'name':'mytag','owner':'tagOwner'}]})
        # updates the channel 'existingCh' with the new provided properties and tags
        # without affecting the other tags and properties of this channel

        update(property = Property, channelName = String)
        >>> update(property={'name':'propName', 'owner':'propOwner', 'value':'propValue'},
                                    channelName='ch1')
        # Add Property to the channel with the name 'ch1'
        # without affecting the other channels using this property

        >>>update(property={'name':'propName', 'owner':'propOwner', 'value':'propValue'},
                                    channelNames=['ch1','ch2','ch3'])
        # Add Property to the channels with the names in the list channelNames
        # without affecting the other channels using this property

        update(tag = Tag, channelName = String)
        >>> update(tag = {'name':'myTag', 'owner':'tagOwner'}, channelName='chName')
        # Add tag to channel with name chName
        # without affecting the other channels using this tag

        update(tag = Tag, channelNames = [String])
        >>> update(tag = {'name':'tagName'}, channelNames=['ch1','ch2','ch3'])
        # Add tag to channels with names in the list channeNames
        # without affecting the other channels using this tag

        update(property = Property)
        update(tag = Tag)

        ## RENAME OPERATIONS ##
        update(channel = Channel, originalChannelName = String)
        >>> update(channel = {'name':'newChannelName','owner':'channelOwner'},
                                     originalChannelName = 'oldChannelName')
        # rename the channel 'oldChannelName' to 'newChannelName'

        update(property = Property, originalPropertyName = String)
        >>> update(property = {'name':'newPropertyName','owner':'propOwner'},
                                       originalPropertyName = 'oldPropertyName')
        # rename the property 'oldPropertyName' to 'newPropertyName'
        # the channels with the old property are also updated

        update(tag = Tag, originalTagName = String)
        >>> update(tab = {'name':'newTagName','owner':'tagOwner'}, originalTagName = 'oldTagName')
        # rename the tag 'oldTagName' to 'newTagName'
        # the channel with the old tag are also updated
        '''

        if not self.__baseURL:
            raise RuntimeError('Olog client not configured correctly')
        if len(kwds) == 1:
            self.__handleSingleUpdateParameter(**kwds)
        elif len(kwds) == 2:
            self.__handleMultipleUpdateParameters(**kwds)
        else:
            raise RuntimeError('incorrect usage: ')

    def __handleSingleUpdateParameter(self, **kwds):
        if 'channel' in kwds:
            ch = kwds['channel']
            r = self.__session.post(self.__baseURL + self.__channelsResource + '/' + ch[u'name'],
                                     data=JSONEncoder().encode(ch),
                                     headers=copy(self.__jsonheader),
                                     verify=False,
                                     auth=self.__auth)
            r.raise_for_status()
        elif 'property' in kwds:
            property = kwds['property']
            r = self.__session.post(self.__baseURL + self.__propertiesResource + '/' + property[u'name'],
                                     data=JSONEncoder().encode(property),
                                     headers=copy(self.__jsonheader),
                                     verify=False,
                                     auth=self.__auth)
            r.raise_for_status()
        elif 'tag' in kwds:
            tag = kwds['tag']
            r = self.__session.post(self.__baseURL + self.__tagsResource + '/' + tag[u'name'],
                          data=JSONEncoder().encode(tag),
                          headers=copy(self.__jsonheader),
                          verify=False,
                          auth=self.__auth)
            r.raise_for_status()
        elif 'tags' in kwds:
            r = self.__session.post(self.__baseURL + self.__tagsResource,
                          data=JSONEncoder().encode(kwds['tags']),
                          headers=copy(self.__jsonheader),
                          verify=False,
                          auth=self.__auth)
            r.raise_for_status()
        else:
            raise RuntimeError(' unkown key ')

    def __handleMultipleUpdateParameters(self, **kwds):
        if 'tag' in kwds and 'channelName' in kwds:
            # identity operation performed to prevent side-effects
            tag = dict(kwds['tag'])
            channels = [{u'name': kwds['channelName'].strip(), u'owner': self.__userName, u'tags': [tag]}]
            tag = dict(tag)
            tag[u'channels'] = channels
            self.__session.post(self.__baseURL + self.__tagsResource + '/' + tag[u'name'],
                          data=JSONEncoder().encode(tag),
                          headers=copy(self.__jsonheader),
                          verify=False,
                          auth=self.__auth).raise_for_status()
        elif 'tag' in kwds and 'channelNames' in kwds:
            # identity operation performed to prevent side-effects
            tag = dict(kwds['tag'])
            channels = []
            for eachChannel in kwds['channelNames']:
                channels.append({u'name': eachChannel, u'owner': self.__userName, u'tags': [tag]})
            tag = dict(tag)
            tag[u'channels'] = channels
            self.__session.post(self.__baseURL + self.__tagsResource + '/' + tag[u'name'],
                          data=JSONEncoder().encode(tag),
                          headers=copy(self.__jsonheader),
                          verify=False,
                          auth=self.__auth).raise_for_status()
        elif 'property' in kwds and 'channelName' in kwds:
            # identity operation performed to prevent side-effects
            property = dict(kwds['property'])
            channels = [{u'name': kwds['channelName'].strip(), u'owner': self.__userName, u'properties': [property]}]
            property = dict(property)
            property[u'channels'] = channels
            self.__session.post(self.__baseURL + self.__propertiesResource + '/' + property[u'name'],
                          data=JSONEncoder().encode(property),
                          headers=copy(self.__jsonheader),
                          verify=False,
                          auth=self.__auth).raise_for_status()
        elif 'property' in kwds and 'channelNames' in kwds:
            # identity operation performed to prevent side-effects
            property = dict(kwds['property'])
            channels = []
            for eachChannel in kwds['channelNames']:
                channels.append({u'name': eachChannel.strip(), u'owner': self.__userName, u'properties': [property]})
            property = dict(property)
            property[u'channels'] = channels
            self.__session.post(self.__baseURL + self.__propertiesResource + '/' + property[u'name'],
                          data=JSONEncoder().encode(property),
                          headers=copy(self.__jsonheader),
                          verify=False,
                          auth=self.__auth).raise_for_status()
        elif 'originalChannelName' in kwds and 'channel' in kwds:
            ch = kwds['channel']
            channelName = kwds['originalChannelName'].strip()
            self.__session.post(self.__baseURL + self.__channelsResource + '/' + channelName,
                          data=JSONEncoder().encode(ch),
                          headers=copy(self.__jsonheader),
                          verify=False,
                          auth=self.__auth).raise_for_status()
        elif 'originalPropertyName' in kwds and 'property' in kwds:
            prop = kwds['property']
            propName = kwds['originalPropertyName'].strip()
            self.__session.post(self.__baseURL + self.__propertiesResource + '/' + propName,
                          data=JSONEncoder().encode(prop),
                          headers=copy(self.__jsonheader),
                          verify=False,
                          auth=self.__auth).raise_for_status()
        elif 'originalTagName' in kwds and 'tag' in kwds:
            tag = kwds['tag']
            tagName = kwds['originalTagName'].strip()
            self.__session.post(self.__baseURL + self.__tagsResource + '/' + tagName,
                          data=JSONEncoder().encode(tag),
                          headers=copy(self.__jsonheader),
                          verify=False,
                          auth=self.__auth).raise_for_status()
        else:
            raise RuntimeError(' unknown keys')



class Ssl3HttpAdapter(HTTPAdapter):
    """"Transport adapter" that allows us to use SSLv3."""

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_SSLv23)

