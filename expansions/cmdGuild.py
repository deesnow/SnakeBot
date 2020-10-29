import discord
from discord.ext import commands
import logging

from handlers import db_handler as mongo
from handlers import rosterdf
from handlers import embed_generator as eg
from handlers import guild_handler as gh
from botSettings.settings import ROLES


class Guild(commands.Cog, name='Guild Parancsok'):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.info('Init cmdGuild COG')
        self.eg = eg.EmbedGen(self.bot)
        self.db = mongo.Dbhandler()
        self.gh = gh.GuildHandles(self.bot)

#--------------------------------------------------------
#--------------------------------------------------------

    @commands.command(aliases=['gs'],pass_context=True, name='GuildSave')
    @commands.has_any_role(*ROLES)  # User need this role to run command 
    
    async def guildsave(self, ctx, save_name):
        await ctx.message.add_reaction("🐍")

        self.ctx = ctx
        self.save_name = save_name
        self.user_id = self.ctx.author.id

        self.allycode = self.db.get_allycode(self.user_id)

        if type(self.allycode) == int:
            await self.ctx.message.add_reaction("⏳")

            #Get all allycodes for all guild member.
            self.msg1 = await self.ctx.send('Guild adatok lekérdezése folyamatban 🔎')
            self.guild_member_codes = await self.gh.fetch_guild(self.allycode)

            if type(self.guild_member_codes) == list:
                await self.ctx.send('✅ - Guild adatok letöltve, játékosok roosterének lekérdezése folyamatban 🔎')
                self.players_data = await self.gh.fetch_players(self.guild_member_codes)
                await self.ctx.send('✅ - Játékos adatok letöltve, mentések indítása ⏳')
                # SAVE PLAYERS DATA
                self.player_save = self.gh.guild_save(self.players_data, self.save_name)
                if  'Error' in  self.player_save:
                    self.error = self.player_save
                else:
                    if 'Finished' in self.player_save:
                        await self.ctx.send('✅ - Játékos adatok mentése befejezve')
                        if len(self.player_save['Not_Registered']) > 0:
                            self.msg = self.eg.nonreg_embed(self.player_save['Not_Registered'])
                            await self.ctx.send(embed=self.msg)

        
        if 'Error' in self.allycode:
            self.error = self.allycode

        
        if 'Error' in self.error:
            self.error_msg = self.error['Error']
            await ctx.send(f'`💥 - {self.error_msg}`')

        else:
            if self.allycode == "Failed":
                self.logger.error ('Get db.get_allycode -  FAILED')
                await self.ctx.send('Regisztrálva vagy? Nem található ally_code hozzád. Regisztrálj így - snk reg <discord_user> <ally-code>')

    
    @guildsave.error
    async def guildsave_error(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!", error)
            await self.ctx.send('⛔ - NINCS MEGFELELŐ JOGOSULTSÁGOD!!!')
        if isinstance(error, commands.MissingRequiredArgument):
            self.logger.info(f'Guildsave ERROR - {error}')
            print(f'Guildsave ERROR - {error}')
            await self.ctx.send('⛔ - HIÁNYZÓ PARAMÉTER! - Helyes parancs: `snk gs <mentés_neve>`')


#--------------------------------------------------------

    @commands.command(aliases=['gd'],pass_context=True, name='GuildTörlés')
    @commands.has_any_role(*ROLES)  # User need this role to run command 
    
    async def guilddel(self, ctx, save_name):
        await ctx.message.add_reaction("🐍")

        self.ctx = ctx
        self.save_name = save_name
        self.user_id = self.ctx.author.id

        self.allycode = self.db.get_allycode(self.user_id)

        if type(self.allycode) == int:
            await self.ctx.message.add_reaction("⏳")

            #Get all allycodes for all guild member.
            self.msg1 = await self.ctx.send('Guild adatok lekérdezése folyamatban 🔎')
            self.guild_member_codes = await self.gh.fetch_guild(self.allycode)

            if type(self.guild_member_codes) == list:
                await self.ctx.send('✅ - Guild adatok letöltve, játékosok mentésének törlése folyamatban ⏳')
                self.guild_delete = self.gh.guild_del(self.guild_member_codes, self.save_name)
                self.finished = len(self.guild_delete['Finished'])
                await self.ctx.send(f'✅ {self.finished} metés sikeresen törölve.')
                if len(self.guild_delete['Failed']) != 0:
                    self.msg_failed = 'A következő törlések nem sikerültek:\n```xml \n'
                    for self.failed in self.guild_delete['Failed']:
                        self.failed_ac = self.failed['allyCode']
                        self.failed_name = self.failed['name']
                        self.msg_failed += f'<{self.failed_ac}> - - - {self.failed_name} \n'

                    self.msg_failed += '```'
                    self.ctx.send(self.msg_failed)
        else:
            if self.allycode == "Failed":
                self.logger.error ('Get db.get_allycode -  FAILED')
                await self.ctx.send('Regisztrálva vagy? Nem található ally_code hozzád. Regisztrálj így - snk reg <discord_user> <ally-code>')
            elif type(self.allycode) == dict and 'Error' in self.allycode:
                    self.error = self.allycode

        
        if 'Error' in self.error:
            self.error_msg = self.error['Error']
            await ctx.send(f'`💥 - {self.error_msg}`')



    
    @guilddel.error
    async def guilddel_error(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!", error)
            await self.ctx.send('⛔ - NINCS MEGFELELŐ JOGOSULTSÁGOD!!!')
        if isinstance(error, commands.MissingRequiredArgument):
            self.logger.info(f'Guildsave ERROR - {error}')
            print(f'Guildsave ERROR - {error}')
            await self.ctx.send('⛔ - HIÁNYZÓ PARAMÉTER! - Helyes parancs: `snk gs <mentés_neve>`')





# --------------------------------
def setup(bot):
    bot.add_cog(Guild(bot))
