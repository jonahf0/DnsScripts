from argparse import ArgumentParser
from nameservers import get_ns


def main(domain):

    ns = get_ns(domain)


if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument("-domain", help="the domain to get information for")

    # add:
    #   cache snooping
    #   discovery methods
    #

    args = parser.parse_args()

    main(args.domain)
