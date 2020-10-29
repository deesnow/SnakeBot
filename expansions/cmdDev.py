from discord.ext import commands
from botSettings import settings
import logging

from handlers import db_handler as mongo
from handlers import cache
from handlers import jobsQueue as queue
import shortuuid




# Discord Bot cog

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = mongo.Dbhandler()
        self.logger = logging.getLogger(__name__)
        self.logger.info('Init cmdRoster COG')
        self.cache = cache.MyCacheLayer(self.bot)
        self.queue = queue.jobsQueue()
        self.settings = settings
        

    @commands.command(aliases=['Development'],pass_context=True, name='dev')
    async def dev(self, ctx):
        await ctx.message.add_reaction("⏳")
        self.uid = shortuuid.uuid()
        self.allycodes = [376764962, 146197219, 631896435]
        if self.settings.SHITTYBOT_REQUESTS < 3:
            self.queue.add_request(self.uid)
            self.pos = self.queue.get_qposition(self.uid)
            self.msg1 = await ctx.send(f'Várakozó kérések száma: {self.pos}')

            #self.player_data = self.cache.get_chached(self.allycode)
            #if self.player_data is None:
            self.player_data = await  self.cache.get_allycode(self.allycodes)
            # else:
            #     print('Player data was chached')

            await ctx.send('Played data ready')

        else:
            self.msg1 = await ctx.send(f'Várakozó kérések száma több mint 3: {self.pos}')
        


        



    @dev.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')
        else:
            await self.ctx.send('⛔ - Szar van a palacsintában, próbáld újra \n')








# ---------------------------------------------
def setup(bot):
    bot.add_cog(Dev(bot))