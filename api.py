from fastapi import FastAPI
from jsonParse import jsonParse
from os import path,listdir
from formaters import refactorDirName
from pathlib import PurePath
from scrapedManga import scapeManga

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

@app.get("/see/{id}")
async def read_item(id:str):
    s = scapeManga()
    s.id = id
    return s.obteinUrlManga(id)
        
@app.get("/see/{id}/{cap}")
async def read_item(id:str,cap:int):
    s = scapeManga()
    return s.obteinUrlCap(id,cap)

@app.get("/last")
async def read_item():
    s = scapeManga()
    return s.obteinLastRelated()    

