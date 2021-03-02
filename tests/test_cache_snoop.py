from cache_snoop import get_ttl_from_ns, norecurse_cache_snoop, \
    get_response_times

def test_get_ttl_from_ns():
    assert get_ttl_from_ns("google.com") == 300
    assert get_ttl_from_ns("boss.latech.edu") == 60

#this may occasionally fail during a test;
#this is due to the instability of testing conditions for response times
def test_get_response_times():
    first, avg1 = get_response_times("google.com", "dns.google")
    second, avg2 = get_response_times("google.com", "dns.google")
    diff = abs(first - second)
    assert diff <= avg1[0] + avg1[1] and diff <= avg2[0] + avg2[1] 

#this may fail occasionally too;
#sometimes, there will be a SERVFAIL error from the response, but
#this should only occasionally happen
def test_norecurse_cache_snoop():
    assert norecurse_cache_snoop("google.com", "dns.google") == True
    assert norecurse_cache_snoop("amazon.com", "ns1.google.com") == False