from discord.ext import commands
import asyncio
import db_handler as mongo
import swgoh_handler
import logging
import settings
from datetime import datetime 

db = mongo.Dbhandler()
sw = swgoh_handler.Swgoh()

class BgTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.info('Init bg COG')

  
    async def user_progress(self):
        #snake
        #channel = self.bot.get_channel(451385630543577088)
        channel = self.bot.get_channel(int(settings.CHANNEL_ID))
        await channel.send('SnakeBot start daily background roster check for registered users')
        #Get list of {ally:code , user_id}
        while True:
            self.alluser = db.getalluser()
            self.counter = 0
            self.today = datetime.today()
            nextrun = datetime( self.today.year, self.today.month, self.today.day +1 , 3, 0 , 0  )

            for self.user in self.alluser:
                self.discord_id = self.user['discord_id']
                self.allycode = self.user['ally_code']

                #Get progress data from swgoh.gg, and write it to DB
                try:
                    self.newdata = sw.swgoh_getuser(self.allycode)
                    try:
                        self.write_user = db.user_update(self.discord_id, self.newdata['data'])
                        self.counter += 1
                    except Exception as error:
                        self.logger.error('Mongo DB progress update - FAILED from bg task')
                        print(error)
                    #write daily roster data into xxnowxx
                    try:
                        self.write_user = db.save_roster(self.discord_id, 'xxnowxx' , self.newdata)
                        
                    except Exception as error:
                        self.logger.error('Mongo DB roster update - FAILED from bg task')
                        print(error)

                    

                except Exception as error:
                    self.logger.error('swgoh_getuser drop exeption for user {}'.format(self.discord_id))
                    print(error)
                await asyncio.sleep(2)

            await channel.send('Daily backgroud progress save DONE for {} users'.format(self.counter))
            self.logger.info('Daily backgroud progress save DONE for {} users'.format(self.counter))
            self.delta = nextrun - datetime.now()

            await channel.send('Next cycle will run after {} seconds'.format (self.delta.total_seconds()))
            self.logger.info('Next cycle will run after {} seconds'.format (self.delta.total_seconds()))

            await asyncio.sleep(self.delta.total_seconds())
            await channel.send('Daily backgroud progress start the next cycle')
            self.logger.info('Daily backgroud progress start the next cycle')

        self.logger.info('BG task is ended , while loop is False')
#-------------------------------------------------------------------------------
  
        

                
                

#-------------------------------------------------------------------------------
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('BG task called')
        #self.bg_task = self.bot.loop.create_task(self.user_progress())

    @commands.command(pass_context=True)
    @commands.has_any_role('Master') # User need this role to run command (can have multiple)
    async def startbg(self, ctx):
        self.ctx = ctx
        await self.ctx.message.add_reaction("🐍")
        self.bg_task = self.bot.loop.create_task(self.user_progress())
        #await channel.send('Daily roster saves - STARTED')


    @commands.command(pass_context=True)
    @commands.has_any_role('Master') # User need this role to run command (can have multiple)
    async def stopbg(self, ctx):
        self.ctx = ctx
        await self.ctx.message.add_reaction("🐍")
        channel = self.bot.get_channel(int(settings.CHANNEL_ID))
        #Snake
        #channel = self.bot.get_channel(573490564646043649)
        self.bg_task.cancel()
        await channel.send('Daily roster saves - STOPPED')


def setup(bot):
    bot.add_cog(BgTask(bot))