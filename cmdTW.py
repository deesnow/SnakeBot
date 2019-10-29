import time
import discord
from numpy import *
from discord.ext import commands
from async_swgoh_help import async_swgoh_help, settings
import settings as mysettings
 
creds = settings(mysettings.HELPAPI_USER, mysettings.HELPAPI_PASS)
client = async_swgoh_help(creds)
 
class TW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    @commands.command(aliases=['Territory War'],pass_context=True)
    @commands.has_any_role('Master', 'Officer')  # User need this role to run command (can have multiple)
 
    async def tw(self, ctx, allycode1: int, allycode2: int):
        tic()
        await ctx.message.add_reaction("⏳")
 
        character_list = ["DARTHREVAN",
                          "DARTHMALAK",
                          "JEDIKNIGHTREVAN",
                          "PADMEAMIDALA",
                          "GRIEVOUS",
                          "GEONOSIANBROODALPHA"]
 
        ship_list = ["MILLENNIUMFALCON",
                     "JEDISTARFIGHTERANAKIN"]
 
        character_list2 = ["Darth Revan",
                           "Darth Malak",
                           "Jedi Knight Revan",
                           "Padmé Amidala",
                           "General Grievous",
                           "Geonosian Brood Alpha"]
 
        ship_list2 = ["Han's Millennium Falcon",
                      "Anakin's Eta-2 Starfighter"]
 
        rg1 = self.bot.loop.create_task(client.fetchGuilds(allycode1))
        rg2 = self.bot.loop.create_task(client.fetchGuilds(allycode2))

        self.msg1 = await ctx.send('Guild adatok lekérdezése folyamatban 🔎')
        
        await rg1
        await rg2

        raw_guild1 = rg1._result
        raw_guild2 = rg2._result
 
        temp1 = 0
        temp2 = 0
 
        try:
            raw_guild1['message'] == 'Cannot fetch data'
            await ctx.send("Hibás ally 1 kód!")
            await ctx.message.add_reaction("❌")
            temp1 = -1
        except:
            pass
 
        try:
            raw_guild2['message'] == 'Cannot fetch data'
            await ctx.send("Hibás ally 2 kód!")
            await ctx.message.add_reaction("❌")
            temp2 = -1
        except:
            pass
 
        if temp1 != -1 and temp2 != -1:
 
            #await ctx.message.add_reaction("✅")
            await self.msg1.edit(content='✅ - Guild adatok letöltve, játékosok roosterének lekérdezése folyamatban 🔎')
            
 
            self.gddata1 = self.bot.loop.create_task( self.fetchGuildRoster(raw_guild1))
            self.gddata2 = self.bot.loop.create_task( self.fetchGuildRoster(raw_guild2))
            await self.gddata1
            await self.gddata2

            guilddata1 = self.gddata1._result
            guilddata2 = self.gddata2._result

            msg2 = await self.msg1.edit(content='✅ - Játoés roster adatok letöltve, feldolgozás folyamatban 🔄')
 
            embed = discord.Embed(title=raw_guild1[0]['name'] + ' vs ' + raw_guild2[0]['name'], url="https://swgoh.gg/p/" + str(raw_guild2[0]['roster'][0]['allyCode']) + "/", color=0x7289da)
 
            overview1 = self.overview(raw_guild1, guilddata1)
            overview2 = self.overview(raw_guild2, guilddata2)
 
            lth: int = 6
 
            embed.add_field(name='=========== Összefoglaló ===========', value=
            '```Létszám         ::  ' + ' ' * (lth - len(str(overview1['tagok_szama']))) + str(overview1['tagok_szama']) + ' vs ' + str(overview2['tagok_szama']) + '\n' +
            'GP              :: ' + ' ' * (lth - len(str(overview1['ossz_gp']))) + str('{:,}'.format(overview1['ossz_gp'])) + 'M vs ' + str('{:,}'.format(overview2['ossz_gp'])) + 'M\n' +
            'Avg Arena Rank  ::  ' + ' ' * (lth - len(str(overview1['squad_avg']))) + str('{:,}'.format(overview1['squad_avg'])) + ' vs ' + str('{:,}'.format(overview2['squad_avg'])) + '\n' +
            'Avg Fleet Rank  ::  ' + ' ' * (lth - len(str(overview1['fleet_avg']))) + str('{:,}'.format(overview1['fleet_avg'])) + ' vs ' + str('{:,}'.format(overview2['fleet_avg'])) + '\n' +
            'G11             :: ' + ' ' * (lth - len(str(overview1['g11']))) + str('{:,}'.format(overview1['g11'])) + ' vs ' + str('{:,}'.format(overview2['g11'])) + '\n' +
            'G12             :: ' + ' ' * (lth - len(str(overview1['g12']))) + str('{:,}'.format(overview1['g12'])) + ' vs ' + str('{:,}'.format(overview2['g12'])) + '\n' +
            'G13             ::  ' + ' ' * (lth - len(str(overview1['g13']))) + str('{:,}'.format(overview1['g13'])) + ' vs ' + str('{:,}'.format(overview2['g13'])) + '\n' +
            'Zetas           :: ' + ' ' * (lth - len(str(overview1['zetas']))) + str('{:,}'.format(overview1['zetas'])) + ' vs ' + str('{:,}'.format(overview2['zetas'])) + '\n' +
            '6 Dot mods      :: ' + ' ' * (lth - len(str(overview1['6dot']))) + str('{:,}'.format(overview1['6dot'])) + ' vs ' + str('{:,}'.format(overview2['6dot'])) + '\n' +
            '10+ speed mods  :: ' + ' ' * (lth - len(str(overview1['10speed']))) + str('{:,}'.format(overview1['10speed'])) + ' vs ' + str('{:,}'.format(overview2['10speed'])) + '\n' +
            '15+ speed mods  :: ' + ' ' * (lth - len(str(overview1['15speed']))) + str('{:,}'.format(overview1['15speed'])) + ' vs ' + str('{:,}'.format(overview2['15speed'])) + '\n' +
            '20+ speed mods  ::  ' + ' ' * (lth - len(str(overview1['20speed']))) + str('{:,}'.format(overview1['20speed'])) + ' vs ' + str('{:,}'.format(overview2['20speed'])) + '\n' +
            '25+ speed mods  ::  ' + ' ' * (lth - len(str(overview1['25speed']))) + str('{:,}'.format(overview1['25speed'])) + ' vs ' + str('{:,}'.format(overview2['25speed'])) + '\n' +
            '100+ off mods   :: ' + ' ' * (lth - len(str(overview1['100off']))) + str('{:,}'.format(overview1['100off'])) + ' vs ' + str('{:,}'.format(overview2['100off'])) + '```')
 
            i = 0
            j: int = 30
 
            for a in character_list:
 
                lth = round((j - len(character_list2[i])) / 2)
                if lth <= 8:
                    lth += 2
 
                guild1 = self.character_data_search(guilddata1, character_list[i])
                guild2 = self.character_data_search(guilddata2, character_list[i])
 
                embed.add_field(name='=' * (lth - 2) + ' ' + character_list2[i] + ' ' + '=' * (lth - 2), value=
                '```#    :: ' + ' ' * round(1 / len(str(guild1['osszes']))) + str(guild1['osszes']) + ' vs ' + str(guild2['osszes']) + '\n' +
                '5*   :: ' + ' ' * round(1 / len(str(guild1['otcsillag']))) + str(guild1['otcsillag']) + ' vs ' + str(guild2['otcsillag']) + '\n' +
                '6*   :: ' + ' ' * round(1 / len(str(guild1['hatcsillag']))) + str(guild1['hatcsillag']) + ' vs ' + str(guild2['hatcsillag']) + '\n' +
                '7*   :: ' + ' ' * round(1 / len(str(guild1['hetcsillag']))) + str(guild1['hetcsillag']) + ' vs ' + str(guild2['hetcsillag']) + '\n' +
                'g11  :: ' + ' ' * round(1 / len(str(guild1['g11']))) + str(guild1['g11']) + ' vs ' + str(guild2['g11']) + '\n' +
                'g12  :: ' + ' ' * round(1 / len(str(guild1['g12']))) + str(guild1['g12']) + ' vs ' + str(guild2['g12']) + '\n' +
                'g13  :: ' + ' ' * round(1 / len(str(guild1['g13']))) + str(guild1['g13']) + ' vs ' + str(guild2['g13']) + '\n' +
                'z    :: ' + ' ' * round(1 / len(str(guild1['egyzeta']))) + str(guild1['egyzeta']) + ' vs ' + str(guild2['egyzeta']) + '\n' +
                'zz   :: ' + ' ' * round(1 / len(str(guild1['ketzeta']))) + str(guild1['ketzeta']) + ' vs ' + str(guild2['ketzeta']) + '\n' +
                'zzz  :: ' + ' ' * round(1 / len(str(guild1['haromzeta']))) + str(guild1['haromzeta']) + ' vs ' + str(guild2['haromzeta']) + '```')
                i += 1
 
            i = 0
            j: int = 30
 
            for a in ship_list:
 
                lth = round((j - len(ship_list2[i])) / 2)
                if lth <= 8:
                    lth += 2
 
                guild1 = self.ship_data_search(guilddata1, ship_list[i])
                guild2 = self.ship_data_search(guilddata2, ship_list[i])
 
                embed.add_field(name='=' * (lth - 2) + ' ' + ship_list2[i] + ' ' + '=' * (lth - 2), value=
                '```#    :: ' + ' ' * round(1 / len(str(guild1['osszes']))) + str(guild1['osszes']) + ' vs ' + str(guild2['osszes']) + '\n' +
                '5*   :: ' + ' ' * round(1 / len(str(guild1['otcsillag']))) + str(guild1['otcsillag']) + ' vs ' + str(guild2['otcsillag']) + '\n' +
                '6*   :: ' + ' ' * round(1 / len(str(guild1['hatcsillag']))) + str(guild1['hatcsillag']) + ' vs ' + str(guild2['hatcsillag']) + '\n' +
                '7*   :: ' + ' ' * round(1 / len(str(guild1['hetcsillag']))) + str(guild1['hetcsillag']) + ' vs ' + str(guild2['hetcsillag']) + '\n' + '```')
                i += 1

            await ctx.send(":metal: :metal: :metal: Yohooooo... Itt vannak az adatok  :metal: :metal: :metal: ")
            await ctx.send(embed=embed)
 
            elapsedTime = toc()
            #await ctx.send("Elapsed time: %f seconds.\n" %elapsedTime)
 
        else:
            pass
 
    @tw.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')
        else:
            await self.ctx.send('⛔ - Szar van a palacsintában, próbáld újra \n')
 
 
    async def fetchGuildRoster(self, raw_guild):
        guilddata = []
        chardata_ally = []
        chardata_ally2 = []
        i: int = 0
        lth = int_(len(raw_guild[0]['roster']))
        lthp2 = int_(round(lth/2, 0))
        while i < lthp2:
            chardata_ally.insert(i, raw_guild[0]['roster'][i]['allyCode'])
            i += 1
    
        gd1 = self.bot.loop.create_task(client.fetchPlayers(chardata_ally))
    
        while i < lth:
            chardata_ally2.insert(i, raw_guild[0]['roster'][i]['allyCode'])
            i += 1
    
        gd2 = self.bot.loop.create_task(client.fetchPlayers(chardata_ally2))

        await gd1
        await gd2
        
        guilddata = gd1._result + gd2._result
    
        return guilddata
 
 
    def overview(self, GuildpPlayersData, GuilDdata):
        guild_ow = {
            "tagok_szama": 0,
            "ossz_gp": 0.0,
            "squad_avg": 0.0,
            "fleet_avg": 0.0,
            "g11": 0,
            "g12": 0,
            "g13": 0,
            "zetas": 0,
            "6dot": 0,
            "10speed": 0,
            "15speed": 0,
            "20speed": 0,
            "25speed": 0,
            "100off": 0
        }
    
        s_avg = 0
        f_avg = 0
    
        guild_ow['tagok_szama'] = GuildpPlayersData[0]['members']
        guild_ow['ossz_gp'] = round(GuildpPlayersData[0]['gp'] / 1000000, 1)
    
        i = 0
        for a in GuilDdata:
            chardata = GuilDdata[i]['roster']
            s_avg += GuilDdata[i]['arena']['char']['rank']
            f_avg += GuilDdata[i]['arena']['ship']['rank']
            j = 0
            for b in chardata:
                if chardata[j]['gear'] == 11:
                    guild_ow["g11"] += 1
                if chardata[j]['gear'] == 12:
                    guild_ow["g12"] += 1
                if chardata[j]['gear'] == 13:
                    guild_ow["g13"] += 1
                for c in chardata[j]['skills']:
                    if c['tier'] == 8 and c['isZeta'] == True:
                        guild_ow['zetas'] += 1
                for d in chardata[j]['mods']:
                    if d['pips'] == 6:
                        guild_ow['6dot'] += 1
                    for e in d['secondaryStat']:
                        if e['unitStat'] == "UNITSTATSPEED" and e['value'] >= 10:
                            guild_ow['10speed'] += 1
                        if e['unitStat'] == "UNITSTATSPEED" and e['value'] >= 15:
                            guild_ow['15speed'] += 1
                        if e['unitStat'] == "UNITSTATSPEED" and e['value'] >= 20:
                            guild_ow['20speed'] += 1
                        if e['unitStat'] == "UNITSTATSPEED" and e['value'] >= 25:
                            guild_ow['25speed'] += 1
                        if e['unitStat'] == "UNITSTATOFFENSE" and e['value'] >= 100:
                            guild_ow['100off'] += 1
                j += 1
            i += 1
    
        guild_ow['squad_avg'] = round(s_avg / guild_ow['tagok_szama'], 1)
        guild_ow['fleet_avg'] = round(f_avg / guild_ow['tagok_szama'], 1)
    
        return guild_ow
    
    
    def character_data_search(self, guilddata, charname):
        character = {"osszes": 0,
                    "otcsillag": 0,
                    "hatcsillag": 0,
                    "hetcsillag": 0,
                    "g11": 0,
                    "g12": 0,
                    "g13": 0,
                    "egyzeta": 0,
                    "ketzeta": 0,
                    "haromzeta": 0,
                    "karakternev": charname
                    }
    
        i = 0
        for a in guilddata:
            chardata = guilddata[i]['roster']
            j = 0
            for b in chardata:
                if chardata[j]['defId'] == charname:
                    character["osszes"] += 1
                    if chardata[j]['rarity'] == 5:
                        character["otcsillag"] += 1
                    if chardata[j]['rarity'] == 6:
                        character["hatcsillag"] += 1
                    if chardata[j]['rarity'] == 7:
                        character["hetcsillag"] += 1
                    if chardata[j]['gear'] == 11:
                        character["g11"] += 1
                    if chardata[j]['gear'] == 12:
                        character["g12"] += 1
                    if chardata[j]['gear'] == 13:
                        character["g13"] += 1
                    sumz = 0
                    for c in chardata[j]['skills']:
                        if c['tier'] == 8 and c['isZeta'] == True:
                            sumz += 1
                    if sumz == 1:
                        character["egyzeta"] += 1
                    if sumz == 2:
                        character["ketzeta"] += 1
                    if sumz == 3:
                        character["haromzeta"] += 1
                j += 1
            i += 1
    
        return character
    
    def ship_data_search(self, guilddata, shipname):
        ship = {"osszes": 0,
                "otcsillag": 0,
                "hatcsillag": 0,
                "hetcsillag": 0,
                "karakternev": shipname
                }
    
        i = 0
        for a in guilddata:
            shipdata = guilddata[i]['roster']
            j = 0
            for b in shipdata:
                if shipdata[j]['defId'] == shipname:
                    ship["osszes"] += 1
                    if shipdata[j]['rarity'] == 5:
                        ship["otcsillag"] += 1
                    if shipdata[j]['rarity'] == 6:
                        ship["hatcsillag"] += 1
                    if shipdata[j]['rarity'] == 7:
                        ship["hetcsillag"] += 1
                j += 1
            i += 1
    
        return ship
 
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
        #print( "Elapsed time: %f seconds.\n" %tempTimeInterval )
        return tempTimeInterval
 
def tic():
    # Records a time in TicToc, marks the beginning of a time interval
    toc(False)
 
 
def setup(bot):
    bot.add_cog(TW(bot))