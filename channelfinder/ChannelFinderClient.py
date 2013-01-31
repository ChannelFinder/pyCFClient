'''
Copyright (c) 2010 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on Feb 15, 2011

@author: shroffk

'''
import re
import requests
from requests import auth
from copy import copy
from _conf import _conf
try: 
    from json import JSONDecoder, JSONEncoder
except ImportError: 
    from simplejson import JSONDecoder, JSONEncoder
from CFDataTypes import Channel, Property, Tag
from collections import OrderedDict    


class ChannelFinderClient(object):
    '''
    The ChannelFinderClient provides a connection object to perform 
    set, update, delete and find operations.
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
            if username and password:
                self.__auth = auth.HTTPBasicAuth(username, password)
            else:
                self.__auth = None
            requests.get(self.__baseURL + self.__tagsResource, verify=False, headers=copy(self.__jsonheader)).raise_for_status()
        except:
            raise Exception, 'Failed to create client to ' + self.__baseURL

    def __getDefaultConfig(self, arg, value):
        if value == None and _conf.has_option('DEFAULT', arg):
            return _conf.get('DEFAULT', arg)
        else:
            return value
        
    def __getAllChannels(self):
        '''
        Returns a list of all the channels
        '''
        if self.connection:
            resp = requests.get(self.__baseURL + self.__channelsResource,
                                headers=copy(self.__jsonheader),
                                verify=False,
                                auth=self.__auth)
            resp.raise_for_status()
            j = JSONDecoder().decode(resp.content.json())
            self.decodeChannels(j)
            if (resp[u'headers']['status'] != '404'):
                j = JSONDecoder().decode(resp[u'body'])
                return self.decodeChannels(j)
        return None

    def set(self, **kwds):
        '''
        method to allow various types of set operations on one or many channels, tags or properties
        The operation creates a new entry if none exists and destructively replaces existing entries.
        set(channel = Channel)
        >>> set(channel=Channel('channelName', 'channelOwner'))
        
        set(channels = [Channel])
        >>> set(channels=[Channel('chName1','chOwner'),Channel('chName2','chOwner')])
        
        set(tag = Tag)
        >>> set(tag=Tag('tagName','tagOwner'))
        
        set(tags = [Tag])
        >>> set(tags=[Tag('tag1','tagOwner'),Tag('tag2','tagOwner')])
        
        set(property = Property )
        >>> set(property=Property('propertyName','propertyOwner'))
        
        set(properties = [Property])
        >>> set(properties=[Property('prop1','propOwner'),'prop2','propOwner']) 
                   
        *** IMP NOTE: Following operation are destructive ***
        *** if you simply want to append a tag or property use the update operation***
        
        set(tag=Tag, channelName=String)
        >>> set(tag=Tag('tagName','tagOwner), channelName='chName')
        # will create/replace specified Tag
        # and add it to the channel with the name = channelName
        
        set(tag=Tag, channelNames=[String])
        >>> set (tag=Tag('tagName','tagOwner), channelNames=['ch1','ch2','ch3'])
        # will create/replace the specified Tag 
        # and add it to the channels with the names specified in channelNames
        # and delete it from all other channels
        
        set(property=Property, channelName=String)
        >>> set(property=Property('propName','propOwner','propValue'), channelName='channelName')
        # will create/replace the specified Property 
        # and add it to the channel with the name = channelName
        
        set(property=Property, channelNames=[String])
        >>> set(property=Property('propName','propOwner','propValue'), channelNames=[String])
        # will create/replace the specified Property
        # and add it to the channels with the names specified in channelNames
        # and delete it from all other channels
        
        '''
        if len(kwds) == 1:
            self.__hadleSingleAddParameter(**kwds)
        elif len(kwds) == 2:
            self.__handleMultipleAddParameters(**kwds)
        else:
            raise Exception, 'incorrect usage: '
    
    def __hadleSingleAddParameter(self, **kwds):
        if 'channel' in kwds :
            ch = kwds['channel']
            r = requests.put(self.__baseURL + self.__channelsResource + '/' + ch.Name, \
                             data=JSONEncoder().encode(self.__encodeChannel(ch)), \
                             headers=copy(self.__jsonheader), \
                             verify=False, \
                             auth=self.__auth)
            r.raise_for_status()
        elif 'channels' in kwds :
            r = requests.post(self.__baseURL + self.__channelsResource, \
                              data=JSONEncoder().encode(self.__encodeChannels(kwds['channels'])), \
                              headers=copy(self.__jsonheader), \
                              verify=False, \
                              auth=self.__auth)
            r.raise_for_status()
        elif 'tag' in kwds:
            r = requests.put(self.__baseURL + self.__tagsResource + '/' + kwds['tag'].Name, \
                             data=JSONEncoder().encode(self.__encodeTag(kwds['tag'])), \
                             headers=copy(self.__jsonheader), \
                             verify=False, \
                             auth=self.__auth)
            r.raise_for_status()
        elif 'tags' in kwds:
            r = requests.post(self.__baseURL + self.__tagsResource, \
                             data=JSONEncoder().encode({'tags':{'tag':self.__encodeTags(kwds['tags'])}}), \
                             headers=copy(self.__jsonheader), \
                             verify=False, \
                             auth=self.__auth)
            r.raise_for_status()
        elif 'property' in kwds:
            r = requests.put(self.__baseURL + self.__propertiesResource + '/' + kwds['property'].Name, \
                             data=JSONEncoder().encode(self.__encodeProperty(kwds['property'])) , \
                             headers=copy(self.__jsonheader), \
                             verify=False, \
                             auth=self.__auth)
            r.raise_for_status()
        elif 'properties' in kwds:
            r = requests.post(self.__baseURL + self.__propertiesResource, \
                              data=JSONEncoder().encode({'properties':\
                                                         {'property':\
                                                          self.__encodeProperties(kwds['properties'])}}), \
                              headers=copy(self.__jsonheader), \
                              verify=False, \
                              auth=self.__auth)
            r.raise_for_status()                               
        else:
            raise Exception, 'Incorrect Usage: unknown key'   
    
    def __handleMultipleAddParameters(self, **kwds):
        # set a tag to a channel
        if 'tag' in kwds and 'channelName' in kwds:
            channels = [Channel(kwds['channelName'].strip(), self.__userName, tags=[kwds['tag']])]
            requests.put(self.__baseURL + self.__tagsResource + '/' + kwds['tag'].Name, \
                         data=JSONEncoder().encode(self.__encodeTag(kwds['tag'], withChannels=channels)), \
                         headers=copy(self.__jsonheader), \
                         verify=False, \
                         auth=self.__auth).raise_for_status()
        elif 'tag' in kwds and 'channelNames' in kwds:
            channels = []
            for eachChannel in kwds['channelNames']:
                channels.append(Channel(eachChannel, self.__userName, tags=[kwds['tag']]))
            requests.put(self.__baseURL + self.__tagsResource + '/' + kwds['tag'].Name, \
                         data=JSONEncoder().encode(self.__encodeTag(kwds['tag'], withChannels=channels)), \
                         headers=copy(self.__jsonheader), \
                         verify=False, \
                         auth=self.__auth).raise_for_status()
        elif 'property' in kwds and 'channelName' in kwds:
            channels = [Channel(kwds['channelName'].strip(), self.__userName, properties=[kwds['property']])]
            requests.put(self.__baseURL + self.__propertiesResource + '/' + kwds['property'].Name, \
                         data=JSONEncoder().encode(self.__encodeProperty(kwds['property'], withChannels=channels)), \
                         headers=copy(self.__jsonheader), \
                         verify=False, \
                         auth=self.__auth).raise_for_status()
        elif 'property' in kwds and 'channelNames' in kwds:
            channels = []
            for eachChannel in kwds['channelNames']:
                channels.append(Channel(eachChannel, self.__userName, properties=[kwds['property']]))
            requests.put(self.__baseURL + self.__propertiesResource + '/' + kwds['property'].Name, \
                         data=JSONEncoder().encode(self.__encodeProperty(kwds['property'], withChannels=channels)), \
                         headers=copy(self.__jsonheader), \
                         verify=False, \
                         auth=self.__auth).raise_for_status()
        elif 'property' in kwds and 'channels' in kwds:
            requests.put(self.__baseURL + self.__propertiesResource + '/' + kwds['property'].Name, \
                         data=JSONEncoder().encode(self.__encodeProperty(kwds['property'], withChannels=kwds['channels'])), \
                         headers=copy(self.__jsonheader), \
                         verify=False, \
                         auth=self.__auth).raise_for_status()
        else:
            raise Exception, 'Incorrect Usage: unknown keys'
    
    def __checkResponseState(self, r):
        '''
        simply checks the return status of the http response
        '''
        if not int(r[u'headers']['status']) <= 206:
            match = re.search(r'<b>description</b>([\S\s]*?)</p>', r[u'body'])
            msg = match.group(1)
            raise Exception, 'HTTP Error status: ' + r[u'headers']['status'] + \
                ' Cause: ' + msg
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
        >>> find(name='pattern1,pattern2')
        will return all the channels which match either pattern1 OR pattern2
        
        >>> find(property=[('propA','pattern1,pattern2')])
        will return all the channels which have the property propA  and 
        whose values match pattern1 OR pattern2
        
        >>> find(property=[('propA', 'pattern1'),('propB', 'pattern2')])
        will return all the channels which have properties
        _propA_ with value matching _pattern1_ AND _propB_ with value matching _pattern2_
        
        >>> find(tagName='pattern1,pattern2')
        will return all the channels which have the tags matching pattern1 AND pattern2
                
        To query for the existance of a tag or property use findTag and findProperty.                  
        '''
        if not self.__baseURL:
            raise Exception, 'Connection not created'
        if not len(kwds) > 0:
            raise Exception, 'Incorrect usage: atleast one parameter must be specified'
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
            else:
                raise Exception, 'unknown find argument ' + key
        return self.findByArgs(args)
    
    def findByArgs(self, args):
        url = self.__baseURL + self.__channelsResource
        r = requests.get(url, \
                         params=args, \
                         headers=copy(self.__jsonheader), \
                         verify=False, \
                         auth=self.__auth)
        try:
            r.raise_for_status()
            return self.__decodeChannels(r.json())
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
        r = requests.get(url,
                         headers=copy(self.__jsonheader),
                         verify=False,
                         auth=self.__auth)
        try:
            r.raise_for_status()
            return self.__decodeTag(r.json())
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
        r = requests.get(url, headers=copy(self.__jsonheader), verify=False)
        try:
            r.raise_for_status()
            return self.__decodeProperty(r.json())
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
        r = requests.get(url, headers=copy(self.__jsonheader), verify=False)
        try:
            r.raise_for_status()
            return self.__decodeTags(r.json())
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
        r = requests.get(url, headers=copy(self.__jsonheader), verify=False)
        try:
            r.raise_for_status()
            return self.__decodeProperties(r.json())
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
        >>> delete(tag=Tag('myTag','tagOwner'), channelName = 'chName') 
        # delete the tag from the specified channel _chName_
        
        delete(tag = Tag ,channelNames = [String])
        >>> delete(tag=Tag('myTag','tagOwner'), channelNames=['ch1','ch2','ch3'])
        # delete the tag from all the channels specified in the channelNames list
        
        delete(property = Property ,channelName = String)
        >>> delete(property = Property('propName','propOwner') ,channelName = 'chName')
        # delete the property from the specified channel
        
        delete(property = Property ,channelNames = [String])
        >>> delete(property = Property('propName','propOwner') ,channelNames = ['ch1','ch2','ch3'])
        # delete the property from all the channels in the channelNames list
        '''
        if len(kwds) == 1:
            self.__handleSingleDeleteParameter(**kwds)
        elif len(kwds) == 2:
            self.__handleMultipleDeleteParameters(**kwds)
        else:
            raise Exception, 'incorrect usage: Delete a single Channel/tag/property'
    
    def __handleSingleDeleteParameter(self, **kwds):
        if 'channelName' in kwds:
            url = self.__baseURL + self.__channelsResource + '/' + kwds['channelName'].strip()
            requests.delete(url, \
                            headers=copy(self.__jsonheader), \
                            verify=False, \
                            auth=self.__auth).raise_for_status()
            pass
        elif 'tagName' in kwds:
            url = self.__baseURL + self.__tagsResource + '/' + kwds['tagName'].strip()
            requests.delete(url, \
                            verify=False, \
                            headers=copy(self.__jsonheader), \
                            auth=self.__auth).raise_for_status()
            pass
        elif 'propertyName' in kwds:
            url = self.__baseURL + self.__propertiesResource + '/' + kwds['propertyName'].strip()
            requests.delete(url, \
                            headers=copy(self.__jsonheader), \
                            verify=False, \
                            auth=self.__auth).raise_for_status()
            pass
        else:
            raise Exception, ' unkown key use channelName, tagName or proprtyName'
    
    def __handleMultipleDeleteParameters(self, **kwds):
        if 'tag' in kwds and 'channelName' in kwds:
            requests.delete(self.__baseURL + self.__tagsResource + '/' + kwds['tag'].Name + '/' + kwds['channelName'].strip(), \
                            headers=copy(self.__jsonheader), \
                            verify=False, \
                            auth=self.__auth).raise_for_status()
        elif 'tag' in kwds and 'channelNames' in kwds:
            # find channels with the tag
            channelsWithTag = self.find(tagName=kwds['tag'].Name)
            # delete channels from which tag is to be removed
            channelNames = [channel.Name for channel in channelsWithTag if channel.Name not in kwds['channelNames']]
            self.set(tag=kwds['tag'], channelNames=channelNames)
        elif 'property' in kwds and 'channelName' in kwds:
            requests.delete(self.__baseURL + self.__propertiesResource + '/' + kwds['property'].Name + '/' + kwds['channelName'], \
                            headers=copy(self.__jsonheader), \
                            verify=False, \
                            auth=self.__auth).raise_for_status()
        elif 'property' in kwds and 'channelNames' in kwds:
            channelsWithProp = self.find(property=[(kwds['property'].Name, '*')])
            channels = [channel for channel in channelsWithProp if channel.Name not in kwds['channelNames']]
            self.set(property=kwds['property'], channels=channels)        
        else:
            raise Exception, ' unkown keys'

#===============================================================================
# Update methods
#===============================================================================
    def update(self, **kwds):
        '''
        update(channel = Channel)
        >>> update(channel = Channel('existingCh',
                                     'chOwner',
                                     properties=[
                                        Property('newProp','propOwner','Val'),
                                        Property('existingProp','propOwner','newVal')],
                                     tags=[Tag('mytag','tagOwner')])
        # updates the channel 'existingCh' with the new provided properties and tags 
        # without affecting the other tags and properties of this channel 
        
        update(property = Property, channelName = String)
        >>> update(property=Property('propName', 'propOwner', 'propValue'), 
                                    channelName='ch1')
        # Add Property to the channel with the name 'ch1'
        # without affecting the other channels using this property 
        
        >>>update(property=Property('propName', 'propOwner', 'propValue'), 
                                    channelNames=['ch1','ch2','ch3'])
        # Add Property to the channels with the names in the list channelNames
        # without affecting the other channels using this property 
        
        update(tag = Tag, channelName = String)
        >>> update(tag = Tag('myTag','tagOwner'), channelName='chName')
        # Add tag to channel with name chName
        # without affecting the other channels using this tag
        
        update(tag = Tag, channelNames = [String])
        >>> update(tag = Tag('tagName'), channelNames=['ch1','ch2','ch3'])
        # Add tag to channels with names in the list channeNames
        # without affecting the other channels using this tag 

        update(property = Property)
        update(tag = Tag)
        
        ## RENAME OPERATIONS ##    
        update(channel = Channel, originalChannelName = String)
        >>> update(channel = Channel('newChannelName','channelOwner), 
                                     originalChannelName = 'oldChannelName')
        # rename the channel 'oldChannelName' to 'newChannelName'
        
        update(property = Property, originalPropertyName = String)
        >>> update(property = Property('newPropertyName','propOwner'), 
                                       originalPropertyName = 'oldPropertyName')
        # rename the property 'oldPropertyName' to 'newPropertyName'
        # the channels with the old property are also updated
        
        update(tab = Tag, originalTagName = String)
        >>> update(tab = Tag('newTagName','tagOwner'), originalTagName = 'oldTagName')
        # rename the tag 'oldTagName' to 'newTagName'
        # the channel with the old tag are also updated
        '''
        
        if not self.__baseURL:
            raise Exception, 'Olog client not configured correctly'
        if len(kwds) == 1:
            self.__handleSingleUpdateParameter(**kwds)
        elif len(kwds) == 2:
            self.__handleMultipleUpdateParameters(**kwds)
        else:
            raise Exception, 'incorrect usage: '
    
    def __handleSingleUpdateParameter(self, **kwds):
        if 'channel' in kwds:
            ch = kwds['channel']
            requests.post(self.__baseURL + self.__channelsResource + '/' + ch.Name, \
                                     data=JSONEncoder().encode(self.__encodeChannel(ch)), \
                                     headers=copy(self.__jsonheader), \
                                     verify=False, \
                                     auth=self.__auth).raise_for_status()
        elif 'property' in kwds:
            property = kwds['property']
            requests.post(self.__baseURL + self.__propertiesResource + '/' + property.Name, \
                                     data=JSONEncoder().encode(self.__encodeProperty(property)), \
                                     headers=copy(self.__jsonheader), \
                                     verify=False, \
                                     auth=self.__auth).raise_for_status()            
        elif 'tag' in kwds:
            tag = kwds['tag']
            requests.post(self.__baseURL + self.__tagsResource + '/' + tag.Name, \
                          data=JSONEncoder().encode(self.__encodeTag(tag)), \
                          headers=copy(self.__jsonheader), \
                          verify=False, \
                          auth=self.__auth).raise_for_status()
        else:
            raise Exception, ' unkown key '
        
    def __handleMultipleUpdateParameters(self, **kwds):
        if 'tag' in kwds and 'channelName' in kwds:
            tag = kwds['tag']
            channels = [Channel(kwds['channelName'].strip(), self.__userName)]
            requests.post(self.__baseURL + self.__tagsResource + '/' + tag.Name, \
                          data=JSONEncoder().encode(self.__encodeTag(tag, withChannels=channels)), \
                          headers=copy(self.__jsonheader), \
                          verify=False, \
                          auth=self.__auth).raise_for_status()
        elif 'tag' in kwds and 'channelNames' in kwds:
            tag = kwds['tag']
            channels = []
            for eachChannel in kwds['channelNames']:
                channels.append(Channel(eachChannel, self.__userName))
            requests.post(self.__baseURL + self.__tagsResource + '/' + tag.Name, \
                          data=JSONEncoder().encode(self.__encodeTag(tag, withChannels=channels)), \
                          headers=copy(self.__jsonheader), \
                          verify=False, \
                          auth=self.__auth).raise_for_status()
        elif 'property' in kwds and 'channelName' in kwds:
            property = kwds['property']
            channels = [Channel(kwds['channelName'].strip(), self.__userName, properties=[property])]
            requests.post(self.__baseURL + self.__propertiesResource + '/' + property.Name, \
                          data=JSONEncoder().encode(self.__encodeProperty(property, withChannels=channels)), \
                          headers=copy(self.__jsonheader), \
                          verify=False, \
                          auth=self.__auth).raise_for_status()
        elif 'property' in kwds and 'channelNames' in kwds:
            property = kwds['property']
            channels = []
            for eachChannel in kwds['channelNames']:
                channels.append(Channel(eachChannel, self.__userName, properties=[property]))
            requests.post(self.__baseURL + self.__propertiesResource + '/' + property.Name, \
                          data=JSONEncoder().encode(self.__encodeProperty(property, withChannels=channels)), \
                          headers=copy(self.__jsonheader), \
                          verify=False, \
                          auth=self.__auth).raise_for_status()          
        elif 'originalChannelName' in kwds and 'channel' in kwds:
            ch = kwds['channel']
            channelName = kwds['originalChannelName'].strip()
            requests.post(self.__baseURL + self.__channelsResource + '/' + channelName, \
                          data=JSONEncoder().encode(self.__encodeChannel(ch)) , \
                          headers=copy(self.__jsonheader), \
                          verify=False, \
                          auth=self.__auth).raise_for_status()
        elif 'originalPropertyName' in kwds and 'property' in kwds:
            prop = kwds['property']
            propName = kwds['originalPropertyName'].strip()
            requests.post(self.__baseURL + self.__propertiesResource + '/' + propName, \
                          data=JSONEncoder().encode(self.__encodeProperty(prop)), \
                          headers=copy(self.__jsonheader), \
                          verify=False, \
                          auth=self.__auth).raise_for_status()
        elif 'originalTagName' in kwds and 'tag' in kwds: 
            tag = kwds['tag']
            tagName = kwds['originalTagName'].strip()
            requests.post(self.__baseURL + self.__tagsResource + '/' + tagName, \
                          data=JSONEncoder().encode(self.__encodeTag(tag)), \
                          headers=copy(self.__jsonheader), \
                          verify=False, \
                          auth=self.__auth).raise_for_status()
        else:
            raise Exception, ' unkown keys'

#===============================================================================
# Methods for encoding decoding will be make private
#===============================================================================
    @classmethod
    def __decodeChannels(cls, body):
        '''
        decode the representation of a list of channels to a list of Channel objects 
        '''
        if not body[u'channels']:
            return None
        channels = []
        # if List then Multiple channels are present in the body
        if isinstance(body[u'channels']['channel'], list):
            for channel in body['channels']['channel']:
                channels.append(cls.__decodeChannel(channel))
        # if Dict the single channel present in the body
        elif isinstance(body[u'channels']['channel'], dict):
            channels.append(cls.__decodeChannel(body[u'channels']['channel']))
        return channels

    @classmethod
    def __decodeChannel(self, body):
        '''
        decode the representation of a channel to the Channel object
        '''
        return Channel(body[u'@name'], body[u'@owner'], properties=self.__decodeProperties(body), tags=self.__decodeTags(body))
    
    @classmethod
    def __decodeProperties(cls, body):
        '''
        decode the representation of a list of properties to a list of Property object
        '''
        ## TODO handle the case where there is a single property dict
        if body[u'properties'] and body[u'properties']['property']:
            properties = []
            if isinstance(body[u'properties']['property'], list):                
                for validProperty in [ property for property in body[u'properties']['property'] if '@name' in property and '@owner' in property]:
                        properties.append(cls.__decodeProperty(validProperty))
            elif isinstance(body[u'properties']['property'], dict):
                properties.append(cls.__decodeProperty(body[u'properties']['property']))
            return properties
        else:
            return None
        
    @classmethod
    def __decodeProperty(cls, propertyBody):
        '''
        decode the representation of a property to a Property object
        '''
        if '@value' in propertyBody:
            return Property(propertyBody['@name'], propertyBody['@owner'], propertyBody['@value'])
        else:
            return Property(propertyBody['@name'], propertyBody['@owner'])
    
    @classmethod
    def __decodeTags(cls, body):
        '''
        decode the representation of a list of tags to a list of Tag objects
        '''
        ## TODO handle the case where there is a single tag dict
        if body[u'tags'] and body[u'tags']['tag']:
            tags = []
            if isinstance(body[u'tags']['tag'], list):
                for validTag in [ tag for tag in body[u'tags']['tag'] if '@name' in tag and '@owner' in tag]:
                    tags.append(cls.__decodeTag(validTag))
            elif isinstance(body[u'tags']['tag'], dict):
                tags.append(cls.__decodeTag(body[u'tags']['tag']))
            return tags
        else:
            return None    
    
    @classmethod
    def __decodeTag(cls, tagBody):
        '''
        decode a representation of a tag to the Tag object
        '''
        return Tag(tagBody['@name'], tagBody['@owner'])
    
    @classmethod    
    def __encodeChannels(cls, channels):
        '''
        encodes a list of Channels
        '''
        ret = {u'channels':{}}
        if len(channels) == 1:
            ret[u'channels'] = {u'channel':cls.__encodeChannel(channels[0])}
        elif len (channels) > 1:
            ret[u'channels'] = {u'channel':[]}
            for channel in channels:
                if issubclass(channel.__class__, Channel):                
                    ret[u'channels'][u'channel'].append(cls.__encodeChannel(channel))
        return ret

    @classmethod
    def __encodeChannel(cls, channel):
        '''
        encodes a single channel
        '''
        d = {}
        d['@name'] = channel.Name
        d['@owner'] = channel.Owner
        if channel.Properties:
            d['properties'] = {'property':cls.__encodeProperties(channel.Properties)}            
        if channel.Tags:
            d['tags'] = {'tag':cls.__encodeTags(channel.Tags)}
        return d
    
    @classmethod
    def __encodeProperties(cls, properties):
        '''
        encodes a list of properties
        '''
        d = []
        for validProperty in [ property for property in properties if issubclass(property.__class__, Property)]:
                d.append(cls.__encodeProperty(validProperty))
        return d
    
    @classmethod
    def __encodeProperty(cls, property, withChannels=None):
        '''
        encodes a single property
        '''
        if not withChannels:
            if property.Value or property.Value is '':
                return {'@name':str(property.Name), '@value':property.Value, '@owner':property.Owner}
            else:
                return {'@name':str(property.Name), '@owner':property.Owner}
        else:
            d = OrderedDict([('@name', str(property.Name)), ('@value', property.Value), ('@owner', property.Owner)])
            d.update(cls.__encodeChannels(withChannels))
            return d
    
    @classmethod
    def __encodeTags(cls, tags):
        '''
        encodes a list of tags
        '''
        d = []
        for validTag in [ tag for tag in tags if issubclass(tag.__class__, Tag)]:
            d.append(cls.__encodeTag(validTag))
        return d
        
    @classmethod
    def __encodeTag(cls, tag, withChannels=None):
        '''
        encodes a single tag
        '''
        if not withChannels:
            return {'@name':tag.Name, '@owner':tag.Owner}
        else:
            d = OrderedDict([('@name', tag.Name), ('@owner', tag.Owner)])
            d.update(cls.__encodeChannels(withChannels))
            return d
        


        
