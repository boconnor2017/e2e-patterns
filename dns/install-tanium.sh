iptables -A INPUT -i eth0 -p udp --dport 53 -j ACCEPT
sh saveiptables.sh
iptables -L
systemctl disable systemd-resolved.service
systemctl stop systemd-resolved
sh run-docker-compose.sh
