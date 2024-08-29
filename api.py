from fastapi import FastAPI
from jsonParse import jsonParse
from os import path
from formaters import refactorDirName
from pathlib import PurePath

class config: 
    localPath: str
    def __init__(self,localPath):
        self.localPath = localPath
        pass

def loadConfig():
    with open('config.json','r') as file:
        
        content = file.read()
        file.close()
        json = jsonParse(content)
        localPath = PurePath(json["localPath"])

        print(f"\n \n --- Local path: {localPath} --- \n \n" )
        return config(localPath)

config = loadConfig()
app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/see/{name}")
async def read_item(name:str):
    print(config.localPath)
    route = path.join(config.localPath,refactorDirName(name),f'{refactorDirName(name)}.json')
    print(route)
    with open(route, 'r') as file:    
        content = file.read()
        file.close()
        return jsonParse(content)   
    

