#!/usr/bin/env python

import subprocess
import os
import time,threading
# first install ConfigParser by running command 'sudo apt-get install python-configparser'
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('settings.ini')

Passwrd = 'root123'

# Getting Server Ips from settings file
S1 = config.get('HostList', 'H1')
S2 = config.get('HostList', 'H2')
S3 = config.get('HostList', 'H9')
S4 = config.get('HostList', 'H10')

# Getting Client Ips from settings file
C1 = config.get('HostList', 'H8')
C2 = config.get('HostList', 'H7')
C3 = config.get('HostList', 'H16')
C4 = config.get('HostList', 'H15')

# Getting ports from settings file
P1 = config.get('Port', 'P1')
P2 = config.get('Port', 'P2')
P3 = config.get('Port', 'P3')
P4 = config.get('Port', 'P4')

# Getting data values from settings file
D1 = config.get('DataTransfer', 'D1')
D2 = config.get('DataTransfer', 'D2')
D3 = config.get('DataTransfer', 'D3')
D4 = config.get('DataTransfer', 'D4')


os.system("sshpass -p %s ssh -o StrictHostKeyChecking=no -f %s iperf -s -p %s"%(Passwrd,('hduser1@'+S1),P1))
os.system("sshpass -p %s ssh -o StrictHostKeyChecking=no -f %s iperf -s -p %s"%(Passwrd,('hduser1@'+S2),P2))
os.system("sshpass -p %s ssh -o StrictHostKeyChecking=no -f %s iperf -s -p %s"%(Passwrd,('hduser1@'+S3),P3))
os.system("sshpass -p %s ssh -o StrictHostKeyChecking=no -f %s iperf -s -p %s"%(Passwrd,('hduser1@'+S4),P4))

time.sleep(2)

def StartClient( client,server,data ,port):
	cmd = "sshpass -p %s ssh -o StrictHostKeyChecking=no -f %s iperf -c %s -n %s -p %s"%(Passwrd,client,server,data,port)
	os.system(cmd)

Clientdata = [(('hduser1@'+C1),S1,D1,P1),
			  (('hduser1@'+C2),S2,D1,P2),
			  (('hduser1@'+C3),S3,D1,P3),
			  (('hduser1@'+C4),S4,D1,P4),
		     ]


for i in Clientdata:
	t = threading.Thread( target=StartClient, args=i )
	t.start()
	t.join()
