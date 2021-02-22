from dns import resolver

def get_master_ns(name):

    response = resolver.resolve(name, "SOA")

    return response.response.answer[0][0].mname.to_text()

def get_ns(name):

    nameservers = []

    response = resolver.resolve(name, "NS").response.answer[0]

    for ns in response:

        nameservers.append( ns.target.to_text() )

    return nameservers