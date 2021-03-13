from argparse import ArgumentParser
from dns import resolver
from itertools import repeat
from functools import reduce
from ipaddress import ip_address
from return_response import resolve_with_server_closure, rl_with_server_closure
import threading as th

from host_discovery import multithreaded_discovery

# closure function that returns the lookup function;
# binds the lookup space and resolver/reverse-lookup functions to
# the returned function
def range_lookup(server=None, space=5, out=False):

    forward_resolve = resolve_with_server_closure(server, out)

    rev_lookup = rl_with_server_closure(server, out)

    lookup_space = space

    verbose = out

    def func_to_return(hostname):

        # try to get the ip of a hostname;
        # False if there is no ip
        ip = forward_resolve(hostname)

        if ip != False:

            # create a range of ips centered around the recently discovered one
            ip_range = [
                (ip_address(ip) + i).exploded
                for i in range(-lookup_space, lookup_space)
                if i != 0
            ]

            # map the reverse lookup function to each ip
            hosts = list(map(rev_lookup, ip_range))

            hosts.append(ip)

            return hosts

        else:

            return [False]

    return func_to_return


# creates a list from a text "wordslist" file, then decides which function
# to map to the list based on whether there is a server or not;
# instead of using the resolver closure for both cases, resolve_hostname
# is used because of speed improvements
def wordlist_lookup(domain, wordlist, server=None, space=5, out=False):

    with open(wordlist, "r") as f:

        # in the list comprehension, remove the newline characters
        words = [word.replace("\n", "") for word in f]

    # create the range lookup function;
    # resolves a hostname, then reverse looks up surrounding
    # ip addresses
    resolver_func = range_lookup(server, space, False)

    # list(ips) is a list of lists, so reduce it down to a single
    # list

    other_func = resolve_with_server_closure(server, out)


    final_ips = filter(
        lambda b: b != False,
        reduce(
            lambda a, b: a + b,
            map(resolver_func, [word + "." + domain for word in words]),
        ),
    )

    return list(set(final_ips))


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

    wordlist_lookup(args.domain, args.wordlist, args.server, args.space, True)
