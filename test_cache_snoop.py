from cache_snoop import perform_cache_snoop, deduce_cache_snoop

def test_on_root():
    response = perform_cache_snoop("google.com", "a.root-servers.net")

    assert len(response.answer) == 0
    assert len(response.authority) == 1

'''
def test_deduce_is_cached():
    #response = perform_cache_snoop("google.com", "dns.google")

    assert deduce_cache_snoop("google.com", "dns.google") == True

def test_deduce_is_not():
    #response = perform_cache_snoop("zonetransfer.me", "dns.google")

    assert deduce_cache_snoop("zonetransfer.me", "dns.google") == False'''
