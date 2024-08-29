from PIL import Image
from os import remove
class optimizer:
    path: str
    mode: str
    quality: int

    def __init__(self, path,mode,quality):
        self.path = path
        self.mode = mode
        self.quality = quality
        pass

    def optimize(self,removed):
        try: 
            img = Image.open(self.path)
            pathOptimzed= f'{self.path[:-4]}.webp'
            img.save(pathOptimzed,format=self.mode,quality=self.quality, optimize=True)
            if removed:
                remove(self.path)
            return True
        except Exception as e: 
            print(f"Error: {e}")
            return False