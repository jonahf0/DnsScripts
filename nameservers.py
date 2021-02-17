from dns import resolver

def get_ns(domain):

    nameservers = []

    response = resolver.resolve(domain, "NS").response.answer[0]

    for ns in response:

        nameservers.append( ns.target.to_text() )

    return nameservers