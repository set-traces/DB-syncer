
import sys

from api import *

def getHelp():
    print("Missing argument: Server. Use sync like this: python3 sync.py [server (local or centralized)] [flags]")
    print("Potentional flags")
    print("--use-http: Forces the use of http over https (local will always use http")

if __name__ == '__main__':
    print("Welcome to set traces data sync")

    args = sys.argv
    if len(args) < 2:
        print("not enough arguments")
        getHelp()
        sys.exit(1)
    
    protocol = "https://"

    if ("--use-http" in args or args[1] == "local"):
        protocol = "http://"

    localUrl = protocol+"localhost:8080"
    centralizedUrl = protocol+"backend.settraces.com"

    local = False
    centralized = False

    if args[1] == "help":
        getHelp()
        sys.exit(1)

    if args[1] == "local":
        url = localUrl
    elif args[1] == "centralized":
        url = centralizedUrl
    else:
        print("Missing argument: Server. Use sync like this: python3 sync.py [server (local or centralized)] [flags]")
        print("Use python3 sync.py help - to get more help")
    print(url)

    getProjects()