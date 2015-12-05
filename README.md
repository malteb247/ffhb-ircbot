## ffhb-ircbot
A module for [sopel](https://github.com/sopel-irc/sopel) with [FreifunkBremen](https://github.com/FreifunkBremen) features.

## sample output

###.top

```
.top
[TOP] 1: borgfeld-turnhalle1 (40) 
[TOP] 2: ServiceBureau-Jugendinfo... (34) 
[TOP] 3: FreifunkLuxemburgerstr50 (24) 
[TOP] 4: hvbs06 (19) 
[TOP] 5: bunte-eiche (18) 
```

###.node *NODENAME*

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

###.status

```
.status
[STATUS] Von 415 bekannten Knoten sind 180 online (43.37%). 
[STATUS] Es sind 313 clients verbunden (~1.74 je Knoten). 
```
