'''
Created on Feb 15, 2011

@author: shroffk
'''
import re
from channelfinder.lib.restful_lib import Connection
from copy import copy
from _conf import _conf
try: 
    from json import JSONDecoder, JSONEncoder
except ImportError: 
    from simplejson import JSONDecoder, JSONEncoder
from Channel import Channel, Property, Tag
try: 
    from collections import OrderedDict
except :
    from channelfinder.lib.myCollections import OrderedDict

    


class ChannelFinderClient(object):
    '''
    classdocs
    '''

    connection = None
    __jsonheader = {'content-type':'application/json', 'accept':'application/json'}    
    __channelsResource = 'resources/channels'
    __propertiesResource = 'resources/properties'
    __tagsResource = 'resources/tags'
 
    def __init__(self, BaseURL=None, username=None, password=None):
        '''
        Constructor
        '''
        try:            
            self.__baseURL = self.__getDefaultConfig('BaseURL', BaseURL)
            self.__userName = self.__getDefaultConfig('username', username)
            self.__password = self.__getDefaultConfig('password', password)
#            print 'creating a connection to ', self.__baseURL, self.__userName, self.__password
            self.connection = Connection(self.__baseURL, username=self.__userName, password=self.__password)
            resp = self.connection.request_get('/resources/tags', headers=copy(self.__jsonheader))
            if resp[u'headers']['status'] != '200':
                print 'error status' + resp[u'headers']['status']
        except:
            raise

    def __getDefaultConfig(self, arg, value):
        if value == None and _conf.has_option('DEFAULT', arg):
            return _conf.get('DEFAULT', arg)
        else:
            return value
        
    def getAllChannels(self):
        if self.connection:
            resp = self.connection.request_get('/resources/channels', headers=copy(self.__jsonheader))
            if (resp[u'headers']['status'] != '404'):
                j = JSONDecoder().decode(resp[u'body'])
                return self.decodeChannels(j)
#        return a None if fail
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
        >>> set(property=Property('propertyName','propertyOwner','propertyValue'))
        
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
        if not self.connection:
            raise Exception, 'Connection not created'
        if len(kwds) == 1:
            self.__hadleSingleAddParameter(**kwds)
        elif len(kwds) == 2:
            self.__handleMultipleAddParameters(**kwds)
        else:
            raise Exception, 'incorrect usage: '
    
    def __hadleSingleAddParameter(self, **kwds):
        if 'channel' in kwds :
            ch = kwds['channel']
            response = self.connection.request_put(self.__channelsResource + '/' + ch.Name, \
                                                   body=JSONEncoder().encode(self.encodeChannel(ch)), \
                                                   headers=copy(self.__jsonheader))
            self.__checkResponseState(response)
        elif 'channels' in kwds :
            response = self.connection.request_post(self.__channelsResource, \
                                                   body=JSONEncoder().encode(self.encodeChannels(kwds['channels'])), \
                                                   headers=copy(self.__jsonheader))
            self.__checkResponseState(response)
        elif 'tag' in kwds:
            response = self.connection.request_put(self.__tagsResource + '/' + kwds['tag'].Name, \
                                                   body=JSONEncoder().encode(self.encodeTag(kwds['tag'])), \
                                                   headers=copy(self.__jsonheader))
            self.__checkResponseState(response)
        elif 'tags' in kwds:
            response = self.connection.request_post(self.__tagsResource, \
                                                    body=JSONEncoder().encode({'tags':{'tag':self.encodeTags(kwds['tags'])}}), \
                                                    headers=copy(self.__jsonheader))
            self.__checkResponseState(response)
        elif 'property' in kwds:
            response = self.connection.request_put(self.__propertiesResource + '/' + kwds['property'].Name, \
                                                   body=JSONEncoder().encode(self.encodeProperty(kwds['property'])) , \
                                                   headers=copy(self.__jsonheader))
            self.__checkResponseState(response)
        elif 'properties' in kwds:
            response = self.connection.request_post(self.__propertiesResource, \
                                                    body=JSONEncoder().encode({'properties':\
                                                                               {'property':\
                                                                                self.encodeProperties(kwds['properties'])}}) , \
                                                    headers=copy(self.__jsonheader))
            self.__checkResponseState(response)                                
        else:
            raise Exception, 'Incorrect Usage: unknown key'   
    
    def __handleMultipleAddParameters(self, **kwds):
        # set a tag to a channel
        if 'tag' in kwds and 'channelName' in kwds:
            channels = [Channel(kwds['channelName'], self.__userName, tags=[kwds['tag']])]
            response = self.connection.request_put(self.__tagsResource + '/' + kwds['tag'].Name, \
                                                    body=JSONEncoder().encode(self.encodeTag(kwds['tag'], withChannels=channels)), \
                                                    headers=copy(self.__jsonheader))
            self.__checkResponseState(response)
        elif 'tag' in kwds and 'channelNames' in kwds:
            channels = []
            for eachChannel in kwds['channelNames']:
                channels.append(Channel(eachChannel, self.__userName, tags=[kwds['tag']]))
            response = self.connection.request_put(self.__tagsResource + '/' + kwds['tag'].Name, \
                                                    body=JSONEncoder().encode(self.encodeTag(kwds['tag'], withChannels=channels)), \
                                                    headers=copy(self.__jsonheader))
            self.__checkResponseState(response)
        elif 'property' in kwds and 'channelName' in kwds:
            channels = [Channel(kwds['channelName'], self.__userName, properties=[kwds['property']])]
            response = self.connection.request_put(self.__propertiesResource + '/' + kwds['property'].Name, \
                                                   body=JSONEncoder().encode(self.encodeProperty(kwds['property'], withChannels=channels)), \
                                                   headers=copy(self.__jsonheader))
            self.__checkResponseState(response)
        elif 'property' in kwds and 'channelNames' in kwds:
            channels = []
            for eachChannel in kwds['channelNames']:
                channels.append(Channel(eachChannel, self.__userName, properties=[kwds['property']]))
            try:
                response = self.connection.request_put(self.__propertiesResource + '/' + kwds['property'].Name, \
                                                       body=JSONEncoder().encode(self.encodeProperty(kwds['property'], withChannels=channels)), \
                                                       headers=copy(self.__jsonheader))
            except Exception:
                print Exception
            self.__checkResponseState(response)
        else:
            raise Exception, 'Incorrect Usage: unknown keys'
    
    def __checkResponseState(self, r):
        '''
        simply checks the return status of the http response
        '''
        if not int(r[u'headers']['status']) <= 206:
            match = re.search(r'<b>description</b>([\S\s]*?)</p>', r[u'body'])
            msg  = match.group(1)
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
        if not self.connection:
            raise Exception, 'Connection not created'
        if not len(kwds) > 0:
            raise Exception, 'Incorrect usage: atleast one parameter must be specified'
        url = self.__channelsResource
        args = []
        for key in kwds:
            if key == 'name':
                patterns = kwds[key].split(',')
                for eachPattern in patterns:
                    args.append(('~name',eachPattern))
            elif key == 'tagName':
                patterns = kwds[key].split(',')
                for eachPattern in patterns:
                    args.append(('~tag',eachPattern))
            elif key == 'property':
                for prop in kwds[key]:
                    patterns = prop[1].split(',')
                    for eachPattern in patterns:
                        args.append((prop[0],eachPattern))
            else:
                raise Exception, 'unknown find argument '+key 
#        url = self.__channelsResource + self.createQueryURL(kwds)
        r = self.connection.request_get(url, args=args, headers=copy(self.__jsonheader))
        if self.__checkResponseState(r):
            return self.decodeChannels(JSONDecoder().decode(r[u'body']))
    
    @classmethod
    def createQueryURL(cls, parameters):
        url = []
        for parameterKey in parameters.keys():            
            if parameterKey == 'name':
                url.append('~name=' + str(parameters['name']))
            elif parameterKey == 'tagName':
                url.append('~tag=' + str(parameters['tagName']))
            elif parameterKey == 'property':
                if isinstance(parameters['property'], list):
                    for prop in parameters['property']:                        
                        if len(prop) == 1:
                            url.append(str(prop[0] + '=*'))
                        else:
                            url.append(str(prop[0] + '=' + prop[1]))
                else:
                    raise Exception, 'Incorrect usage: property=[("propName","propValPattern"),("propName","propValPatter")]'                    
            else:
                raise Exception, 'Incorrect usage: unknow key ' + parameterKey
        return '?' + '&'.join(url)
            
    def findTag(self, tagName):
        '''
        Searches for the _exact_ tagName and returns a single Tag object if found
        '''
        url = self.__tagsResource + '/' + tagName
        r = self.connection.request_get(url, headers=copy(self.__jsonheader))
#        JSONDecoder().decode(r[u'body'])
#        print r
        if r[u'headers']['status'] == '404':
            return None
        elif self.__checkResponseState(r):
            return self.decodeTag(JSONDecoder().decode(r[u'body']))
        else:
            return None
               
    
    def findProperty(self, propertyName):
        '''
        Searches for the _exact_ propertyName and return a single Property object if found
        '''
        url = self.__propertiesResource + '/' + propertyName
        r = self.connection.request_get(url, headers=copy(self.__jsonheader))
        if r[u'headers']['status'] == '404':
            return None
        elif self.__checkResponseState(r):
            return self.decodeProperty(JSONDecoder().decode(r[u'body']))
        else:
            return None
        
    def getAllTags(self):
        '''
        return a list of all the Tags present - even the ones not associated w/t any channel
        '''
        url = self.__tagsResource
        r = self.connection.request_get(url, headers=copy(self.__jsonheader))       
        if self.__checkResponseState(r):
            return self.decodeTags(JSONDecoder().decode(r[u'body']))
    
    def getAllProperties(self):
        '''
        return a list of all the Properties present - even the ones not associated w/t any channel
        '''
        url = self.__propertiesResource
        r = self.connection.request_get(url, headers=copy(self.__jsonheader))
        if self.__checkResponseState(r):
            return self.decodeProperties(JSONDecoder().decode(r[u'body']))
        
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
        if not self.connection:
            raise Exception, 'Connection not created'
        if len(kwds) == 1:
            self.__handleSingleDeleteParameter(**kwds)
        elif len(kwds) == 2:
            self.__handleMultipleDeleteParameters(**kwds)
        else:
            raise Exception, 'incorrect usage: Delete a single Channel/tag/property'
    
    def __handleSingleDeleteParameter(self, **kwds):
        if 'channelName' in kwds:
            url = self.__channelsResource + '/' + kwds['channelName']
            response = self.connection.request_delete(url, headers=copy(self.__jsonheader))   
            self.__checkResponseState(response)
            pass
        elif 'tagName' in kwds:
            url = self.__tagsResource + '/' + kwds['tagName']
            response = self.connection.request_delete(url, headers=copy(self.__jsonheader))
            self.__checkResponseState(response)
            pass
        elif 'propertyName' in kwds:
            url = self.__propertiesResource + '/' + kwds['propertyName']
            response = self.connection.request_delete(url, headers=copy(self.__jsonheader))
            self.__checkResponseState(response)
            pass
        else:
            raise Exception, ' unkown key use channelName, tagName or proprtyName'
    
    def __handleMultipleDeleteParameters(self, **kwds):
        if 'tag' in kwds and 'channelName' in kwds:
            response = self.connection.request_delete(self.__tagsResource + '/' + kwds['tag'].Name + '/' + kwds['channelName'], \
                                                     headers=copy(self.__jsonheader))
            self.__checkResponseState(response)
        elif 'tag' in kwds and 'channelNames' in kwds:
            # find channels with the tag
            channelsWithTag = self.find(tagName=kwds['tag'].Name)
            # delete channels from which tag is to be removed
            channelNames = [channel.Name for channel in channelsWithTag if channel.Name not in  kwds['channelNames']]
            self.set(tag=kwds['tag'], channelNames=channelNames)
        elif 'property' in kwds and 'channelName' in kwds:
            response = self.connection.request_delete(self.__propertiesResource + '/' + kwds['property'].Name + '/' + kwds['channelName'], \
                                                      headers=copy(self.__jsonheader))
            self.__checkResponseState(response)
        elif 'property' in kwds and 'channelNames' in kwds:
            channelsWithProp = self.find(property=[(kwds['property'].Name, '*')])
            channelNames = [channel.Name for channel in channelsWithProp if channel.Name not in kwds['channelNames']]
            self.set(property=kwds['property'], channelNames=channelNames)        
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
        
        if not self.connection:
            raise Exception, 'Connection not created'
        if len(kwds) == 1:
            self.__handleSingleUpdateParameter(**kwds)
        elif len(kwds) == 2:
            self.__handleMultipleUpdateParameters(**kwds)
        else:
            raise Exception, 'incorrect usage: '
    
    def __handleSingleUpdateParameter(self, **kwds):
        if 'channel' in kwds:
            ch = kwds['channel']
            response = self.connection.request_post(self.__channelsResource + '/' + ch.Name, \
                                                    body=JSONEncoder().encode(self.encodeChannel(ch)), \
                                                    headers=copy(self.__jsonheader))
            self.__checkResponseState(response)
        elif 'property' in kwds:
            property = kwds['property']
            response = self.connection.request_post(self.__propertiesResource + '/' + property.Name, \
                                                    body=JSONEncoder().encode(self.encodeProperty(property)), \
                                                    headers=copy(self.__jsonheader))
            self.__checkResponseState(response)
        elif 'tag' in kwds:
            tag = kwds['tag']
            response = self.connection.request_post(self.__tagsResource + '/' + tag.Name, \
                                                    body=JSONEncoder().encode(self.encodeTag(tag)), \
                                                    headers=copy(self.__jsonheader))
        else:
            raise Exception, ' unkown key '
        
    def __handleMultipleUpdateParameters(self, **kwds):
        if 'tag' in kwds and 'channelName' in kwds:
            tag = kwds['tag']
            channels = [Channel(kwds['channelName'], self.__userName)]
            response = self.connection.request_post(self.__tagsResource + '/' + tag.Name, \
                                                    body=JSONEncoder().encode(self.encodeTag(tag, withChannels=channels)), \
                                                    headers=copy(self.__jsonheader))
            self.__checkResponseState(response) 
        elif 'tag' in kwds and 'channelNames' in kwds:
            tag = kwds['tag']
            channels = []
            for eachChannel in kwds['channelNames']:
                channels.append(Channel(eachChannel, self.__userName))
            response = self.connection.request_post(self.__tagsResource + '/' + tag.Name, \
                                                    body=JSONEncoder().encode(self.encodeTag(tag, withChannels=channels)), \
                                                    headers=copy(self.__jsonheader))
            self.__checkResponseState(response)
        elif 'property' in kwds and 'channelName' in kwds:
            property = kwds['property']
            channels = [Channel(kwds['channelName'], self.__userName, properties=[property])]
            response = self.connection.request_post(self.__propertiesResource + '/' + property.Name, \
                                                    body=JSONEncoder().encode(self.encodeProperty(property, withChannels=channels)),\
                                                    headers=copy(self.__jsonheader))
            self.__checkResponseState(response)
        elif 'property' in kwds and 'channelNames' in kwds:
            property = kwds['property']
            channels = []
            for eachChannel in kwds['channelNames']:
                channels.append(Channel(eachChannel, self.__userName, properties=[property]))
            response = self.connection.request_post(self.__propertiesResource + '/' + property.Name, \
                                                    body=JSONEncoder().encode(self.encodeProperty(property, withChannels=channels)),\
                                                    headers=copy(self.__jsonheader))    
            self.__checkResponseState(response)                         
        elif 'originalChannelName' in kwds and 'channel' in kwds:
            ch = kwds['channel']
            channelName = kwds['originalChannelName']
            response = self.connection.request_post(self.__channelsResource + '/' + channelName, \
                                                    body=JSONEncoder().encode(self.encodeChannel(ch)) , \
                                                    headers=copy(self.__jsonheader))                
            self.__checkResponseState(response)
        elif 'originalPropertyName' in kwds and 'property' in kwds:
            prop = kwds['property']
            propName = kwds['originalPropertyName']
            response = self.connection.request_post(self.__propertiesResource + '/' + propName, \
                                                    body=JSONEncoder().encode(self.encodeProperty(prop)), \
                                                    headers=copy(self.__jsonheader))
            self.__checkResponseState(response)
        elif 'originalTagName' in kwds and 'tag' in kwds: 
            tag = kwds['tag']
            tagName = kwds['originalTagName']
            response = self.connection.request_post(self.__tagsResource + '/' + tagName, \
                                                    body=JSONEncoder().encode(self.encodeTag(tag)), \
                                                    headers=copy(self.__jsonheader))
            print response
            self.__checkResponseState(response)
        else:
            raise Exception, ' unkown keys'

#===============================================================================
# Methods for encoding decoding will be make private
#===============================================================================
    @classmethod
    def decodeChannels(cls, body):
        '''
        '''
        if not body[u'channels']:
            return None
        channels = []
        # if List then Multiplce channels are present in the body
        if isinstance(body[u'channels']['channel'], list):
            for channel in body['channels']['channel']:
                channels.append(cls.decodeChannel(channel))
        # if Dict the single channel present in the body
        elif isinstance(body[u'channels']['channel'], dict):
            channels.append(cls.decodeChannel(body[u'channels']['channel']))
        return channels

    @classmethod
    def decodeChannel(self, body):
        return Channel(body[u'@name'], body[u'@owner'], properties=self.decodeProperties(body), tags=self.decodeTags(body))
    
    @classmethod
    def decodeProperties(cls, body):
        ## TODO handle the case where there is a single property dict
        if body[u'properties'] and body[u'properties']['property']:
            properties = []
            if isinstance(body[u'properties']['property'], list):                
                for validProperty in [ property for property in body[u'properties']['property'] if '@name' in property and '@owner' in property]:
                        properties.append(cls.decodeProperty(validProperty))
            elif isinstance(body[u'properties']['property'], dict):
                properties.append(cls.decodeProperty(body[u'properties']['property']))
            return properties
        else:
            return None
        
    @classmethod
    def decodeProperty(cls, propertyBody):
        if '@value' in propertyBody:
            return Property(propertyBody['@name'], propertyBody['@owner'], propertyBody['@value'])
        else:
            return Property(propertyBody['@name'], propertyBody['@owner'])
    
    @classmethod
    def decodeTags(cls, body):
        ## TODO handle the case where there is a single tag dict
        if body[u'tags'] and body[u'tags']['tag']:
            tags = []
            if isinstance(body[u'tags']['tag'], list):
                for validTag in [ tag for tag in body[u'tags']['tag'] if '@name' in tag and '@owner' in tag]:
                    tags.append(cls.decodeTag(validTag))
            elif isinstance(body[u'tags']['tag'], dict):
                tags.append(cls.decodeTag(body[u'tags']['tag']))
            return tags
        else:
            return None    
    
    @classmethod
    def decodeTag(cls, tagBody):
        return Tag(tagBody['@name'], tagBody['@owner'])
    
    @classmethod    
    def encodeChannels(cls, channels):
        '''
        encodes a list of Channel
        '''
        ret = {u'channels':{}}
        if len(channels) == 1:
            ret[u'channels'] = {u'channel':cls.encodeChannel(channels[0])}
        elif len (channels) > 1:
            ret[u'channels'] = {u'channel':[]}
            for channel in channels:
                if issubclass(channel.__class__, Channel):                
                    ret[u'channels'][u'channel'].append(cls.encodeChannel(channel))
        return ret

    @classmethod
    def encodeChannel(cls, channel):
        d = {}
        d['@name'] = channel.Name
        d['@owner'] = channel.Owner
        if channel.Properties:
            d['properties'] = {'property':cls.encodeProperties(channel.Properties)}            
        if channel.Tags:
            d['tags'] = {'tag':cls.encodeTags(channel.Tags)}
        return d
    
    @classmethod
    def encodeProperties(cls, properties):
        d = []
        for validProperty in [ property for property in properties if issubclass(property.__class__, Property)]:
                d.append(cls.encodeProperty(validProperty))
        return d
    
    @classmethod
    def encodeProperty(cls, property, withChannels=None):
        if not withChannels:
            if property.Value:
                return {'@name':str(property.Name), '@value':property.Value, '@owner':property.Owner}
            else:
                return {'@name':str(property.Name), '@owner':property.Owner}
        else:
            d = OrderedDict([('@name', str(property.Name)), ('@value', property.Value), ('@owner', property.Owner)])
            d.update(cls.encodeChannels(withChannels))
            return d
    
    @classmethod
    def encodeTags(cls, tags):
        d = []
        for validTag in [ tag for tag in tags if issubclass(tag.__class__, Tag)]:
            d.append(cls.encodeTag(validTag))
        return d
        
    @classmethod
    def encodeTag(cls, tag, withChannels=None):
        if not withChannels:
            return {'@name':tag.Name, '@owner':tag.Owner}
        else:
            d = OrderedDict([('@name', tag.Name), ('@owner', tag.Owner)])
            d.update(cls.encodeChannels(withChannels))
            return d
        


        
