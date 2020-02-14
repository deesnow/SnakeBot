import time
import discord
import logging
from discord.ext import commands
import db_handler as mongo
from async_swgoh_help import async_swgoh_help, settings
import settings as mysettings
import swgoh_handler

creds = settings(mysettings.HELPAPI_USER, mysettings.HELPAPI_PASS)
client = async_swgoh_help(creds)
db = mongo.Dbhandler()
sw = swgoh_handler.Swgoh()

class GuildSave(commands.Cog, name='Guild Commands'):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.info(f'Init {__name__} COG')

    @commands.command(aliases=['GuildSave'],pass_context=True, name='gs')
    @commands.has_any_role('Master', 'Grand Inquisitor', 'Officer')  # User need this role to run command (can have multiple)
    
    async def gs(self, ctx, allycode1: int, savename):
        await ctx.message.add_reaction("⏳")
        
        # Get ally allycode with client.fetchGuilds(allycode1)
        rg1 = self.bot.loop.create_task(client.fetchGuilds(allycode1))
        self.msg1 = await ctx.send('Guild adatok lekérdezése folyamatban 🔎')
        await rg1

        guildrawdata = rg1._result 

        await self.msg1.edit(content='✅ - Guild adatok letöltve, játékosok roosterének lekérdezése folyamatban 🔎')
        
        
        #Create a list of allycodes from result.
        allycodes = []
        
        lght = len(guildrawdata[0]['roster'])
        i = 0
        while i < lght:
            allycodes.append(guildrawdata[0]['roster'][i]['allyCode'])
            i += 1

              




        # save data for every guild member if registered, if not than add to non-reg list
        not_registered = ""
        datafetch_error = []
        
        self.msg2 = await ctx.send(f'Játékos adatok letöltése')

        counter = 1

        for allycode in allycodes:

            discord_ID, username  = db.get_discordID(allycode)

            if discord_ID != None:
                
                
                
                try:
                    players_data = sw.swgoh_getuser(allycode)
                    await self.msg2.edit(content=f'Data of {username} fetched')
                    self.logger.info(f'Data of {username} fetched for {allycode}')
                    if players_data != None:
                        try:
                            save_user = db.save_roster(discord_ID, savename, players_data)
                            await self.msg2.edit(content=f'✅ {counter}. - {username} - Roster adatok elmentve.')
                            self.logger.info(f'Data saved for {username}')
                        except Exception as error:
                            self.logger.error(f'Data save FAILED for {username}')
                    else:
                        datafetch_error.append(username)
                        self.logger.error(f'Data fetch error from swgoh.gg for {allycode} - {username}')


                except Exception as error:
                    pass

            else:
                not_registered += str(allycode) + '\n'
                self.logger.error(f'{allycode} is not registered')

            counter += 1
        
        self.logger.info(f'All allycode checked, prepare last embed')
        embed = discord.Embed(title='GuildSave Output')
        embed.add_field(name='=====Nem regisztrált Ally Kódok:=====', value=not_registered)

        await ctx.send(embed=embed)





            



    @gs.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')
        else:
            await self.ctx.send('⛔ - Szar van a palacsintában, próbáld újra \n')



    # async def checkuser_reg(allycode):
        
    #     try:
    #         self.check = sw.swgoh_getuser(allycode)
    #         return True

    





def setup(bot):
    bot.add_cog(GuildSave(bot))