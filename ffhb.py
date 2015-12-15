#!/usr/bin/python2
# -*- coding: utf-8 -*-

import urllib2
import json
import sopel.module
import threading
import time
import math

NODELIST_URL = "http://downloads.bremen.freifunk.net/data/nodelist.json"
NODES_URL = "http://downloads.bremen.freifunk.net/data/nodes.json"
STATUS_OVERALL = "http://status.ffhb.tk/data/overall.json"
STATUS_URL_RELOAD_MINUTES = 5
CHANNEL = "#ffhb_gelaber"

#CACHE-DB
status_db = {}

def setup(bot):
    def monitor(bot):
        time.sleep(5)
        while True:
            ffhb_gateway(bot, None, CHANNEL)
            time.sleep(STATUS_URL_RELOAD_MINUTES * 60)

    t = threading.Thread(target=monitor, args=(bot,))
    t.start()


def get_json(url):
    """ Retrieve data from url and create json object

    :param url: http url that returns json
    :return: JSON object
    """
    response = urllib2.urlopen(url).read()
    # decode response text
    response_text = response.decode("utf-8")
    return json.loads(response_text)


def send_messages(bot, prefix, messages, to=None):
    """Send messages with prefix by bot as a private message

    :param bot: Instance of bot to use
    :param prefix: the command name
    :param messages: list of messages to send
    :param to: message receiver, if None the message goes to the channel
    """

    if to is not None and "#" not in to:
        bot.say("[{}] {} \r\n".format(prefix.upper(), to + ": Ich sende dir eine Privatnachricht."))

    for m in messages:
        if to is not None:
            bot.msg(to, "[{}] {} \r\n".format(prefix.upper(), m))
        else:
            bot.say("[{}] {} \r\n".format(prefix.upper(), m))


@sopel.module.commands('status')
def ffhb_status(bot, trigger):
    """Send status of the FFHB network

    :param bot: bot that triggered
    :param trigger: command that triggered
    :return:
    """
    command_name = "status"
    nodes = get_json(NODELIST_URL)
    messages = []
    total_count = 0.0
    online_count = 0.0
    client_count = 0.0

    for node in nodes["nodes"]:
        if node["status"]["online"]:
            online_count += 1
        client_count += node["status"]["clients"]
        total_count += 1

    messages.append("Von {} bekannten Knoten sind {} online ({}%)."
                    .format(int(total_count),
                            int(online_count),
                            round(online_count / (total_count / 100), 2)))

    messages.append("Es sind {} clients verbunden (~{} je Knoten)."
                    .format(int(client_count),
                            round(client_count / online_count, 2)))

    send_messages(bot, command_name, messages)


@sopel.module.commands('node')
def ffhb_node(bot, trigger):
    """Send status of a node

    :param bot: bot that triggered
    :param trigger: command that triggered
    """
    command_name = "node"
    search_text = trigger.group(2).lower()
    info = get_json(NODES_URL)
    messages = ["Zu diesem Knoten liegen keine Infos vor."]
    found_node = None

    for n in info["nodes"]:
        node = info["nodes"][n]
        if node["nodeinfo"]["node_id"].lower() == search_text or node["nodeinfo"]["hostname"].lower() == search_text:
            found_node = node
            break

    if found_node is None:
        send_messages(bot, command_name, messages)
        return

    messages = []
    node_info = found_node["nodeinfo"]
    auto_update = None

    # gateways have no autoupdater
    if "autoupdater" in node_info["software"]:
        if node_info["software"]["autoupdater"]["enabled"]:
            auto_update = "Auto-update {}".format(node_info["software"]["autoupdater"]["branch"])
        else:
            auto_update = "Auto-update AUS"

    messages.append("{} ({})".format(node_info["hostname"],
                                     node_info["node_id"]))

    if "owner" in found_node["nodeinfo"]:
        messages.append("Kontakt  : " + node_info["owner"]["contact"])
    else:
        messages.append("Kontakt  : n/a")

    status = "OFFLINE"

    if found_node["flags"]["online"]:
        status = "online ({} clients)".format(found_node["statistics"]["clients"])

    messages.append("Status   : " + status)

    if "hardware" in node_info:
        messages.append("Model    : " + node_info["hardware"]["model"])

    if auto_update is not None:
        messages.append("Firmware : {} ({})".format(node_info["software"]["firmware"]["release"], auto_update))
    else:
        messages.append("Firmware : {}".format(node_info["software"]["firmware"]["release"]))

    messages.append("http://bremen.freifunk.net/meshviewer/#!v:m;n:" + node_info["node_id"])

    send_messages(bot, command_name, messages)


@sopel.module.commands('top')
def ffhb_top(bot, trigger):
    command_name = "top"
    nodes_json = get_json(NODELIST_URL)
    nodes_json["nodes"].sort(key=client_count, reverse=True)
    nodes = nodes_json["nodes"]

    messages = []

    for idx in range(0, 5):
        messages.append("{}: {} ({})".format(idx + 1, shorter(nodes[idx]["name"]), nodes[idx]["status"]["clients"]))

    send_messages(bot, command_name, messages)


@sopel.module.commands('vpn')
def ffhb_gateway(bot, trigger, to=None):
    """Send status of the FFHB gateways/vpn-servers

    :param bot: bot that triggered
    :param trigger: command that triggered
    :param to: message receiver, if None the message goes to the channel
    :return:
    """
    command_name = "vpn"
    limit = 50
    # Selector
    if trigger is not None and trigger.group(2) is not None:
        vpn_server = trigger.group(2).lower()
    else:
        vpn_server = "all"
    if "." not in vpn_server:
        vpn_server += ".bremen.freifunk.net"

    services = ["ntp", "addresses", "dns", "uplink"]
    status = get_json(STATUS_OVERALL)['vpn-servers']

    messages = []
    for vpn in status:
        if vpn_server == vpn or "all" in vpn_server:
            for service in services:
                changed = False
                if vpn not in status_db:
                    status_db[vpn] = {}
                    changed = True
                if service not in status_db[vpn]:
                    status_db[vpn][service] = {"ipv4":0,"ipv6":0}


                if status[vpn][service]["ipv4"]["percent-good"] != status_db[vpn][service]["ipv4"]:
                    status_db[vpn][service]["ipv4"] = status[vpn][service]["ipv4"]["percent-good"]
                    changed = True

                if status[vpn][service]["ipv6"]["percent-good"] != status_db[vpn][service]["ipv6"]:
                    status_db[vpn][service]["ipv6"] = status[vpn][service]["ipv6"]["percent-good"]
                    changed = True

                if (status[vpn][service]["ipv4"]["percent-good"] < limit or status[vpn][service]["ipv6"]["percent-good"] < limit) and (changed or to is None):
                    messages.append("{} - {}: (IPv4: {}%, IPv6: {}%)".format(vpn,
                                                                           service,
                                                                           status[vpn][service]["ipv4"]["percent-good"],
                                                                           status[vpn][service]["ipv6"]["percent-good"]))
    if len(messages) > 0:
        if to is None:
            send_messages(bot, command_name, messages)
        else:
            send_messages(bot, command_name, messages, to)
    else:
        if to is None:
            send_messages(bot, command_name, ["Network is running without problems :)"])


def shorter(s, length=27, ext="..."):
    if len(s) > length:
        return s[:length - 3] + ext
    return s


def client_count(node):
    try:
        return int(node["status"]["clients"])
    except KeyError:
        return 0
