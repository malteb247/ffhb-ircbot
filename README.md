## ffhb-ircbot
A module for [sopel](https://github.com/sopel-irc/sopel) with [FreifunkBremen](https://github.com/FreifunkBremen) features.

## sample output

### .top

```
.top
[TOP] 1: borgfeld-turnhalle1 (40)
[TOP] 2: ServiceBureau-Jugendinfo... (34)
[TOP] 3: FreifunkLuxemburgerstr50 (24)
[TOP] 4: hvbs06 (19)
[TOP] 5: bunte-eiche (18)
```

### .node *NODENAME*

```
.node menkar01
[NODE] menkar01 (14cc20a5dc70)
[NODE] Kontakt  : ec8or
[NODE] Status   : OFFLINE
[NODE] Model    : TP-Link TL-WR841N/ND v9
[NODE] Firmware : 2015.1.2+bremen2 (Auto-update stable)
[NODE] http://bremen.freifunk.net/meshviewer/#!v:m;n:14cc20a5dc70
```

```
.node poplar_02
[NODE] poplar_02 (c4e984b0da68)
[NODE] Kontakt  : ec8or
[NODE] Status   : online (2 clients)
[NODE] Model    : TP-Link CPE210 v1.0
[NODE] Firmware : 2015.1.2+bremen2~testing (Auto-update testing)
[NODE] http://bremen.freifunk.net/meshviewer/#!v:m;n:c4e984b0da68
```

### .status

```
.status
[STATUS] Von 415 bekannten Knoten sind 180 online (43.37%).
[STATUS] Es sind 313 clients verbunden (~1.74 je Knoten).
```

### .vpn
Commands
* status of all vpns: `.status`, `.status all`
* status of specific vpn:`.status vpn01`, `.status vpn01.bremen.freifunk.net`

Answer: It replies only not working systems (based on count/client avg)

```
[VPN] vpn06.bremen.freifunk.net - uplink: (IPv4: 1, IPv6: 1) count:2
[VPN] vpn02.bremen.freifunk.net - ntp: (IPv4: 0, IPv6: 0) count:2
[VPN] vpn02.bremen.freifunk.net - addresses: (IPv4: 0, IPv6: 2) count:2
[VPN] vpn02.bremen.freifunk.net - dns: (IPv4: 0, IPv6: 0) count:2
[VPN] vpn02.bremen.freifunk.net - uplink: (IPv4: 0, IPv6: 0) count:2
[VPN] vpn03.bremen.freifunk.net - addresses: (IPv4: 1, IPv6: 2) count:2
[VPN] vpn03.bremen.freifunk.net - uplink: (IPv4: 1, IPv6: 1) count:2
[VPN] vpn05.bremen.freifunk.net - uplink: (IPv4: 1, IPv6: 1) count:2
[VPN] vpn01.bremen.freifunk.net - uplink: (IPv4: 2, IPv6: 1) count:2
```
