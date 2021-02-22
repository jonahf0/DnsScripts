from dns import resolver, query, message

def query_data(name, server):

    serv_addr = resolver.resolve(server, "A")[0].address

    name_message = message.make_query(name, "A")

    return name_message, serv_addr

def return_response(name, server):
    
    name_message, server_addr = query_data(name, server)

    response = query.udp(name_message, server_addr)

    return response

def return_response_tcp(name, server):

    name_message, server_addr = query_data(name, server)

    response = query.tcp(name_message, server_addr)

    return response


def return_response_norecurse(name, server):
    
    name_message, server_addr = query_data(name, server)

    name_message.flags = 0

    response = query.udp(name_message, server_addr)

    return response