'''
Created on Feb 11, 2011

@author: shroffk
'''

try: 
    from UserDict import UserDict
except:
    print 'importError'
    
class Dictionary(UserDict):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        UserDict.__init__(self, params);
        
    def __setitem__(self, key, item):
        UserDict.__setitem__(self, key, item)
        