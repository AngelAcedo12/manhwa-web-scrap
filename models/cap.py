class cap:
    name: str
    chapter: int
    imgUrls = []
    _id:str

    def __init__(self, name, chapter,imgUrls,_id):
        self.name = name
        self.chapter = chapter
        self._id = _id
        self.imgUrls = imgUrls

