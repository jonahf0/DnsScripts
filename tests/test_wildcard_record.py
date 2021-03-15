from wildcard_record import *


def test_generate_names():

    test_list = generate_names("example.com")

    assert len(test_list) == 3

    for entry in test_list:

        assert type(int(entry.strip(".example.com"))) == int


def test_check_names():

    assert check_names(generate_names("google.com"), "dns.google") == False

    assert check_names(generate_names("danbooru.us"), "dns.google") == True
