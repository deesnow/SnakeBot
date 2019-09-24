from discord.ext import commands
import asyncio
import logging
import settings
from datetime import datetime 


class UserUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.info('Init Test COG')

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
def setup(bot):
    bot.add_cog(UserUpdate(bot))