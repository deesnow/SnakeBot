import discord
from discord.ext import commands
import asyncio
import time
import logging
import settings
from datetime import datetime
import bgDB_handler as mongo

db = mongo.Bg_dbhandler()



class HelpApiTest(commands.Cog, name="TEST COG"):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.info('Init Test COG')

#-------------------------------------------------------------------------------

    @commands.command(pass_context=True)
    # 
    async def test(self, ctx):
        # reset = db.reset()

        # if reset:
        #     print(f'Reset Done')
        # else:
        #     print(f'Error')

        #time.sleep(120)

        tasks = asyncio.Task.all_tasks()
        
        

        for task in tasks:
            
            
            print (task)
            if task._state !='FINISHED':
                try:
                    if task._coro.cr_code.co_name == 'user_progress' and task._state == 'PENDING':
                        task.cancel()
                        print('--------------------------------------')
                        break
                    else:
                        print ('not matched coro')
                except Exception as error:
                    pass
                
            
           


        print(tasks)


        
 
#-------------------------------------------------------------------------------
def setup(bot):
    bot.add_cog(HelpApiTest(bot))