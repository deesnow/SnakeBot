import logging
#import asyncio
import motor.motor_asyncio
from botSettings import settings


class mDbhandler(object):
    '''Motor based Db handler function for the Snakebot.'''
    # pylint: disable=too-many-instance-attributes
    # Eight is reasonable in this case.


    def __init__(self, logger=None):
        self.logger = logging.getLogger(__name__)
        
        if settings.DB_PROD:
            self.mongouri = f'mongodb://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/?authSource=admin'
            self.mclient = motor.motor_asyncio.AsyncIOMotorClient(self.mongouri)
            
            
        else:
            self.mclient = motor.motor_asyncio.AsyncIOMotorClient(host="localhost", port=27017)
            
        self.mdb = self.mclient['mydatabase']
        
        

# --------------------------------------------------------------------

    async def find_char(self, name):
        self.name = name
        self.mcol = self.mdb['UnitsList']
        self.filter = f'.*{self.name}.*'
        self.results = []
        self.ids = []
        self.cursor = self.mcol.find({'base_id': {'$regex' : self.filter}})
        
        for self.docs in await self.cursor.to_list(length=5):
            self.ids.append(self.docs['base_id'])
            self.results.append(self.docs)

        
        self.cursor = self.mcol.find({'name': {'$regex' : self.filter}})
        for self.docs in await self.cursor.to_list(length=5):
            if self.docs['base_id'] not in self.ids:
                self.ids.append(self.docs['base_id'])
                self.results.append(self.docs)


        self.cursor = self.mcol.find({'alias': {'$regex' : self.filter}})
        for self.docs in await self.cursor.to_list(length=5):
            if self.docs['base_id'] not in self.ids:
                self.ids.append(self.docs['base_id'])
                self.results.append(self.docs)

        

        
        return self.results


# --------------------------------------------------------------------

    async def get_alias(self, id):
        self.mcol = self.mdb['UnitsList']

        result = await self.mcol.find_one({'base_id': id})
        try:
            alias = result['alias']
        except KeyError:
            alias = []

        return alias

# --------------------------------------------------------------------
    async def set_alias(self, id, new_alias):
        self.mcol = self.mdb['UnitsList']

        await self.mcol.update_one({'base_id':id}, {'$set': {'alias': new_alias}})
        self.logger.info(f'{id} is updated with {new_alias} alias')

        return True
# --------------------------------------------------------------------
    async def add_team(self, team_name, members, ids, server_id):
        self.mcol = self.mdb['Squads']
        self.new_team = {
            'TeamName': team_name,
            'ServerID' : server_id,
            'Members': members,
            'Ids': ids,
            'Category': None
        }

        self.result = await self.mcol.insert_one(self.new_team)

        return self.result


# --------------------------------------------------------------------
    async def search_team(self, team_name, server_id):
        self.mcol = self.mdb['Squads']
        self.results = []
        self.filter = f'.*{team_name}.*'

        self.cursor = self.mcol.find({'TeamName': {'$regex' : self.filter}, 'ServerID':server_id })
        for self.docs in await self.cursor.to_list(length=10):
            self.results.append(self.docs)
        
        return self.results

# --------------------------------------------------------------------
    async def list_team(self, server_id):
        self.mcol = self.mdb['Squads']
        self.results = []
        self.filter = {'ServerID': server_id}

        self.cursor = self.mcol.find(self.filter)
        for self.docs in await self.cursor.to_list(length=10):
            self.results.append(self.docs)
        
        return self.results

# --------------------------------------------------------------------
    async def get_team(self, team_name, server_id):
        self.mcol = self.mdb['Squads']
        
        self.filter = {'TeamName': team_name, 'ServerID':server_id}

        self.result = await self.mcol.find_one(self.filter)
        
        return self.result

# --------------------------------------------------------------------
    async def delete_team(self, team_name, server_id):
        self.mcol = self.mdb['Squads']
        
        self.filter = {'TeamName': team_name, 'ServerID':server_id}

        self.cursor = await self.mcol.delete_one(self.filter)
        
        
        return self.cursor


# --------------------------------------------------------------------
    async def valid_char(self, char):
        self.mcol = self.mdb['UnitsList']

        self.result = await self.mcol.find_one({'alias': char})

        if self.result != None:
            return self.result['base_id'], self.result['name'] 
        else:
            None
        
        
       





# --------------------------------------------------------------------

# --------------------------------------------------------------------

# --------------------------------------------------------------------