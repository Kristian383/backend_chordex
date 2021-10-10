from collections import UserList
from flask import Flask
from flask_restful import Api
# from flask_jwt import JWT
from flask_jwt_extended import JWTManager


from security import authenticate, identity

from resources.user import UserRegister, User, UserList, UserLogin
from resources.artist import Artist, ArtistList, ArtistUserList
from resources.song import Song, SongList, UsersSongList
from resources.website import Website, WebsiteList
from resources.user_notes import UserNotes, UserNotesList

from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config['JWT_AUTH_URL_RULE'] = '/login'        #jwt flask
app.secret_key = "kiki"

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


# jwt = JWT(app, authenticate, identity)             # vraca access token
jwt = JWTManager(app)             # vraca access token


api.add_resource(UserRegister, "/register")
api.add_resource(UserList, "/users")
api.add_resource(User, "/user/<int:user_id>")

api.add_resource(UserLogin, '/login')


# vraca sve userove artiste s pjesmama
api.add_resource(ArtistList, "/artists")
# ispisuje sve pjesme odredenog artista   (za odredenog usera)
api.add_resource(ArtistUserList, "/artist/<string:username>")
# ispisuje sve pjesme artista odredenog usera
api.add_resource(Artist, "/artist/<string:name>")

api.add_resource(SongList, "/songs")
api.add_resource(UsersSongList, "/songs/<string:username>")
api.add_resource(Song, "/song/<string:username>")
# api.add_resource(Song, "/song/<int:user_id>")

# ovo sluzi za ubacivanje webvssite linkova
api.add_resource(Website, "/website/<string:username>")
# dohvacanje svih websiteova od usera
api.add_resource(WebsiteList, "/websites/<string:username>")
#api.add_resource(WebsiteList, "/websites")

# api.add_resource(UserNotesList, "/notes")   #provjera za developera
api.add_resource(UserNotes, "/notes/<string:username>")


# api.add_resource(User, "/user/<string:username>")


if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True, port=5000)
