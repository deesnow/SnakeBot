import time
from numpy import *
from discord.ext import commands
from api_swgoh_help import api_swgoh_help, settings
import settings as mysettings
 
creds = settings(mysettings.HELPAPI_USER, mysettings.HELPAPI_PASS)

client = api_swgoh_help(creds)

class Top80(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Top 80'])
    #@commands.has_any_role('CobraAdmin')  # User need this role to run command (can have multiple)
    async def Top80(self,ctx,allycode:int):

        tic()
        await ctx.message.add_reaction("⏳")

        raw_player = client.fetchPlayers(allycode)

        temp = 0

        try:
            raw_player['status_code'] == 404
            await ctx.send("Hibás ally kód!")
            await ctx.message.add_reaction("❌")
            temp = -1
        except:
            pass

        if temp != -1:

            await ctx.message.add_reaction("✅")

            player = fetchPlayerRoster(raw_player)

            await ctx.send(ctx.message.author.mention + "  " + player['jatekosnev'] + " top 80 karakter GP-je: " + str('{:,}'.format(player['top80'])))

            toc()

        else:
            pass


    @Top80.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')

def fetchPlayerRoster(raw_player):
    player = {
        "jatekosnev": " ",
        "top80": 0
    }

    temp = []
    player['jatekosnev'] = raw_player[0]['name']
    i = 0
    for a in raw_player[0]['roster']:
        if raw_player[0]['roster'][i]['combatType'] == "CHARACTER":
            temp.insert(i, raw_player[0]['roster'][i]['gp'])
        i += 1
    temp.sort(reverse=True)

    i = 0
    while i < 80:
        player['top80'] += temp[i]
        i += 1

    return player

def TicTocGenerator():
    # Generator that returns time differences
    ti = 0  # initial time
    tf = time.time()  # final time
    while True:
        ti = tf
        tf = time.time()
        yield tf - ti  # returns the time difference


TicToc = TicTocGenerator()  # create an instance of the TicTocGen generator


# This will be the main function through which we define both tic() and toc()
def toc(tempBool=True):
    # Prints the time difference yielded by generator instance TicToc
    tempTimeInterval = next(TicToc)
    if tempBool:
        print("Elapsed time: %f seconds.\n" % tempTimeInterval)


def tic():
    # Records a time in TicToc, marks the beginning of a time interval
    toc(False)


def setup(bot):
    bot.add_cog(Top80(bot))