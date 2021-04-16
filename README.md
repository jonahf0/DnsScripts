  This is one of my first repositories. It is meant to consist of DNS footprinting and enumeration scripts, ultimately culminating in a more comprehensive DNS enumeration tool. It is very inspired by the fierce.pl script, and these will likely have much of the same functionality.
  
  Unique to these scripts in comparison to fierce.pl are the host_discovery.py and cache_snoop.py scripts. The cache_snoop.py script currently is a fully-fledged command-line tool that tries to snoop on a nameserver's cache; host_discovery.py bruteforce searches for all actual hosts using a reverse-lookup-into-forward-lookup strategy.
  
  Current features to this repo:
    1. tests for the different scripts, libraries, etc.
    2. cache-snooping script
    3. bruteforce host discovery script 
    4. bruteforce dictionary lookup script
    5. A main script that packages these together
