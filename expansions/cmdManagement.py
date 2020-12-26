from discord.ext import commands
from handlers import mdb_handler as mdb
from botSettings import settings
import logging
from botSettings.settings import ROLES



# Discord Bot cog

class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mdb = mdb.mDbhandler()
        self.logger = logging.getLogger(__name__)
        self.logger.info('Init cmdManagement COG')

    @commands.command(aliases= ['search', 'sc'])
    @commands.has_any_role(*ROLES)  # User need this role to run command
    async def search_char(self, ctx, char):
        self.char = char
        

        await ctx.message.add_reaction("🐍")
        if settings.DB_SERVER_CONNECTION:
            self.result = self.bot.loop.create_task(self.mdb.find_char(self.char))
            await self.result
            count = 1
            for char in self.result._result:
                char_id = char['base_id']
                
                await ctx.send(f'{count}.  {char_id}')
                count += 1

        else:
            await ctx.send('Database connection is DOWN!')


# ---------------------------------------------
def setup(bot):
    bot.add_cog(Management(bot))