'''
Created on Feb 15, 2011

@author: shroffk
'''
from restful_lib import Connection
try: from json import JSONDecoder, JSONEncoder
except ImportError: from simplejson import JSONDecoder, JSONEncoder
from Channel import Channel, Property, Tag

class ChannelFinderClient(object):
    '''
    classdocs
    '''

    connection = None
    __jsonheader = {'content-type':'application/json', 'accept':'application/json'}    
    __channelsResource = 'resources/channels'
    __propertiesResources = 'resources/properties'
    __tagsResource = 'resources/tags'
 
    def __init__(self, BaseURL=None, username=None, password=None):
        '''
        Constructor
        '''
        try:
            self.connection = Connection(BaseURL, username=username, password=password)
        except Exception:
            Exception.message
            raise Exception
        resp = self.connection.request_get('/resources/channels', headers=self.__jsonheader)
        if resp[u'headers']['status'] != '200':
            print 'error status' + resp[u'headers']['status']
            raise Exception
        
    def getAllChannels(self):
        if self.connection:
            resp = self.connection.request_get('/resources/channels', headers=self.__jsonheader)
            if (resp[u'headers']['status'] != '404'):
                j = JSONDecoder().decode(resp[u'body'])
                return self.decodeChannels(j)

    def add(self, **kwds):
        '''
        method to allow various types of add operations to add one or many channels, tags or properties
        channel = single Channel obj
        channels = list of Channel obj
        '''
        if not self.connection:
            raise Exception, 'Connection not created'
        if 'channel' in kwds and not 'channels' in kwds:
            ch = kwds['channel']
            print JSONEncoder().encode(self.encodeChannel(ch))
            print self.__channelsResource + '/' + ch.Name
#            b = '{"channels": {"channel": {"@name": "pyChannelName", "@owner": "pyChannelOwner"}}}'
#            response = self.connection.request_put(self.__channelsResource + '/' + ch.Name, body=JSONEncoder().encode(self.encodeChannels([ch])), headers=self.__jsonheader)
            response = self.connection.request_put(self.__channelsResource + '/' + ch.Name, body=JSONEncoder().encode(self.encodeChannel(ch)), headers=self.__jsonheader)
            print response
            if not int(response[u'headers']['status']) <= 206:
                raise Exception, 'HTTP Error status: ' + response[u'headers']['status']
            pass
        else:
            raise Exception, 'incorrect Usage: cannot use both channel and channels'   
        pass
    
    def find(self, **kwds):
        '''
        Method allows you to query for a channel/s based on name, properties, tags
        name = channelNamePattern
        propertyName = propertyValuePattern
        tag = tagNamePattern
        
        special pattern matching char 
        * for multiple char
        ? for single char
        
        TODO figure out how python/json will handle the multivalue maps
        to specify multiple patterns simple pass a ????        
        '''
        if not self.connection:
            raise Exception, 'Connection not created'
        if not len(kwds) > 0:
            raise Exception, 'Incorrect usage: atleast one parameter must be specified'
        url = self.__channelsResource + self.createQueryURL(kwds)  
        r = self.connection.request_get(url, headers=self.__jsonheader)
        return self.decodeChannels(JSONDecoder().decode(r[u'body']))
        
    def remove(self, **kwds):
        '''
        Method to delete a channel, property, tag
        channel = name of channel to be removed
        tag = tag name of the tag to be removed from all channels
        property = property name of property to be removed from all channels
        '''
        if not self.connection:
            raise Exception, 'Connection not created'
        if not len(kwds) == 1:
            raise Exception, 'incorrect usage: Delete a single Channel/tag/property'
        if 'channel' in kwds:
            url = self.__channelsResource + '/' + kwds['channel']
            print url
            r = self.connection.request_delete(url, headers=self.__jsonheader)
            print r
            if not int(r[u'headers']['status']) <= 206:
                raise Exception, 'HTTP Error status: ' + r[u'headers']['status']
            pass
        elif 'tag' in kwds:
            pass
        else:
            pass        
        pass
    
    @classmethod
    def createQueryURL(cls, parameters):
        url = []
        for parameterKey in parameters.keys():            
            if parameterKey == 'name':
                url.append('~name=' + str(parameters['name']))
            elif parameterKey == 'tag':
                url.append('~tag=' + str(parameters['tag']))
            else:
                url.append(parameterKey + '=' + str(parameters[parameterKey]))
        return '?' + '&'.join(url)
        
    
    @classmethod
    def decodeChannels(self, body):
        '''
        '''
        if not body[u'channels']:
            return None
        channels = []
        # if List then Multiplce channels are present in the body
        if isinstance(body[u'channels']['channel'], list):
            for channel in body['channels']['channel']:
                channels.append(self.decodeChannel(channel))
        # if Dict the single channel present in the body
        elif isinstance(body[u'channels']['channel'], dict):
            channels.append(self.decodeChannel(body[u'channels']['channel']))
        return channels

    @classmethod
    def decodeChannel(self, body):
        return Channel(body[u'@name'], body[u'@owner'], properties=self.decodeProperties(body), tags=self.decodeTags(body))
    
    @classmethod
    def decodeProperties(self, body):
        ## TODO handle the case where there is a single property dict
        if body[u'properties'] and body[u'properties']['property']:
            properties = []
            for validProperty in [ property for property in body[u'properties']['property'] if '@name' in property and '@owner' in property]:
                    properties.append(Property(validProperty['@name'], validProperty['@owner'], validProperty['@value']))
            return properties
        else:
            return None
    
    @classmethod
    def decodeTags(self, body):
        ## TODO handle the case where there is a single tag dict
        if body[u'tags'] and body[u'tags']['tag']:
            tags = []
            for validTag in [ tag for tag in body[u'tags']['tag'] if '@name' in tag and '@owner' in tag]:
                tags.append(Tag(validTag['@name'], validTag['@owner']))
            return tags
        else:
            return None    
    
    @classmethod    
    def encodeChannels(self, channels):
        '''
        encodes a list of Channel
        '''
        ret = {u'channels':{}}
        if len(channels) == 1:
            ret[u'channels'] = {u'channel':self.encodeChannel(channels[0])}
        elif len (channels) > 1:
            ret[u'channels'] = {u'channel':[]}
            for channel in channels:
                if issubclass(channel.__class__, Channel):                
                    ret[u'channels'][u'channel'].append(self.encodeChannel(channel))
        return ret

    @classmethod
    def encodeChannel(cls, channel):
        d = {}
        d['@name'] = channel.Name
        d['@owner'] = channel.Owner
        if channel.Properties:
            d['properties'] = {'property':[]}
            for validProperty in [ property for property in channel.Properties if issubclass(property.__class__, Property)]:
                d['properties']['property'].append({'@name':str(validProperty.Name), '@value':validProperty.Value, '@owner':validProperty.Owner})
        if channel.Tags:
            d['tags'] = {'tag':[]}
            for validTag in [ tag for tag in channel.Tags if issubclass(tag.__class__, Tag)]:
                d['tags']['tag'].append({'@name':validTag.Name, '@owner':validTag.Owner})
        return d
        
