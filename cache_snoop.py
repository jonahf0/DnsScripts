from dns import resolver, query, message, rcode
from tcp_latency import measure_latency
from nameservers import get_ns
from return_response import return_response

def get_ttl_from_ns(domain):

    nameservers = get_ns(domain)
    
    response = return_response(domain, nameservers[0])

    return response.answer[0].ttl

def deduce_from_ttl(domain, server):

    official_ttl = get_ttl_from_ns(domain)

    response = return_response(domain, server)

    response_time_1 = response.time

    response_ttl_1 = response.answer[0].ttl

    response = return_response(domain, server)

    response_time_2 = response.time

    response_ttl_2 = response.answer[0].ttl
    
    return (official_ttl - response_ttl) > 1

def deduce_from_latency(domain, server):
    
    avg_latency = sum( measure_latency(domain, port=53, runs=5) ) / 5

    response_1 = return_response(domain, server)

    response_2 = return_response(domain, server)

    return abs(avg_latency - response_2) <= abs(avg_latency - response_1)

def deduce_cache_snoop(domain, server):

    deduce_from_latency(domain, server)

    deduce_from_ttl(domain, server)

    
