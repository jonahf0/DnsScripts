from dns import resolver, query, message

def query_data(domain, server):

    serv_addr = resolver.resolve(server, "A")[0].address

    domain_message = message.make_query(domain, "A")

    return domain_message, serv_addr

def return_response(domain, server):
    
    domain_message, server_addr = query_data(domain, server)

    response = query.udp(domain_message, server_addr)

    return response

def return_response_tcp(domain, server):

    domain_message, server_addr = query_data(domain, server)

    response = query.tcp(domain_message, server_addr)

    return response


def return_response_norecurse(domain, server):
    
    domain_message, server_addr = query_data(domain, server)

    domain_message.flags = 0

    response = query.udp(domain_message, server_addr)

    return response