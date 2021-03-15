from argparse import ArgumentParser
from functools import reduce
from ipaddress import ip_address
from return_response import resolve_with_server_closure, rl_with_server_closure
import threading as th

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
def wordlist_lookup(domain, wordlist, server=None, space=5, out=False):

    with open(wordlist, "r") as f:

        # in the list comprehension, remove the newline characters
        words = [word.replace("\n", "") for word in f]

    # create the range lookup function;
    # resolves a hostname, then reverse looks up surrounding
    # ip addresses
    resolver_func = range_lookup(server, space, out)

    final_ips = reduce(
        lambda a, b: a + b,
        filter(
            lambda b: b != False,
            map(resolver_func, [word + "." + domain for word in words]),
        ),
    )

    return list(final_ips)


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
