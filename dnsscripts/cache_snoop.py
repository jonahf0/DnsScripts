# import stuff from dns for resolution and checking
from dns import resolver, query, message, rcode, exception

# nameservers module helps get master nameserver for a hostname
from nameservers import get_master_ns

# return_response module helps make a query to a specific server,
# returning the response
from return_response import *

# for running as a standalone script as opposed to integrated
# with a larger dns-focused script
from argparse import ArgumentParser

from statistics import stdev, mean

# queries the authoritative nameservers for domain's ttl;
# returns that ttl;
# used for deducing for comparing the offical ttl to the cached entry's ttl
def get_ttl_from_ns(name):

    # gets the master nameserver from the SOA record
    nameserver = get_master_ns(name)

    # returns the response from querying the master for the name
    response = return_response(name, nameserver)

    # return the TTL from the response's answer section --
    # may cause an error from the master refusing to give an answer
    return response.answer[0].ttl


def get_response_times(name, server):

    # get second response time;
    # gets compared to the first time in order to estimate
    # how much different that response time difference compared
    # to a later-calculated average response time
    second = return_response(name, server).time * 1000

    # here's that later-calculated average:
    # queries the server 10 times, appending each time difference
    # to the times list, then calculates an average
    times = []

    for i in range(0, 10):
        one = return_response(name, server).time * 1000
        two = return_response(name, server).time * 1000

        times.append(abs(two - one))

    # a tuple to represent the average difference between response times
    # and the standard dev of them
    avg_difference = (mean(times), stdev(times))

    return second, avg_difference


# concludes whether or not the hostname was cached or not if verbose;
# IMPORTANT: guesses based on TTLs or typically more accurate than guesses
# based on response times, but not always (ex: yelp.com)
def print_conclusion(initial_time, initial_ttl, second, avg_difference, official_ttl):

    # initial_ttl is occasionally equal to official-1,
    # even though it is not cached;
    # theoretically, offical should always equal initial if it was
    # NOT cached
    if official_ttl > initial_ttl + 1:
        print("Based on the TTLs, the hostname was likely cached")
    else:
        print("Based on the TTLs, the hostname was likely NOT cached")

    # if the difference between the initial and second are much higher than
    # the upper bounds of the avg, then it is likely not cached
    if (initial_time - second) <= avg_difference[0] + avg_difference[1]:
        print("Based on the response times, the hostname was likely cached")
    else:
        print("Based on the response times, the hostname was likely NOT cached")


# prints info about calculations and such if verbose
def print_info(initial_time, initial_ttl, name, server):

    print("Initial response time: {} miliseconds".format(initial_time))
    print("Initial response TTL: {} seconds\n".format(initial_ttl))

    print("Calculating different response times...")
    second, avg_difference = get_response_times(name, server)

    print("Second response time: {} miliseconds".format(second))
    print(
        "Average difference between consequent response times: {} miliseconds".format(
            avg_difference[0]
        )
    )
    print(
        "Standard deviation of those times: {} miliseconds\n".format(avg_difference[1])
    )

    print("Fetching TTL from Master Nameserver...")
    official_ttl = get_ttl_from_ns(name)

    print("TTL from Master: {} seconds\n".format(official_ttl))

    print(
        "Note: Conclusions based on the TTLs are more accurate\nthan conclusions based on the response times...\n"
    )

    print_conclusion(initial_time, initial_ttl, second, avg_difference, official_ttl)


# "gets straight to the point" when no verbosity
def reach_conclusion(initial_time, initial_ttl, name, server):

    second, avg_difference = get_response_times(name, server)

    official_ttl = get_ttl_from_ns(name)

    print_conclusion(initial_time, initial_ttl, second, avg_difference, official_ttl)


# main function for deducing whether or not a hostname is cached;
# should run after trying a non-polluting cache-snoop, since
def deduce_cache_snoop(name, server, verbose=False):

    # get a first response, the most important one:
    # the TTL for it will probably match the master server's TTL if not cached;
    # the first response time is generally quite large compared to cached response times
    try:
        initial_response = return_response(name, server)
        initial_time = initial_response.time * 1000
        initial_ttl = initial_response.answer[0].ttl

        if verbose:
            print_info(initial_time, initial_ttl, name, server)
        else:
            reach_conclusion(initial_time, initial_ttl, name, server)

    # IndexError from the overly-complex OOP-laden response object;
    # response.answer[0] may not have an answer and may cause this
    except IndexError:

        # 5 is a refusal to answer the intial query
        if initial_response.rcode() == 5:
            print("The target server refused the query for {}...\n".format(name))

        # the other IndexError comes from there being no answer at all,
        # but the server in question will point toward another  server for
        # future queries
        else:
            print("The target server did not have an answer for {}...".format(name))
            print(
                "The response indicates to query at {}\n".format(
                    initial_response.authority[0][0].mname.to_text()
                )
            )


# the first cache_snoop function to try;
# attempts to make a nonrecursive query
def norecurse_cache_snoop(name, server):

    response = return_response_norecurse(name, server)

    if response.rcode() == 0:
        if len(response.answer) == 0:
            print("The hostname {} was NOT cached.".format(name))
        else:
            print("The hostname {} was cached!".format(name))

        return True

    else:
        print("The server had an issue with the non-recursive query...")
        print("Response code: {}\n".format(rcode.to_text(response.rcode())))
        return False


# the main function;
# practically runs either norecurse or deduce cache_snoop functions
# with a verbosity
def cache_snoop(name, server, norecurse=True, deduce=True, verbose=False):

    attempt_one = False

    if norecurse:
        attempt_one = norecurse_cache_snoop(name, server)

    if not attempt_one and deduce:

        deduce_cache_snoop(name, server, verbose)


if __name__ == "__main__":

    parser = ArgumentParser(
        description="This script will try to snoop a certain hostname on a nameserver."
        + " If the target nameserver will not accept non-recursive queries, then the program will try to deduce whether or not the name was cached by"
        + " comparing the time-to-live values from the target and authoritative namservers and will compare the first and"
        + " second response times to an average response time and standard deviation.\n",
        epilog="The first method of cache-snooping is NON-polluting and will not leave the targeted hostname cached in the target nameserver."
        + " The second and third methods of cache-snooping ARE polluting and will leave the targeted hostname cached in the target nameserver, so BE CAREFUL with these methods",
    )
    parser.add_argument("hostname", help="The hostname to check the target cache for")
    parser.add_argument(
        "nameserver", help="The nameserver that you are targeting for cache-snooping"
    )
    parser.add_argument(
        "--verbose", help="Verbosity for deducing cached entries", action="store_true"
    )
    parser.add_argument(
        "--no-deduce", help="Opts out of deducing cached entires", action="store_true"
    )
    parser.add_argument(
        "--only-deduce",
        help="Opts of out sending nonrecursive queries and only deduces;\nthis is helpful when you know the target server will refuse non-recursive queries",
        action="store_true",
    )

    args = parser.parse_args()

    name = args.hostname
    server = args.nameserver

    if args.verbose:
        verbose = args.verbose
    else:
        verbose = False

    if args.no_deduce:
        deduce = False
        norecurse = True

    elif args.only_deduce:
        deduce = True
        norecurse = False

    else:
        deduce = True
        norecurse = True

    cache_snoop(name, server, norecurse, deduce, verbose)
