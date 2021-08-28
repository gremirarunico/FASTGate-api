#!/usr/bin/pyhthon3

# An example of use of the library
from FASTGate import FASTGate

if (__name__ == "__main__"):
    # Hard coded credentials (this is bad, but this is just an example)
    myFast = FASTGate("username", 'password')
    myFast.verbose = 0
    myFast.connect()
    myFast.load()
    # myFast.isLogged()
    myFast.smartLogin()
    print(myFast.info()['uptime'])
    myFast.save()
    #myFast.reboot()
    # myFast.logout()
