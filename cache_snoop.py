from dns import resolver, query, message, rcode
from nameservers import get_master_ns
from return_response import *
from sys import argv

#queries the authoritative nameservers for domain's ttl
#returns that ttl
#used for deducing for comparing the offical ttl to the cached entry's ttl
def get_ttl_from_ns(name):

    nameserver = get_master_ns(name)

    response = return_response(name, nameserver)

    return response.answer[0].ttl

def get_response_times(name, server):
    
    #initial = return_response(domain, server).time * 1000

    second = return_response(name, server).time * 1000
    
    times = []

    for i in range(0,10):
        one = return_response(name, server).time * 1000
        two = return_response(name, server).time * 1000

        times.append(abs(two-one))

    avg_difference = sum(times)/len(times)

    return second, avg_difference

def print_conclusion(initial_time, initial_ttl, second, avg_difference, official_ttl):
    
    if official_ttl > initial_ttl:
        print("Based on the TTLs, the hostname was likely cached")
    else:
        print("Based on the TTLs, the hostname was likely NOT cached")

    if (initial_time - second) <= avg_difference:
        print("Based on the response times, the hostname was likely cached")
    else:
        print("Based on the response times, the hostname was likely NOT cached")

def print_info(initial_time, initial_ttl, name, server):

    print("Initial response time: {} miliseconds".format(initial_time))
    print("Initial response TTL: {} seconds\n".format(initial_ttl))

    print("Calculating different response times...")
    second, avg_difference = get_response_times(name, server)

    print("Second response time: {} miliseconds".format(second))
    print("Average difference between consequent response times: {} miliseconds\n".format(avg_difference))

    print("Fetching TTL from Master Nameserver...")
    official_ttl = get_ttl_from_ns(name)

    print("TTL from Master: {} seconds\n".format(official_ttl))

    print("Note: Conclusions based on the TTLs are more accurate\nthan conclusions based on the response times...\n")

    print_conclusion(initial_time, initial_ttl, second, avg_difference, official_ttl)

def reach_conclusion(initial_time, initial_ttl, name, server):
    
    second, avg_difference = get_response_times(name, server)

    official_ttl = get_ttl_from_ns(name)

    print_conclusion(initial_time, initial_ttl, second, avg_difference, official_ttl)

def deduce_cache_snoop(name, server, verbose=False):
    
    try:
        initial_response = return_response(name, server)
        initial_time = initial_response.time * 1000
        initial_ttl = initial_response.answer[0].ttl

        if verbose:
            print_info(initial_time, initial_ttl, name, server)
        else:
            reach_conclusion(initial_time, initial_ttl, name, server)

    except IndexError:
        print("The target server did not have an answer for {}...".format(name))
        print("The response indicates to query at {}".format(initial_response.authority[0][0].mname.to_text()))

    except resolver.NoAnswer:
        print("The master nameserver did not give an answer for {}...".format(name))
