from argparse import ArgumentParser
from functools import reduce
from ipaddress import ip_address
from return_response import resolve_with_server_closure, rl_with_server_closure
from socket import gethostbyname
from queue import Queue

import threading as th
import os.path

# closure function that returns the lookup function;
# binds the lookup space and resolver/reverse-lookup functions to
# the returned function
def range_lookup(server=None, space=5, out=False):

    # store the verbosity and lookup range
    verbose = out
    lookup_space = space

    # get the resolve / lookup functions
    forward_resolve = resolve_with_server_closure(server, False)
    rev_lookup = rl_with_server_closure(server, False)

    # create a set of hosts and ip pairs;
    # the set prevents there from being repeats
    set_of_hosts = set()

    # the closure
    def func_to_return(hostname):

        # the closure's return value will either be this, a list
        # of tuples, or False
        hosts_and_ips = []

        # try to get the ip of a hostname;
        # False if there is no ip
        hit_ip = forward_resolve(hostname)

        if hit_ip != False:

            # check to make sure this tuple isn't already in the set
            if hit_ip not in set_of_hosts:

                set_of_hosts.add(hit_ip)

                hosts_and_ips.append(hit_ip)

                if out:
                    print("{}: {}".format(hit_ip[0], hit_ip[1]))

            # create a range of ips centered around the recently discovered one
            ip_range = [
                (ip_address(hit_ip[1]) + i).exploded
                for i in range(-lookup_space, lookup_space)
                if i != 0
            ]

            # create a list of tuples of hostnames and ips around the range;
            # filters out False entries
            range_hosts = list(filter(lambda a: a != False, map(rev_lookup, ip_range)))

            # do the same thing for the first ip, but for each tuple in the range's hosts
            for key_val in range_hosts:

                host, ip = key_val

                if key_val not in set_of_hosts:

                    set_of_hosts.add((host, ip))

                    hosts_and_ips.append((host, ip))

                    if out:
                        print("{}: {}".format(host, ip))

            return hosts_and_ips

        else:

            return False

    return func_to_return


# creates a list from a text "wordslist" file, then decides which function
# to map to the list based on whether there is a server or not;
# instead of using the resolver closure for both cases, resolve_hostname
# is used because of speed improvements
def wordlist_lookup(domain, wordlist, server=None, space=5, out=False, queue=None):

    words = wordlist

    # create the range lookup function;
    # resolves a hostname, then reverse looks up surrounding
    # ip addresses
    resolver_func = range_lookup(server, space, out)

    try:
        final_ips = reduce(
            lambda a, b: a + b,
            filter(
                lambda b: b != False,
                map(resolver_func, [word + "." + domain for word in words]),
            ),
        )

    except TypeError:
        final_ips = []

    if queue != None:
        queue.put(list(final_ips))

    else:
        return list(final_ips)

def multithreaded_lookup(domain, wordlist, server=None, space=5, threads=0, out=False):
    
    #make a new global queue
    queue = Queue()

    #get the size that the wordlist lists will be 
    size_of_sublists = int(len(wordlist)/threads)

    #create the sublists out of the wordlist
    subwordlists = [ wordlist[i:i+size_of_sublists] for i in range(0, len(wordlist), size_of_sublists) ]

    current_threads = []

    for sublist in subwordlists:

        #each thread receives a point to the queue
        thread = th.Thread(
            None, target=wordlist_lookup, args=[domain, sublist, server, space, out, queue]
        )

        thread.start()
        current_threads.append(thread)

    for thread in current_threads:
        thread.join()

    #returns the list that represents the queue
    return reduce(lambda a, b: a + b, queue.queue)

def main(domain, wordlist_file, server=None, space=5, threads=0, out=False):

    with open(wordlist_file, "r") as f:

        # in the list comprehension, remove the newline characters
        words = [word.rstrip() for word in f]

    if threads > 0:
        multithreaded_lookup(domain, words, server, space, threads, out)

    else:
        wordlist_lookup(domain, words, server, space, out)


if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument(
        "domain", help="domain to analyze and perform reverse lookups for"
    )
    parser.add_argument(
        "wordlist",
        help="a list of words to create test hostnames to bruteforce lookup; hopefully some of the words will reveal actual hosts",
    )
    parser.add_argument(
        "--server",
        help="optional server to use to lookup, with the default being the user's nameservers; a good place to try would be the target domain's servers",
    )
    parser.add_argument(
        "--space",
        help="how many addresses above and below a successful wordlist-lookup host the program should try to reverse lookup",
        type=int,
        default=5,
    )
    parser.add_argument(
        "--threads",
        help="how many threads should be used for performing the bruteforcing",
        type=int,
        default=0,
    )

    args = parser.parse_args()

    if not os.path.exists(args.wordlist):
        parser.exit(message="The wordlist file does not exist!\n")

    if args.threads < 0:
        parser.exit(message="Thread count cannot be lower than zero!\n")

    if args.space < 0:
        parser.exit(message="Lookup range cannot be lower than zero!\n")

    try:
        if args.server != None: 
            server = gethostbyname(args.server)

        else:
            server = None

    except Exception as e:
        parser.exit(message="There was problem with the server!\nHere is the error: {}\n".format(e))

    main(args.domain, args.wordlist, server, args.space, args.threads, True)
