from socket import gethostbyaddr

def reverse_lookup(ip):
    data = gethostbyaddr(ip)

    return data[0]