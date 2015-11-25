from urllib.request import urlopen
import json
import sopel.module
import time


def get_json(url):
    url = url
    r = urlopen(url)
    p = r.readall()
    text = p.decode("utf-8")
    return json.loads(text)


def say(bot, prefix, content):
    msg = "[{}] {}".format(prefix.upper(), content)
    bot.say(msg)
    print(msg)


@sopel.module.commands('status', 'network')
def ffhb_status(bot, trigger):
    command_name = "status"
    nodes = get_json("http://downloads.bremen.freifunk.net/data/nodelist.json")

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

    msg = "Es sind {} Knoten bekannt. {} sind online ({}%).".format(total_count,
                                                                    online_count,
                                                                    round(online_count / (total_count / 100), 2))
    say(bot, command_name, msg)

    msg = "Es sind {} clients verbunden, {} je Knoten.".format(client_count,
                                                               round(client_count / online_count, 2))
    say(bot, command_name, msg)

    msg = "{} ist die Node mit den meisten Clients. {} ({}%).".format(max_client_node_name,
                                                                      max_client_count,
                                                                      round(max_client_count / (client_count / 100), 2))
    say(bot, command_name, msg)


@sopel.module.commands('node', 'knoten')
def ffhb_node(bot, trigger):
    command_name = "node"
    search_text = trigger.split(' ')[1].lower()
    info = get_json("http://downloads.bremen.freifunk.net/data/nodes.json")

    found_node = None

    for n in info["nodes"]:
        node = info["nodes"][n]
        if node["nodeinfo"]["node_id"].lower() == search_text or node["nodeinfo"]["hostname"].lower() == search_text:
            found_node = node
            break

    if found_node is None:
        say(bot, "NODE", "Zu diesem Knoten liegen keine Infos vor.")
        return

    node_info = found_node["nodeinfo"]
    auto_update ="Auto-update AUS"
    if node_info["software"]["autoupdater"]["enabled"]:
        auto_update = "Auto-update {}".format(node_info["software"]["autoupdater"]["branch"])

    say(bot, "NODE", "{} ({})".format(node_info["hostname"],
                                      node_info["node_id"]))

    if "owner" in found_node["nodeinfo"]:
        say(bot, command_name, "Kontakt  : " + node_info["owner"]["contact"])
    else:
        say(bot, command_name, "Kontakt  : n/a")

    status = "OFFLINE"

    if found_node["flags"]["online"]:
        status = "online ({} clients)".format(found_node["statistics"]["clients"])

    say(bot, command_name, "Status   : " + status)
    say(bot, command_name, "Model    : " + node_info["hardware"]["model"])
    say(bot, command_name, "Firmware : {} ({})".format(node_info["software"]["firmware"]["release"], auto_update))
    say(bot, command_name, "http://bremen.freifunk.net/meshviewer/#!v:m;n:" + node_info["node_id"])


@sopel.module.commands('faq', 'answers', 'antworten')
def faq(bot, trigger):
    say(bot, "FAQ", "Antworten auf häufig gestellte Fragen findest du hier: http://bremen.freifunk.net/faq.html")
