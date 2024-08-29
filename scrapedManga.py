from os import path,mkdir, remove
from pathlib import PurePath
from requests import get
from bs4 import BeautifulSoup
from jsonParse  import jsonParse
from models.cap import cap
from models.manga import manga
from optimizer import optimizer
import threading
from convertTime import convertTime
import time
from formaters import refactorDirName

class scapeManga:
    # Configuration parants
    optimizedImg= True
    replaceOptimized= True
    removeOriginal= True
    quality = 10
    debug = False

    id = ''
    urlPri = ''
    urlPriObteinManga = ''
    uriLastRelated = '' 
    localPath = ''

    def __init__(self, id):
        self.id = id
        self.urlPri = f'https://manhwawebbackend-production.up.railway.app/chapters/see/{id}'
        self.urlPriObteinManga = f'https://manhwawebbackend-production.up.railway.app/manhwa/see/{id}'
        self.uriLastRelated = f'https://manhwawebbackend-production.up.railway.app/manhwa/nuevos'
        self.loadConfig()
        pass

    def __init__(self):
        self.id = id
        self.urlPri = f'https://manhwawebbackend-production.up.railway.app/chapters/see/{id}'
        self.urlPriObteinManga = f'https://manhwawebbackend-production.up.railway.app/manhwa/see/{id}'
        self.uriLastRelated = f'https://manhwawebbackend-production.up.railway.app/manhwa/nuevos'
        self.loadConfig()
        pass
    
    def loadConfig(self):
        try:
            with open('config.json', 'r') as file:
                content = file.read()
                jsonContent = jsonParse(content)    
                self.optimizedImg = jsonContent['optimizedImg']
                self.replaceOptimized = jsonContent['replaceOptimized']
                self.removeOriginal = jsonContent['removeOriginal']
                self.debug = jsonContent['debug']
                self.quality = jsonContent['quality']
                self.localPath = jsonContent['localPath']
                file.close()
        except Exception as e:  
            if self.debug:
                print(f"Error: {e}")  
            pass
            

        return True
    

   

    def jsonToObj(self,jsonContent):
        return cap(jsonContent['name'], jsonContent['chapter']['chapter'],jsonContent['chapter']['img'], jsonContent['_id'])

    def jsonToObjManga(self,jsonContent):
        return manga(jsonContent['name_esp'], jsonContent['numero_cap_esp'])


    
    def downloadCap(self,url, dir_path, file_name):
            # Get the content of the cap
            responseCap = get(url)
            if responseCap.ok:
                content= responseCap.text
                # Parse the content of the cap to json
                jsonContent = jsonParse(content)    
                # Create an object cap from the json

                cap = self.jsonToObj(jsonContent)
                try:
                    with open(path.join(dir_path, file_name, f'{refactorDirName(cap.name)}.json'), 'w') as file:
                        file.write(content)
                        file.close()
                except Exception as e:
                    if self.debug:
                        print(f"Error: {e}")  
                    pass
                count = 1
                for img in cap.imgUrls:
                    suffix = PurePath(img).suffix
                    imgName = PurePath(img).name
                    imgResponse = get(img)
                    oldPath = path.join(dir_path, file_name, f'{count}{suffix}')
                    if imgResponse.ok:
                        # Save the image
                        numberFile = str(count)
                        existFile = path.exists(path.join(dir_path, file_name, f'{numberFile}.webp'))
                        
                        if existFile == False or self.replaceOptimized: 

                            with open(path.join(dir_path, file_name, oldPath), 'wb') as file: 
                                
                                file.write(imgResponse.content)
                                file.close()
                                

                            if suffix == '.jpg' or suffix == '.jpeg' or self.replaceOptimized:

                                oldPath = path.join(dir_path, file_name, f'{numberFile}{suffix}')
                                threading.Thread(target=self.optimizedImage, args=(oldPath,)).start()
                        else: 
                            print(f"File {numberFile} already exists ✅")
                            pass
                        count += 1
                    else:
                        print(f"Error downloading image {imgName} ❌")
                        errors_in_download += 1
            
    def obteinProgress(self,maxCap, current):
        progress = ''
        actualProgress = current/maxCap * 10
        for i in range(0, 10):
            
            if i <= actualProgress :
                progress += '█'
            else:
                progress += '▓'
        return progress + f' {actualProgress * 10}%'
    

    def download(self, manga, jsonContent):
        maxCap = manga._numero_cap
        capComplete = 0
        errors_in_download = 0
        dir_name = refactorDirName(manga._nombre) 
        dir_path = path.join(self.localPath,dir_name)

        print(f"Downloading {manga._nombre}... \n")

        try:
            mkdir(dir_path)
        except Exception as e:  
            if self.debug:
                print(f"Error: {e}")  
            	
        try:
            with open(path.join(dir_path, f'{refactorDirName(manga._nombre)}.json'),'w', encoding="utf-8") as file:
                file.write(jsonContent)
                file.close()
        except Exception as e:
            if self.debug:
                print(f"Error: {e}")  
            pass
        for i in range(1, maxCap+1):
                # Create the URL for the cap
                initTime = time.time()
                url = self.urlPri+'-'+str(i)
                # print('URL: '+ url)
                file_name = PurePath(url).name
                # print(f"Downloading {file_name}...")
                hilo: threading.Thread
                try: 
                    mkdir(path.join(dir_path, file_name),dir_fd=None)
                except Exception as e:
                    if self.debug:
                        print(f"Error: {e}")  
            
                try:
                    self.downloadCap(url, dir_path, file_name)    
                   
                except Exception as e:
                    if self.debug:
                        print(f"Error: {e}")  
                    continue                           
                finally:
                    capComplete += 1
                    
                    print(f"Total caps downloaded: {capComplete} | {maxCap} \n ")
                    print(f'{self.obteinProgress(maxCap, capComplete)} \n')
                    print(f"Errors in download: {errors_in_download} \n") 
                    print(f"Time: {convertTime().convert(time.time()-initTime)} \n")
                            
    # Get the manga from the URL
    def obteinManga(self):
        
        response = get(self.urlPriObteinManga)

        if response.ok:
            content = response.text
            jsonContent = jsonParse(content)
      
            manga = self.jsonToObjManga(jsonContent)
            print(f"Obtenido: {manga._nombre} ✅ \n")
            self.download(manga,content)
            return True
        else:
            print('Error al obtener el manga: '+ response.status_code)
            return False


    # Optimize the image using the optimizer class 
    def optimizedImage(self, path):
        op = optimizer(path,  'WEBP',10)
        responseOptimize = op.optimize(removed=self.removeOriginal)
        if(responseOptimize):
            # print(f"Optimized {path} ✅")
            pass
        else:
            print(f"Error optimizing {path} ❌")


    def obteinLastRelated(self):
        response = get(self.uriLastRelated)
        if response.ok:
            content = response.text
            json_content = jsonParse(content)
            try:
                mkdir(path.join(self.localPath,'lastRelated'))
            except Exception as e:  
                if self.debug:
                    print(f"Error: {e}")
                pass
            
            with open(path.join(self.localPath,'lastRelated','lastRelated.json'),'w', encoding="utf-8") as file:
            
                file.write(content)
                file.close()

            print(f"Obtenido: Last related ✅ \n")
            return json_content
        else:
            print('Error al obtener el manga: '+ response.status_code)
            return {}


    def obteinUrlManga(self,id):

        response = get(f'https://manhwawebbackend-production.up.railway.app/manhwa/see/{id}')

        if response.ok:
            content = response.text
            jsonContent = jsonParse(content)

            return {"data":jsonContent}
        else:
    
            return {"error": "Error al obtener el manga"}  
    
    def obteinUrlCap(self,id,cap):
        response = get(f'https://manhwawebbackend-production.up.railway.app/chapters/see/{id}-{cap}')

        if response.ok:
            content = response.text
            jsonContent = jsonParse(content)
          
            return {"data":jsonContent}
        else:
    
            return {"error": "Error al obtener el manga"}
        
    def obteinUrlLasted(self):
        response = get('https://manhwawebbackend-production.up.railway.app/manhwa/nuevos')

        if response.ok:
            content = response.text
            jsonContent = jsonParse(content)
            return {"data":jsonContent}
        else:
    
            return {"error": "Error al obtener el manga"}