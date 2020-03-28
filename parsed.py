
import json
from api import doCreateScript, doCreateRole, doCreateLine
import os


def fileUpload(handler, pid, stid):
    print("\n")
    print("Enter relative path to file:")
    rPath = input(">>>")
    data = readFile(rPath)
    handleFile(handler, pid, stid, data)

def handleFile(handler, pid, stid, data):
        
    scriptId = createScript(handler, pid, stid, data)
    nameToId = createRoles(handler, pid, scriptId, data)
    #criptId = "id"
    #nameToId = {'':'', 'Hatten': 'cdf21f92-9cf3-41d9-8a5c-1513bcb514ed', 'Henriette': '8e9371ef-6839-4156-b90d-d7537eb2b7e5', 'Henrik': '8a701344-8b34-485b-984a-06d684462c80', 'Roy': '025dcea8-0281-4c08-b3b7-40607d5abf2c', 'Noldar': '8f7b8e5d-8ea5-4193-9bff-6c08fb3fb369', 'Trangballe': '7d1a9180-6c05-47f2-88b2-e67c434e417f', 'Rekvisiter': '027f60db-ea35-4b61-a6dd-e39c8ccf1f57'}
    createLines(handler, pid, scriptId, data, nameToId)
    print("finished uploading %s", data['name'])

def createLines(handler, pid, scriptId, data, nameToId):
    added = 0
    for line in data['lines']:
        try:
            line['role'] = line['roles'][0]
        except:
            try:
                line['role'] = line['role']
            except:
                line['role'] = ""
            pass
        line['role'] = nameToId[line['role']]
        added += doCreateLine(handler, pid, scriptId, line['type'], line['text'], line['role'])
    return added == len(data['lines'])

def createRoles(handler, pid, stid, data):
    nameToId = {'': ''}
    for role in data['rolesMeta']:
        [name, id] = doCreateRole(handler, pid, stid, role['role'], role['description'])
        nameToId[name] = id
    return nameToId

def createScript(handler, pid, stid, data):
    return doCreateScript(handler, pid, stid, data['name'], data['description'])

def folder(handler, pid, stid):
    print("\n")
    print("Enter relative path to folder - finish with /")
    rPath = input(">>>")
    
    for f in os.listdir(rPath):
        pth = rPath + f
        print("handeling file %s" % pth)
        data = readFile(pth)
        handleFile(handler, pid, stid, data)
    

def readFile(p):
    with open(p, "r") as f:
        return json.loads(f.read())