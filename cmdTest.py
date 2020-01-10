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

        # keys = [613986173, 827499228, 359893537, 194547796]
        keys =[613986173, 827499228, 359893537, 194547796, 527658436, 737866539, 737127234, 864734664, 383988679, 683824426, 932267176, 351149782, 719656952, 119286182,
                443237516, 971371787, 736643423, 531984861, 943991955, 651847991, 893828848, 634188731, 328955735, 249564568]

        data = await self.cache.get_allycodes(keys)

        print ('got it')


        


        
 
#-------------------------------------------------------------------------------
def setup(bot):
    bot.add_cog(HelpApiTest(bot))