from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Host
from mininet.cli import CLI
from mininet.log import setLogLevel, info, debug
from mininet.link import Link, Intf, TCLink
from mininet.topo import Topo
from mininet.util import dumpNodeConnections, isShellBuiltin
from subprocess import call, check_output
from subprocess import Popen, PIPE, STDOUT
import logging
import os
import re
import select
import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger( __name__ )

class HugeTopo(Topo):
    logger.debug("Class HugeTopo")
    CoreSwitchList = []
    AggSwitchList = []
    EdgeSwitchList = []
    HostList = []
    iNUMBER = 0
    def __init__(self):
        logger.debug("Class HugeTopo init")
        iNUMBER = 4

        self.iNUMBER = iNUMBER
        self.iCoreLayerSwitch = iNUMBER
        self.iAggLayerSwitch = iNUMBER * 2
        self.iEdgeLayerSwitch = iNUMBER * 2
        self.iHost = self.iEdgeLayerSwitch * 2


        #Init Topo
        Topo.__init__(self)

    def createTopo(self):
        logger.debug("Start create Core Layer Swich")
        self.createCoreLayerSwitch(self.iCoreLayerSwitch)
        logger.debug("Start create Agg Layer Swich ")
        self.createAggLayerSwitch(self.iAggLayerSwitch)
        logger.debug("Start create Edge Layer Swich ")
        self.createEdgeLayerSwitch(self.iEdgeLayerSwitch)
        logger.debug("Start create Host")
        self.createHost(self.iHost)

    """
    Create Switch and Host
    """

    def createCoreLayerSwitch(self, NUMBER):
        logger.debug("Create Core Layer")
        for x in range(1, NUMBER+1):
            PREFIX = "100"
            if x >= int(10):
                PREFIX = "10"
            self.CoreSwitchList.append(self.addSwitch(PREFIX + str(x)))

    def createAggLayerSwitch(self, NUMBER):
        logger.debug( "Create Agg Layer")
        for x in range(1, NUMBER+1):
            PREFIX = "200"
            if x >= int(10):
                PREFIX = "20"
            self.AggSwitchList.append(self.addSwitch(PREFIX + str(x)))

    def createEdgeLayerSwitch(self, NUMBER):
        logger.debug("Create Edge Layer")
        for x in range(1, NUMBER+1):
            PREFIX = "300"
            if x >= int(10):
                PREFIX = "30"
            self.EdgeSwitchList.append(self.addSwitch(PREFIX + str(x)))

    def createHost(self, NUMBER):
        logger.debug("Create Host")
        for x in range(1, NUMBER+1):
            PREFIX = "800"
            if x >= int(10):
                PREFIX = "80"
            self.HostList.append(self.addHost(PREFIX + str(x), ip='10.0.0.%s'  %                                                                             (x+11), cls=DockerHost ))

    """
    Create Link
    """
    def createLink(self):
        logger.debug("Create Core to Agg")
        for x in range(0, self.iAggLayerSwitch, 2):
            self.addLink(self.CoreSwitchList[0], self.AggSwitchList[x], bw=1000,                                                                              )#loss=5)
            self.addLink(self.CoreSwitchList[1], self.AggSwitchList[x], bw=1000,                                                                              )#loss=5)
        for x in range(1, self.iAggLayerSwitch, 2):
            self.addLink(self.CoreSwitchList[2], self.AggSwitchList[x], bw=1000,                                                                              )#loss=5)
            self.addLink(self.CoreSwitchList[3], self.AggSwitchList[x], bw=1000,                                                                              )#loss=5)

        logger.debug("Create Agg to Edge")
        for x in range(0, self.iAggLayerSwitch, 2):
            self.addLink(self.AggSwitchList[x], self.EdgeSwitchList[x], bw=100)
            self.addLink(self.AggSwitchList[x], self.EdgeSwitchList[x+1], bw=100                                                                             )
            self.addLink(self.AggSwitchList[x+1], self.EdgeSwitchList[x], bw=100                                                                             )
            self.addLink(self.AggSwitchList[x+1], self.EdgeSwitchList[x+1], bw=1                                                                             00)

        logger.debug("Create Edge to Host")
        for x in range(0, self.iEdgeLayerSwitch):
            ## limit = 2 * x + 1
            self.addLink(self.EdgeSwitchList[x], self.HostList[2 * x])
            self.addLink(self.EdgeSwitchList[x], self.HostList[2 * x + 1])

def enableSTP():
    """
    //HATE: Dirty Code
    """
    for x in range(1,5):
        cmd = "ovs-vsctl set Bridge %s stp_enable=true" % ("100" + str(x))
        os.system(cmd)
        print cmd

    for x in range(1, 9):
        cmd = "ovs-vsctl set Bridge %s stp_enable=true" % ("200" + str(x))
        os.system(cmd)
        print cmd
        cmd = "ovs-vsctl set Bridge %s stp_enable=true" % ("300" + str(x))
        os.system(cmd)
        print cmd

def iperfTest(net, topo):
    logger.debug("Start iperfTEST")
    h1000, h1015, h1016 = net.get(topo.HostList[0], topo.HostList[14], topo.Host                                                                             List[15])

    #iperf Server
    h1000.popen('iperf -s -u -i 1 > iperf_server_differentPod_result', shell=Tru                                                                             e)

    #iperf Server
    h1015.popen('iperf -s -u -i 1 > iperf_server_samePod_result', shell=True)

    #iperf Client
    h1016.cmdPrint('iperf -c ' + h1000.IP() + ' -u -t 10 -i 1 -b 100m')
    h1016.cmdPrint('iperf -c ' + h1015.IP() + ' -u -t 10 -i 1 -b 100m')

def pingTest(net):
    logger.debug("Start Test all network")
    net.pingAll()

def createTopo():
    logging.debug("LV1 Create HugeTopo")
    topo = HugeTopo()
    topo.createTopo()
    topo.createLink()

    logging.debug("LV1 Start Mininet")
    CONTROLLER_IP = "127.0.0.1"
    CONTROLLER_PORT = 6633
    net = Mininet(topo=topo, link=TCLink, controller=None, autoSetMacs = True)
    net.addController( 'controller',controller=RemoteController,ip=CONTROLLER_IP                                                                             ,port=CONTROLLER_PORT)
    net.start()

    logger.debug("LV1 dumpNode")
    enableSTP()
    dumpNodeConnections(net.hosts)

    logger.debug("Sleeping before pingTest");
    #time.sleep(30);
    pingTest(net)
    #time.sleep(30);
    #iperfTest(net, topo)


    CLI(net)

class DockerHost( Host ):

    "Docker host"

    def __init__( self, name, image='hadoop1:latest', dargs=None, startString=No                                                                             ne, **kwargs ):
        self.image = image
        self.dargs = dargs
        if startString is None:
            self.startString = "/bin/bash"
            self.dargs = "-ti"
        else:
            self.startString = startString
        Host.__init__( self, name, **kwargs )

    #def cmd( self, *args, **kwargs ):
    #    print "cmd sending "+str(args)
    #    ret=Host.cmd(self, *args, **kwargs )
    #    print ret
    #    return ret

    def sendCmd( self, *args, **kwargs ):
        assert not self.waiting
        printPid = kwargs.get( 'printPid', True )
        # Allow sendCmd( [ list ] )
        if len( args ) == 1 and type( args[ 0 ] ) is list:
            cmd = args[ 0 ]
        # Allow sendCmd( cmd, arg1, arg2... )
        elif len( args ) > 0:
            cmd = args
        # Convert to string
        if not isinstance( cmd, str ):
            cmd = ' '.join( [ str( c ) for c in cmd ] )
        if not re.search( r'\w', cmd ):
            # Replace empty commands with something harmless
            cmd = 'echo -n'
        self.lastCmd = cmd
        printPid = printPid and not isShellBuiltin( cmd )
        if len( cmd ) > 0 and cmd[ -1 ] == '&':
            # print ^A{pid}\n{sentinel}
            cmd += ' printf "\\001%d\n\\177" $! \n'
        else:
            # print sentinel
            cmd += '; printf "\\177"'
        self.write( cmd + '\n' )
        self.lastPid = None
        self.waiting = True

    def popen( self, *args, **kwargs ):
        # Tell mnexec to execute command in our cgroup
        mncmd = [ 'docker', 'attach', "mininet-"+self.name ]
        return Host.popen( self, *args, mncmd=mncmd, **kwargs )

    def terminate( self ):
        "Send kill signal to Node and clean up after it."
        if self.shell:
            call(["docker stop mininet-"+self.name], shell=True)
        self.cleanup()

    def startShell( self ):
        "Start a shell process for running commands"
        if self.shell:
            error( "%s: shell is already running" )
            return
        # Remove any old container with this name
        print "Removing any old host still running"
        call(["docker stop mininet-"+self.name], shell=True)
        call(["docker rm mininet-"+self.name], shell=True)

        # Create run command
        print "Start Docker Host"
        cmd = ["docker","run","--privileged","-h",self.name ,"--name=mininet-"+s                                                                             elf.name]
        if self.dargs is not None:
            cmd.extend([self.dargs])
        cmd.extend(["--net='none'",self.image,self.startString])

        self.shell = Popen( cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_f                                                                             ds=True )
        self.stdin = self.shell.stdin
        self.stdout = self.shell.stdout
        self.pid = self.shell.pid
        self.pollOut = select.poll()
        self.pollOut.register( self.stdout )
        # Maintain mapping between file descriptors and nodes
        # This is useful for monitoring multiple nodes
        # using select.poll()
        self.outToNode[ self.stdout.fileno() ] = self
        self.inToNode[ self.stdin.fileno() ] = self
        self.execed = False
        self.lastCmd = None
        self.lastPid = None
        self.readbuf = ''
        self.waiting = False

        # I need the PID, but I need to wait for it to start.
        # TODO, make a loop check
        call("sleep 1", shell=True)
        pid_cmd = ["docker","inspect","--format='{{ .State.Pid }}'","mininet-"+s                                                                             elf.name]
        pidp = Popen( pid_cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds                                                                             =False )
        ps_out = pidp.stdout.readlines()
        self.pid = int(ps_out[0])


if __name__ == '__main__':
    setLogLevel('info')
    if os.getuid() != 0:
        logger.debug("You are NOT root")
    elif os.getuid() == 0:
        createTopo()
