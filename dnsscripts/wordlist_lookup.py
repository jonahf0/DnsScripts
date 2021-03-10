from argparse import ArgumentParser
from return_response import return_response
from host_discovery import reverse_forward_lookup
from dns import rcode
from ipaddress import ip_address
import threading as th

def range_lookup(ip, server, space=5):

    middle_address = ip_address(ip)

    for num in range(0, space):

        response = reverse_forward_lookup( middle_address - space + num, server)

        analyze_response( response, server)

    for num in range(1, space + 1):

        response = reverse_forward_lookup( middle_address + num, server )

        analyze_response( response, server )

def analyze_response(response, server, space=5):
    
    rc = response.resolve_chaining()

    if rc.cnames != []:

        cname_pointing = " --> ".join([ x.to_rdataset()[0].to_text() for x in rc.cnames ])

        addresses = [ ip.to_text() for ip in rc.answer ]

        for ip in addresses:
            range_lookup(ip, server, space=5)

        return "".join( [cname_pointing, "".join(addresses) ] )

    elif rc.answer != None:
        
        address = rc.answer[0].to_text()

        return address

def wordlist_lookup(domain, server, wordlist, space=5):

    with open(wordlist, "r") as f:
        words = [ word.replace("\n", "") for word in f ]

    for word in words:

        response = return_response(
            word + "." + domain, server
        )

        if rcode.to_text(response.rcode()) != "NXDOMAIN":
            
            address_string = analyze_response(response, server, space)
            
            print("{} --> {}".format(word+"."+domain, address_string))

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument("domain")
    parser.add_argument("server")
    parser.add_argument("wordlist")
    parser.add_argument("--space")
    parser.add_argument("--threads", type=int,default=0)

    args = parser.parse_args()

    wordlist_lookup(args.domain, args.server, args.wordlist, args.threads)