import time
from numpy import *
from discord.ext import commands
from async_swgoh_help import async_swgoh_help, settings
import settings as mysettings
 
creds = settings(mysettings.HELPAPI_USER, mysettings.HELPAPI_PASS)

client = async_swgoh_help(creds)

class Top80(commands.Cog, name='Top 80 GP'):
    def __init__(self, bot):
        self.bot = bot
        self.relicTierGp= {
            '2': 0,
            '3': 759,
            '4': 1594,
            '5': 2505,
            '6': 3492,
            '7': 4554,
            '8': 6072,
            '9': 7969
        }

    @commands.command(aliases=['top80'], description='Top80 characters GP' )
    #@commands.has_any_role('CobraAdmin')  # User need this role to run command (can have multiple)
    async def Top80(self, ctx, allycode:int):
        self.allycode = allycode
        tic()
        await ctx.message.add_reaction("⏳")

        #raw_player = client.fetchPlayers(allycode)
        p1 = self.bot.loop.create_task(client.fetchPlayers(self.allycode))
        await p1

        self.raw_player = p1._result




        temp = 0

        try:
            self.raw_player['message'] == 'Cannot fetch data'
            await ctx.send("Hibás ally kód!")
            await ctx.message.add_reaction("❌")
            temp = -1
        except:
            pass

        if temp != -1:

            await ctx.message.add_reaction("✅")

            player = fetchPlayerRoster(self, self.raw_player)

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

def fetchPlayerRoster(self, raw_player):
    self.player = {
        "jatekosnev": " ",
        "top80": 0
    }

    temp = []
    self.player['jatekosnev'] = raw_player[0]['name']
    i = 0
    for a in raw_player[0]['roster']:
        if raw_player[0]['roster'][i]['combatType'] == "CHARACTER":
            temp.insert(i, raw_player[0]['roster'][i]['gp'])
            if raw_player[0]['roster'][i]['gear'] == 13:
                reliclvl =  str(raw_player[0]['roster'][i]['relic']['currentTier'])
                relicGp = self.relicTierGp[reliclvl]
                fullGp = raw_player[0]['roster'][i]['gp'] + relicGp
                temp.insert(i, fullGp)
        i += 1
    temp.sort(reverse=True)

    i = 0
    while i < 80:
        self.player['top80'] += temp[i]
        i += 1

    return self.player


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