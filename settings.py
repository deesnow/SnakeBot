import os
import json

#Global variables

PROD = False #Set this to True if production


def discord_setup(default_path='settings.json'):
    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as discord_settings:
            return json.load(discord_settings)
        
      
ds = discord_setup()

if PROD:
    release = "production"

else:
    release = "development"



VERSION = ds[release]['version']
TOKEN = ds[release]['token']
DB_HOST = ds[release]['db_host']
DB_PORT = ds[release]['db_port']
DB_USER = ds[release]['db_user']
DB_PASS = ds[release]['password']
DB_AUTHSource = ds[release]['authSource']
DB_AUTHMech = ds[release]['authMechanism']
# MONGO_CLIENT = 'mongodb://' + DB_HOST + ':' + DB_PORT + '/'
CHANNEL_ID = ds[release]['botchannel_id']



 



