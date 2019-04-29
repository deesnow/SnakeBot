import discord
from discord.ext import commands

# Discord Bot cog

class GetLinks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases= ['malac', 'malak'])
    async def getlink_malak(self, ctx):
        await ctx.message.add_reaction("🐍")
        await ctx.send('Ez az a link amire vágytál: https://docs.google.com/document/d/1wNiQWwOrcKEJ0H_uIFhHw6K_kxCVyK-G3Us8sh7mNdI/edit?usp=sharing')
    



# ---------------------------------------------
def setup(bot):
    bot.add_cog(GetLinks(bot))
