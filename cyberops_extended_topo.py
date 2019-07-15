#!/usr/bin/python2

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():
	net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')
	info( '*** Adding controller\n' )
	info( '*** Add switches\n')
	S5 = net.addSwitch('S5', cls=OVSKernelSwitch, failMode='standalone')
	S9 = net.addSwitch('S9', cls=OVSKernelSwitch, failMode='standalone')
	S10 = net.addSwitch('S10', cls=OVSKernelSwitch, failMode='standalone')
	R1 = net.addHost('R1', cls=Node, intf='R1-eth0', ip='209.165.201.11/27')	
	R4 = net.addHost('R4', cls=Node, intf='R4-eth0', ip='209.165.201.1/27')
	R1.cmd('sysctl -w net.ipv4.ip_forward=1')
	R4.cmd('sysctl -w net.ipv4.ip_forward=1')
		
	info( '*** Add hosts\n')
	H1 = net.addHost('H1', cls=Host, ip='192.168.0.11/24', defaultRoute='via 192.168.0.1')
	H2 = net.addHost('H2', cls=Host, ip='192.168.0.12/24', defaultRoute='via 192.168.0.1')
	H3 = net.addHost('H3', cls=Host, ip='192.168.0.13/24', defaultRoute='via 192.168.0.1')
	H4 = net.addHost('H4', cls=Host, ip='192.168.0.14/24', defaultRoute='via 192.168.0.1')
	H5 = net.addHost('H5', cls=Host, ip='209.165.200.235/27', defaultRoute='via 209.165.200.225')
	H6 = net.addHost('H6', cls=Host, ip='209.165.200.236/27', defaultRoute='via 209.165.200.225')
	H7 = net.addHost('H7', cls=Host, ip='192.168.1.17/24', defaultRoute='via 192.168.1.1')
	H8 = net.addHost('H8', cls=Host, ip='192.168.1.18/24', defaultRoute='via 192.168.1.1')
	H9 = net.addHost('H9', cls=Host, ip='198.51.100.171/24', defaultRoute='via 198.51.100.1')
	H10 = net.addHost('H10', cls=Host, ip='209.165.202.133/27', defaultRoute='via 209.165.202.129')
	H11 = net.addHost('H11', cls=Host, ip='203.0.113.202/24', defaultRoute='via 203.0.113.1')
	
	info( '*** Add links\n')
	#net.addLink( R1, R4, intfName2='R4-eth0', params2={ 'ip' : '209.165.201.1/27' } )
	net.addLink( R1, R4)
	net.addLink( H9, R4, intfName2='R4-eth1', params2={ 'ip' : '198.51.100.1/24' } )
	net.addLink( H10, R4, intfName2='R4-eth2', params2={ 'ip' : '209.165.202.129/27' } )
	net.addLink( H11, R4, intfName2='R4-eth3', params2={ 'ip' : '203.0.113.1/24' } )
	net.addLink(S5, R1, intfName2='R1-eth1', params2={ 'ip' : '209.165.200.225/27' } )
	net.addLink(S9, R1, intfName2='R1-eth2', params2={ 'ip' : '192.168.0.1/24' } )
	net.addLink(S10, R1, intfName2='R1-eth3', params2={ 'ip' : '192.168.1.1/24' } )
	net.addLink(H1, S9)
	net.addLink(H2, S9)
	net.addLink(H3, S9)
	net.addLink(H4, S9)
	net.addLink(H7, S10)
	net.addLink(H8, S10)
	net.addLink(H6, S5)
	net.addLink(H5, S5)	
			
	info( '*** Starting network\n')
	net.build()
	
	info( '*** Starting controllers\n')
	for controller in net.controllers:
		controller.start()
		
	info( '*** Starting switches\n')
	net.get('S9').start([])
	net.get('S10').start([])
	net.get('S5').start([])
	
	info( '*** Add routes\n')
	R1.cmd('ip route add default via 209.165.201.1')
	R4.cmd('ip route add to 209.165.200.224/27 via 209.165.201.11')
	#R4.cmd('ip route add to 192.168.0.0/16 via 209.165.201.11')

        info( '*** Adding FW rules\n')
        R1.cmd('iptables -t nat -A POSTROUTING -o R1-eth0 -j MASQUERADE')
        R1.cmd('iptables -A FORWARD -i R1-eth0 -o R1-eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT')
        R1.cmd('iptables -A FORWARD -i R1-eth1 -o R1-eth0 -j ACCEPT')
        #R1.cmd('iptables -N LOGGING')
        #R1.cmd('iptables -A FORWARD -j LOGGING')
        #R1.cmd('iptables -A LOGGING -j LOG --log-prefix "IPTables-Dropped: " --log-level 7')
        #R1.cmd('#iptables -A LOGGING -j ULOG --ulog-prefix "IPTables-Dropped"')
        #R1.cmd('iptables -A LOGGING -j DROP')
	
	info( '*** Post configure switches and hosts\n')
	CLI(net)
	net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

