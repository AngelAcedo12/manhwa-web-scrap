from os import path,mkdir
from pathlib import PurePath
from requests import get
from bs4 import BeautifulSoup
import json
from cap import cap

dir_saved = str(input("Enter the path to the save Manga: "))
id = str(input("Enter the id: "))
urlPri = f'https://manhwawebbackend-production.up.railway.app/chapters/see/{id}'
maxCap = int(input("Enter the number of cap: ")) 
name = str(input("Enter the name of the manga: "))

def download(urlPri, maxCap):
    capComplete = 0
    errors_in_download = 0
    dir_path = path.join(dir_saved,name)
    try:
        mkdir(dir_path)
    except Exception as e:  
        print(f"Error: {e}")   
         
        
    for i in range(1, maxCap+1):
            
            url = urlPri+'-'+str(i)
            print('URL: '+ url)
            file_name = PurePath(url).name
            print(f"Downloading {file_name}...")
            try: 
                mkdir(path.join(dir_path, file_name),dir_fd=None)
            except Exception as e:
                print(f"")
           
            try:
                    responseCap = get(url)
                    
                    if responseCap.ok:
                        print('--Content find--- \n') 
                        content= responseCap.text
                        jsonContent = parseJson(content)    
                        cap = jsonToObj(jsonContent)
                        for img in cap.imgUrls:
                            imgName = PurePath(img).name
                            imgResponse = get(img)
                            if imgResponse.ok:
                                with open(path.join(dir_path, file_name, imgName), 'wb') as file:
                                    print(f"Image {imgName} downloaded")
                                    file.write(imgResponse.content)
                                                    
                            else:
                                print(f"Error downloading image {imgName} ❌")
                    
            except Exception as e:
                print(f"")
                errors_in_download += 1
                continue                           
            finally:
                capComplete += 1
                print(f"Cap {i} downloaded  ✅" )
                print(f"Total caps downloaded: {capComplete} \n " + "Progress: " + str((capComplete/maxCap)*100) + "%") 
                        
                
def parseHtml(content):
    return BeautifulSoup(content, 'json.parser')

def parseJson(content):
    return json.loads(content)

def jsonToObj(jsonContent):
    return cap(jsonContent['name'], jsonContent['chapter']['chapter'],jsonContent['chapter']['img'], jsonContent['_id'])

if __name__ == '__main__':
    download(urlPri, maxCap)
    print(' --- Download complete --- ✅')
