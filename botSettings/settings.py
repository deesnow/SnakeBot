from pathlib import Path
import json

#Global variables

PROD = True #Set this to True if production
DB_PROD = True #Set this to True if production


def discord_setup(path):
    if Path.is_file(path):
        with open(path, 'rt') as discord_settings:
            return json.load(discord_settings)
    else:
        return None
        
path = Path.cwd() / 'botSettings/settings.json'
ds = discord_setup(path)

if PROD:
    release = "production"

else:
    release = "development"



VERSION = ds[release]['version']
TOKEN = ds[release]['token']
if DB_PROD:
    DB_HOST = ds[release]['db_host']
    DB_PORT = ds[release]['db_port']
else:
    DB_HOST = ds['dev_db']['db_host']
    DB_PORT = ds['dev_db']['db_port']
DB_USER = ds[release]['db_user']
DB_PASS = ds[release]['password']
DB_AUTHSource = ds[release]['authSource']
DB_AUTHMech = ds[release]['authMechanism']
EXTENSIONS = ds[release]['extensions']
# MONGO_CLIENT = 'mongodb://' + DB_HOST + ':' + DB_PORT + '/'
CHANNEL_ID = ds[release]['botchannel_id']
HELPAPI_USER = ds[release]['helpapi_user']
HELPAPI_PASS = ds[release]['helpapi_pass']
SHITTYBOT = ds[release]['shittybot']
DB_SERVER_CONNECTION = False
SHITTYBOT_REQUESTS = 0
CRINOLO_IP = ds[release]['crinolostat_ip']
CRINOLO_PORT = ds[release]['crinolostat_port']
ROLES = ds['roles']