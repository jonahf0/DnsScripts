from socket import gethostbyaddr

def reverse_lookup(ip):
    try:
        data = gethostbyaddr(ip)
        return data[0]

    except Exception as e:
        #print("Unable to reverse-lookup: {}".format(e))
        return False