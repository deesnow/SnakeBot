import discord
from discord.ext import commands
import db_handler as mongo
import swgoh_handler

db = mongo.Db_handler()
sw = swgoh_handler.Swgoh()

class SaveRoster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(aliases= ['sr', 'save'],pass_context = True)
    @commands.has_any_role('Master')
    async def saveroster(self, ctx, user, save_name):
        self.ctx = ctx
        cmd_channel = self.ctx.message.channel
        self.save_name = save_name
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
            self.newdata = sw.swgoh_getuser(self.allycode)
            #await self.ctx.send('Userdata from swgoh.gg --> \n {}'.format(self.newdata['galactic_power']))
        except Exception as error:
            print(error)

        try:
            self.write_user = db.save_roster(self.user_id, self.save_name , self.newdata)
        except Exception as error:
            print(error)
        if self.write_user == "Done":
            await self.ctx.send('User roster data is saved as {}'.format(self.save_name))
        else:
            await self.ctx.send('Upate roster date is FAILED, check logs for more datails.')

    @saveroster.error
    async def saveroster_error(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!")
            await self.ctx.send('⛔ - You don\'t have the right permission!!!')
    





# --------------------------------
def setup(bot):
    bot.add_cog(SaveRoster(bot))
