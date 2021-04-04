from dns import resolver, zone, query, xfr

# attempts to perform a zone transfer on the target
def perform_zone_transfer(domain, server):

    serv_addr = resolver.resolve(server, "A")[0].address

    try:
        records = zone.from_xfr(query.xfr(serv_addr, domain))

        deliverable = []

        for record in sorted(records.nodes.keys()):
            deliverable.append(records[record].to_text(record))

    except xfr.TransferError:
        return False

    return deliverable
