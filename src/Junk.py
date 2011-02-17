'''
Created on Feb 14, 2011

@author: shroffk
'''
import sys, os
import httplib2
import socks
from restful_lib import Connection
try: from json import JSONDecoder, JSONEncoder
except ImportError: from simplejson import JSONDecoder, JSONEncoder

if __name__ == '__main__':
    print sys.version_info
#    httplib2.debuglevel = 4
#    h = httplib2.Http(proxy_info = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, '192.168.1.130', 3128))
#    resp, content = h.request("http://www.google.com")
#    h.add_credentials('boss', '1234')
    h = httplib2.Http('.cache')
    resp, content = h.request('https://channelfinder.nsls2.bnl.gov:8181/ChannelFinder/resources/channels')
    jsonheader = {'content-type':'application/json', 'accept':'application/json'}
    conn = Connection('https://channelfinder.nsls2.bnl.gov:8181/ChannelFinder')
    response = conn.request_get('resources/channels', headers=jsonheader)
#    print response
    print '-----------------Multiple Channels------------------------'
    resp = conn.request_get('resources/channels?~name=Test_first:a<000>:0:*', headers=jsonheader)
    print resp[u'body']
    if (resp[u'headers']['status'] != '404'):
        j = JSONDecoder().decode(resp[u'body'])
        print j
        
    print '-----------------Single Channels------------------------'
    resp = conn.request_get('resources/channels?~name=Test_first:a<000>:0:2', headers=jsonheader)
    print resp[u'body']
    if (resp[u'headers']['status'] != '404'):
        j = JSONDecoder().decode(resp[u'body'])
        print j
        
    print '-----------------Single Channels------------------------'
    resp = conn.request_get('resources/channels/Test_first:a%3C000%3E:0:0', headers=jsonheader)
    print resp[u'body']
    if (resp[u'headers']['status'] != '404'):
        j = JSONDecoder().decode(resp[u'body'])
        print j
    
#    xmlheader = {'content-type':'application/xml','accept':'application/xml'}
#    print'--------------------------------XML------------------------------'
#    resp = conn.request_get('resources/channels?~name=Test_first:a<000>:0:*',headers=xmlheader)
#    print resp
    
    pass
