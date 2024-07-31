import sys
import json

def getParams():
    params = {}
    for arg in sys.argv:
        if arg.startswith("--"):
            parts = arg.split("=")  
            params.update({parts[0][2:]: parts[1]})
    return params

def isfloat(input):
    try:
        float(input)
        return True
    except ValueError:
        return False

def pairValues(param, di, parent = ""):
    if param == "target":
        return
        
    if param in di:
        if isinstance(di[param], dict):
            pairValues(di[param])
        elif isinstance(di[param],bool): 
            di.update({param: True if (params[param] == True or params[param].lower() == "true") else False} if parent == "" 
                    else {param: True if (params[f"{parent}.{param}"] == True or params[f"{parent}.{param}"].lower() == "true") else False})
            return
        elif isfloat(di[param]):  
            di.update({param: float(params[param])} if parent == "" else {param: float(params[f"{parent}.{param}"])})
            return
        elif di[param].isdigit():  
            di.update({param: int(params[param])} if parent == "" else {param: int(params[f"{parent}.{param}"])})
            return       
        elif isinstance(di[param],str):  
            di.update({param: params[param]} if parent == "" else {param: params[f"{parent}.{param}"]})
            return
        else:
            print(f"unknown type: {parent}: {param}")
            return
    else:
        if param.find(".") > -1:
            parts = param.split(".",1)
            if parent == "": pairValues(parts[1], di[parts[0]], parts[0])
            else: pairValues(parts[1], di[parts[0]], f"{parent}.{parts[0]}" )
        
fileContentPrefix = "export const environment = "
params = getParams()
target = params["target"]

with open(target,"r") as f:
    data = f.read().replace(fileContentPrefix,"").strip()    
    idxSemi = data.rfind(';')
    if idxSemi > -1: data = data[0:idxSemi]

loaded = dict(json.loads(data))

for param in params:  
    pairValues(param, loaded)

with open(target,"w") as f:
    f.write(f"{fileContentPrefix}{json.dumps(loaded)};")

# Sample scripts
# & E:/Python/python.exe e:/projects/testbeds/python/backfill/backfill.py --target=environment.ts --images.account.token.field1=SomeVal --images.account.acctId=SomeVal --production=false --apiUrl=http://someserver.com --shopifyBridgeUrl=http://www.someothersite.com --auth.domain=tests --auth.clientId=west --someField1=4.5 
# & E:/Python/python.exe e:/projects/testbeds/python/backfill/backfill.py --images.account.token.field1=SomeVal
# --images.account.token.field1=SomeVal --images.account.acctId=SomeVal --production=false --apiUrl=http://someserver.com 
# --shopifyBridgeUrl=http://www.someothersite.com --auth.domain=tests --auth.clientId=west --someField1=4.5
