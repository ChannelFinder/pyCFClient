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
    jsonheader = {'content-type':'application/json', 'accept':'application/json'}
 
    def __init__(self, BaseURL=None, username=None, password=None):
        '''
        Constructor
        '''
        try:
            self.connection = Connection(BaseURL)
        except Exception:
            Exception.message
            raise Exception
        resp = self.connection.request_get('/resources/channels', headers=self.jsonheader)
        if resp[u'headers']['status'] != '200':
            print 'error status' + resp[u'headers']['status']
            raise Exception
        
    def getAllChannels(self):
        if self.connection:
            resp = self.connection.request_get('/resources/channels', headers=self.jsonheader)
            if (resp[u'headers']['status'] != '404'):
                j = JSONDecoder().decode(resp[u'body'])
                return self.decodeChannels(j)

 #   def addChannel(self, **kwds):
 #       if 'name' in kwds and 'owner' in kwds:
 #           channel = Channel(kwds['name'], kwds['owner'])
 #       pass

    def addChannel(self, channel):
        if issubclass(channel.__class__, Channel):
            pass
        pass
    
    def decodeChannels(self, body):
        '''
        '''
        channels = []
        for channel in body['channels']['channel']:
            channels.append(self.decodeChannel(channel))
        return channels

    def decodeChannel(self, body):
        return Channel(body[u'@name'], body[u'@owner'], properties=self.decodeProperties(body), tags=self.decodeTags(body))
    
    def decodeProperties(self, body):
        if body[u'properties']['property']:
            properties = []
            for validProperty in [ property for property in body[u'properties']['property'] if '@name' in property and '@owner' in property]:
                    properties.append(Property(validProperty['@name'], validProperty['@value'], validProperty['@owner']))
            return properties
        else:
            return None
    
    def decodeTags(self, body):
        if body[u'tags']['tag']:
            tags = []
            for validTag in [ tag for tag in body[u'tags']['tag'] if '@name' in tag and '@owner' in tag]:
                tags.append(Tag(validTag['@name'], validTag['owner']))
            return tags
        else:
            return None    
        
    def encodeChannels(self, channels):
        '''
        '''
        ret = {'channels':{'channel':[]}}
        for channel in channels:
            if issubclass(channel.__class__, Channel):
                d = {}
                d['@name'] = channel.Name
                d['@owner'] = channel.Owner
                if channel.Properties:
                    d['properties'] = {'property':[]}
                    for validProperty in [ validProperty for property in channel.Properties if issubclass(property.__class__, Property)]:
                        d['properties']['property'].append({'@name':validProperty.Name, '@value':validProperty.Value, '@owner':validProperty.Owner})
                if channel.Tags:
                    d['tags'] = {'tag':[]}
                    for validTag in [ validTag for tag in channel.Tags if issubclass(tag.__class__, Tag)]:
                        d['tags']['tag'].append({'@name':validTag.Name, '@owner':validTag.Owner})
                ret['channels']['channel'].append(d)
        return ret
                    
                        
                
            
