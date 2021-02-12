from dns import resolver, query, message

#possibly  implement other function if tor interface desired
    #else, proxychains could be fine
    #new_resolver = resolver.Resolver(configure=False)
    #new_resolver.nameservers = ['127.0.0.1']
    #new_resolver.port = 9053

def perform_cache_snoop(domain, server):
    
    domain_message = message.make_query(domain, "A")

    domain_message.flags = 0

    server_addr = resolver.resolve(server, "A")[0].address

    response = query.tcp(domain_message, server_addr)

    return response

def cache_snoop(domain, server):

    print("Attempting to snoop on {} for {}".format(server, domain))

    perform_cache_snoop(domain, server)

    

    

