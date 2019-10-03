from discord.ext import commands
import asyncio
import logging
import settings
from datetime import datetime
import db_handler as mongo

db = mongo.Dbhandler()



class CollectSrInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.info('Init ServerInfo COG')

#-------------------------------------------------------------------------------


    #@commands.Cog.listener()
    #async def on_ready(self):
    @commands.command(pass_context=True)
    
    async def srv(self, ctx):
        print('Collect ServerInfo task called')
        #self.bg_task = self.bot.loop.create_task(self.user_progress())
        # update all User server info (Avatar_url, Servers, and roles)

        for self.guild in self.bot.guilds:
            for self.user in self.guild.members:
                self.discord_id = self.user.id
                self.url = self.user.avatar_url._url
                self.guild_id = str(self.user.guild.id)
                self.filtered_roles = {}
                for self.role in self.user.roles:
                    self.filtered_roles[self.role.name] = str(self.role.id)
                self.server_dict = {}
                self.server_dict[self.guild_id ] = {
                                "name" : self.user.roles[0].guild.name,
                                "rolesOfUser" : self.filtered_roles
                                    }

                self.linkD = db.linkDiscord(self.discord_id, self.server_dict, self.url)
                if self.linkD == "Done":
                    self.logger.info(f'Server info is linked for user: {self.user.name} {self.user.discriminator}', exc_info=True)
                else:
                    self.logger.error(f'Server info is link FAILED for user: {self.user.name} {self.user.discriminator}', exc_info=True)
                await asyncio.sleep(0.1)







#-------------------------------------------------------------------------------
def setup(bot):
    bot.add_cog(CollectSrInfo(bot))