from host_discovery import *
from ipaddress import IPv4Address


def test_host_discovery():
    assert host_discovery("8.8.8.8/32") == [("dns.google.","8.8.8.8")]


def test_multithreaded_vs_singlethreaded():
    assert len(multithreaded_discovery("74.192.196.0/28", 4)) == len(
        host_discovery("74.192.196.0/28")
    )

def test_rl_with_server_closure():
    func = rl_with_server_closure("8.8.8.8")
    assert func("208.67.222.222") == ("resolver1.opendns.com.","208.67.222.222")
