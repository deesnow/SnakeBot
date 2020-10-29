import datetime
import pymongo
import json

import logging

from botSettings import settings as mysettings
from handlers import async_swgoh_help

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
            self.dbclient = pymongo.MongoClient(host=mysettings.DB_HOST,
                                                port=mysettings.DB_PORT,
                                                username=mysettings.DB_USER,
                                                password=mysettings.DB_PASS,
                                                authSource=mysettings.DB_AUTHSource,
                                                authMechanism=mysettings.DB_AUTHMech,
                                                connect=True)
            self.logger.info('Bot is connected to %s DB server', mysettings.DB_HOST)
        else:
            self.dbclient = pymongo.MongoClient(host=mysettings.DB_HOST,
                                                port=mysettings.DB_PORT,
                                                connect=True)
            self.logger.info('Bot is connected to %s DB server', mysettings.DB_HOST)
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
            self.col_cache.update_one(self.filter, self.new_value, upsert=True)
            self.logger.info(f'{self.key} added to the cacheDB')
        except Exception as error:
            self.logger.error(f'{self.key} update FAILED on the cacheDB \n{error}')
    
    #----------------------------------------------------------------------
    def get(self, key):
        """
        Get and return value if the data is not older that the defined hours
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

    def __init__(self, bot):
        """Layer Constructor"""

        self.logger = logging.getLogger(__name__)
        self.cachedb = MyCacheDB()
        self.settings = mysettings
        self.cred = async_swgoh_help.settings(self.settings.HELPAPI_USER, self.settings.HELPAPI_PASS)
        self.client = async_swgoh_help.async_swgoh_help(self.cred)
        #self.crinolo = async_swgoh_help.CrinoloStat()
        self.bot = bot

    #----------------------------------------------------------------------
    # async def get_chached(self, key, prio=None, stats=None):
    #     self.keys = keys
    #     self.players_data = []
    #     if prio == 1:
    #         self.validity_hours = 6
    #     else:
    #         self.validity_hours = 24

    #     self.valid_from = datetime.datetime.now() - datetime.timedelta(hours=self.validity_hours) 

    #     self.returns = self.cachedb.get(self.keys)
    #     if (self.returns != None) and (self.returns['date_accessed'] > self.valid_from):
    #         self.players_data.append(self.returns['data'])
    #         return self.players_data
    #         self.logger.info(f'Data was cached for {self.keys}')

    #     else:
    #         return None



    
    async def get_allycode(self, keys, prio=None, stats=None):
        """
        Search allycodes in cache. If the key/keys chached than return the rooster data.
        If the key is not cached, than fetch it, store it in the cache and return the data back 
        """
        self.keys = keys
        self.players_data = []
        self.cached_keys = []
        self.non_cached_keys = []

        if prio == 1:
            self.validity_hours = 1
        else:
            self.validity_hours = 24

        self.valid_from = datetime.datetime.now() - datetime.timedelta(hours=self.validity_hours)    

        if type(self.keys) == int:
            self.returns = self.cachedb.get(self.keys)
            if (self.returns != None) and (self.returns['date_accessed'] > self.valid_from):
                self.players_data.append(self.returns['data'])
                return self.players_data
                self.logger.info(f'Data was cached for {self.keys}')
            else:
                #get data from swgoh.gg API, update cacheDB, and return data back
                self.rawdata = self.bot.loop.create_task(self.client.fetchPlayers(self.keys))
                await self.rawdata
                #Add crinolostats data to roster json -- later implementation 
                #self.roster_stats = self.crinolo.fetch_sdata(self.rawdata._result[0])
                #await self.roster_stats
                self.players_data.append(self.rawdata._result[0])

                self.cachedb.update(self.keys, self.rawdata._result[0]) #update cacheDB


                return self.players_data 
            
        elif type(self.keys) == list:
            for self.key in self.keys:
                self.returns = self.cachedb.get(self.key)
                if (self.returns != None) and (self.returns['date_accessed'] > self.valid_from):
                    self.players_data.append(self.returns['data'])
                else:
                    self.non_cached_keys.append(self.key) #add non-cached allycodes to the list

            if len(self.non_cached_keys) > 20:
                self.lth = round(len(self.non_cached_keys)/2)
                self.keys1 = self.non_cached_keys[:self.lth]
                self.keys2 = self.non_cached_keys[self.lth:]

                self.fetchplayer1 = self.bot.loop.create_task(self.client.fetchPlayers(self.keys1))
                
                self.fetchplayer2 = self.bot.loop.create_task(self.client.fetchPlayers(self.keys2))
                await self.fetchplayer1
                await self.fetchplayer2
                #HIBAKEZELÉS HIÁNYZIK
                self.rawplayers = self.fetchplayer1._result + self.fetchplayer2._result

                self.players_data += self.rawplayers

                for self.player in self.rawplayers:         #update cacheDB
                    self.cachedb.update(self.player['allyCode'], self.player)



            elif len(self.non_cached_keys) == 0:
                pass
            
            else:
                self.rawplayers = self.bot.loop.create_task(self.client.fetchPlayers(self.non_cached_keys))
                await self.rawplayers
                self.players_data += self.rawplayers._result
                #self.players_sdata = self.crinolo.fetch_sdata(self.players_data)
                #await self.players_sdata
                for self.player in self.rawplayers._result:         #update cacheDB
                    self.cachedb.update(self.player['allyCode'], self.player)


            return self.players_data 
