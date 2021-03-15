from wordlist_lookup import *


def test_range_lookup():

    range_function = range_lookup()

    assert range_function("dns.google") == [False for i in range(0, 9)] + [
        ("dns.google", "8.8.4.4")
    ] or [False for i in range(0, 9)] + [("dns.google", "8.8.8.8")]

    range_function = range_lookup("208.67. 222.222", space=3)

    assert range_function("dns.google") == [False for i in range(0, 5)] + [
        ("dns.google", "8.8.4.4")
    ] or [False for i in range(0, 5)] + [("dns.google", "8.8.8.8")]
