import logging
import asyncio
import motor.motor_asyncio
from botSettings import settings


class mDbhandler(object):
    '''Motor based Db handler function for the Snakebot.'''
    # pylint: disable=too-many-instance-attributes
    # Eight is reasonable in this case.


    def __init__(self, logger=None):
        self.logger = logging.getLogger(__name__)
        
        if settings.DB_PROD:
            self.mongouri = f'mongodb://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/mydatabase?authSource=admin'
            self.mclient = motor.motor_async.AsyncIOMotorClient(self.mongouri)
            
            
        else:
            self.mclient = motor.motor_asyncio.AsyncIOMotorClient(host="localhost", port=27017)
            
        self.mdb = self.mclient['mydatabase']
        
        

# --------------------------------------------------------------------

    async def find_char (self, name):
        self.name = name
        self.mcol = self.mdb['UnitsList']
        self.filter = f'.*{self.name}.*'
        self.cursor = self.mcol.find({'name': {'$regex' : self.filter}})
        self.results = []
        for self.docs in await self.cursor.to_list(length=20):
            self.results.append(self.docs)
        return self.results
        