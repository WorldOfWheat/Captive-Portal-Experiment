#!bin/sh

INTERFACE=wlan0
WEBSERVER=192.168.0.68

iptables -t filter -F
iptables -t nat -F
iptables -t filter -X
iptables -t nat -X

iptables -P FORWARD ACCEPT

iptables -N AUTHORIZED
iptables -A FORWARD -i $INTERFACE -j AUTHORIZED
iptables -A FORWARD -o $INTERFACE -j AUTHORIZED

iptables -t nat -N AUTHORIZED
iptables -t nat -A PREROUTING -i $INTERFACE -j AUTHORIZED
iptables -t nat -A PREROUTING -i wlan0 -p udp --dport 53 -j DNAT --to-destination $WEBSERVER:53
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
