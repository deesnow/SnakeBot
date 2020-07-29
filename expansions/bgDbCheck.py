from discord.ext import commands, tasks
from handlers import db_handler as mongo
from botSettings import settings
import logging
import logging.config

class DbCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = mongo.Dbhandler()
        self.logger = logging.getLogger(__name__)
        self.logger.info('Init DbCheck COG')
        self.db_check.start()
        

    def cog_unload(self):
        self.db_check.cancel()

    @tasks.loop(minutes=2.0)
    async def db_check(self):
        self.db.update_status()
        print (f'DB Status is {settings.DB_SERVER_CONNECTION}')

    @db_check.before_loop
    #Waiting until the bot is ready before the loop starts
    async def before_db_check(self):
        print('db_check is waiting...')
        await self.bot.wait_until_ready()
        




# ---------------------------------------------
def setup(bot):
    bot.add_cog(DbCheck(bot))
