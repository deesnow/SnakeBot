import pymongo
import json
from dateutil.parser import parse
import datetime
import settings
import logging


class Bg_dbhandler(object):
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
                                                connect=True)
            self.logger.info('BgTask db handler is connected to %s DB server', settings.DB_HOST)
        else:
            self.dbclient = pymongo.MongoClient(host=settings.DB_HOST,
                                                port=settings.DB_PORT,
                                                connect=True)
            self.logger.info('BgTask db handler is connected to %s DB server', settings.DB_HOST)
            # self.dbclient = pymongo.MongoClient(host=settings.DB_HOST,
            #                                     port=settings.DB_PORT,
            #                                     username=settings.DB_USER,
            #                                     password=settings.DB_PASS,
            #                                     authSource=settings.DB_AUTHSource,
            #                                     authMechanism=settings.DB_AUTHMech,
            #                                     connect=True)
        self.mydb = self.dbclient['mydatabase']
        self.mycol = self.mydb['bgTasks']

    def reset(self):
        self.now = datetime.datetime.now()
        self.filter = {"_id":"progress"}
        self.data = {
                    "startTime": False,
		            "lastId": "userId",
		            "cycle": 0,
		            "error": None}
                    
        self.newvalue = {"$set": self.data }

        try:
            self.mycol.update_one(self.filter, self.newvalue)
            self.logger.info(f'Reset value set for progress bg')
            return True          
        except Exception as error:
            self.logger.error(f'Reset value exception occured \n{error}')
            return False

    def set(self, key, value):
        self.key = key
        self.value = value
        self.filter = {"_id":"progress"}
        self.data = {"$set": {self.key: self.value}}

        try:
            self.mycol.update_one(self.filter, self.data)
            self.logger.info(f'Set_value for {self.key} Done')
            return True          
        except Exception as error:
            self.logger.error(f'Set_value for {self.key} Failed\n{error}')
            return False

    def get_progress(self):
        self.filter = {"_id":"progress"}

        try:
            self.progress_data = self.mycol.find_one(self.filter)
            return self.progress_data
        except Exception as error:
            self.logger.error(f'Get values from progress Failed\n{error}')
            return False


        

