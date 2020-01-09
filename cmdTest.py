import discord
from discord.ext import commands
import asyncio
import time
import logging
import settings
from datetime import datetime
import bgDB_handler as mongo
import cache

db = mongo.Bg_dbhandler()



class HelpApiTest(commands.Cog, name="TEST COG"):
    def __init__(self, bot):
        self.bot = bot
        self.cache = cache.MyCacheLayer(self.bot)
        self.logger = logging.getLogger(__name__)
        self.logger.info('Init Test COG')

#-------------------------------------------------------------------------------

    @commands.command(pass_context=True)
    # 
    async def test(self, ctx, key):

        keys = [376764962, 567793738, 471941296]

        data = await self.cache.get_allycodes(keys)

        print ('got it')


        


        
 
#-------------------------------------------------------------------------------
def setup(bot):
    bot.add_cog(HelpApiTest(bot))