from discord.ext import commands
import asyncio
import logging
import settings
from datetime import datetime 


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
        else:
            self.user = ctx.author
        self.url = self.user.avatar_url._url
        self.guild_name = self.user.roles[0].guild.name
        self.user_roles = self.user.roles[0].guild._roles

            

        await ctx.send(f'Link for the user: {self.url} ; {self.guild_name} ; {self.user_roles}')
            
    



#-------------------------------------------------------------------------------
def setup(bot):
    bot.add_cog(HelpApiTest(bot))