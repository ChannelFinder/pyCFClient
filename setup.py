'''
Created on Apr 4, 2011

@author: shroffk
'''

from setuptools import setup, find_packages

setup(name='channelfinder',
      version='1.0',
      description='Python ChannelFinder Client Lib',
      author='Kunal Shroff',
      author_email='shroffk@bnl.gov',
      packages=find_packages(),
      scripts=['cf-update-ioc']
     )
