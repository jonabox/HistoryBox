from models import Picture
from random import choice
from urllib.request import urlopen

class RandomPicture:

    def __init__(self):
        picCount = Picture.query.count()
        randomName = str(choice(range(1, picCount + 1)))
        picture = Picture.query.filter_by(name=randomName).first()

        self.name = picture.name
        self.url = picture.url
        self.txt = str(urlopen(picture.txt).read()).strip("b'")
        self.likes = picture.likes

    def getName(self): return self.name

    def getUrl(self): return self.url

    def getTxt(self): return self.txt

    def getLikes(self): return self.likes

    def randomize(self):
        picCount = Picture.query.count()
        randomName = str(choice(range(1, picCount + 1)))
        picture = Picture.query.filter_by(name=randomName).first()

        self.url = picture.url
        self.txt = str(urlopen(picture.txt).read()).strip("b'")
        self.likes = picture.likes

