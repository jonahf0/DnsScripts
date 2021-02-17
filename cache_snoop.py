from dns import resolver, query, message, rcode
from tcp_latency import measure_latency
from nameservers import get_ns

def perform_cache_snoop(domain, server):
    
    domain_message = message.make_query(domain, "A")

    domain_message.flags = 0

    server_addr = resolver.resolve(server, "A")[0].address

    response = query.tcp(domain_message, server_addr)

    return response

def get_ttl_from_ns(domain):

    nameservers = get_ns(domain)

    ns_addr = resolver.resolve(nameservers[0], "A")[0].address

    domain_message = message.make_query(domain, "A")

    response = query.tcp(domain_message, ns_addr)
    
    return response.answer[0].ttl

def deduce_from_ttl(domain, server):

    official_ttl = get_ttl_from_ns(domain)

    domain_message = message.make_query(domain, "A")

    addr = resolver.resolve(server, "A")[0].address

    response = query.tcp(domain_message, addr)

    response_ttl = response.answer[0].ttl

    print("official({}) - response({}) is greater than 1".format(official_ttl, response_ttl))
    
    eturn (official_ttl - response_ttl) > 1


def deduce_cache_snoop(domain, server):

    pass 


    
