# antique-watchdog

Antique-watchdog alias antique book store watchdog.

Issues:
 - script still only prints results in terminal
 - script can only get query with no restrictions (like just particular publisher or language or year of releasing)
 - code looks messy
 - script undivided into smaller functions, probably needs to refactor
 - sometimes results are contaminated by nonsense (based on inconsistency of data)

To do:
 - instead of single query to allow user to define query and restrictions, probably use csv and some dict instead of single string
 - to decide if let the program or the script to find the queries file and separate queries
 - to make user to define time to run this script via commandline tool (and later via gui maybe?)