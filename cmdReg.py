import discord
from discord.ext import commands
import db_handler as mongo

db = mongo.Db_handler()

# Discord Bot cog

class Reg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pont+')


    @commands.command(aliases= ['reg', 'r'])
    async def register(self, ctx, user,  ally_code):
        await ctx.message.add_reaction("🐍")
        if user != "me":
            reg_id = ctx.message.mentions[0].id
            reg_disc = ctx.message.mentions[0].discriminator
            reg_name = ctx.message.mentions[0].display_name
            reg_user = reg_name + "#" + reg_disc
        else:
            reg_id= ctx.author.id
            reg_user = str(ctx.author)

        try:
            ally_code = int(ally_code)

            user_data = {'discord_id':reg_id,
                            'user_id':reg_user,
                            'ally_code': ally_code }
            try:
                action = db.user_add(user_data)
                
                if action == "Done":
                    await ctx.send('{} user with {} allycode is REGISTERED'.format(ctx.author, ally_code))
                elif action == "Already":
                    await ctx.send('{} user with {} allycode is already REGISTERED'.format(ctx.author, ally_code))
                else:
                    await ctx.send('Something went wrong, check Bot logs') 
            except Exception as identifier:
                pass
        except:
            await ctx.send('Hahooo {} \
                The <{}> is not a valid ally_code.Only numbers are accepted and add it without <->.'.format(ctx.author.mention, ally_code))



# ---------------------------------------------
def setup(bot):
    bot.add_cog(Reg(bot))
