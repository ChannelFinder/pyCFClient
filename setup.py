'''
Created on Apr 4, 2011

@author: shroffk
'''

from setuptools import setup

from os import path

cur_dir = path.abspath(path.dirname(__file__))

with open(path.join(cur_dir, 'requirements.txt')) as f:
    requirements = f.read().split()

extras_require = {
    'PySide': ['PySide'],
    'pyepics': ['pyepics'],
    'perf': ['psutil'],
    'testing-ioc': ['pcaspy'],
    'test': ['codecov', 'pytest', 'pytest-cov', 'coverage', 'coveralls', 'pcaspy']
}

setup(
    name='channelfinder',
    version='3.0.0',
    description='Python ChannelFinder Client Lib',
    author='Kunal Shroff',
    author_email='shroffk@bnl.gov',
    url='http://channelfinder.sourceforge.net/channelfinderpy',
    scripts=['cf-update-ioc', 'cf-monitor-test'],
    packages=['channelfinder', 'channelfinder/util', 'channelfinder/cfUpdate', 'test'],
    long_description="""\
    Python ChannelFinder Client Lib
    """,
    license='GPL',
    install_requires=requirements,
)
