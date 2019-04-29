import discord
from discord.ext import commands
import db_handler as mongo
import swgoh_handler

db = mongo.Db_handler()
sw = swgoh_handler.Swgoh()

class CkeckUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(aliases= ['cu', 'check'])
    async def checkuser(self, ctx, user):
        self.ctx = ctx
        await self.ctx.message.add_reaction("🐍")
        
        if user != "me":
            self.user_id = self.ctx.message.mentions[0].id
            
        else:
            self.user_id = self.ctx.author.id

        try:
            self.allycode = db.get_allycode(self.user_id)
        except Exception as error:
            print(error)
        
        try:
            self.newdata = sw.swgoh_getuser(self.allycode)['data']
            await self.ctx.send('Userdata from swgoh.gg --> \n {}'.format(self.newdata['galactic_power']))
        except Exception as error:
            print(error)

        

       
        
# ---------------------------------------------
def setup(bot):
    bot.add_cog(CkeckUser(bot))
