from discord.ext import commands
import asyncio
import time
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

    @commands.command(pass_context=True)
    # 
    async def test(self, ctx):
        

        self.TicToc = self.ticTocGenerator()

        self.tic()

        asyncio.sleep(5)

        self.toc()

    def ticTocGenerator(self):
        # Generator that returns time differences
        ti = 0           # initial time
        tf = time.time() # final time
        while True:
            ti = tf
            tf = time.time()
            yield tf-ti # returns the time difference
    
    
    
    # This will be the main function through which we define both tic() and toc()
    async def toc(self, tempBool=True):
        # Prints the time difference yielded by generator instance TicToc
        tempTimeInterval = next(self.TicToc)
        if tempBool:
            print( "Elapsed time: %f seconds.\n" %tempTimeInterval )
            await ctx.send("Elapsed time: %f seconds.\n" %tempTimeInterval)
    
    def tic(self):
        # Records a time in TicToc, marks the beginning of a time interval
        self.toc(False)
        

    
        
 
#-------------------------------------------------------------------------------
def setup(bot):
    bot.add_cog(HelpApiTest(bot))