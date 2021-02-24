from ipaddress import ip_network
from socket import gethostbyaddr
from return_response import return_response

def host_discovery(ipnetwork, server):
    
    network = ip_network(ipnetwork)

    potential_hosts = []

    for host in network:
        try:
            name = gethostbyaddr(host.exploded)[0]
            print(
                "{}: {}".format(
                    name,
                    return_response(name, server).answer[0][0].to_text()
                )
            )
        
        except:
            pass