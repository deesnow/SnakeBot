import datetime
import pymongo
import json

import logging

from async_swgoh_help import async_swgoh_help, settings
import settings as mysettings

########################################################################
class MyCacheDB:
    """
    Class object for provide cacheDB basic action
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """CacheDB Basic Action Constructor"""
        self.logger = logging.getLogger(__name__)

        if mysettings.DB_PROD:
            self.dbclient = pymongo.MongoClient(host=settings.DB_HOST,
                                                port=settings.DB_PORT,
                                                username=settings.DB_USER,
                                                password=settings.DB_PASS,
                                                authSource=settings.DB_AUTHSource,
                                                authMechanism=settings.DB_AUTHMech,
                                                connect=True)
            self.logger.info('Bot is connected to %s DB server', settings.DB_HOST)
        else:
            self.dbclient = pymongo.MongoClient(host=settings.DB_HOST,
                                                port=settings.DB_PORT,
                                                connect=True)
            self.logger.info('Bot is connected to %s DB server', settings.DB_HOST)
            # self.dbclient = pymongo.MongoClient(host=settings.DB_HOST,
            #                                     port=settings.DB_PORT,
            #                                     username=settings.DB_USER,
            #                                     password=settings.DB_PASS,
            #                                     authSource=settings.DB_AUTHSource,
            #                                     authMechanism=settings.DB_AUTHMech,
            #                                     connect=True)
        self.mydb = self.dbclient['mydatabase']
        self.col_cache = self.mydb['cache']
        

    #----------------------------------------------------------------------
    def __contains__(self, key):
        """
        Returns True or False depending on whether or not the key is in the 
        cache
        """
        self.key = key
        self.player = self.col_cache.find_one({"_id":self.key})
        if self.player != None:
            return True
        else:
            return False
 
    #----------------------------------------------------------------------
    def update(self, key, value):
        """
        Update the cache dictionary and optionally remove the oldest item
        """
        self.key = key
        self.value = value
        self.filter = {"_id": self.key}
        self.new_value = {'$set':
                            {'date_accessed': datetime.datetime.now(),
                            'data': self.value}
                            }

        try:
            col_cache.update_one(self.filter, self.new_value)
            self.logger.info(f'{self.key} added to the cacheDB')
        except Exception as error:
            self.logger.error(f'{self.key} update FAILED on the cacheDB \n{error}')
    
    #----------------------------------------------------------------------
    def get(self, key):
        """
        Get and retunt value if the data is not older that the defined hours
        """
        

        self.key = key
        
        self.filter = {'_id': self.key}

        try:
            self.query =  self.col_cache.find_one(self.filter)
            return self.query

        except Exception as error:
            self.logger.error(f'Get {self.key} FAILED from the cacheDB \n{error}')
            return False
 
    #----------------------------------------------------------------------
    

    
########################################################################

class MyCacheLayer:
    """
    Class object for provide cacheLayer fuctionlities.
    Bot call this layer instead of swgoh.help API directly.
    This layer responsible to provide the data from cache if it is valid,
    or refresh it from the API.
    """

    def __init__(self):
        """Layer Constructor"""

        self.cachedb = MyCacheDB()
        self.creds = settings(mysettings.HELPAPI_USER, mysettings.HELPAPI_PASS)
        self.client = async_swgoh_help(creds)

    
    async def get_allycodes(self, keys, prio=None):
        self.keys = keys
        self.datas = []
        self.cached_keys = []
        self.not_cached_keys = []

        if prio == 1:
            self.validity_hours = 6
        else:
            self.validity_hours = 24

        self.valid_until = datetime.datetime.now() + datetime.timedelta(hours=self.validity_hours)    

        if self.keys == int:
            self.returns = self.cachedb.get(self.keys)
            if self.returns != None and self.returns['date_accessed'] < self.valid_until:
                return self.returns['data']
            else:
                self.apicall = client

            
        elif self.keys == list:
            for self.key in self.keys:




