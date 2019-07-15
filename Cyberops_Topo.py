#!/usr/bin/python2

"""
cyberops_top.py: Sets up, configures and start Cisco CyberOps Course Topology.

The example topology creates a router and two IP subnets:

    1. 10.0.0.0/24   (R1-eth1, IP: 10.0.0.1)
    2. 172.16.0.0/24 (R1-eth2, IP: 172.16.0.1)

Subnet 1 is the internal network containing: 
    - 1 Single switch
    - 3 Three internal hosts -  H1, H2 and H3

Subnet 2 represents the external network containing:
    - 1 External host, H4

The Topology implemented by this script looks like the diagram below:
                            
                            ------       ------
                            | R1 |-------| H4 |
                            ------       ------
                              |
                              |
                            ------
                    |-------| S1 |-------|
                    |       ------       |
                    |         |          |
                    |         |          |    
                  ------    ------     ------
                  | H1 |    | H2 |     | H3 |
                  ------    ------     ------
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, NOX, OVSController
#from mininet.node import Controller
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

from mininet.node import OVSKernelSwitch, UserSwitch

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):
    "A LinuxRouter connecting three IP subnets"


    def build( self, **_opts ):
        
#        c1 = Controller( 'c1', port=6633 )
        
        defaultIP = '10.0.0.1/24' 
        router = self.addNode( 'R1', cls=LinuxRouter, ip=defaultIP )

        s1 = self.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')

        self.addLink( s1, router, intfName2='R1-eth1',
                      params2={ 'ip' : defaultIP } )

        H1 = self.addHost( 'H1', ip='10.0.0.11/24',
                           defaultRoute='via 10.0.0.1' )
        H2 = self.addHost( 'H2', ip='10.0.0.12/24',
                           defaultRoute='via 10.0.0.1' )
        H3 = self.addHost( 'H3', ip='10.0.0.13/24',
                           defaultRoute='via 10.0.0.1' )
        H4 = self.addHost( 'H4', ip='172.16.0.40/12',
                           defaultRoute='via 172.16.0.1' )

        self.addLink( H4, router, intfName2='R1-eth2',
                      params2={ 'ip' : '172.16.0.1/12' } )

        info( '*** Add links\n')
        self.addLink( H1, s1 )
        self.addLink( H2, s1 )
        self.addLink( H3, s1 )


def run():
    "Test linux router"
    info("\n\nCyberOPS Topology:\n\n          ------       ------\n          | R1 |-------| H4 |\n          ------       ------\n            |\n            |\n          ------\n  |-------| S1 |-------|\n  |       ------       |\n  |         |          |\n  |         |          |\n------    ------     ------\n| H1 |    | H2 |     | H3 |\n------    ------     ------\n\n")
    topo = NetworkTopo()
    net = Mininet( topo=topo, controller=None )  # controller is used by s1-s3
    net.start()
    info( '*** Routing Table on Router:\n' )
    print net[ 'R1' ].cmd( 'route' )
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
