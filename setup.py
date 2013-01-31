'''
Created on Apr 4, 2011

@author: shroffk
'''

from distutils.core import setup

setup(name='channelfinder',
      version='2.0.0',
      packages=['channelfinder'],
      description='Python ChannelFinder Client Lib',
      author='Kunal Shroff',
      author_email='shroffk@bnl.gov',
      scripts=['cf-update-ioc', 'cf-monitor-test']
     )
