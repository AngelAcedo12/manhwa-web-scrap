from scrapedManga import scapeManga
import time
from convertTime import convertTime 
import threading 
def dowmloadManga():
    dir_saved = str(input("Enter the path to the save Manga: "))
    id = str(input("Enter the id: "))
    scrape = scapeManga(dir_saved=dir_saved, id=id)
    initTime = time.time()
    status = scrape.obteinManga()
    if status:
        print("Manga downloaded successfully ✅")
        print(f"Total time: {convertTime().convert(time.time()-initTime)}")
    else:
        print("Error downloading manga ❌")


def main():

    print("1. Download manga")
    print("2. Exit")
    option = int(input("Enter an option: "))
    if option == 1:
        threading.Thread(dowmloadManga()).start()
        main()
    elif option == 2:
        exit()
    else:
        print("Invalid option")
        main()



if __name__ == '__main__':
  
        try:
            main()
        except Exception as e:
            print(f"Error: {e}")
          
    
    
   