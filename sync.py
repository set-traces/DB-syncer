
import sys

from api import RESTHandler, getProjects, createNewProject, createNewScriptType
import parsed
from time import sleep

def getHelp():
    print("Missing argument: Server. Use sync like this: python3 sync.py [server (local or centralized)] [flags]")
    print("Potentional flags")
    print("--use-http: Forces the use of http over https (local will always use http")

def getProjectId(handler):
    projects = getProjects(handler)
    projects.append({'id':'', 'name':'Create new project...'})
    print("Choose project to upload to")
    for project, counter in zip(projects, range(len(projects))):
        print("%2i: %s" %(counter, project['name']))
    print("Select project (c to cancel)")
    chosen = input(">>>")
    try:
        numb = int(chosen)
    except:
        # value is not a number
        print("Bye!")
        sys.exit(1)
    if projects[numb]['id'] == '': # create new project
        id = createNewProject(handler)
    else:
        id = projects[numb]['id']
    
    return id


def getTypes(handler, id):
    print("\n\n")
    print("Time to choose script types")
    result = handler.get("/project/")
    j = result.json()
    spesificProject = {}
    
    for p in j:
        if p['id'] == id:
            spesificProject = p
    sts = spesificProject['scriptTypes']
    sts.append({'id':'', 'name':'Create new script type...'})
    if (len(sts) == 1):
        print("No existsing types found")
        return createNewScriptType(handler, id)
    else:
        for t, i in zip(sts, range(len(sts))):
            print("%2i: %s" % (i, t['name']))
        
        
        print("Choose script type (c to cancel)")

        try:
            n = int(input(">>>"))
        except:
            print("bye!")
            sys.exit(1)
        if sts[n]['id'] == '': # create new
            return createNewScriptType(handler, id)
        return sts[n]['id']

def uploadParsed(handler, projectId, scriptId):
    print("Choose mode: (c to cancel)")
    print(" 0: upload folder")
    print(" 1: upload file")
    try:
        c = int(input(">>>"))
    except:
        print("bye!")
        sys.exit(1)
    options = [parsed.folder, parsed.fileUpload]
    if (c > 1 or c < 0):
        print("wrong format")
        return uploadParsed(handler, projectId, scriptId)
    return options[c](handler, projectId, scriptId)

def main():
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
    
    print("\n")
    print("Using backend located at: %s" % url)
    print("\n")

    handler = RESTHandler(url)

    id = getProjectId(handler)
    print("Using projectId: %s" % id)
    typeId = getTypes(handler, id)
    print("\n")
    print("Using script type id: %s" % typeId)
    print("\n")
    print("\n")
    print("Choose mode:")
    print("0. Upload parsed data")
    sleep(.5)
    print("... Choosing Upload due to lack of other choices")

    options = [uploadParsed]

    options[0](handler, id, typeId)

if __name__ == '__main__':
    main()