from sqlalchemy import Column, Integer, String
import datetime
from app.database import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    # title = db.relationship('Title', backref = 'title', lazy = 'dynamic')
    pw_hash = db.Column(db.String(480))
    # just use a name for all those cultures that have no middle, first, etc. distinction
    name = db.Column(db.String(240))
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    created_on = db.Column(db.DateTime)
    images = db.relationship("WordCloudImage", backref="user")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % (self.nickname)

##########################################

class Title(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
          
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Title: %r>' % self.title


class WordCloudImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    twitter_username = db.Column(db.String(60))
    image_url = db.Column(db.String(120))
    created = db.Column(db.DateTime, server_default=db.func.now())


class TweetsStack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    twitter_username = db.Column(db.String(60))
    tweets_json = db.Column(db.Text)
    last_tweet_id = db.Column(db.String(50))
    created = db.Column(db.DateTime, server_default=db.func.now())
