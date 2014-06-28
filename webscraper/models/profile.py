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

    def get_url_profile(self, **kwargs):
        '''
        Returns URL for retrieving user's profile.
        This method must be implemented by subclasses.
        '''
        pass

    def as_profile_dict(self):
        '''
        Convert a specific profile (i.e. Facebook Profile) into WebScraper Profile
        This method must be implemented by subclasses.
        '''


class Facebook(Profile):

    def get_url_profile(self, **kwargs):
        return "http://graph.facebook.com/v1.0/"+kwargs['username']

    def as_profile_dict(self, **kwargs):
        #TODO: usar os atributos com self ou entai usar o __init__
        profile = Profile()
        profile._id = ObjectId()
        profile.name = kwargs['first_name'] + " " + kwargs['last_name']
        profile.username = kwargs['username']
        profile.short_description = "A web developer at globo.com"
        profile.image = "user profile image"
        profile.popularity = 10
        profile.updated = datetime.now()

        return profile


class Twitter(Profile):
    pass


# simply add new classes and implement methods to add new places where scrap from