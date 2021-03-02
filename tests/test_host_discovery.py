from host_discovery import *
from ipaddress import IPv4Address

def test_multithreaded_vs_singlethreaded():
    assert len(multithreaded_discovery("74.192.196.0/28", "dns.google", 4)) == len(host_discovery("74.192.196.0/28", "dns.google"))

def test_one_vs_two():
    assert host_discovery("74.192.196.0/28", "dns.google") == host_discovery_two("74.192.196.0/28", "dns.google")

def test_reverse_forward_lookup():
    assert reverse_forward_lookup(IPv4Address("8.8.8.8"), "resolver1.opendns.com") == "8.8.8.8" or "8.8.4.4"