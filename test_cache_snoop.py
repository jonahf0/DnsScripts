from cache_snoop import deduce_from_ttl, \
    get_ttl_from_ns, deduce_cache_snoop

#def test_on_root():
    #response = perform_cache_snoop("google.com", "a.root-servers.net")

#    assert len(response.answer) == 0
#    assert len(response.authority) == 1

def test_get_ttl_from_ns():
    assert get_ttl_from_ns("google.com") == 300

def test_deduce_from_ttl():
    assert deduce_from_ttl("google.com", "dns.google") == True
    assert deduce_from_ttl("digi.ninja", "dns.google") == False
