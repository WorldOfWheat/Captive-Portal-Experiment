#!bin/sh

INTERFACE=wlan0
WEBSERVER=192.168.0.4

iptables -t filter -F
iptables -t nat -F
iptables -t filter -X
iptables -t nat -X

iptables -P FORWARD DROP

iptables -N AUTHORIZED
iptables -A FORWARD -i $INTERFACE -j AUTHORIZED
iptables -A FORWARD -i $INTERFACE -d $WEBSERVER -j ACCEPT

iptables -t nat -A PREROUTING -i wlan0 -p udp --dport 53 -j DNAT --to-destination $WEBSERVER:53
iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE