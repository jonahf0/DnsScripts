from ipaddress import ip_network
from socket import gethostbyaddr, herror
from itertools import repeat
from functools import reduce
from argparse import ArgumentParser
from dns import resolver
import threading as th
from queue import Queue

def rl_with_server_closure(server):

    cl_resolver = resolver.Resolver()

    cl_resolver.nameservers = [server]

    def func_to_return(host, out=False):
        try:
            response = cl_resolver.resolve_address(host)

            hostname = response.rrset[0].to_text()
            
            if out:
                print("{}: {}".format( hostname, host ))

            return host

        except Exception as e:
            return False

    return func_to_return

def reverse_lookup(host, out=False):
    try:
        hostname, aliases, ip = gethostbyaddr(host)

        if out:
            print("{}: {}".format( hostname, ip[0] ))

        return ip[0]

    except Exception as e:
        return False

def host_discovery(ipnetwork, server=None, out=False, queue=False):

    network = ip_network(ipnetwork)

    potential_hosts = [ ip.exploded for ip in network ]

    if server != None:

        reverse_lookup_closure = rl_with_server_closure(server)

        potential_hosts = filter(
            lambda a: a != False,
            map(
                reverse_lookup_closure,
                potential_hosts,
                repeat(out)
            )
        )

    else:
        potential_hosts = filter(
            lambda a: a != False,
            map(
                reverse_lookup,
                potential_hosts,
                repeat(out)
            )
        )
    
    hosts = list(potential_hosts)

    if not out and queue:
        queue.put(hosts)


    elif not out:
        return hosts

def multithreaded_discovery(ipnetwork, threads, server=None, out=False):

    if not out:
        queue = Queue()

    else:
        queue = False

    network = ip_network(ipnetwork)

    subnets = [ i for i in network.subnets( int(threads**(.5)) ) ]
    current_threads = []

    for num in range(0, len(subnets)):

        x = th.Thread(
            None,
            target=host_discovery,
            args=[subnets[num], server, out, queue]
        )

        x.start()
        current_threads.append(x)

    for thread in current_threads:
        thread.join()

    if queue:
        return reduce( lambda a,b: a+b, queue.queue )

def main(network, server=None, threads=0, out=False):

        if threads > 0:

            multithreaded_discovery(network, threads, server, out)

        else:

            host_discovery(network, server, out)



if __name__ == "__main__":

    parser = ArgumentParser(description="This script attempts to discover each host in a given network-address range; brute-force is used, so BE CARFUL with how "+\
        "large of an address range you wish to discover. Multithreading may speed this process up by a large factor.")
    parser.add_argument("network", help="A network's IP range in CIDR notation (ex: 192.168.0.0/24)")
    parser.add_argument("--server", default=None, help="Optional server to make queries to; it can be any server, but a good place to start\nwould be the target domain's master server."+\
        " By default, the host's nameservers are used.")
    parser.add_argument("--threads", type=int, default=0, help="The amount of threads to use for discovery. Ultimately, this may NOT be the number of threads used, since the network may not be divisible for that many threads.")

    args = parser.parse_args()
    
    main(args.network, args.server, args.threads, True)
