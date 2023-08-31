yum -y update
yum -y install git bindutils ansible
yum -y install https://repo.ius.io/ius-release-el$(rpm -E '%{rhel}').rpm
yum -y install python3
python3 --version
mkdir /usr/local/drop
git clone https://github.com/boconnor2017/e2e-patterns.git /usr/local/e2e-patterns
systemctl start docker
systemctl status docker
curl https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/dns/resolv.conf >> /run/systemd/resolve/new-resolv.conf
rm /run/systemd/resolve/stub-resolv.conf
rm /etc/resolv.conf
cp /run/systemd/resolve/new-resolv.conf /run/systemd/resolve/stub-resolv.conf
cp /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
#systemctl restart systemd-resolved.service
