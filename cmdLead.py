from async_swgoh_help import async_swgoh_help, settings
from discord.ext import commands
import settings as mysettings
import logging

creds = settings(mysettings.HELPAPI_USER, mysettings.HELPAPI_PASS)
client = async_swgoh_help(creds)

class Leader(commands.Cog,  name='Guild Commands'):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.info('Init cmdRoster COG')
#--------------------------------------------------------

    @commands.command(pass_context=True, name='lead')
    @commands.has_any_role('Master', 'Officer', 'Confederate Generals', 'Generals')  # User need this role to run command (can have multiple)
 
    async def lead(self, ctx, allycode: int):

        self.allycode = allycode
        
        await ctx.message.add_reaction("⏳")

        rg = self.bot.loop.create_task(client.fetchGuilds(allycode))
        
        self.msg1 = await ctx.send('Guild adatok lekérdezése folyamatban 🔎')
        
        await rg
        raw_guild = rg._result

        for i in raw_guild[0]['roster']:
            if i["guildMemberLevel"] == "GUILDLEADER":
                self.leader_name = i["name"]
                self.leader_allycode = i["allyCode"]
                break
        

        self.msg2 = await ctx.send(f'Leader Name: {self.leader_name} \nLeader Allycode: {self.leader_allycode}')

    @lead.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')
        else:
            await self.ctx.send('⛔ - Szar van a palacsintában, próbáld újra \n')









# --------------------------------
def setup(bot):
    bot.add_cog(Leader(bot))


