from cache_snoop import perform_cache_snoop

def test_analyze_answer():
    pass

def test_domain_is_cached():
    response = perform_cache_snoop("google.com", "a.root-servers.net") 
    assert len(response.answer) == 0
    assert len(response.authority) == 1
