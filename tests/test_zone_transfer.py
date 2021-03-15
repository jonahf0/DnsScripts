from zone_transfer import perform_zone_transfer


def test_zonetransfer_me_output():
    assert perform_zone_transfer("zonetransfer.me", "nsztm1.digi.ninja") == [
        '@ 7200 IN SOA nsztm1.digi.ninja. robin.digi.ninja. 2019100801 172800 900 1209600 3600\n@ 300 IN HINFO "Casio fx-700G" "Windows XP"\n@ 301 IN TXT "google-site-verification=tyP28J7JAUHA9fw2sHXMgcCC0I6XBmmoVi04VlMewxA"\n@ 7200 IN MX 0 ASPMX.L.GOOGLE.COM.\n@ 7200 IN MX 10 ALT1.ASPMX.L.GOOGLE.COM.\n@ 7200 IN MX 10 ALT2.ASPMX.L.GOOGLE.COM.\n@ 7200 IN MX 20 ASPMX2.GOOGLEMAIL.COM.\n@ 7200 IN MX 20 ASPMX3.GOOGLEMAIL.COM.\n@ 7200 IN MX 20 ASPMX4.GOOGLEMAIL.COM.\n@ 7200 IN MX 20 ASPMX5.GOOGLEMAIL.COM.\n@ 7200 IN A 5.196.105.14\n@ 7200 IN NS nsztm1.digi.ninja.\n@ 7200 IN NS nsztm2.digi.ninja.',
        '_acme-challenge 301 IN TXT "6Oa05hbUJ9xSsvYy7pApQvwCUSSGgxvrbdizjePEsZI"',
        "_sip._tcp 14000 IN SRV 0 0 5060 www",
        "14.105.196.5.IN-ADDR.ARPA 7200 IN PTR www",
        "asfdbauthdns 7900 IN AFSDB 1 asfdbbox",
        "asfdbbox 7200 IN A 127.0.0.1",
        "asfdbvolume 7800 IN AFSDB 1 asfdbbox",
        "canberra-office 7200 IN A 202.14.81.230",
        'cmdexec 300 IN TXT "; ls"',
        'contact 2592000 IN TXT "Remember to call or email Pippa on +44 123 4567890 or pippa@zonetransfer.me when making DNS changes"',
        "dc-office 7200 IN A 143.228.181.132",
        "deadbeef 7201 IN AAAA dead:beaf::",
        "dr 300 IN LOC 53 20 56.558 N 1 38 33.526 W 0.00m",
        'DZC 7200 IN TXT "AbCdEfG"',
        'email 2222 IN NAPTR 1 1 "P" "E2U+email" "" email.zonetransfer.me\nemail 7200 IN A 74.125.206.26',
        'Hello 7200 IN TXT "Hi to Josh and all his class"',
        "home 7200 IN A 127.0.0.1",
        'Info 7200 IN TXT "ZoneTransfer.me service provided by Robin Wood - robin@digi.ninja. See http://digi.ninja/projects/zonetransferme.php for more information."',
        "internal 300 IN NS intns1\ninternal 300 IN NS intns2",
        "intns1 300 IN A 81.4.108.41",
        "intns2 300 IN A 167.88.42.94",
        "office 7200 IN A 4.23.39.254",
        "ipv6actnow.org 7200 IN AAAA 2001:67c:2e8:11::c100:1332",
        "owa 7200 IN A 207.46.197.32",
        'robinwood 302 IN TXT "Robin Wood"',
        "rp 321 IN RP robin robinwood",
        'sip 3333 IN NAPTR 2 3 "P" "E2U+sip" "!^.*$!sip:customer-service@zonetransfer.me!" .',
        'sqli 300 IN TXT "\' or 1=1 --"',
        'sshock 7200 IN TXT "() { :]}; echo ShellShocked"',
        "staging 7200 IN CNAME www.sydneyoperahouse.com.",
        "alltcpportsopen.firewall.test 301 IN A 127.0.0.1",
        "testing 301 IN CNAME www",
        "vpn 4000 IN A 174.36.59.154",
        "www 7200 IN A 5.196.105.14",
        "xss 300 IN TXT \"'><script>alert('Boo')</script>\"",
    ]


def test_cannot_transfer():
    assert perform_zone_transfer("google.com", "dns.google") == False
