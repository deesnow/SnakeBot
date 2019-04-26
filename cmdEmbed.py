import discord
from discord.ext import commands
import db_handler as mongo

db = mongo.Db_handler()

class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(aliases= ['dis', 'dp'])
    async def display(self, ctx):
        
        self.embed = discord.Embed(
            title = 'Command Title',
            description = 'This is a description',
            color = discord.Color.dark_blue()
        )

        self.embed.set_footer(text = 'This is a footer.')
        self.embed.set_image(url='https://i.imgur.com/NWFHq9y.jpg')
        self.embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/558224062166335509/430849dd3a3d2b9179aaa0006ca22d88.png')
        self.embed.set_author(name='SnakeBot', icon_url='https://cdn.discordapp.com/avatars/558224062166335509/430849dd3a3d2b9179aaa0006ca22d88.png')
        self.embed.add_field(name='Filed1', value='Value1', inline=False)
        self.embed.add_field(name='Filed2', value='Value2', inline=True)
        self.embed.add_field(name='Filed3', value='Value3', inline=True)

        await ctx.send(embed = self.embed)


# ---------------------------------------------
def setup(bot):
    bot.add_cog(Embed(bot))
