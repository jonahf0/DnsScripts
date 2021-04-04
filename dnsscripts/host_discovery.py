from ipaddress import ip_network
from return_response import rl_with_server_closure
from itertools import repeat
from functools import reduce
from argparse import ArgumentParser
from dns import resolver
import threading as th
from queue import Queue
from socket import gethostbyname

# the main host_discovery lookup function, with multithreaded_discovery calling this one
# but in multiple threads;
# maps a reverse_lookup function to each ip in the ip_network object
def host_discovery(ipnetwork, server=None, out=False, queue=False):

    network = ip_network(ipnetwork)

    # get every possible host in the ip_network object
    potential_hosts = [ip.exploded for ip in network]

    # function bound by resolver;
    # the resolver may use the default host nameservers
    reverse_lookup_closure = rl_with_server_closure(server, out)

    potential_hosts = filter(
        lambda a: a != False, map(reverse_lookup_closure, potential_hosts)
    )

    # create a list from the filter object
    hosts = list(potential_hosts)

    # if there IS a queue and the program is NOT verbose,
    # then there are threads that want to return final list;
    # since queue would be a reference to a queue and not just a copy,
    # there is no stack issues
    if not out and queue:
        queue.put(hosts)

    # if NOT verbose, the return hosts
    elif not out:
        return hosts


# multithreaded function that creates tries to create the specified number of threads
# to use with the host_discovery function
def multithreaded_discovery(ipnetwork, threads, server=None, out=False):

    # create a queue so ips can be actually returned and not
    # printed out
    if not out:
        queue = Queue()

    # set queue to False just for checking
    else:
        queue = False

    network = ip_network(ipnetwork)

    # this tries to create different subnets based on the amount of threads;
    # because of this, there may not be as many threads as specified by the user
    subnets = [i for i in network.subnets(int(threads ** (0.5)))]
    current_threads = []

    # create a thread for each subnet and then start the thread
    for num in range(0, len(subnets)):

        x = th.Thread(
            None, target=host_discovery, args=[subnets[num], server, out, queue]
        )

        x.start()
        current_threads.append(x)

    # join the threads
    for thread in current_threads:
        thread.join()

    # if there is a queue, then reduce the queue to a single
    # list; since each item in the queue's queue variable would
    # be a list, then the return value is a single list
    if queue:
        return reduce(lambda a, b: a + b, queue.queue)


def main(network, server=None, threads=0, out=False):

    if threads > 0:

        multithreaded_discovery(network, threads, server, out)

    else:

        host_discovery(network, server, out)


if __name__ == "__main__":

    parser = ArgumentParser(
        description="This script attempts to discover each host in a given network-address range; brute-force is used, so BE CARFUL with how "
        + "large of an address range you wish to discover. Multithreading may speed this process up by a large factor."
    )
    parser.add_argument(
        "network", help="A network's IP range in CIDR notation (ex: 192.168.0.0/24)"
    )
    parser.add_argument(
        "--server",
        default=None,
        help="Optional server to make queries to; it can be any server, but a good place to start\nwould be the target domain's master server."
        + " By default, the host's nameservers are used.",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=0,
        help="The amount of threads to use for discovery. Ultimately, this may NOT be the number of threads used, since the network may not be divisible for that many threads.",
    )

    args = parser.parse_args()

    try:
        if args.server != None:
            server = gethostbyname(args.server)

        else:
            server = None

    except Exception as e:
        parser.exit(
            message="There was problem with the server!\nHere is the error: {}\n".format(
                e
            )
        )

    if args.threads < 0:
        parser.exit(message="Thread count cannot be lower than zero!\n")

    main(args.network, server, args.threads, True)
