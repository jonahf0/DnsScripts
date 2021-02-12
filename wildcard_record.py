from dns import resolver
from random import randint

def generate_names(domain):

    wildcard_names = []

    for i in range(0,3):
        
        wildcard_names.append( str( randint(0, 100000) ) + ".{}".format(domain) )

    return wildcard_names

def check_names(wildcard_names , server):

    serv_addr = resolver.resolve(server, "A")[0].address

    for entry in wildcard_names:
        
        try:
            answer = resolver.resolve(entry , "A")
        
        except:
            return False

    return True

def wildcard_record(domain, server):
    
    wildcard_names = generate_names( domain )

    return check_names(wildcard_names, server)

        
