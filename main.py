from scrapedManga import scapeManga
import time
from convertTime import convertTime 
import threading 
from jsonParse import jsonParse
from fastapi import FastAPI


dirPath = 'C:/Users/Usuario/Downloads/manga'



def dowmloadManga():
   
    id = str(input("Enter the id: "))
    scrape = scapeManga(id=id)
    initTime = time.time()
    status = scrape.obteinManga()
    if status:
        print("Manga downloaded successfully ✅")
        print(f"Total time: {convertTime().convert(time.time()-initTime)}")
    else:
        print("Error downloading manga ❌")

def lastRelated():
    scrape = scapeManga()
    initTime = time.time()
    scrape.obteinLastRelated()

def loadConfig():
    try: 
        with open('config.json','r') as file:
            content = file.read()
            file.close()
            json = jsonParse(content)
            dirPath = json["localPath"]
            print(f"\n \n --- Local path: {dirPath} --- \n \n" )

       
    except Exception as e:
        print(f"Error: {e}")
        return False
    

def main():
    loadConfig()
    print("1. Download manga")
    print("2. Obtein last related")
    print("3. Exit")
    option = int(input("Enter an option: "))
    if option == 1:
        threading.Thread(dowmloadManga()).start()
        main()
    elif option == 2:
        threading.Thread(lastRelated()).start()
    elif option == 3:
        exit()
    else:
        print("Invalid option")
        main()
        


try:
    main()
except Exception as e:
    print(f"Error: {e}")
    main()








          
    
    
   