from api_swgoh_help import api_swgoh_help, settings
import time
from discord.ext import commands

import settings as mysettings
 
creds = settings(mysettings.HELPAPI_USER, mysettings.HELPAPI_PASS)

client = api_swgoh_help(creds)

class RANK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['JatekosRang'])
    @commands.has_any_role('Member', 'Master')  # User need this role to run command (can have multiple)
    async def rang(self, ctx, allycode: int):
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

            print(raw_player[0]['name'])

            await ctx.message.add_reaction("✅")

            player = fetchPlayerRoster(raw_player)

            player = fetchPlayerRanknev(player )

            await ctx.send(ctx.message.author.mention + " a jelenlegi rang pontszámod: " + str('{:,}'.format(player['rank'])) + ".  A rangod pedig: " + str(player['ranknev']))

            print(player['jatekosnev'])

            toc()

        else:
            pass

    @rang.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')


def fetchPlayerRanknev(player):

    if player['rank'] >= 0 and player['rank'] <= 5:
        player['ranknev'] = "Párafarmer"
    if player['rank'] > 5 and player['rank'] <= 10:
        player['ranknev'] = "Droid"
    if player['rank'] > 10 and player['rank'] <= 15:
        player['ranknev'] = "Scavenger / Roncsvadász"
    if player['rank'] > 15 and player['rank'] <= 20:
        player['ranknev'] = "Pirate / Kalóz"
    if player['rank'] > 20 and player['rank'] <= 25:
        player['ranknev'] = "Smuggler / Csempész"
    if player['rank'] > 25 and player['rank'] <= 30:
        player['ranknev'] = "Bounty Hunter / Fejvadász"
    if player['rank'] > 30 and player['rank'] <= 35:
        player['ranknev'] = "Rebel / Stormtrooper"
    if player['rank'] > 35 and player['rank'] <= 40:
        player['ranknev'] = "X-Wing Pilot / Tie-Fighter Pilot"

    return player

def fetchPlayerRoster(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "ranknev": " "
    }

    player['jatekosnev'] = raw_player[0]['name']
    i = 0
    t = 0
    s = 0
    for a in raw_player[0]['roster']:
        a = raw_player[0]['roster'][i]
        if a['defId'] == "GEONOSIANBROODALPHA" and a['gear'] >= 13:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 2:
                player['rank'] += 1
        if a['defId'] == "GEONOSIANSOLDIER" and a['gear'] >= 12:
            player['rank'] += 1
        if a['defId'] == "GEONOSIANSPY" and a['gear'] >= 12:
            player['rank'] += 1
        if a['defId'] == "SUNFAC" and a['gear'] >= 12:
            player['rank'] += 1
        if a['defId'] == "POGGLETHELESSER" and a['gear'] >= 12:
            player['rank'] += 1


        if a['defId'] == "GRIEVOUS" and a['gear'] >= 13:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 2:
                player['rank'] += 1
        if a['defId'] == "B1BATTLEDROIDV2" and a['gear'] >= 13:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 1:
                player['rank'] += 1
        if a['defId'] == "B2SUPERBATTLEDROID" and a['gear'] >= 13:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 1:
                player['rank'] += 1
        if a['defId'] == "MAGNAGUARD" and a['gear'] >= 13:
            player['rank'] += 1
        if a['defId'] == "DROIDEKA" and a['gear'] >= 12:
            player['rank'] += 1


        if a['defId'] == "DARTHTRAYA" and a['gear'] >= 12:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 2:
                player['rank'] += 1
        if a['defId'] == "DARTHSION" and a['gear'] >= 13:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 1:
                player['rank'] += 1
        if a['defId'] == "DARTHNIHILUS" and a['gear'] >= 12:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 1:
                player['rank'] += 1
        if a['defId'] == "GRANDADMIRALTHRAWN" and a['gear'] >= 12:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 1:
                player['rank'] += 1
        if a['defId'] == "COUNTDOOKU" and a['gear'] >= 12:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 1:
                player['rank'] += 1


        if a['defId'] == "DARTHREVAN" and a['gear'] >= 13:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 3:
                player['rank'] += 1
        if a['defId'] == "BASTILASHANDARK" and a['gear'] >= 13:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 1:
                player['rank'] += 1
        if a['defId'] == "SITHTROOPER" and a['gear'] >= 12:
            player['rank'] += 1
        if a['defId'] == "SITHMARAUDER" and a['gear'] >= 12:
            player['rank'] += 1
        if a['defId'] == "EMPERORPALPATINE" and a['gear'] >= 12:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 2:
                player['rank'] += 1


        if a['defId'] == "DARTHMALAK" and a['gear'] >= 13:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 2:
                player['rank'] += 1
        if a['defId'] == "NUTEGUNRAY" and a['gear'] >= 12:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 1:
                player['rank'] += 1


        if a['defId'] == "MOTHERTALZIN" and a['gear'] >= 12:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 2:
                player['rank'] += 1
        if a['defId'] == "ASAJVENTRESS" and a['gear'] >= 13:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 2:
                player['rank'] += 1
        if a['defId'] == "NIGHTSISTERZOMBIE" and a['gear'] >= 12:
            player['rank'] += 1
        if a['defId'] == "DAKA" and a['gear'] >= 13:
            player['rank'] += 1
        if a['defId'] == "TALIA" and a['gear'] >= 12 and s == 0:
            t = 1
            player['rank'] += 1
        if a['defId'] == "NIGHTSISTERSPIRIT" and a['gear'] >= 12 and t == 0:
            s = 1
            player['rank'] += 1


        if a['defId'] == "WATTAMBOR" and a['gear'] >= 12:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 1:
                player['rank'] += 1


        if a['defId'] == "CAPITALCHIMAERA" and a['rarity'] == 7 and a['level'] == 85:
            j = 0
            for b in raw_player[0]['roster']:
                b = raw_player[0]['roster'][j]
                if b['defId'] == "GRANDADMIRALTHRAWN" and b['gear'] >= 12:
                    temp = 0
                    for c in a['skills']:
                        if c['tier'] == 8:
                            temp += 1
                    if temp == 5:
                        player['rank'] += 1
                j += 1
        if a['defId'] == "CAPITALSTARDESTROYER" and a['rarity'] == 7 and a['level'] == 85:
            j = 0
            for b in raw_player[0]['roster']:
                b = raw_player[0]['roster'][j]
                if b['defId'] == "GRANDMOFFTARKIN" and b['gear'] >= 12:
                    temp = 0
                    for c in a['skills']:
                        if c['tier'] == 8:
                            temp += 1
                    if temp == 5:
                        player['rank'] += 1
                j += 1
        if a['defId'] == "CAPITALNEGOTIATOR" and a['rarity'] == 7 and a['level'] == 85:
            j = 0
            for b in raw_player[0]['roster']:
                b = raw_player[0]['roster'][j]
                if b['defId'] == "GENERALKENOBI" and b['gear'] >= 12:
                    temp = 0
                    for c in a['skills']:
                        if c['tier'] == 8:
                            temp += 1
                    if temp == 5:
                        player['rank'] += 1
                j += 1
        if a['defId'] == "GEONOSIANSTARFIGHTER2" and a['rarity'] == 7 and a['level'] == 85:
            j = 0
            for b in raw_player[0]['roster']:
                b = raw_player[0]['roster'][j]
                if b['defId'] == "GEONOSIANSOLDIER" and b['gear'] >= 12:
                    temp = 0
                    for c in a['skills']:
                        if c['tier'] == 8:
                            temp += 1
                    if temp >= 3:
                        player['rank'] += 1
                j += 1
        if a['defId'] == "GEONOSIANSTARFIGHTER3" and a['rarity'] == 7 and a['level'] == 85:
            j = 0
            for b in raw_player[0]['roster']:
                b = raw_player[0]['roster'][j]
                if b['defId'] == "GEONOSIANSPY" and b['gear'] >= 12:
                    temp = 0
                    for c in a['skills']:
                        if c['tier'] == 8:
                            temp += 1
                    if temp >= 3:
                        player['rank'] += 1
                j += 1
        if a['defId'] == "HOUNDSTOOTH" and a['rarity'] == 7 and a['level'] == 85:
            j = 0
            for b in raw_player[0]['roster']:
                b = raw_player[0]['roster'][j]
                if b['defId'] == "BOSSK" and b['gear'] >= 12:
                    temp = 0
                    for c in a['skills']:
                        if c['tier'] == 8:
                            temp += 1
                    if temp >= 3:
                        player['rank'] += 1
                j += 1
        if a['defId'] == "GEONOSIANSTARFIGHTER1" and a['rarity'] == 7 and a['level'] == 85:
            j = 0
            for b in raw_player[0]['roster']:
                b = raw_player[0]['roster'][j]
                if b['defId'] == "SUNFAC" and b['gear'] >= 12:
                    temp = 0
                    for c in a['skills']:
                        if c['tier'] == 8:
                            temp += 1
                    if temp >= 3:
                        player['rank'] += 1
                j += 1
        if a['defId'] == "MILLENNIUMFALCON" and a['rarity'] == 7 and a['level'] == 85:
            j = 0
            d = 0
            e = 0
            for b in raw_player[0]['roster']:
                b = raw_player[0]['roster'][j]
                if b['defId'] == "HANSOLO" and b['gear'] >= 12:
                    d = 1
                if b['defId'] == "CHEWBACCALEGENDARY" and b['gear'] >= 12:
                    e = 1
                j += 1
            if d == 1 and e == 1:
                temp = 0
                for c in a['skills']:
                    if c['tier'] == 8:
                        temp += 1
                if temp == 4:
                    player['rank'] += 1
        i += 1

    return player


def TicTocGenerator():
    # Generator that returns time differences
    ti = 0           # initial time
    tf = time.time() # final time
    while True:
        ti = tf
        tf = time.time()
        yield tf-ti # returns the time difference

TicToc = TicTocGenerator() # create an instance of the TicTocGen generator

# This will be the main function through which we define both tic() and toc()
def toc(tempBool=True):
    # Prints the time difference yielded by generator instance TicToc
    tempTimeInterval = next(TicToc)
    if tempBool:
        print( "Elapsed time: %f seconds.\n" %tempTimeInterval )

def tic():
    # Records a time in TicToc, marks the beginning of a time interval
    toc(False)


def setup(bot):
    bot.add_cog(RANK(bot))