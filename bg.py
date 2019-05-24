from discord.ext import commands
import asyncio
import db_handler as mongo
import swgoh_handler
import logging

db = mongo.Db_handler()
sw = swgoh_handler.Swgoh()

class BgTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.info('Init bg COG')

  
    async def user_progress(self):
        #channel = self.bot.get_channel(451385630543577088)
        channel = self.bot.get_channel(573490564646043649)
        await channel.send('SnakeBot start daily background roster check for registered users')
        #Get list of {ally:code , user_id}
        while True:
            self.alluser = db.getalluser()
            self.counter = 0

            for self.user in self.alluser:
                self.discord_id = self.user['discord_id']
                self.allycode = self.user['ally_code']

                #Get progress data from swgoh.gg, and write it to DB
                try:
                    self.newdata = sw.swgoh_getuser(self.allycode)['data']
                    try:
                        self.write_user = db.user_update(self.discord_id, self.newdata)
                        self.counter += 1
                    except Exception as error:
                        self.logger.error('Mongo DB update - FAILED from bg task')
                        print(error)
                except Exception as error:
                    self.logger.error('swgoh_getuser drop exeption for user {}'.format(self.discord_id))
                    print(error)

            await channel.send('Daily backgroud roster save DONE for {} users'.format(self.counter))
            self.logger.info('Daily backgroud roster save DONE for {} users'.format(self.counter))
            await asyncio.sleep(86400)

                
                


    
    @commands.Cog.listener()
    async def on_ready(self):
        print('BG task called')
        #self.bg_task = self.bot.loop.create_task(self.user_progress())

    @commands.command(pass_context=True)
    @commands.has_any_role('Master') # User need this role to run command (can have multiple)
    async def startbg(self, ctx):
        
        self.bg_task = self.bot.loop.create_task(self.user_progress())
        #await channel.send('Daily roster saves - STARTED')


    @commands.command(pass_context=True)
    @commands.has_any_role('Master') # User need this role to run command (can have multiple)
    async def stopbg(self, ctx):
        channel = self.bot.get_channel(451385630543577088)
        #channel = self.bot.get_channel(573490564646043649)
        self.bg_task.cancel()
        await channel.send('Daily roster saves - STOPPED')


def setup(bot):
    bot.add_cog(BgTask(bot))