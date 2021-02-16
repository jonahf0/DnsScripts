from dns import resolver, query, message, rcode
from tcp_latency import measure_latency

def perform_cache_snoop(domain, server):
    
    domain_message = message.make_query(domain, "A")

    domain_message.flags = 0

    server_addr = resolver.resolve(server, "A")[0].address

    response = query.tcp(domain_message, server_addr)

    return response

def deduce_cache_snoop(domain, server):

    pass

    

    

