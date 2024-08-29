from PIL import Image
from os import remove
class optimizer:
    path: str
    mode: str

    def __init__(self, path,mode):
        self.path = path
        self.mode = mode
        pass

    def optimize(self):
        try: 
            img = Image.open(self.path)
            pathOptimzed= f'{self.path[:-4]}.webp'
            img.save(pathOptimzed,format=self.mode, optimize=True)
            remove(self.path)
            return True
        except Exception as e: 
            print(f"Error: {e}")
            return False