#!/usr/bin/python
"""
Created on Mar 19, 2012

A python script to ensure that the cf-update-ioc is working correctly.
The script requires the setup of two files
e.g.
>cat nagios01.host01.dbl
>test:cf-update-daemon{test}

>cat nagios02.host02.dbl
>test:cf-update-daemon{test}

The script will touch each file, with a short delay and will check that
Channelfinder has been appropriately updated.

python cf-monitor-test /complete/path/to/daemon/dir -i initialFile -f finalFile

@author: shroffk
"""

import sys
import os
import re
from optparse import OptionParser
from time import sleep

from channelfinder import ChannelFinderClient

SEVR = {0: "OK     ", 1: "Minor  ", 2: "Major  "}


def main():
    usage = "usage: %prog -i initial-file -f final-file directory "
    parser = OptionParser(usage=usage)
    parser.add_option(
        "-i",
        "--initial-file",
        action="store",
        type="string",
        dest="initialFile",
        help="the initial-file",
    )
    parser.add_option(
        "-f",
        "--final-file",
        action="store",
        type="string",
        dest="finalFile",
        help="the --final-file",
    )
    opts, args = parser.parse_args()
    if args == None or len(args) == 0:
        parser.error("Please specify a directory")
    if not opts.initialFile:
        parser.error("Please specify a initial test files")
    if not opts.finalFile:
        parser.error("Please specify a final test files")
    mainRun(opts, args)


def mainRun(opts, args):
    for directory in args:
        initialFile = os.path.normpath(directory + "/" + opts.initialFile)
        iHostName, iIocName = getArgsFromFilename(initialFile)
        finalFile = os.path.normpath(directory + "/" + opts.finalFile)
        fHostName, fIocName = getArgsFromFilename(finalFile)
        if getPVNames(initialFile) != getPVNames(finalFile):
            sys.exit(1)
        pvNames = getPVNames(initialFile)
        if len(pvNames) == 0:
            sys.exit(1)
        """
        Touch the initial file and check channelfinder
        """
        touch(initialFile)
        sleep(2)
        check(pvNames, iHostName, iIocName)
        """
        Touch the final file and check channelfinder
        """
        touch(finalFile)
        sleep(2)
        check(pvNames, fHostName, fIocName)
        sys.exit


def check(pvNames, hostName, iocName):
    try:
        client = ChannelFinderClient()
    except:
        raise RuntimeError("Unable to create a valid webResourceClient")
    channels = client.find(property=[("hostName", hostName), ("iocName", iocName)])
    if channels and len(pvNames) == len(channels):
        for channel in channels:
            if channel.Name not in pvNames:
                sys.exit(2)
    else:
        sys.exit(2)


def touch(fname, times=None):
    with open(fname, "a"):
        os.utime(fname, times)


def getArgsFromFilename(completeFilePath):
    fileName = os.path.split(os.path.normpath(completeFilePath))[1]
    pattern4Hostname = "(\S+?)\.\S+"
    match = re.search(pattern4Hostname, fileName)
    if match:
        hostName = match.group(1)
    else:
        hostName = None
    pattern4Iocname = "\S+?\.(\S+?)\.\S+"
    match = re.search(pattern4Iocname, fileName)
    if match:
        iocName = match.group(1)
    else:
        iocName = None
    return hostName, iocName


def getPVNames(completeFilePath, pattern=None):
    try:
        f = open(completeFilePath)
        pvNames = f.read().splitlines()
        pvNames = map(lambda x: x.strip(), pvNames)
        pvNames = filter(lambda x: len(x) > 0, pvNames)
        if pattern:
            pvNames = [
                re.match(pattern, pvName).group()
                for pvName in pvNames
                if re.match(pattern, pvName)
            ]
        return pvNames
    except IOError:
        return None
    finally:
        f.close()


if __name__ == "__main__":
    main()
    pass
