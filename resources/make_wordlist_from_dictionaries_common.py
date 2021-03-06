#   this was just a script to read from the /etc/dicionaries-common/words file on my Debian 10 distro;
#the goal was to create a wordslist WITHOUT the names and possessive nouns from that file in order to eventually
#pass it to a bruteforce lookup function
#
#   the script reads from the words file, creating an array of each non-proper or non-possessive noun, and
#the writes it to the wordslist.txt file in the resources directory

with open("/etc/dictionaries-common/words", "r") as f:
    wordlist = [ line for line in f if line[0].capitalize() != line[0] and line.find("'") == -1 ]

with open("wordslist.txt", "w") as f:
    f.write(
            "".join(wordlist)
        )
