from reverse_lookup import reverse_lookup

def test_reverse_lookup():
    assert reverse_lookup("8.8.8.8") == "dns.google"