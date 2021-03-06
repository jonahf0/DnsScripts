#    the goal of this script was to write a program that reads from the output of the fierce.pl perl script
#and parses a list of words from it for bruteforce use against other similar domains (ex: getting output from
#lsu.edu to use against fsu.edu).
#
#   the get_words_from_line function generates an array of relevant words from each line with the format:
#       x.x.x.x   example.com
#with "x.x.x.x" being an IP address and "example.com" bein a hostname. Then, the script creates a list
#of all relenvant words from that domain and then writes it to the generated_wordslist.txt file in resources.
#The idea behind the script is that words found in a domain's hostname space (ex: vpn.example.com or ftp.example.com
#would produce ftp, vpn, and example) would be relevant in bruteforce methods used against other similar domains

def get_words_from_line(line):
    
    try:
    
        split_line = line.split()

        host = split_line[1]

        words = host.split(".")
    
        return words

    except:

        return []

with open("from_fierce.txt", "r") as f:

    list_of_words = set(
            sum(
                [ get_words_from_line(line) for line in f ],
                []
            )
        )

with open("generated_wordlist.txt", "w") as f:
    [ f.write(i+"\n") for i in list_of_words ]
