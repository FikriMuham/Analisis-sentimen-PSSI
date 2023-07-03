import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    HOST = "localhost"
    DATABASE = "sentimen_app"
    USERNAME = "root"
    PASSWORD = ""
    JWT_SECRET_KEY = "Secret123"
    SQLALCHEMY_DATABASE_URI = 'mysql://'+USERNAME+':'+PASSWORD+'@'+HOST+'/'+DATABASE
    # SQLALCHEMY_DATABASE_URI = 'postgresql://keyhjbritoyqcj:804aadb24179eb9cbee788f80dea8929dd5d41030c271942fefb01f488d35ec4@ec2-35-173-83-57.compute-1.amazonaws.com:5432/dek1mr5jkf2kj9'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
