from zone_transfer import perform_zone_transfer
from nameservers import get_ns
from wordlist_lookup import wordlist_lookup, multithreaded_lookup
from wildcard_record import wildcard_record


from os import path
from socket import gethostbyname
from argparse import ArgumentParser
from itertools import repeat

def analyze_hosts(hosts):
    print(hosts)

def perform_wordlist_lookup(domain, wordlist, space=5, server=None, threads=0):

    # read the wordlist
    with open(wordlist, "r") as f:
        words = [word.rstrip() for word in f]

    # perform the wordlist bruteforce lookup
    if threads > 0:
        hostnames = multithreaded_lookup(domain, words, server, space, threads, True)

    else:
        hostnames = wordlist_lookup(domain, words, server, space, True, None)

    return hostnames


def main(
    domain,
    wordlist,
    space=5,
    server=None,
    threads=0,
    snoop=None,
    discovery=None,
    axfr=None
):

    # these first four lines just get an accurate list of nameservers;
    # if the domain given is a subdomain (ex: mail.google.com), then
    # get the root domain (ex: google.com from the previous example)
    temp_domain_list = domain.split(".")
    base_domain = ".".join(
        temp_domain_list[len(temp_domain_list) - 2 : len(temp_domain_list)]
    )

    ns_servers = get_ns(base_domain)
    ns_servers.sort()

    # get the nameservers
    print("Nameservers:")
    for nameserver in ns_servers:
        print("\t{}".format(nameserver))

    if axfr:
        zone_contents = list(
            filter(
                lambda a: a != False,
                map(perform_zone_transfer, repeat(domain), ns_servers),
            )
        )
    
    else:
        zone_contents = False

    if zone_contents:
        print("\nZone transfer succesful:\n")
        
        for i in zone_contents[0]:
            print("\t" + i)

    else:

        # check for wildcard record
        print("\nChecking for wildcard record...")

        wildcard_checked = {wildcard_record(domain, ns) for ns in ns_servers}

        if True in wildcard_checked:
            print("\tWILDCARD DOMAIN LIKELY\n")

        else:
            print("\tNo wildcard record found\n")

            # resolve the nameserver (cmd arg or found) into an IP
            if server != None:
                server = gethostbyname(server)

            else:
                server = gethostbyname(ns_servers[0])

            #separating some of the logic of the main function helped to grasp what it
            #does in the later sections
            hosts = perform_wordlist_lookup(domain, wordlist, space, server, threads)
            analyze_hosts(hosts)

if __name__ == "__main__":

    parser = ArgumentParser(description="A program meant to replace fierce.pl.")

    parser.add_argument("domain", help="the domain to get information for")
    parser.add_argument(
        "--threads",
        type=int,
        help="the amount of threads to use with multithreaded functions",
        default=0,
    )
    parser.add_argument(
        "wordlist", help="list of words to use for bruteforce reverse lookups"
    )
    parser.add_argument(
        "--server",
        help="optional server to use for functions that can be directed to it; by default, servers found are used, but a different server can be used",
    )
    parser.add_argument(
        "--range",
        type=int,
        default=5,
        help="how far above and below the application reverse looks up IPs surrounding a successful bruteforce lookup",
    )
    parser.add_argument(
        "--snoop",
        help="attempt cache snooping on the nameservers; as argument, provide a list of potential websites",
    )
    parser.add_argument(
        "--discovery",
        help="perform bruteforce lookups on suspected contiguous address spaces found; takes the CIDR-notation suffix decimal (ex: the 192.168.0.0/24 would be 24)",
    )
    parser.add_argument(
        "--axfr",
        help="try to perform a zone transfer; if this succeeds, then the program will print it out and stop",
        action="store_true",
    )

    args = parser.parse_args()

    #this part just does some basic cmd args checking
    if args.threads < 0:
        parser.exit(message="Thread count can't be lower than 0!")

    if args.range < 1:
        parser.exit(message="Range has to be higher than 1!")

    if path.exists(args.wordlist) == False:
        parser.exit(message="The wordlist could not be found!")

    if args.snoop != None and path.exists(args.snoop) == False:
        parser.exit(message="The website list could not be found!")

    if args.discovery != None and args.discovery < 0:
        parser.exit(message="The CIDR decimal has to be higher than 0!")

    main(
        args.domain,
        args.wordlist,
        args.range,
        args.server,
        args.threads,
        args.snoop,
        args.discovery,
        args.axfr,
    )
