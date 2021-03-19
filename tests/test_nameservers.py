from nameservers import *

def test_get_ns():
    ns = get_ns("zonetransfer.me")
    ns.sort()
    assert ns == ["nsztm1.digi.ninja.", "nsztm2.digi.ninja."]

def test_get_master_ns():
    assert get_master_ns("google.com") in {"ns1.google.com.", False}
    assert get_master_ns("boss.latech.edu") in {"dns1.latech.edu.", False}