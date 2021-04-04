from dns import resolver
from random import randint

#generates 3 random names to test with the potential wildcard record
def generate_names(domain):

    wildcard_names = []

    for i in range(0, 3):

        wildcard_names.append(str(randint(0, 100000)) + ".{}".format(domain))

    return wildcard_names

#checks the names for wildcard; if it fails at any point, then return False
def check_names(wildcard_names, server):

    try:
        serv_addr = resolver.resolve(server, "A")[0].address

    except Exception:
        return False

    for entry in wildcard_names:

        try:
            answer = resolver.resolve(entry, "A")

        except:
            return False

    return True

#the main function for checking for wildcard record
def wildcard_record(domain, server):

    wildcard_names = generate_names(domain)

    return check_names(wildcard_names, server)
