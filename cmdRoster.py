import discord
from discord.ext import commands
import db_handler as mongo
import swgoh_handler

db = mongo.Db_handler()
sw = swgoh_handler.Swgoh()

class SaveRoster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # SAVE mentioned user date to local DB
    @commands.command(aliases= ['sr', 'save'],pass_context = True)
    @commands.has_any_role('Master') # User need this role to run command (can have multiple)
    async def saveroster(self, ctx, user, save_name):
        self.ctx = ctx
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
    

    # SAVE mentioned user date to local DB
    @commands.command(aliases= ['list', 'ls'],pass_context = True)
    @commands.has_any_role('Master') # User need this role to run command (can have multiple)
    async def listsaves(self, ctx, user):
        self.ctx = ctx
        self.user = user
        await self.ctx.message.add_reaction("🐍")
        if user != "me":
            self.user_id = self.ctx.message.mentions[0].id
            
        else:
            self.user_id = self.ctx.author.id

        try:
            self.roster_saves = db.listsaves(self.user_id)
        except Exception as error:
            print(error)
        
        self.embed = discord.Embed(
            title = 'Roster Saves',
            description = 'Saved status for {}'.format(self.user),
            color = discord.Color.dark_blue()
            )

        self.embed.set_footer(text = 'Are these droids you are looking for?')
        self.embed.add_field(name='--------------------', value='--------------------' , inline=False)
        if self.roster_saves != None:
            for self.item, self.item_date in self.roster_saves.items():
                self.embed.add_field(name=self.item , value=self.item_date , inline=False)
            
            await self.ctx.send(embed=self.embed)




        else:
            await self.ctx.send('`💥 - It seems you don\'t have any saves`')



# --------------------------------
def setup(bot):
    bot.add_cog(SaveRoster(bot))
