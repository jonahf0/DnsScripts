from dns import resolver, query, message

def query_data(name, server, query_type):

    serv_addr = resolver.resolve(server, "A")[0].address

    name_message = message.make_query(name, query_type)

    return name_message, serv_addr

def return_response(name, server):
    
    name_message, server_addr = query_data(name, server, "A")

    response = query.udp(name_message, server_addr, 2.0)

    return response

def return_response_tcp(name, server):

    name_message, server_addr = query_data(name, server, "A")

    response = query.tcp(name_message, server_addr, 2.0)

    return response


def return_response_norecurse(name, server):
    
    name_message, server_addr = query_data(name, server, "A")

    name_message.flags = 0
    
    response = query.udp(name_message, server_addr, 2.0)

    return response