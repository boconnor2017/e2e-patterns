iptables -A INPUT -i eth0 -p udp --dport 53 -j ACCEPT
sh /usr/local/e2e-patterns/dns/saveiptables.sh
iptables -L
systemctl disable systemd-resolved.service
systemctl stop systemd-resolved
sh /usr/local/e2e-patterns/dns/run-docker-compose.sh
