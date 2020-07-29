import pymongo
import json
from dateutil.parser import parse
from botSettings import settings
import logging

class Dbhandler(object):
    '''Db handler function for the Snakebot. Contains all mongo db related method.'''
    # pylint: disable=too-many-instance-attributes
    # Eight is reasonable in this case.


    def __init__(self, logger=None):
        self.logger = logging.getLogger(__name__)

        if settings.DB_PROD:
            self.dbclient = pymongo.MongoClient(host=settings.DB_HOST,
                                                port=settings.DB_PORT,
                                                username=settings.DB_USER,
                                                password=settings.DB_PASS,
                                                authSource=settings.DB_AUTHSource,
                                                authMechanism=settings.DB_AUTHMech,
                                                connect=True,
                                                serverSelectionTimeoutMS = 5)
            
        else:
            self.dbclient = pymongo.MongoClient(host=settings.DB_HOST,
                                                port=settings.DB_PORT,
                                                connect=True,
                                                serverSelectionTimeoutMS = 5)
            
            # self.dbclient = pymongo.MongoClient(host=settings.DB_HOST,
            #                                     port=settings.DB_PORT,
            #                                     username=settings.DB_USER,
            #                                     password=settings.DB_PASS,
            #                                     authSource=settings.DB_AUTHSource,
            #                                     authMechanism=settings.DB_AUTHMech,
            #                                     connect=True)
        self.mydb = self.dbclient['mydatabase']
        #set DB Server status
        try:
            self.server_status = self.mydb.command("serverStatus")
            self.logger.info(f'Bot DB connection is initiated to {settings.DB_HOST} DB server')
            settings.DB_SERVER_CONNECTION = True
        except Exception as error:
            self.logger.error(f'DB connection is BROKEN')
            settings.DB_SERVER_CONNECTION = False
        

    def update_status(self):

        try:
            self.server_status = self.mydb.command("serverStatus")
            settings.DB_SERVER_CONNECTION = True
        except Exception as error:
            self.logger.error(f'DB connection is BROKEN')
            settings.DB_SERVER_CONNECTION = False

    def user_add(self, data):
        # Used by cmdReg
        self.col_discord = self.mydb['SnakeV2']
        self.user_data = data
        self.x = self.col_discord.find_one({"discord_id": str(self.user_data['discord_id'])})
        
        if self.x == None:
            try:
                self.inserted_data = self.col_discord.insert_one(self.user_data)
                self.logger.info("User {} added to the MongoDB".format(self.user_data['user_id']))
                return "Done"
            except Exception:
                self.logger.error('User add is FAILED', exc_info=True)
                return "Failed"
        else:
            
            try:
                self.inserted_data = self.col_discord.find_one_and_update({'discord_id': self.user_data['discord_id']}, {'$set': {'ally_code': self.user_data['ally_code']}} )
                self.logger.info("User {} added to the MongoDB".format(self.user_data['user_id']))
            except Exception:
                self.logger.error('User {} update is FAILED'.format(self.user_data['discord_id']), exc_info=True)
            
            return "Already"
    

        

