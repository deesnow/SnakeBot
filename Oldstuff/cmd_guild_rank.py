from api_swgoh_help import api_swgoh_help, settings
from numpy import *
import discord
import time
from discord.ext import commands

import settings as mysettings
 
creds = settings(mysettings.HELPAPI_USER, mysettings.HELPAPI_PASS)
client = api_swgoh_help(creds)

class GUILDRANK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['GuildRang'])
    @commands.has_any_role('Leader', 'Officer', 'Commander', 'Master')  # User need this role to run command (can have multiple)
    async def guild_rang(self, ctx, allycode: int):
        tic()
        await ctx.message.add_reaction("⏳")

        raw_guild = client.fetchGuilds(allycode)

        temp = 0

        try:
            raw_guild['status_code'] == 404
            await ctx.send("Hibás ally kód!")
            await ctx.message.add_reaction("❌")
            temp = -1
        except:
            pass

        if temp != -1:

            await ctx.message.add_reaction("✅")

            guilddata = fetchGuildRoster(raw_guild)

            player = fetchPlayerRoster(guilddata)

            player.sort(reverse=True, key=Sort)

            player = fetchPlayerRanknev(player)

            i = 0
            n = int_(len(player))
            lth = 0
            while i < n:
                lth2 = int_(len(player[i]['jatekosnev']))
                if lth2 > lth:
                    lth = lth2
                i += 1

            embed = discord.Embed(title='Pilvax Hungary guild rang táblázata',
                                  url="https://swgoh.gg/g/1294/pilvax-hungary/",
                                  color=0x7289da)

            i = 0
            embed.add_field(name='=============== Top 10 Rangú játékos ===============', value=
            '```' + str(player[i]['jatekosnev']) + ' ' * (lth-len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['rank']) + ' pont' + '  ' + str(player[i]['ranknev']) + '\n' +
            str(player[i+1]['jatekosnev']) + ' ' * (lth-len(str(player[i+1]['jatekosnev']))) + ' ' + str(player[i+1]['rank']) + ' pont' + '  ' + str(player[i+1]['ranknev']) + '\n' +
            str(player[i+2]['jatekosnev']) + ' ' * (lth-len(str(player[i+2]['jatekosnev']))) + ' ' + str(player[i+2]['rank']) + ' pont' + '  ' + str(player[i+2]['ranknev']) + '\n' +
            str(player[i+3]['jatekosnev']) + ' ' * (lth-len(str(player[i+3]['jatekosnev']))) + ' ' + str(player[i+3]['rank']) + ' pont' + '  ' + str(player[i+3]['ranknev']) + '\n' +
            str(player[i+4]['jatekosnev']) + ' ' * (lth-len(str(player[i+4]['jatekosnev']))) + ' ' + str(player[i+4]['rank']) + ' pont' + '  ' + str(player[i+4]['ranknev']) + '\n' +
            str(player[i+5]['jatekosnev']) + ' ' * (lth-len(str(player[i+5]['jatekosnev']))) + ' ' + str(player[i+5]['rank']) + ' pont' + '  ' + str(player[i+5]['ranknev']) + '\n' +
            str(player[i+6]['jatekosnev']) + ' ' * (lth-len(str(player[i+6]['jatekosnev']))) + ' ' + str(player[i+6]['rank']) + ' pont' + '  ' + str(player[i+6]['ranknev']) + '\n' +
            str(player[i+7]['jatekosnev']) + ' ' * (lth-len(str(player[i+7]['jatekosnev']))) + ' ' + str(player[i+7]['rank']) + ' pont' + '  ' + str(player[i+7]['ranknev']) + '\n' +
            str(player[i+8]['jatekosnev']) + ' ' * (lth-len(str(player[i+8]['jatekosnev']))) + ' ' + str(player[i+8]['rank']) + ' pont' + '  ' + str(player[i+8]['ranknev']) + '\n' +
            str(player[i+9]['jatekosnev']) + ' ' * (lth-len(str(player[i+9]['jatekosnev']))) + ' ' + str(player[i+9]['rank']) + ' pont' + '  ' + str(player[i+9]['ranknev']) + '\n' + '```')

            i = 10
            embed.add_field(name='=================== Top 11 - 20 ===================', value=
            '```' + str(player[i]['jatekosnev']) + ' ' * (lth-len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['rank']) + ' pont' + '  ' + str(player[i]['ranknev']) + '\n' +
            str(player[i+1]['jatekosnev']) + ' ' * (lth-len(str(player[i+1]['jatekosnev']))) + ' ' + str(player[i+1]['rank']) + ' pont' + '  ' + str(player[i+1]['ranknev']) + '\n' +
            str(player[i+2]['jatekosnev']) + ' ' * (lth-len(str(player[i+2]['jatekosnev']))) + ' ' + str(player[i+2]['rank']) + ' pont' + '  ' + str(player[i+2]['ranknev']) + '\n' +
            str(player[i+3]['jatekosnev']) + ' ' * (lth-len(str(player[i+3]['jatekosnev']))) + ' ' + str(player[i+3]['rank']) + ' pont' + '  ' + str(player[i+3]['ranknev']) + '\n' +
            str(player[i+4]['jatekosnev']) + ' ' * (lth-len(str(player[i+4]['jatekosnev']))) + ' ' + str(player[i+4]['rank']) + ' pont' + '  ' + str(player[i+4]['ranknev']) + '\n' +
            str(player[i+5]['jatekosnev']) + ' ' * (lth-len(str(player[i+5]['jatekosnev']))) + ' ' + str(player[i+5]['rank']) + ' pont' + '  ' + str(player[i+5]['ranknev']) + '\n' +
            str(player[i+6]['jatekosnev']) + ' ' * (lth-len(str(player[i+6]['jatekosnev']))) + ' ' + str(player[i+6]['rank']) + ' pont' + '  ' + str(player[i+6]['ranknev']) + '\n' +
            str(player[i+7]['jatekosnev']) + ' ' * (lth-len(str(player[i+7]['jatekosnev']))) + ' ' + str(player[i+7]['rank']) + ' pont' + '  ' + str(player[i+7]['ranknev']) + '\n' +
            str(player[i+8]['jatekosnev']) + ' ' * (lth-len(str(player[i+8]['jatekosnev']))) + ' ' + str(player[i+8]['rank']) + ' pont' + '  ' + str(player[i+8]['ranknev']) + '\n' +
            str(player[i+9]['jatekosnev']) + ' ' * (lth-len(str(player[i+9]['jatekosnev']))) + ' ' + str(player[i+9]['rank']) + ' pont' + '  ' + str(player[i+9]['ranknev']) + '\n' + '```')

            i = 20
            embed.add_field(name='=================== Top 21 - 30 ===================', value=
            '```' + str(player[i]['jatekosnev']) + ' ' * (lth-len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['rank']) + ' pont' + '  ' + str(player[i]['ranknev']) + '\n' +
            str(player[i+1]['jatekosnev']) + ' ' * (lth-len(str(player[i+1]['jatekosnev']))) + ' ' + str(player[i+1]['rank']) + ' pont' + '  ' + str(player[i+1]['ranknev']) + '\n' +
            str(player[i+2]['jatekosnev']) + ' ' * (lth-len(str(player[i+2]['jatekosnev']))) + ' ' + str(player[i+2]['rank']) + ' pont' + '  ' + str(player[i+2]['ranknev']) + '\n' +
            str(player[i+3]['jatekosnev']) + ' ' * (lth-len(str(player[i+3]['jatekosnev']))) + ' ' + str(player[i+3]['rank']) + ' pont' + '  ' + str(player[i+3]['ranknev']) + '\n' +
            str(player[i+4]['jatekosnev']) + ' ' * (lth-len(str(player[i+4]['jatekosnev']))) + ' ' + str(player[i+4]['rank']) + ' pont' + '  ' + str(player[i+4]['ranknev']) + '\n' +
            str(player[i+5]['jatekosnev']) + ' ' * (lth-len(str(player[i+5]['jatekosnev']))) + ' ' + str(player[i+5]['rank']) + ' pont' + '  ' + str(player[i+5]['ranknev']) + '\n' +
            str(player[i+6]['jatekosnev']) + ' ' * (lth-len(str(player[i+6]['jatekosnev']))) + ' ' + str(player[i+6]['rank']) + ' pont' + '  ' + str(player[i+6]['ranknev']) + '\n' +
            str(player[i+7]['jatekosnev']) + ' ' * (lth-len(str(player[i+7]['jatekosnev']))) + ' ' + str(player[i+7]['rank']) + ' pont' + '  ' + str(player[i+7]['ranknev']) + '\n' +
            str(player[i+8]['jatekosnev']) + ' ' * (lth-len(str(player[i+8]['jatekosnev']))) + ' ' + str(player[i+8]['rank']) + ' pont' + '  ' + str(player[i+8]['ranknev']) + '\n' +
            str(player[i+9]['jatekosnev']) + ' ' * (lth-len(str(player[i+9]['jatekosnev']))) + ' ' + str(player[i+9]['rank']) + ' pont' + '  ' + str(player[i+9]['ranknev']) + '\n' + '```')

            i = 30
            embed.add_field(name='=================== Top 31 - 40 ===================', value=
            '```' + str(player[i]['jatekosnev']) + ' ' * (lth-len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['rank']) + ' pont' + '  ' + str(player[i]['ranknev']) + '\n' +
            str(player[i+1]['jatekosnev']) + ' ' * (lth-len(str(player[i+1]['jatekosnev']))) + ' ' + str(player[i+1]['rank']) + ' pont' + '  ' + str(player[i+1]['ranknev']) + '\n' +
            str(player[i+2]['jatekosnev']) + ' ' * (lth-len(str(player[i+2]['jatekosnev']))) + ' ' + str(player[i+2]['rank']) + ' pont' + '  ' + str(player[i+2]['ranknev']) + '\n' +
            str(player[i+3]['jatekosnev']) + ' ' * (lth-len(str(player[i+3]['jatekosnev']))) + ' ' + str(player[i+3]['rank']) + ' pont' + '  ' + str(player[i+3]['ranknev']) + '\n' +
            str(player[i+4]['jatekosnev']) + ' ' * (lth-len(str(player[i+4]['jatekosnev']))) + ' ' + str(player[i+4]['rank']) + ' pont' + '  ' + str(player[i+4]['ranknev']) + '\n' +
            str(player[i+5]['jatekosnev']) + ' ' * (lth-len(str(player[i+5]['jatekosnev']))) + ' ' + str(player[i+5]['rank']) + ' pont' + '  ' + str(player[i+5]['ranknev']) + '\n' +
            str(player[i+6]['jatekosnev']) + ' ' * (lth-len(str(player[i+6]['jatekosnev']))) + ' ' + str(player[i+6]['rank']) + ' pont' + '  ' + str(player[i+6]['ranknev']) + '\n' +
            str(player[i+7]['jatekosnev']) + ' ' * (lth-len(str(player[i+7]['jatekosnev']))) + ' ' + str(player[i+7]['rank']) + ' pont' + '  ' + str(player[i+7]['ranknev']) + '\n' +
            str(player[i+8]['jatekosnev']) + ' ' * (lth-len(str(player[i+8]['jatekosnev']))) + ' ' + str(player[i+8]['rank']) + ' pont' + '  ' + str(player[i+8]['ranknev']) + '\n' +
            str(player[i+9]['jatekosnev']) + ' ' * (lth-len(str(player[i+9]['jatekosnev']))) + ' ' + str(player[i+9]['rank']) + ' pont' + '  ' + str(player[i+9]['ranknev']) + '\n' + '```')

            i = 40
            embed.add_field(name='=================== Top 41 - 50 ===================', value=
            '```' + str(player[i]['jatekosnev']) + ' ' * (lth-len(str(player[i]['jatekosnev']))) + ' ' * round(1 / len(str(player[i]['rank']))) + str(player[i]['rank']) + ' pont' + '  ' + str(player[i]['ranknev']) + '\n' +
            str(player[i+1]['jatekosnev']) + ' ' * (lth-len(str(player[i+1]['jatekosnev']))) + ' ' * round(1 / len(str(player[i+1]['rank']))) + str(player[i+1]['rank']) + ' pont' + '  ' + str(player[i+1]['ranknev']) + '\n' +
            str(player[i+2]['jatekosnev']) + ' ' * (lth-len(str(player[i+2]['jatekosnev']))) + ' ' * round(1 / len(str(player[i+2]['rank']))) + str(player[i+2]['rank']) + ' pont' + '  ' + str(player[i+2]['ranknev']) + '\n' +
            str(player[i+3]['jatekosnev']) + ' ' * (lth-len(str(player[i+3]['jatekosnev']))) + ' ' * round(1 / len(str(player[i+3]['rank']))) + str(player[i+3]['rank']) + ' pont' + '  ' + str(player[i+3]['ranknev']) + '\n' +
            str(player[i+4]['jatekosnev']) + ' ' * (lth-len(str(player[i+4]['jatekosnev']))) + ' ' * round(1 / len(str(player[i+4]['rank']))) + str(player[i+4]['rank']) + ' pont' + '  ' + str(player[i+4]['ranknev']) + '\n' +
            str(player[i+5]['jatekosnev']) + ' ' * (lth-len(str(player[i+5]['jatekosnev']))) + ' ' * round(1 / len(str(player[i+5]['rank']))) + str(player[i+5]['rank']) + ' pont' + '  ' + str(player[i+5]['ranknev']) + '\n' +
            str(player[i+6]['jatekosnev']) + ' ' * (lth-len(str(player[i+6]['jatekosnev']))) + ' ' * round(1 / len(str(player[i+6]['rank']))) + str(player[i+6]['rank']) + ' pont' + '  ' + str(player[i+6]['ranknev']) + '\n' +
            str(player[i+7]['jatekosnev']) + ' ' * (lth-len(str(player[i+7]['jatekosnev']))) + ' ' * round(1 / len(str(player[i+7]['rank']))) + str(player[i+7]['rank']) + ' pont' + '  ' + str(player[i+7]['ranknev']) + '\n' +
            str(player[i+8]['jatekosnev']) + ' ' * (lth-len(str(player[i+8]['jatekosnev']))) + ' ' * round(1 / len(str(player[i+8]['rank']))) + str(player[i+8]['rank']) + ' pont' + '  ' + str(player[i+8]['ranknev']) + '\n' +
            str(player[i+9]['jatekosnev']) + ' ' * (lth-len(str(player[i+9]['jatekosnev']))) + ' ' * round(1 / len(str(player[i+9]['rank']))) + str(player[i+9]['rank']) + ' pont' + '  ' + str(player[i+9]['ranknev']) + '\n' + '```')



            await ctx.send(embed=embed)

            toc()

        else:
            pass

    @guild_rang.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')

def Sort(a):
    return a['rank']

def fetchPlayerRanknev(player):
    i = 0
    n = int_(len(player))
    while i < n:
        if player[i]['rank'] >= 0 and player[i]['rank'] <= 5:
            player[i]['ranknev'] = "Párafarmer"
        if player[i]['rank'] > 5 and player[i]['rank'] <= 10:
            player[i]['ranknev'] = "Droid"
        if player[i]['rank'] > 10 and player[i]['rank'] <= 15:
            player[i]['ranknev'] = "Roncsvadász"
        if player[i]['rank'] > 15 and player[i]['rank'] <= 20:
            player[i]['ranknev'] = "Kalóz"
        if player[i]['rank'] > 20 and player[i]['rank'] <= 25:
            player[i]['ranknev'] = "Csempész"
        if player[i]['rank'] > 25 and player[i]['rank'] <= 30:
            player[i]['ranknev'] = "Fejvadász"
        if player[i]['rank'] > 30 and player[i]['rank'] <= 35:
            player[i]['ranknev'] = "Stormtrooper"
        if player[i]['rank'] > 35 and player[i]['rank'] <= 40:
            player[i]['ranknev'] = "Tie-Fighter Pilot"
        i += 1

    return player

def fetchGuildRoster(raw_guild):
    guilddata = []
    chardata_ally = []
    chardata_ally2 = []
    i: int = 0
    lth = int_(len(raw_guild[0]['roster']))
    lthp2 = int_(round(lth/2, 0))
    while i < lthp2:
        chardata_ally.insert(i, raw_guild[0]['roster'][i]['allyCode'])
        i += 1

    guilddata = client.fetchPlayers(chardata_ally)

    while i < lth:
        chardata_ally2.insert(i, raw_guild[0]['roster'][i]['allyCode'])
        i += 1

    guilddata += client.fetchPlayers(chardata_ally2)

    return guilddata


def fetchPlayerRoster(guilddata):
    player = [{'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0},
              {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0},
              {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0},
              {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0},
              {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0},
              {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0},
              {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0},
              {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0},
              {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0},
              {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}]

    k = 0
    for g in guilddata:
        player[k]['jatekosnev'] = guilddata[k]['name']
        player[k]['rank'] = 0
        raw_player = guilddata[k]
        i = 0
        t = 0
        s = 0
        for a in raw_player['roster']:
            a = raw_player['roster'][i]
            if a['defId'] == "GEONOSIANBROODALPHA" and a['gear'] >= 13:
                temp = 0
                for b in a['skills']:
                    if b['tier'] == 8 and b['isZeta'] == True:
                        temp += 1
                if temp >= 2:
                    player[k]['rank'] += 1
            if a['defId'] == "GEONOSIANSOLDIER" and a['gear'] >= 12:
                player[k]['rank'] += 1
            if a['defId'] == "GEONOSIANSPY" and a['gear'] >= 12:
                player[k]['rank'] += 1
            if a['defId'] == "SUNFAC" and a['gear'] >= 12:
                player[k]['rank'] += 1
            if a['defId'] == "POGGLETHELESSER" and a['gear'] >= 12:
                player[k]['rank'] += 1


            if a['defId'] == "GRIEVOUS" and a['gear'] >= 13:
                temp = 0
                for b in a['skills']:
                    if b['tier'] == 8 and b['isZeta'] == True:
                        temp += 1
                if temp >= 2:
                    player[k]['rank'] += 1
            if a['defId'] == "B1BATTLEDROIDV2" and a['gear'] >= 13:
                temp = 0
                for b in a['skills']:
                    if b['tier'] == 8 and b['isZeta'] == True:
                        temp += 1
                if temp >= 1:
                    player[k]['rank'] += 1
            if a['defId'] == "B2SUPERBATTLEDROID" and a['gear'] >= 13:
                temp = 0
                for b in a['skills']:
                    if b['tier'] == 8 and b['isZeta'] == True:
                        temp += 1
                if temp >= 1:
                    player[k]['rank'] += 1
            if a['defId'] == "MAGNAGUARD" and a['gear'] >= 13:
                player[k]['rank'] += 1
            if a['defId'] == "DROIDEKA" and a['gear'] >= 12:
                player[k]['rank'] += 1


            if a['defId'] == "DARTHTRAYA" and a['gear'] >= 12:
                temp = 0
                for b in a['skills']:
                    if b['tier'] == 8 and b['isZeta'] == True:
                        temp += 1
                if temp >= 2:
                    player[k]['rank'] += 1
            if a['defId'] == "DARTHSION" and a['gear'] >= 13:
                temp = 0
                for b in a['skills']:
                    if b['tier'] == 8 and b['isZeta'] == True:
                        temp += 1
                if temp >= 1:
                    player[k]['rank'] += 1
            if a['defId'] == "DARTHNIHILUS" and a['gear'] >= 12:
                temp = 0
                for b in a['skills']:
                    if b['tier'] == 8 and b['isZeta'] == True:
                        temp += 1
                if temp >= 1:
                    player[k]['rank'] += 1
            if a['defId'] == "GRANDADMIRALTHRAWN" and a['gear'] >= 12:
                temp = 0
                for b in a['skills']:
                    if b['tier'] == 8 and b['isZeta'] == True:
                        temp += 1
                if temp >= 1:
                    player[k]['rank'] += 1
            if a['defId'] == "COUNTDOOKU" and a['gear'] >= 12:
                temp = 0
                for b in a['skills']:
                    if b['tier'] == 8 and b['isZeta'] == True:
                        temp += 1
                if temp >= 1:
                    player[k]['rank'] += 1


            if a['defId'] == "DARTHREVAN" and a['gear'] >= 13:
                temp = 0
                for b in a['skills']:
                    if b['tier'] == 8 and b['isZeta'] == True:
                        temp += 1
                if temp >= 3:
                    player[k]['rank'] += 1
            if a['defId'] == "BASTILASHANDARK" and a['gear'] >= 13:
                temp = 0
                for b in a['skills']:
                    if b['tier'] == 8 and b['isZeta'] == True:
                        temp += 1
                if temp >= 1:
                    player[k]['rank'] += 1
            if a['defId'] == "SITHTROOPER" and a['gear'] >= 12:
                player[k]['rank'] += 1
            if a['defId'] == "SITHMARAUDER" and a['gear'] >= 12:
                player[k]['rank'] += 1
            if a['defId'] == "EMPERORPALPATINE" and a['gear'] >= 12:
                temp = 0
                for b in a['skills']:
                    if b['tier'] == 8 and b['isZeta'] == True:
                        temp += 1
                if temp >= 2:
                    player[k]['rank'] += 1


            if a['defId'] == "DARTHMALAK" and a['gear'] >= 13:
                temp = 0
                for b in a['skills']:
                    if b['tier'] == 8 and b['isZeta'] == True:
                        temp += 1
                if temp >= 2:
                    player[k]['rank'] += 1
            if a['defId'] == "NUTEGUNRAY" and a['gear'] >= 12:
                temp = 0
                for b in a['skills']:
                    if b['tier'] == 8 and b['isZeta'] == True:
                        temp += 1
                if temp >= 1:
                    player[k]['rank'] += 1


            if a['defId'] == "MOTHERTALZIN" and a['gear'] >= 12:
                temp = 0
                for b in a['skills']:
                    if b['tier'] == 8 and b['isZeta'] == True:
                        temp += 1
                if temp >= 2:
                    player[k]['rank'] += 1
            if a['defId'] == "ASAJVENTRESS" and a['gear'] >= 13:
                temp = 0
                for b in a['skills']:
                    if b['tier'] == 8 and b['isZeta'] == True:
                        temp += 1
                if temp >= 2:
                    player[k]['rank'] += 1
            if a['defId'] == "NIGHTSISTERZOMBIE" and a['gear'] >= 12:
                player[k]['rank'] += 1
            if a['defId'] == "DAKA" and a['gear'] >= 13:
                player[k]['rank'] += 1
            if a['defId'] == "TALIA" and a['gear'] >= 12 and s == 0:
                t = 1
                player[k]['rank'] += 1
            if a['defId'] == "NIGHTSISTERSPIRIT" and a['gear'] >= 12 and t == 0:
                s = 1
                player[k]['rank'] += 1


            if a['defId'] == "WATTAMBOR" and a['gear'] >= 12:
                temp = 0
                for b in a['skills']:
                    if b['tier'] == 8 and b['isZeta'] == True:
                        temp += 1
                if temp >= 1:
                    player[k]['rank'] += 1


            if a['defId'] == "CAPITALCHIMAERA" and a['rarity'] == 7 and a['level'] == 85:
                j = 0
                for b in raw_player['roster']:
                    b = raw_player['roster'][j]
                    if b['defId'] == "GRANDADMIRALTHRAWN" and b['gear'] >= 12:
                        temp = 0
                        for c in a['skills']:
                            if c['tier'] == 8:
                                temp += 1
                        if temp == 5:
                            player[k]['rank'] += 1
                    j += 1
            if a['defId'] == "CAPITALSTARDESTROYER" and a['rarity'] == 7 and a['level'] == 85:
                j = 0
                for b in raw_player['roster']:
                    b = raw_player['roster'][j]
                    if b['defId'] == "GRANDMOFFTARKIN" and b['gear'] >= 12:
                        temp = 0
                        for c in a['skills']:
                            if c['tier'] == 8:
                                temp += 1
                        if temp == 5:
                            player[k]['rank'] += 1
                    j += 1
            if a['defId'] == "CAPITALNEGOTIATOR" and a['rarity'] == 7 and a['level'] == 85:
                j = 0
                for b in raw_player['roster']:
                    b = raw_player['roster'][j]
                    if b['defId'] == "GENERALKENOBI" and b['gear'] >= 12:
                        temp = 0
                        for c in a['skills']:
                            if c['tier'] == 8:
                                temp += 1
                        if temp == 5:
                            player[k]['rank'] += 1
                    j += 1
            if a['defId'] == "GEONOSIANSTARFIGHTER2" and a['rarity'] == 7 and a['level'] == 85:
                j = 0
                for b in raw_player['roster']:
                    b = raw_player['roster'][j]
                    if b['defId'] == "GEONOSIANSOLDIER" and b['gear'] >= 12:
                        temp = 0
                        for c in a['skills']:
                            if c['tier'] == 8:
                                temp += 1
                        if temp >= 3:
                            player[k]['rank'] += 1
                    j += 1
            if a['defId'] == "GEONOSIANSTARFIGHTER3" and a['rarity'] == 7 and a['level'] == 85:
                j = 0
                for b in raw_player['roster']:
                    b = raw_player['roster'][j]
                    if b['defId'] == "GEONOSIANSPY" and b['gear'] >= 12:
                        temp = 0
                        for c in a['skills']:
                            if c['tier'] == 8:
                                temp += 1
                        if temp >= 3:
                            player[k]['rank'] += 1
                    j += 1
            if a['defId'] == "HOUNDSTOOTH" and a['rarity'] == 7 and a['level'] == 85:
                j = 0
                for b in raw_player['roster']:
                    b = raw_player['roster'][j]
                    if b['defId'] == "BOSSK" and b['gear'] >= 12:
                        temp = 0
                        for c in a['skills']:
                            if c['tier'] == 8:
                                temp += 1
                        if temp >= 3:
                            player[k]['rank'] += 1
                    j += 1
            if a['defId'] == "GEONOSIANSTARFIGHTER1" and a['rarity'] == 7 and a['level'] == 85:
                j = 0
                for b in raw_player['roster']:
                    b = raw_player['roster'][j]
                    if b['defId'] == "SUNFAC" and b['gear'] >= 12:
                        temp = 0
                        for c in a['skills']:
                            if c['tier'] == 8:
                                temp += 1
                        if temp >= 3:
                            player[k]['rank'] += 1
                    j += 1
            if a['defId'] == "MILLENNIUMFALCON" and a['rarity'] == 7 and a['level'] == 85:
                j = 0
                d = 0
                e = 0
                for b in raw_player['roster']:
                    b = raw_player['roster'][j]
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
                        player[k]['rank'] += 1
            i += 1
        k += 1

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
    bot.add_cog(GUILDRANK(bot))