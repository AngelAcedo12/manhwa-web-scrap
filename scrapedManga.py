from os import path,mkdir, remove
from pathlib import PurePath
from requests import get
from bs4 import BeautifulSoup
import json
from cap import cap
from manga import manga
from optimizer import optimizer
import threading
from convertTime import convertTime
import time
class scapeManga:
    
    dir_saved = ''
    id = ''
    urlPri = ''
    urlPriObteinManga = ''

    def __init__(self, dir_saved, id):
        self.dir_saved = dir_saved
        self.id = id
        self.urlPri = f'https://manhwawebbackend-production.up.railway.app/chapters/see/{id}'
        self.urlPriObteinManga = f'https://manhwawebbackend-production.up.railway.app/manhwa/see/{id}'
        pass
    
    def parseJson(self,content):
        return json.loads(content)

    def jsonToObj(self,jsonContent):
        return cap(jsonContent['name'], jsonContent['chapter']['chapter'],jsonContent['chapter']['img'], jsonContent['_id'])

    def jsonToObjManga(self,jsonContent):
        return manga(jsonContent['name_esp'], jsonContent['numero_cap_esp'])

    # Refactor the name of the directory to avoid errors and convert it to a valid name
    def refactorDirName(self,dir_name):
        return dir_name.replace(' ', '_').replace(':', '').replace('?', '').replace('¿', '').replace('¡', '').replace('!', '') 
    
    def downloadCap(self,url, dir_path, file_name):
            # Get the content of the cap
            responseCap = get(url)
            if responseCap.ok:
                content= responseCap.text
                # Parse the content of the cap to json
                jsonContent = self.parseJson(content)    
                # Create an object cap from the json

                cap = self.jsonToObj(jsonContent)
                with open(path.join(dir_path, file_name, f'{cap.name}.json'), 'w') as file:
                    file.write(content)
                    file.close()
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
                        if existFile == False:

                            with open(path.join(dir_path, file_name, oldPath), 'wb') as file: 
                                
                                file.write(imgResponse.content)
                                file.close()


                            if suffix == '.jpg' or suffix == '.jpeg':
                                oldPath = path.join(dir_path, file_name, f'{numberFile}{suffix}')
                                threading.Thread(target=self.optimizedImage, args=(oldPath,)).start()
                        else: 
                            # print(f"File {numberFile} already exists ✅")
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
        dir_name = self.refactorDirName(manga._nombre) 
        dir_path = path.join(self.dir_saved,dir_name)
      
        print(f"Downloading {manga._nombre}... \n")

        # print(f"Path: {dir_path} \n")
        
        try:
            mkdir(dir_path)
          
        except Exception as e:  
            # print(f"Error: {e}")   
            # print(f"Dir CREATE")
            pass	
        
        with open(path.join(dir_path, f'{self.refactorDirName(manga._nombre)}.json'),'w') as file:
            file.write(jsonContent)
            file.close()

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
                    print(f"")
            
                try:
                    self.downloadCap(url, dir_path, file_name)    
                   
                except Exception as e:
                    # print(f"Error: {e}")
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
            jsonContent = self.parseJson(content)
      
            manga = self.jsonToObjManga(jsonContent)
            print(f"Obtenido: {manga._nombre} ✅ \n")
            self.download(manga,content)
            return True
        else:
            print('Error al obtener el manga: '+ response.status_code)
            return False


    # Optimize the image using the optimizer class 
    def optimizedImage(self, path):
        op = optimizer(path,  'WEBP')
        responseOptimize = op.optimize()
        if(responseOptimize):
            # print(f"Optimized {path} ✅")
            pass
        else:
            print(f"Error optimizing {path} ❌")





