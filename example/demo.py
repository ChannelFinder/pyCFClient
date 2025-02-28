"""
This module is a demo which provides a interface to access channel finder service to get channel information.
The Channel Finder service uses a web service, and http protocol to provide EPICS channel name, and its related
properties, tags. The properties supported so far are, which is developed against NSLS II storage ring.:
    'elem_type':   element type
    'elem_name':   element name
    'length':      element length
    's_position':  s position along beam trajectory
    'ordinal':     index in simulation code (for NSLS II storage ring, tracy)
    'system':      system, for example, storage ring
    'cell':        cell information
    'girder':      girder information
    'handle':      handle, either setpoint or readback
    'symmetry':    symmetry (A or B for NSLS II storage ring, following the naming convention)



Created on Mar 14, 2011
         National Synchrotron Radiation Facility II
         Brookhaven National Laboratory
         PO Box 5000, Upton, New York, 11973-5000

@author: G. Shen
"""

from channelfinder import ChannelFinderClient

import urllib3

urllib3.disable_warnings()


def prop_demo(channel):
    """
    Demo routine to operate property

    :param channel:
    :return:
    """
    # every property has to be added first before using it.
    properties = []
    propDict = {
        "elem_type": "cf-update",
        "elem_name": "cf-update",
        "dev_name": "cf-update",
        "length": "cf-update",
        "s_position": "cf-update",
        "ordinal": "cf-update",
        "system": "cf-update",
        "cell": "cf-update",
        "girder": "cf-update",
        "handle": "cf-update",
        "symmetry": "cf-update",
        "hostName": "cf-update",
        "iocName": "cf-update",
        "pvStatus": "cf-update",
        "time": "cf-update",
        "ioctest": "cf-update",
        "iocid": "cf-update",
        "iocidtest": "cf-update",
    }

    properties1 = channel.getAllProperties()
    for prop in properties1:
        try:
            del propDict[prop["name"]]
        except KeyError:
            pass
    if len(propDict) > 0:
        for k, v in propDict.items():
            properties.append({"name": k, "owner": v})
        if len(propDict) == 1:
            channel.set(property=properties[0])
        else:
            channel.set(properties=properties)
        print(channel.getAllProperties())
    else:
        print("all properties are in database already.")


def channel_demo(channel):
    """
    Demo routine to operate channel

    :param channel:
    :return:
    """
    try:
        # the file has the following attributes:
        # index, read back, set point, phys name, len[m], s[m], type
        f = open("lat_conf_table.txt", "r")
        lines = f.readlines()
        channels = []

        for line in lines:
            if not (line.startswith("#") or line.startswith("!") or not line.strip()):
                results = line.split()
                if len(results) < 7:
                    # input file format problem
                    raise
                props = [
                    {"name": "elem_type", "value": results[6]},
                    {"name": "elem_name", "value": results[3]},
                    {"name": "length", "value": results[4]},
                    {"name": "s_position", "value": results[5]},
                    {"name": "ordinal", "value": results[0]},
                    {"name": "system", "value": "SR"},
                ]

                if results[1] != "NULL":
                    props.append({"name": "handle", "value": "readback"})
                    channels.append(
                        {"name": results[1], "owner": "cf-update", "properties": props}
                    )
                if results[2] != "NULL":
                    props.append({"name": "handle", "value": "setpoint"})
                    channels.append(
                        {"name": results[2], "owner": "cf-update", "properties": props}
                    )
        channel.set(channels=channels)
    finally:
        f.close()


def tag_demo(channel):
    """
    Demo routine to operate tag.

    :param channel:
    :return:
    """
    # set one tag
    tag = {"name": "example1", "owner": "cf-update"}
    channel.set(tag=tag)

    # set a set of tags
    tags = [
        {"name": "example2", "owner": "cf-update"},
        {"name": "example3", "owner": "cf-update"},
        {"name": "example4", "owner": "cf-update"},
        {"name": "example5", "owner": "cf-update"},
    ]
    channel.set(tags=tags)


def addtag2channel_demo(channel):
    tag = {"name": "example1", "owner": "cf-update"}

    # set a set of tags
    tags = [
        {"name": "example2", "owner": "cf-update"},
        {"name": "example3", "owner": "cf-update"},
        {"name": "example4", "owner": "cf-update"},
        {"name": "example5", "owner": "cf-update"},
    ]

    channels = channel.find(name="SR*")
    channelNames = [ch["name"] for ch in channels]

    # set a tag to many channels
    channel.set(tag=tag, channelNames=channelNames)

    # set tags to many channels
    for tag in tags:
        channel.set(tag=tag, channelNames=channelNames)


def searchchannel_demo(channel):
    """
    Demo routine to search channel names in channel finder.

    :param channel:
    :return:
    """
    channels = channel.find(name="SR*")
    print(len(channels))
    for channel in channels:
        print(channel)


if __name__ == "__main__":
    # cf = ChannelFinderClient(BaseURL='https://localhost:8181/ChannelFinder', username='channel', password='1234')
    cf = ChannelFinderClient()
    # you can use browser to view results
    # http://localhost:8080/ChannelFinder/resources/channels?~name=SR*

    tag_demo(cf)
    prop_demo(cf)
    channel_demo(cf)
    addtag2channel_demo(cf)
    searchchannel_demo(cf)
