import pymongo
import json
from dateutil.parser import parse

import logging


class Db_handler(object):
    def __init__(self, logger=None):
        self.logger = logging.getLogger(__name__)
        # self.dbclient = pymongo.MongoClient('mongodb://localhost:27017')
        self.dbclient = pymongo.MongoClient('mongodb://192.168.0.10:32770',
                                            username='mongo',
                                            password='mongopwd01',
                                            authSource='admin',
                                            authMechanism='SCRAM-SHA-1')
        self.mydb = self.dbclient['mydatabase']
        self.col_chars = self.mydb['characters']
        self.col_ships = self.mydb['ships']
        
    def create_docs(self, collection,  json_file):
        #Create specified MongoDB and fill up with initial data
        self.mycol = self.mydb[collection]
        try:
            if self.mycol.count_documents({})== 0:
                print('writeing data to MongoDb')
            try:
                with open(json_file, 'r' ) as self.file:
                    self.data = json.loads(self.file.read())
                    #print(type(self.data))
            except Exception as e:
                self.logger.error('Failed to Open File')
            try:
                self.ins_ =  self.mycol.insert_many(self.data)
                self.logger.info('MongoDB {} created'.format(self.mycol))
                return self.mycol.count_documents({})
            except Exception as e:
                self.logger.error('MongoDB create FAILED')

            else:
                print('Collection is not empty!!!')
        except Exception as e:
            self.logger.error('Cannot connect to Mongo')

           

    def update_docs(self, collection, filter, data):
        #Update filtered docs in collection
        self.mycol = self.mydb[collection]
        self.fileter = filter
        self.data = {"$set": data}
        try:
            self.mycol.update_one(self.fileter, self.data)
            self.logger.info('MongoDb updated with {0}'.format(self.mycol))            
        except Exception as e:
            self.logger.error('Cannot update {0}'.format(self.mycol))

        
    
    def mass_update(self, collection, json_file):
        #drop all data from collection and recreate from json file
        self.mycol = self.mydb[collection]
        
        if self.mycol.count_documents({}) > 0:
            self.mycol.delete_many({})

        try:
            with open(json_file, 'r' ) as self.file:
                self.data = json.loads(self.file.read())
                #print(type(self.data))
        except Exception as e:
            self.logger.error('Cannot open {0}'.format(self.file))
        try:
            self.ins_ =  self.mycol.insert_many(self.data)
            self.logger.info('Mongo BD update - DONE')
        except Exception as e:
            self.logger.error('Mongo DB update - FAILED')
        


    def user_add(self, data):
        self.col_discord = self.mydb['discordUsers']
        self.user_data = data
        self.x = self.col_discord.find_one({"discord_id": self.user_data['discord_id']})
        
        if self.x == None:
            try:
                self.inserted_data = self.col_discord.insert_one(self.user_data)
                self.logger.info("User {} added to the MongoDB".format(self.user_data['user_id']))
                return "Done"
            except Exception as error:
                self.logger.error('User add is FAILED')
                return "Failed"
        else:
            
            try:
                self.inserted_data = self.col_discord.find_one_and_update({'discord_id': self.user_data['discord_id']}, {'$set': {'ally_code': self.user_data['ally_code']}} )
                self.logger.info("User {} added to the MongoDB".format(self.user_data['user_id']))
            except Exception as error:
                self.logger.error('User {} update is FAILED'.format(self.user_data['discord_id']))
            
            return "Already"

    def getalluser(self):
        self.col_discord = self.mydb['discordUsers']
        try:
            self.alluser = self.col_discord.find({},{'ally_code':1, 'discord_id':1})
            return self.alluser
        except Exception as error:
            self.logger.error('User add is FAILED')
            return "Failed"


    def user_update(self, discord_id, data):
        self.col_discord = self.mydb['discordUsers']
        self.data = data
        self.discord_id = discord_id
        self.query = {'discord_id': self.discord_id, 'progress': {"$exists" : True}}
        self.query2 = {'discord_id': self.discord_id}
        self.datetime = parse(self.data['last_updated'])
        self.date = str(self.datetime.date())

        try:
            self.action1 = self.col_discord.find_one(self.query)
        except Exception as error:
            self.logger.error('User update is FAILED')
            return "Failed"

        if self.action1 == None:  
            

            self.new_value = {'$set': {"progress": {self.date: self.data}}}
            try:
                self.action2 = self.col_discord.update_one(self.query2, self.new_value)
                self.logger.info('User update DONE for {} discordID'.format(self.discord_id))
                return 'Done'
            except Exception as error:
                self.logger.error('User update is FAILED')
                return "Failed"

        else:
            
            if self.date > max(list(self.action1['progress'].keys())):
                self.newkey = "progress." + self.date
                self.new_value = {'$set': {self.newkey: self.data}}
                try:
                    self.action2 = self.col_discord.update_one(self.query2, self.new_value)
                    self.logger.info('User update DONE with new {} progress data'.format(self.date))
                    return 'Done'
                except Exception as error:
                    self.logger.error('User update is FAILED')
                    return "Failed"
            else:
                return 'Already'




    def get_allycode(self, user_id):
        self.col_discord = self.mydb['discordUsers']
        self.user_id = user_id

        try:
            self.allycode = self.col_discord.find_one({'discord_id': self.user_id},{'_id':0, 'ally_code': 1})
            self.logger.info('{} found for {}'.format(self.allycode, self.user_id))
            return self.allycode['ally_code']
        except Exception as error:
            self.logger.error('Get allycode is FAILED. {}'.format(error))
            return "Failed"



    def user_purge(self, discord_user):
        self.discord_user = str(discord_user)
        self.ally_code = ally_code
        self.col_discord = self.mydb['discordUsers']
        self.user_data = {"user_id": self.discord_user}
        self.x = self.col_discord.find_one({"user_id": self.discord_user})

        if self.x != None:
            try:
                self.delete_data = self.col_discord.delete_one(self.user_data)
                self.logger.info("User {} data purged from the MongoDB".format(self.discord_user))
                return "Done"
            except Exception as e:
                self.logger.error('User delete is FAILED')
                return "Failed"
        else:
            self.logger.info('User {} was not in MongoDB')
            return "Already"

    def save_roster(self, discord_id, save_name, data):
        self.discord_id = discord_id
        self.save_name = save_name.replace('.','_')
        self.data = data
        self.roster_data = self.data['units']
        self.col_discord = self.mydb['discordUsers']
        self.query2 = {'discord_id': self.discord_id}
        self.datetime = parse(self.data['data']['last_updated'])
        self.date = str(self.datetime.date())
        self.newkey = "roster." + self.save_name
        self.new_data = {'date': self.date, 'data': self.roster_data}
        self.new_value = {'$set': {self.newkey: self.new_data}}

        try:
            self.action2 = self.col_discord.update_one(self.query2, self.new_value)
            self.logger.info('User update DONE with new {} roster data'.format(self.date))
            return 'Done'
        except Exception as error:
            self.logger.error('User update is FAILED')
            return "Failed"

    def delete_now(self, discord_id):
        self.discord_id = discord_id
        self.col_discord = self.mydb['discordUsers']
        self.rm_data = {'$unset': {'roster.xxnowxx':''}}
        self.query = {'discord_id': self.discord_id}

        try:
            self.rm = self.col_discord.find_one_and_update(self.query, self.rm_data)
            self.logger.info('Temp roster save deleted for {}'.format(self.discord_id))
            return 'Done'
        except Exception as error:
            self.logger.error('User update is FAILED')

        def delete_save(self, discord_id, save):
            self.discord_id = discord_id
            self.save = save
            self.docs = 'roster.' + self.save
        self.col_discord = self.mydb['discordUsers']
        self.rm_data = {'$unset': {self.docs:''}}
        self.query = {'discord_id': self.discord_id}

        try:
            self.rm = self.col_discord.find_one_and_update(self.query, self.rm_data)
            self.logger.info('{}} roster save deleted for {}'.format(self.save,self.discord_id))
            return 'Done'
        except Exception as error:
            self.logger.error('User update is FAILED,' , error)


    def listsaves(self, discord_id):
        self.col_discord = self.mydb['discordUsers']
        self.discord_id = discord_id
        self.query = {'discord_id': self.discord_id, 'roster': {"$exists" : True}}
        self.saves = {}

        try:
            self.roster_saves = self.col_discord.find_one(self.query, {'roster':1})['roster']
            for self.save in self.roster_saves:
                try:
                    self.date = self.roster_saves[self.save]['date']
                except:
                    self.date = 'Not_Saved'
                self.saves[self.save] = self.date
            return self.saves            
        except Exception as error:
            self.logger.error('List saved roster is FAILED')
            return None

    def getdiff(self, discord_id, save1, save2):
        self.col_discord = self.mydb['discordUsers']
        self.discord_id = discord_id
        self.save1 = save1
        self.save2 = save2
        self.match1 = {'$match': {'discord_id': self.discord_id, 'roster': {"$exists" : True}}}
        self.extend = {'$unwind': '$roster.'+ self.save1 + '.data' }
        self.extend2 = {'$unwind': '$roster.'+ self.save2 + '.data' }

        self.shape1 = {'$project' : {'_id':0, 'base_id' :
                    { '$cond': {'if': {'$eq': ['$roster.' +self.save1 + '.data.data.base_id',
                                                '$roster.' +self.save2 + '.data.data.base_id']},
                                'then': '$roster.' +self.save1 + '.data.data.base_id',
                                'else' : '' 
                                }
                    },
                'gear_diff': {'$subtract': ['$roster.' +self.save2 + '.data.data.gear_level',
                                            '$roster.' +self.save1 + '.data.data.gear_level']},
                'rarity_diff': {'$subtract': ['$roster.' +self.save2 + '.data.data.rarity',
                                              '$roster.' +self.save1 + '.data.data.rarity']},
                'name': '$roster.' +self.save1 + '.data.data.name',
                'rarity': '$roster.' +self.save1 + '.data.data.rarity',
                'gear': '$roster.' +self.save1 + '.data.data.gear_level'
                                    }
                    }
        
        self.match2 = {'$match': {'base_id': {'$ne': ''}}}
        self.match3 = {'$match' : {'$or': [{'gear_diff': {'$gt':0}} ,{'rarity_diff':{'$gt': 0}}]}}
        self.pipeline = [self.match1,
                        self.extend,
                        self.extend2,
                        self.shape1,
                        self.match2,
                        self.match3
                        ]
        self.logger.debug('This was the mongo pipeline: {}'.format(self.pipeline))
        #HIBAKEZELES !!!
        self.diff_list = list(self.col_discord.aggregate(self.pipeline))

        return self.diff_list




    def link_add(self, shortname, desc, url):
        self.col_links = self.mydb['links']
        self.shortname = shortname
        self.desc = desc.replace('"', '')
        self.url = url
        self.linkdata = {'shortname': self.shortname,
                        'description': self.desc,
                        'url': self.url
                        }

        try:
            self.link_add = self.col_links.insert_one(self.linkdata)
            self.logger.info('{} is added to the Mongo'.format(self.shortname))
            return 'done'
        except Exception as error:
            self.logger.error('Insert data to DB failed for link_add')
            return 'failed'

    def link_list(self):
        self.col_links = self.mydb['links']
        self.query = {}

        try:
            self.linklist = self.col_links.find(self.query, {'_id':0, 'shortname':1, 'description':1, 'url':1})
            self.logger.info('Links are listed')
            return self.linklist
        except Exception as error:
            self.logger.error('List Link data failed')
            return 'failed'

    def link_get(self, shortname):
        self.col_links = self.mydb['links']
        self.shortname = shortname
        self.query = {'shortname': self.shortname}

        try:
            self.link_list = self.col_links.find(self.query, {'_id':0, 'shortname':1, 'description':1, 'url':1})
            self.logger.info('Link if find')
            return self.link_list
        except Exception as error:
            self.logger.error('Get Link is failed')
            return 'failed'





        



    



