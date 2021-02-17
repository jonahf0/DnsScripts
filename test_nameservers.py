from nameservers import get_ns

def test_get_ns():
    assert get_ns("zonetransfer.me") == ["nsztm1.digi.ninja." , "nsztm2.digi.ninja."]