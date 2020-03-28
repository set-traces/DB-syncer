
import requests
import json
import sys

def getProjects(handler):
    result = handler.get("/project/")
    return result.json()

def createNewProject(handler):
    print("\n\n")
    print("Creating new project!!")
    print("Enter new project name")
    name = input(">>>")
    print("\n")
    print("Cool name! Let's enter a project description")
    desc = input(">>>")
    print("\n")
    print("Great!! I'm creating a new project with name %s" % name)
    res = handler.post('/project/', {'name':name, 'description':desc})
    if (res.ok):
        return res.json()['id']
    else:
        print("Backend not available")
        sys.exit(1)
        return ""


def createNewScriptType(handler, id):
    print("\n\n")
    print("Time to create new scrip type")
    print("Enter name: (c to cancel)")
    name = input(">>>")
    if name == 'c':
        print("Bye!")
        sys.exit(1)
    res = handler.post('/project/%s/type/' % id, {'name':name})
    return res.json()['id']

    
def createScript(name, desc, typeId):
    pass

class RESTHandler:
    def __init__(self, url):
        self.url = url
    
    def _getUrl(self, extension):
        return self.url+"/api"+extension

    def get(self, extension):
        requestsUrl = self._getUrl(extension)
        return requests.get(requestsUrl)

    def post(self, extension, data):
        requestsUrl = self._getUrl(extension)
        return requests.post(requestsUrl, json=data)