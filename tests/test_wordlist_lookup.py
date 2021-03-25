from wordlist_lookup import *

def test_multithreaded_vs_singlethreaded():

    words = ["ns1", "mail"]

    multi = multithreaded_lookup("google.com", words, threads=2, server="216.239.32.10") 
    single = wordlist_lookup("google.com", words, server="216.239.32.10")

    multi.sort()
    single.sort()

    assert multi == single

def test_range_lookup():

    range_function = range_lookup()

    assert range_function("dns.google") == [False for i in range(0, 9)] + [
        ("dns.google", "8.8.4.4")
    ] or [False for i in range(0, 9)] + [("dns.google", "8.8.8.8")]

    range_function = range_lookup("208.67. 222.222", space=3)

    assert range_function("dns.google") == [False for i in range(0, 5)] + [
        ("dns.google", "8.8.4.4")
    ] or [False for i in range(0, 5)] + [("dns.google", "8.8.8.8")]
