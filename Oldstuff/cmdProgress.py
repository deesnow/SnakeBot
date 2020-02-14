import asyncio
import logging
import settings
import discord
from discord.ext import commands
import os

import db_handler as mongo
import progress_handler as progress
db = mongo.Dbhandler()
plot = progress.Progresshandler()


class Progress(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.info('Init cmdProgress COG')
#--------------------------------------------------------
    # Stat command
    @commands.command(pass_context = True)
    async def stats(self, ctx, user):
        self.ctx = ctx
        self.user = user
        self.channel = self.ctx.channel
        channel = self.bot.get_channel(int(settings.CHANNEL_ID))
        

        if user != "me":
            self.user_id = self.ctx.message.mentions[0].id
        else:
            self.user_id = self.ctx.author.id
        
        await self.ctx.message.add_reaction("🐍")

        
        try:
            self.progress_json = db.getProgress(self.user_id)
            await self.ctx.message.add_reaction("✅")
            self.prog_img = plot.get_stats(self.progress_json)
            if self.prog_img != None:
                await self.ctx.send('**Here we are**')
                await self.channel.send(file=discord.File(self.prog_img))
                await asyncio.sleep(5)
                os.remove(self.prog_img)
            else:
                await self.ctx.message.add_reaction("💥")
                await self.ctx.send('Booom.... somehow the charts are not generated!')
                self.logger.error('The {} image path is not valid'.format(self.prog_img))






        except Exception as error:
            print(error)
            self.logger.error('Failed to get Progress data for {} user ID'.format(self.user_id))
            await self.ctx.send('Failed to get Progress data for {}'.format(self.user))



#--------------------------------------------------------

def setup(bot):
    bot.add_cog(Progress(bot))
