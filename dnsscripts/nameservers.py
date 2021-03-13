from dns import resolver, query
from return_response import query_data
from socket import gethostbyaddr

# tries to get a list of nameservers from a host
def get_ns(name):

    nameservers = []

    # gets nameservers response message
    response = resolver.resolve(name, "NS").response.answer[0]

    return [ns.target.to_text() for ns in response]


# try to get the master nameserver for a domain;
# can give an optional nameserver for resolution in case the master does
# not want to cooperate and give an SOA, or can let the default for that nameserver
# be from the default resolver's list
def get_master_ns(name, server=resolver.get_default_resolver().nameservers[0]):

    try:
        response = resolver.resolve(name, "SOA")

        return response.response.answer[0][0].mname.to_text()

    except resolver.NoAnswer:

        server_name = gethostbyaddr(server)[0]

        message, address = query_data(name, server_name, "SOA")

        response = query.udp(message, address)

        return response.authority[0].to_rdataset()[0].mname.to_text()
