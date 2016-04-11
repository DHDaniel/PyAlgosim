import os

try:
    os.system("rm stocks.db")
    os.system("echo > stocks.db")
    print "Database has been wiped and reset"
except:
    print "An unexpected error occured"
