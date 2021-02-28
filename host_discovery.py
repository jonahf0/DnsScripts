from ipaddress import ip_network
from socket import gethostbyaddr, herror
from return_response import return_response
from itertools import repeat
from functools import reduce
from argparse import ArgumentParser
import threading as th
from queue import Queue

def reverse_forward_lookup(host, server, out=False):
    try:
        name = gethostbyaddr(host.exploded)[0]

        response = return_response(name, server).answer[0][0].to_text()

        if out:
           print("{}: {}".format(name, response))

        return response

    except Exception as e:
        return False

def host_discovery_two(ipnetwork, server, out=False):

    network = ip_network(ipnetwork)

    potential_hosts = network.hosts()

    potential_hosts = filter(
        lambda a: a != False,
        map(
            reverse_forward_lookup,
            potential_hosts,
            repeat(server),
            repeat(out)
        )
    )
    
    hosts = list(potential_hosts)

    if not out:
        return hosts

def multithreaded_discovery(ipnetwork, server, threads, out=False):

    if not out:
        queue = Queue()

    else:
        queue = False

    network = ip_network(ipnetwork)

    subnets = list( network.subnets( int(threads**(.5)) ) )
    current_threads = []

    for num in range(0,threads):
        if num > len(subnets)-1:
            break

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


def host_discovery(ipnetwork, server, out=False, queue=False):
    
    network = ip_network(ipnetwork)

    potential_hosts = []

    for host in network:

            potential_hosts.append(
                reverse_forward_lookup(host, server, out)
            )

    if not out and queue:
        queue.put(potential_hosts)

    elif not out:
        return potential_hosts

def main(network, server, threads=0, out=False):

        if threads > 0:
            multithreaded_discovery(network, server, threads, out)

        else:
            host_discovery(network, server, out)



if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("network", help="A network's IP range in CIDR notation (ex: 192.168.0.0/24)")
    parser.add_argument("server", help="The server to make queries to; it can be any server, but a good place to start\nwould be the target domain's master server")
    parser.add_argument("--threads", type=int, default=0, help="The amount of threads to use for discovery")

    args = parser.parse_args()

    main(args.network, args.server, args.threads, True)
