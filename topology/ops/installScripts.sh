sudo apt-get install clusterssh
git clone git://github.com/mininet/mininet
cd mininet
git tag
git checkout -b 2.2.0b3
~/mininet/util/install.sh -a

git clone http://github.com/noxrepo/pox
mkdir ~/pox/ext/opennetmon
git clone https://github.com/TUDelftNAS/SDN-OpenNetMon ~/pox/ext/opennetmon

sudo apt-get install docker.io