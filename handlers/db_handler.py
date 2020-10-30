import logging
import json
import pymongo
from dateutil.parser import parse
from datetime import datetime
from botSettings import settings


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
        except Exception:
            self.logger.error(f'DB connection is BROKEN')
            settings.DB_SERVER_CONNECTION = False
        
# --------------------------------------------------------------------

    def update_status(self):

        try:
            self.server_status = self.mydb.command("serverStatus")
            settings.DB_SERVER_CONNECTION = True
        except Exception as error:
            self.logger.error(f'DB connection is BROKEN')
            settings.DB_SERVER_CONNECTION = False

        

# --------------------------------------------------------------------

# --------------------------------------------------------------------
    def user_add(self, data):
        # Used by cmdReg
        self.col_discord = self.mydb['discordUsers']
        self.user_data = data
        self.x = self.col_discord.find_one({"ally_code": self.user_data['ally_code']})
        
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
                self.inserted_data = self.col_discord.find_one_and_update({'ally_code': self.user_data['ally_code']}, 
                                                                            {'$set': {'discord_id': self.user_data['discord_id'],
                                                                                      'user_id':self.user_data['user_id']}} )
                self.logger.info("User {} added to the MongoDB".format(self.user_data['user_id']))
            except Exception:
                self.logger.error('User {} update is FAILED'.format(self.user_data['discord_id']), exc_info=True)
            
            return "Already"
# --------------------------------------------------------------------

# --------------------------------------------------------------------
    def get_allycode(self, user_id):
        self.col_discord = self.mydb['discordUsers']
        self.user_id = str(user_id)

        if settings.DB_SERVER_CONNECTION == False:
            return {'Error': 'Nincs DB server kapcsolat. Értesítsd DeeSnow-t'}

        else:
            try:
                self.allycode = self.col_discord.find_one({'discord_id': self.user_id},{'_id':0, 'ally_code': 1})
                self.logger.info('%s found for %s', self.allycode, self.user_id)
                return self.allycode['ally_code']

            except ServerSelectionTimeoutError as error:
                self.logger.error(f'ERROR - DB Connection, {error}')
                return {'Error': 'Adatbázis kapcsolat hiba. Értesítsd DeeSnow-t'}
            except Exception:
                
                self.logger.error('Get allycode is FAILED for %s.', self.user_id, exc_info=True)
                return "Failed"
# --------------------------------------------------------------------

    def check_discordid(self, discord_id):
            self.col_discord = self.mydb['discordUsers']
            self.discord_id = str(discord_id)

            if settings.DB_SERVER_CONNECTION == False:
                return {'Error': 'Nincs DB server kapcsolat. Értesítsd DeeSnow-t'}

            else:
                try:
                    self.exist = self.col_discord.find_one({'discord_id': self.discord_id},{'_id':0, 'discord_id': 1})
                    if self.exist == None:
                        return False
                    else:
                        return True

                except ServerSelectionTimeoutError as error:
                    self.logger.error(f'ERROR - DB Connection, {error}')
                    return {'Error': 'Adatbázis kapcsolat hiba. Értesítsd DeeSnow-t'}
                except Exception:
                    
                    self.logger.error('Get allycode is FAILED for %s.', self.user_id, exc_info=True)
                    return {'Error': 'Adatbázis kapcsolat hiba. Értesítsd DeeSnow-t'}
# --------------------------------------------------------------------

    def get_discordid(self, allycode):
            self.col_discord = self.mydb['discordUsers']
            self.allycode = allycode

            if settings.DB_SERVER_CONNECTION == False:
                return {'Error': 'Adatbázis kapcsolat hiba. Értesítsd DeeSnow-t'}

            else:
                try:
                    self.discordid = self.col_discord.find_one({'ally_code': self.allycode},{'_id':0, 'discord_id': 1})
                    self.logger.info('%s found for %s', self.discordid, self.allycode)
                    if self.discordid != None:
                        return self.discordid['discord_id']
                    else:
                        raise ValueError

                
                except ValueError:
                    
                    self.logger.error('Get discordID is FAILED for %s.', self.allycode, exc_info=True)
                    return "Failed"

                except ServerSelectionTimeoutError as error:
                    self.logger.error(f'ERROR - DB Connection, {error}')
                    return {'Error': 'Adatbázis kapcsolat hiba. Értesítsd DeeSnow-t'}
                



# --------------------------------------------------------------------
# --------------------------------------------------------------------

    def get_name(self, allycode):
            self.col_discord = self.mydb['discordUsers']
            self.allycode = allycode

            if settings.DB_SERVER_CONNECTION == False:
                return {'Error': 'Adatbázis kapcsolat hiba. Értesítsd DeeSnow-t'}

            else:
                try:
                    self.name = self.col_discord.find_one({'ally_code': self.allycode},{'_id':0, 'user_id': 1})
                    self.logger.info('%s found for %s', self.name, self.allycode)
                    if self.name != None:
                        return self.name['user_id']
                    else:
                        raise ValueError

                
                except ValueError:
                    
                    self.logger.error('Get Name is FAILED for %s.', self.allycode, exc_info=True)
                    return "Failed"

                except ServerSelectionTimeoutError as error:
                    self.logger.error(f'ERROR - DB Connection, {error}')
                    return {'Error': 'Adatbázis kapcsolat hiba. Értesítsd DeeSnow-t'}
                



# --------------------------------------------------------------------



    def save_roster(self, discord_id, save_name, data):
        self.discord_id = str(discord_id)
        self.save_name = save_name.replace('.','_')
        if type(data) == list:
            self.data = data[0]
        else:
            self.data = data
        
        self.roster_data = self.data['roster']
        self.col_discord = self.mydb['discordUsers']
        self.query2 = {'discord_id': self.discord_id}
        self.datetime = datetime.fromtimestamp(self.data['updated']/ 1e3)
        self.date = str(self.datetime.date())
        self.newkey = "roster." + self.save_name
        self.new_data = {'date': self.date, 'data': self.roster_data}
        self.new_value = {'$set': {self.newkey: self.new_data}}
        self.newkey2 = self.newkey + ".datetime"
        self.new_value2 = {'$set': {self.newkey2: self.datetime}}

        try:
            self.action2 = self.col_discord.update_one(self.query2, self.new_value)
            self.logger.info('User update DONE with new {} roster data for {} discord ID'.format(self.date, self.discord_id))
            
        except Exception:
            self.logger.error('User update is FAILED', exc_info=True)
            return "Failed"

        try:
            self.action3 = self.col_discord.update_one(self.query2, self.new_value2)
            self.logger.info(f'Datetime is inserted to {self.discord_id} ID')
            return 'Done'
        except Exception:
            self.logger.error(f'Datetime insert is FAILED for {self.discord_id} ID', exc_info=True)
            return "Failed"
        
# --------------------------------------------------------------------

    def delete_save(self, discord_id, save):
        self.discord_id = str(discord_id)
        self.save = save
        self.col_discord = self.mydb['discordUsers']
        self.rm_data = 'roster.' + self.save
        self.rm_data = {'$unset': {self.rm_data:''}}
        self.query = {'discord_id': self.discord_id}

        try:
            self.rm = self.col_discord.find_one_and_update(self.query, self.rm_data)
            self.logger.info('%s roster save deleted for %s', self.save, self.discord_id)
            return 'Done'
        except Exception:
            return  "Failed"
            self.logger.error('User update is FAILED,' , exc_info=True)


# --------------------------------------------------------------------

    def get_roster(self, ally_code, save):
        self.col_discord = self.mydb['discordUsers']
        self.ally_code = ally_code
        self.save = save
        self.dict_key = 'roster.' + self.save + '.data' 
        self.query = {'ally_code': self.ally_code, self.dict_key:{'$exists':True}}
        self.filter = {self.dict_key:1}

        try:
            self.saved_roster = self.col_discord.find_one(self.query, self.filter)
            if self.saved_roster is None:
                return None
            else:
                return self.saved_roster['roster'][self.save]['data']
        except Exception as error:
            if settings.DB_SERVER_CONNECTION == False:
                return {'Error': 'Adatbázis kapcsolat megszakadt! Értesítsd DeeSnow-t!'}
            self.logger.error(f'get_roster is FAILED for {self.ally_code} ID', exc_info=True)

# --------------------------------------------------------------------

    def listsaves(self, discord_id):
        self.col_discord = self.mydb['discordUsers']
        self.discord_id = str(discord_id)
        self.query = {'discord_id': self.discord_id, 'roster': {"$exists" : True}}
        self.saves = {}

        if settings.DB_SERVER_CONNECTION == False:
            return {'Error': 'Adatbázis kapcsolat hiba. Értesítsd DeeSnow-t'}

        try:
            self.roster_saves = self.col_discord.find_one(self.query, {'roster':1})['roster']
            for self.save in self.roster_saves:
                try:
                    self.date = self.roster_saves[self.save]['date']
                except:
                    self.date = 'Not_Saved'
                self.saves[self.save] = self.date
            return self.saves            
        except Exception:
            self.logger.error('List saved roster is FAILED', exc_info=True)
            return None

# --------------------------------------------------------------------

    def delete_save_by_allycode(self, allycode, save):
        self.allycode = allycode
        self.save = save
        self.col_discord = self.mydb['discordUsers']
        self.rm_data = 'roster.' + self.save
        self.rm_data = {'$unset': {self.rm_data:''}}
        self.query = {'ally_code': self.allycode}

        try:
            self.rm = self.col_discord.find_one_and_update(self.query, self.rm_data)
            self.logger.info('%s roster save deleted for %s', self.save, self.allycode)
            return 'Done'
        except Exception:
            return  "Failed"
            self.logger.error('Delete save for {self.allycode} FAILED,' , exc_info=True)



# --------------------------------------------------------------------








# --------------------------------------------------------------------


