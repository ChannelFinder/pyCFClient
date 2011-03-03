'''
Created on Feb 15, 2011

@author: shroffk
'''
from lib.restful_lib import Connection
try: from json import JSONDecoder, JSONEncoder
except ImportError: from simplejson import JSONDecoder, JSONEncoder
from Channel import Channel, Property, Tag
import time

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
        tag = single Tag obj
        tags = list of Tag obj
        '''
        if len(kwds) != 1:
            raise Exception, 'Incorrect usage:'
        if not self.connection:
            raise Exception, 'Connection not created'
        if 'channel' in kwds :
            ch = kwds['channel']
#            print JSONEncoder().encode(self.encodeChannel(ch))
#            print self.__channelsResource + '/' + ch.Name
#            b = '{"channels": {"channel": {"@name": "pyChannelName", "@owner": "pyChannelOwner"}}}'
#            response = self.connection.request_put(self.__channelsResource + '/' + ch.Name, body=JSONEncoder().encode(self.encodeChannels([ch])), headers=self.__jsonheader)
            response = self.connection.request_put(self.__channelsResource + '/' + ch.Name, \
                                                   body=JSONEncoder().encode(self.encodeChannel(ch)), \
                                                   headers=self.__jsonheader)
#            print response
            self.__checkResponseState(response)
            pass
        elif 'channels' in kwds :
            print JSONEncoder().encode(self.encodeChannels(kwds['channels']))
            response = self.connection.request_post(self.__channelsResource, \
                                                   body=JSONEncoder().encode(self.encodeChannels(kwds['channels'])), \
                                                   headers=self.__jsonheader)
            self.__checkResponseState(response)
            pass
        elif 'tag' in kwds:
#            print self.__tagsResource + '/' + kwds['tag'].Name
#            print JSONEncoder().encode(self.encodeTag(kwds['tag']))
            response = self.connection.request_put(self.__tagsResource + '/' + kwds['tag'].Name, \
                                                   body=JSONEncoder().encode(self.encodeTag(kwds['tag'])), \
                                                   headers=self.__jsonheader)
#            print response
            self.__checkResponseState(response)
        elif 'tags' in kwds:
#            print JSONEncoder().encode({'tags':{'tag':self.encodeTags(kwds['tags'])}})
            response = self.connection.request_post(self.__tagsResource, \
                                                    body=JSONEncoder().encode({'tags':{'tag':self.encodeTags(kwds['tags'])}}), \
                                                    headers=self.__jsonheader)
            self.__checkResponseState(response)
        elif 'property' in kwds:
            response = self.connection.request_put(self.__propertiesResource + '/' + kwds['property'].Name, \
                                                   body=JSONEncoder().encode(self.encodeProperty(kwds['property'])) , \
                                                   headers=self.__jsonheader)
            self.__checkResponseState(response)
        elif 'properties' in kwds:
            response = self.connection.request_post(self.__propertiesResource, \
                                                    body=JSONEncoder().encode({'properties':\
                                                                               {'property':\
                                                                                self.encodeProperties(kwds['properties'])}}) , \
                                                    headers=self.__jsonheader)
            self.__checkResponseState(response)                                
        else:
            raise Exception, 'Incorrect Usage: unknow key'   
        pass
    
    def __checkResponseState(self, r):
        '''
        simply checks the return status of the http response
        if the return status us 404 it returns None
        '''
        if r[u'headers']['status'] == '404':
            return None        
        elif not int(r[u'headers']['status']) <= 206:
                raise Exception, 'HTTP Error status: ' + r[u'headers']['status'] + r[u'body']
        return r
    
    def find(self, **kwds):
        '''
        Method allows you to query for a channel/s based on name, properties, tags
        name = channelNamePattern
        propertyName = propertyValuePattern
        tag = tagNamePattern
        
        special pattern matching char 
        * for multiple char
        ? for single char
        
        To query for the existance of a tag or property use findTag and findProperty.
                
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
        
    def findTag(self, tagName):
        '''
        Searches for the _exact_ tagName and returns a single Tag object if found
        '''
        url = self.__tagsResource + '/' + tagName
        r = self.connection.request_get(url, headers=self.__jsonheader)
#        JSONDecoder().decode(r[u'body'])
#        print r
        if self.__checkResponseState(r):
            return self.decodeTag(JSONDecoder().decode(r[u'body']))
        else:
            return None
    
    def findProperty(self, propertyName):
        '''
        Searches for the _exact_ propertyName and return a single Property object if found
        '''
        url = self.__propertiesResource + '/' + propertyName
        r = self.connection.request_get(url, headers=self.__jsonheader)
        print r
        if self.__checkResponseState(r):
            return self.decodeProperty(JSONDecoder().decode(r[u'body']))
        else:
            return None
        
        
    def getAllTags(self):
        '''
        return a list of all the Tags present - even the ones not associated w/t any channel
        '''
        url = self.__tagsResource
        r = self.connection.request_get(url, headers=self.__jsonheader)
        #------------------------------------------------------------------------------ 
        # this is a hack to solve the 505 problem
        #------------------------------------------------------------------------------ 
        if r[u'headers']['status'] == '505':
            r = self.connection.request_get(url, headers=self.__jsonheader)
        if self.__checkResponseState(r):
            return self.decodeTags(JSONDecoder().decode(r[u'body']))
    
    def getAllProperties(self):
        '''
        return a list of all the Properties present - even the ones not associated w/t any channel
        '''
        url = self.__propertiesResource
        r = self.connection.request_get(url, headers=self.__jsonheader)
        #------------------------------------------------------------------------------ 
        # this is a hack to solve the 505 problem
        #------------------------------------------------------------------------------ 
        if r[u'headers']['status'] == '505':
            r = self.connection.request_get(url, headers=self.__jsonheader)
        if self.__checkResponseState(r):
            return self.decodeProperties(JSONDecoder().decode(r[u'body']))
        
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
        if 'channelName' in kwds:
            url = self.__channelsResource + '/' + kwds['channelName']
            response = self.connection.request_delete(url, headers=self.__jsonheader)
            #------------------------------------------------------------------------------ 
            # this is a hack to solve the 505 problem
            #------------------------------------------------------------------------------ 
            if response[u'headers']['status'] == '505':
                response = self.connection.request_delete(url, headers=self.__jsonheader)      
            self.__checkResponseState(response)
            pass
        elif 'tagName' in kwds:
            url = self.__tagsResource + '/' + kwds['tagName']
            response = self.connection.request_delete(url, headers=self.__jsonheader)
            self.__checkResponseState(response)
            pass
        elif 'propertyName' in kwds:
            url = self.__propertiesResource + '/' + kwds['propertyName']
            response = self.connection.request_delete(url, headers=self.__jsonheader)
            self.__checkResponseState(response)
            pass
        else:
            raise Exception, ' unkown key use channelName, tagName or proprtyName'
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
            for validProperty in [ property for property in body[u'properties']['property'] if '@name' in property and '@owner' in property]:
                    properties.append(cls.decodeProperty(validProperty))
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
            for validTag in [ tag for tag in body[u'tags']['tag'] if '@name' in tag and '@owner' in tag]:
                tags.append(cls.decodeTag(validTag))
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
    def encodeProperty(cls, property):
        if property.Value:
            return {'@name':str(property.Name), '@value':property.Value, '@owner':property.Owner}
        else:
            return {'@name':str(property.Name), '@owner':property.Owner}
    
    @classmethod
    def encodeTags(cls, tags):
        d = []
        for validTag in [ tag for tag in tags if issubclass(tag.__class__, Tag)]:
            d.append(cls.encodeTag(validTag))
        return d
        
    @classmethod
    def encodeTag(cls, tag):
        return {'@name':tag.Name, '@owner':tag.Owner}   

        
