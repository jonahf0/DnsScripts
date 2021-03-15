from nameservers import get_ns


def test_get_ns():
    ns = get_ns("zonetransfer.me")
    ns.sort()
    assert ns == ["nsztm1.digi.ninja.", "nsztm2.digi.ninja."]
