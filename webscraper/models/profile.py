# coding: utf-8
from bson.objectid import ObjectId
from datetime import datetime
from webscraper.repository import ProfileRepository, Property, Collection


class Profile(Collection, ProfileRepository):

    __collection__ = 'profile'

    _id = Property(ObjectId, "profile id")
    name = Property(unicode, "user name")
    username = Property(unicode, "username")
    short_description = Property(unicode, "user name")
    image = Property(unicode, "user profile image")
    popularity = Property(int, "user popularity")
    updated = Property(datetime, "updated time")



class Facebook(Profile):
    pass


class Twitter(Profile):
    pass
