#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import json
import sopel.module

NODELIST_URL = "http://downloads.bremen.freifunk.net/data/nodelist.json"
NODES_URL = "http://downloads.bremen.freifunk.net/data/nodes.json"


def get_json(url):
    """ Retrieve data from url and create json object

    :param url: http url that returns json
    :return: JSON object
    """
    response = urllib2.urlopen(url).read()
    # decode response text
    response_text = response.decode("utf-8")
    return json.loads(response_text)


def send_messages(bot, prefix, messages, nick=None):
    """Send messages with prefix by bot as a private message

    :param bot: Instance of bot to use
    :param prefix: the command name
    :param messages: list of messages to send
    :param nick: message receiver, if None the message goes to the channel
    """

    for m in messages:
        if nick is not None:
            bot.msg(nick, "[{}] {} \r\n".format(prefix.upper(), m))
        else:
            bot.say("[{}] {} \r\n".format(prefix.upper(), m))


@sopel.module.commands('status', 'network')
def ffhb_status(bot, trigger):
    """Send status of the FFHB network

    :param bot: bot that triggered
    :param trigger: command that triggered
    :return:
    """
    command_name = "status"
    nodes = get_json(NODELIST_URL)
    messages = []
    total_count = 0
    online_count = 0
    client_count = 0

    max_client_node_name = ""
    max_client_count = 0

    for node in nodes["nodes"]:
        if node["status"]["online"]:
            online_count += 1
        client_count += node["status"]["clients"]
        total_count += 1

        if max_client_count < node["status"]["clients"]:
            max_client_count = node["status"]["clients"]
            max_client_node_name = node["name"]

    if len(max_client_node_name) > 30:
        max_client_node_name = max_client_node_name[:27] + "..."

    messages.append("Von {} bekannten Knoten sind {} online ({}%)."
                    .format(total_count,
                            online_count,
                            round(online_count / (total_count / 100), 2)))

    messages.append("Es sind {} clients verbunden (~{} je Knoten)."
                    .format(client_count,
                            round(client_count / online_count, 2)))

    messages.append("{} ist die Node mit den meisten Clients. {} ({}%)."
                    .format(max_client_node_name,
                            max_client_count,
                            round(max_client_count / (client_count / 100), 2)))

    send_messages(bot, command_name, messages)


@sopel.module.commands('node', 'knoten')
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
    auto_update = "Auto-update AUS"
    if node_info["software"]["autoupdater"]["enabled"]:
        auto_update = "Auto-update {}".format(node_info["software"]["autoupdater"]["branch"])

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
    messages.append("Model    : " + node_info["hardware"]["model"])
    messages.append("Firmware : {} ({})".format(node_info["software"]["firmware"]["release"], auto_update))
    messages.append("http://bremen.freifunk.net/meshviewer/#!v:m;n:" + node_info["node_id"])

    send_messages(bot, command_name, [trigger.nick + ": Ich sende dir eine Privatnachricht."])
    send_messages(bot, command_name, messages, trigger.nick)
