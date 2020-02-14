from database import db, dbPictures


class User(db.Model):
    email = db.Column(db.String(80), primary_key=True, unique=True)
    password = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    birthday = db.Column(db.String(80))
    picsLiked = db.Column(db.String(2000))
    picsUnliked = db.Column(db.String(2000))
    profilePicUrl = db.Column(db.String(250))

    email_confirmed = db.Column(db.Boolean())

    def __init__(self, email, password, username, name, lastname, birthday=None):
        self.email = email
        self.password = password
        self.username = username
        self.name = name
        self.lastname = lastname
        self.email_confirmed = False
        self.birthday = birthday
        self.picsLiked = ""
        self.picsUnliked = ""
        self.profilePicUrl = "http://greenboxprofiles.s3.amazonaws.com/default.jpg"

    def appendLikedPics(self, url):

        if url in self.picsUnliked:
            self.picsUnliked = self.picsUnliked.replace(" " + url, "")

        self.picsLiked += " " + url

    def removeFromLikedPics(self, url):
        if url in self.picsLiked:
            self.picsLiked = self.picsLiked.replace(" " + url, "")

    def getPicsLikes(self):
        result = self.picsLiked.lstrip(" ").split(" ")

        if result == ['']: return []

        return result

    def appendUnlikedPics(self, url):

        if url in self.picsLiked:
            self.picsLiked = self.picsLiked.replace(" " + url, "")

        self.picsUnliked += " " + url

    def removeFromUnlikedPics(self, url):
        if url in self.picsUnliked:
            self.picsUnliked = self.picsUnliked.replace(" " + url, "")

    def getPicsUnlikes(self):

        result = self.picsUnliked.split(" ")

        if result == ['']: return []
        return result

    def __repr__(self):
        return '<User %r>' % self.email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.username)


class Picture(dbPictures.Model):
     name = dbPictures.Column(dbPictures.String(80), primary_key=True, unique=True)
     url = dbPictures.Column(dbPictures.String(80), unique=True)
     txt = dbPictures.Column(dbPictures.String(80))
     likes = dbPictures.Column(dbPictures.String(80))


     def __init__(self, name, url, txt, likes):
          self.name = name
          self.url = url
          self.txt = txt
          self.likes = likes

     def get_url(self):
          return str(self.url)
     def get_txt(self):
          return str(self.txt)
     def get_likes(self):
          return int(self.likes)
