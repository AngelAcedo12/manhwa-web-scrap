from os import path,mkdir
from pathlib import PurePath
from requests import get
from bs4 import BeautifulSoup
import json
from cap import cap
from manga import manga
dir_saved = str(input("Enter the path to the save Manga: "))
id = str(input("Enter the id: "))
urlPri = f'https://manhwawebbackend-production.up.railway.app/chapters/see/{id}'
urlPriObteinManga = f'https://manhwawebbackend-production.up.railway.app/manhwa/see/{id}'

def obteinManga(url):
    response = get(url)
    
    if response.ok:
        content = response.text
        jsonContent = parseJson(content)
        manga = jsonToObjManga(jsonContent)
        print(f"Obtenido: {manga._nombre} ✅ \n")
        download(manga)
        return True
    else:
        print('Error al obtener el manga: '+ response.status_code)
        return False



def download(manga):
    maxCap = manga._numero_cap
    capComplete = 0
    errors_in_download = 0
    print(f"Downloading {manga._nombre}... \n")

    dir_name = refactorDirName(manga._nombre) 
    dir_path = path.join(dir_saved,dir_name)
    print(f"Path: {dir_path} \n")
    try:
        mkdir(dir_path)
    except Exception as e:  
        # print(f"Error: {e}")   
        print(f"")
        
    for i in range(1, maxCap+1):
            # Create the URL for the cap
            url = urlPri+'-'+str(i)
            print('URL: '+ url)
            file_name = PurePath(url).name
            print(f"Downloading {file_name}...")
            try: 
                mkdir(path.join(dir_path, file_name),dir_fd=None)
            except Exception as e:
                print(f"")
           
            try:
                downloadCap(url, dir_path, file_name)    
            except Exception as e:
                # print(f"Error: {e}")
                continue                           
            finally:
                capComplete += 1
                print(f"Total caps downloaded: {capComplete} | {maxCap} \n ")
                print(f'{obteinProgress(maxCap, capComplete)} \n')
                print(f"Errors in download: {errors_in_download} \n") 
                        
                

def parseJson(content):
    return json.loads(content)

def jsonToObj(jsonContent):
    return cap(jsonContent['name'], jsonContent['chapter']['chapter'],jsonContent['chapter']['img'], jsonContent['_id'])

def jsonToObjManga(jsonContent):
    return manga(jsonContent['name_esp'], jsonContent['numero_cap_esp'])

# Refactor the name of the directory to avoid errors and convert it to a valid name
def refactorDirName(dir_name):
    return dir_name.replace(' ', '_').replace(':', '').replace('?', '').replace('¿', '').replace('¡', '').replace('!', '') 

def downloadCap(url, dir_path, file_name):
    # Get the content of the cap
    responseCap = get(url)
    if responseCap.ok:
        content= responseCap.text
        # Parse the content of the cap to json
        jsonContent = parseJson(content)    
        # Create an object cap from the json
        cap = jsonToObj(jsonContent)
        count = 1
        for img in cap.imgUrls:
            suffix = PurePath(img).suffix
            imgName = PurePath(img).name
            imgResponse = get(img)
            if imgResponse.ok:
                # Save the image
                numberFile = str(count)
                with open(path.join(dir_path, file_name, f'{numberFile}{suffix}'), 'wb') as file:
                                    
                    file.write(imgResponse.content)
                                                    
                    count += 1
            else:
                print(f"Error downloading image {imgName} ❌")
                errors_in_download += 1


def obteinProgress(maxCap, current):
    progress = ''
    actualProgress = current/maxCap * 10
   
    
    for i in range(0, 10):
        
        if i <= actualProgress :
            progress += '█'
        else:
            progress += '▓'
    return progress + f' {actualProgress * 10}%'




if __name__ == '__main__':
    status = obteinManga(urlPriObteinManga)
    if status:
        print("Manga downloaded successfully ✅")
    else:
        print("Error downloading manga ❌")
    
   
