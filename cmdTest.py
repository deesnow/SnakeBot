from discord.ext import commands
import asyncio
import logging
import settings
from datetime import datetime
import db_handler as mongo

db = mongo.Dbhandler()



class HelpApiTest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.info('Init Test COG')

#-------------------------------------------------------------------------------

    async def getGuild(self, taskNo):
        
        self.starttime = datetime.now()
        self.logger.info(f"No{taskNo} task is started.")
        await asyncio.sleep(10)
        self.logger.info(f"No{taskNo} task is completed")
        return taskNo + 10





    @commands.command(pass_context=True)
    # 
    async def test(self, ctx):
        self.ctx = ctx
        await self.ctx.message.add_reaction("🐍")

        myloop = asyncio.get_event_loop()

        tasklist = await asyncio.gather(self.getGuild(1), self.getGuild(2), self.getGuild(3))
        
        self.logger.info(f"{tasklist}")        
        self.logger.info(f"Just something to print")

    @commands.command(pass_context=True)
    # Get avatar pic URL
    async def pic(self, ctx, user='me'):
        self.ctx = ctx
        await self.ctx.message.add_reaction("🐍")

        if user != "me":
            
            self.user = ctx.message.mentions[0]
            self.discord_id = str(self.ctx.message.mentions[0].id)
        else:
            self.user = ctx.author
            self.discord_id = str(self.ctx.author.id)
        self.url = self.user.avatar_url._url
        
        #self.guild_name = self.user.roles[0].guild.name
        self.guild_id = str(self.user.guild.id)
        self.user_roles = self.user.roles
        self.filtered_roles = {}
        for self.role in self.user_roles:
            self.filtered_roles[self.role.name] = str(self.role.id)
        self.server_dict = {}
        self.server_dict[self.guild_id ] = {
                        "name" : self.user.roles[0].guild.name,
                        "rolesOfUser" : self.filtered_roles
                            }

        self.linkD = db.linkDiscord(self.discord_id, self.server_dict, self.url)
        if self.linkD == "Done":
            await ctx.message.add_reaction("✅")
            await ctx.send(f'Server info successfully linked')
        else:
            await ctx.message.add_reaction("💥")
            await ctx.send(f'Something whent wrong. Check the logs.')

 
#-------------------------------------------------------------------------------
def setup(bot):
    bot.add_cog(HelpApiTest(bot))