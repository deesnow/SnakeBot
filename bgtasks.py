#Background Tasks called by the __main__ and run on the background

import asyncio
import logging
import pymongo
import discord
from discord.ext import commands

class BgTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
                

    async def task1(self):
        for i in 10:
            print('Task1 - {} cycle'.format(i)
            #await asyncio.sleep(60)

    @commands.Cog.listener()
    async def on_ready(self):
        self.bg_task = self.bot.loop.create_task(self.task1())
        print('BG task called')
        
    
    

    


def setup(bot):
    bot.add_cog(BgTasks(bot))
    
    





