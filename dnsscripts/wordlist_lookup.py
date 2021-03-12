from argparse import ArgumentParser
from dns import resolver
from socket import gethostbyname
from itertools import repeat
from ipaddress import ip_address
import threading as th

#returns a function based on the resolver created by passing a
#specific server to the "creater" function
def resolve_with_server_closure(server=None):

    #create the resolver, give it the server to use,
    #then "bind" that resolver to a function to return that resolves
    #hostnames
    res = resolver.Resolver()

    if server != None:
        res.nameservers = [server]

    def func_to_return(hostname, out=False):

        try:

            response = res.resolve(hostname, "A")

            ip = response.rrset[0].to_text()

            if out:

                print("{}: {}".format(hostname, ip))

            return ip

        except Exception as e:

            return False

    return func_to_return

#creates a list from a text "wordslist" file, then decides which function
#to map to the list based on whether there is a server or not;
#instead of using the resolver closure for both cases, resolve_hostname
#is used because of speed improvements
def wordlist_lookup(domain, wordlist, server=None, threads=0, out=False):
    
    with open(wordlist, "r") as f:

        #in the list comprehension, remove the newline characters
        words = [ word.replace("\n", "") for word in f ]

    #call the closure function to return a resolver function;
    #if server == None, then the resolver that is bound by the closure
    #simply uses the host's nameservers for resolving
    resolver_func = resolve_with_server_closure(server)
    
    #since the resolver function returns False if there is no resolution,
    #filter removes False entries
    ips = list(
                filter(
        
                    lambda b: b != False,
                    
                    map(
                        resolver_func,

                        [ word+"."+domain for word in words ],

                        repeat(out)
                    )
            )
        )
         
    #ips = [ ip for ip in [ resolver_func(word+"."+domain, out) for word in words ] if ip != False ]

    return ips

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument("domain", help="domain to analyze and perform reverse lookups for")
    parser.add_argument("wordlist", help="a list of words to create test hostnames to bruteforce lookup; hopefully some of the words will reveal actual hosts")
    parser.add_argument("--server", help="optional server to use to lookup, with the default being the user's nameservers; a good place to try would be the target domain's servers")
    parser.add_argument("--space", help="how many addresses above and below a successful wordlist-lookup host the program should try to reverse lookup", type=int, default=5)
    parser.add_argument("--threads", help="how many threads should be used for performing the bruteforcing", type=int,default=0)

    args = parser.parse_args()

    wordlist_lookup(args.domain, args.wordlist, args.server, args.threads, True)