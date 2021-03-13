from dns import resolver, query, message

# returns a function based on the resolver created by passing a
# specific server to the "creater" function
def resolve_with_server_closure(server=None, out=False):

    # create the resolver, give it the server to use,
    # then "bind" that resolver to a function to return that resolves
    # hostnames
    res = resolver.Resolver()

    if server != None:
        res.nameservers = [server]

    verbose = out

    def func_to_return(hostname):

        try:

            response = res.resolve(hostname, "A")

            ip = response.rrset[0].to_text()

            if verbose:

                print("{}: {}".format(hostname, ip))

            return ip

        except Exception as e:

            return False

    return func_to_return


# closure function that binds a specific resolver to a function that reverse
# looks up a hostname;
# used for reverse lookups
def rl_with_server_closure(server=None, out=False):

    cl_resolver = resolver.Resolver()

    if server != None:
        cl_resolver.nameservers = [server]

    verbose = out

    # the resolver is bound to this function;
    # if the servers for the resolver are not modified, then the
    # resolver uses the host's nameservers
    def func_to_return(host):
        try:
            response = cl_resolver.resolve_address(host)

            hostname = response.rrset[0].to_text()

            if verbose:
                print("{}: {}".format(hostname, host))

            return host

        except Exception as e:
            return False

    return func_to_return


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
