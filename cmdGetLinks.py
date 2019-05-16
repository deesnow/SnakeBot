import discord
from discord.ext import commands
import db_handler as mongo
db = mongo.Db_handler()


# Discord Bot cog

class GetLinks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(aliases= ['malac', 'malak'])
    async def getlink_malak(self, ctx):
        await ctx.message.add_reaction("🐍")
        await ctx.send('Ez az a link amire vágytál: https://docs.google.com/document/d/1wNiQWwOrcKEJ0H_uIFhHw6K_kxCVyK-G3Us8sh7mNdI/edit?usp=sharing')

    @commands.command(aliases= ['al', 'addl'])
    async def add_link(self, ctx, name, desc, url):
        self.ctx = ctx
        self.name = name
        self.desc = desc
        self.url = url
        await ctx.message.add_reaction("🐍")

        self.add = db.link_add(self.name, self.desc, self.url)
        if self.add == "done":
            await ctx.send('LinkDB updated ✅')
        else:
            await ctx.send('LinkDB update failed! 💥')

    @commands.command(aliases= ['ll'])
    async def list_link(self, ctx):
        self.ctx = ctx
        await ctx.message.add_reaction("🐍")

        self.embed = discord.Embed(
            title = 'Saved Links',
            description = '-------------------',
            color = discord.Color.dark_blue()
            )
        self.embed.set_footer(text = 'Are these droids you are looking for?')
        #self.embed.add_field(name='--------------------', value='--------------------' , inline=False)

        self.result = db.link_list()
        if self.result != "failed":
            for link in self.result:
                self.name = link['shortname']
                self.desc = link['description']
                self.url = link['url']
                self.embed.add_field(name= self.name, value= self.desc , inline=False)
            await self.ctx.send(embed=self.embed)
        else:
            await ctx.send('💥 List is empty!')

    @commands.command(aliases= ['getlink', 'gl'])
    async def get_link(self, ctx, name):
        self.ctx = ctx
        self.name = name
        await ctx.message.add_reaction("🐍")

        

        self.result = db.link_get(self.name)
        if self.result != "failed":
            for link in self.result:
                self.name = link['shortname']
                self.desc = link['description']
                self.url = link['url']

                self.embed = discord.Embed(
                        title = 'Saved Link for {}'.format(self.name),
                        description = '-------------------',
                        color = discord.Color.dark_blue()
                        )
                self.embed.set_footer(text = 'Are these droids you are looking for?')
                #self.embed.add_field(name='--------------------', value='--------------------' , inline=False)
                
                self.embed.add_field(name= 'Link:', value=self.url  , inline=False)

            await self.ctx.send(embed=self.embed)
        else:
            await ctx.send('💥 List is empty!')



    



# ---------------------------------------------
def setup(bot):
    bot.add_cog(GetLinks(bot))
