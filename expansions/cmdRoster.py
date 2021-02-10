import discord
from discord.ext import commands
import logging

from handlers import db_handler as mongo
from handlers import mdb_handler as mdb
from handlers import cache
from handlers import rosterdf
from handlers import embed_generator as eg
from botSettings.settings import ROLES

db = mongo.Dbhandler()

class SaveRoster(commands.Cog, name='Roster Parancsok'):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.info('Init cmdRoster COG')
        self.cache = cache.MyCacheLayer(self.bot)
        self.eg = eg.EmbedGen(self.bot)
        self.mdb = mdb.mDbhandler()
        
#--------------------------------------------------------
#--------------------------------------------------------


    # SAVE mentioned user date to local DB
    @commands.command(aliases= ['sr', 'save'],pass_context = True, name='RosterMentés')
    @commands.has_any_role(*ROLES) # User need this role to run command (can have multiple)
    async def saveroster(self, ctx, user, save_name):
        self.ctx = ctx
        self.save_name = save_name
        await self.ctx.message.add_reaction("🐍")
        
        

        if user != "me":
            self.user_id = self.ctx.message.mentions[0].id
            
        else:
            self.user_id = self.ctx.author.id

        try:
            self.allycode = db.get_allycode(self.user_id)
            self.msg1 = await ctx.send(f'🔎 Allycode a játékoshoz azonosítva, adatok lekérdezése ... \nEz a folyamat az API terheltség függvényében akár 1-2 percet is igénybe vehet.')
            await ctx.message.add_reaction("⏳")

            try:
                self.newdata = await self.cache.get_allycode(self.allycode, prio=1)
                await ctx.message.add_reaction("☀")
                self.msg1 = await ctx.send(f'Játékos adatok letöltve. Mentés ...' )
                #await self.ctx.send('Userdata from swgoh.gg --> \n {}'.format(self.newdata['galactic_power']))
                try:
                    self.write_user = db.save_roster(self.user_id, self.save_name , self.newdata)
                except Exception as error:
                    print(error)
                if self.write_user == "Done":
                    await ctx.message.add_reaction("✅")
                    self.msg1 = await ctx.send(f'Játékos adatok mentve __***{self.save_name}***__ néven' )
                else:
                    await ctx.message.add_reaction("💥")
                    self.msg1 = await ctx.send(f'*** Játékos adatok mentése SIKERTELEN! ***' )
            except Exception as error:
                print(error)
                await ctx.send(f'*** Játékos adatok mentése SIKERTELEN! ***' )
                await ctx.send(f'A Cache kezelésben hiba keletkezett')
        except Exception as error:
            print(error)
            self.msg1 = await ctx.send(f'*** Nem található az AllyCode a játékoshoz. Ellenőrizd a regisztrációt! ***')


    @saveroster.error
    async def saveroster_error(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!", error)
            await self.ctx.send('⛔ - NINCS MEGFELELŐ JOGOSULTSÁGOD!!!')

    #---------------------------------------------------------------------------------------
    #Delete SAVE
    @commands.command(aliases= ['ds', 'del'],pass_context = True,  name='MentésTörlés')    
    @commands.has_any_role(*ROLES) # User need this role to run command (can have multiple)
    async def del_save(self, ctx, user, save):
        self.ctx = ctx
        self.save_name = save
        await self.ctx.message.add_reaction("🐍")
        
        

        if user != "me":
            self.discord_id = self.ctx.message.mentions[0].id
            
        else:
            self.discord_id = self.ctx.author.id

        try:
            self.ds = db.delete_save(self.discord_id, self.save_name)
            self.logger.info('Delete roster %s save for user %s is Done', self.save_name, self.discord_id, exc_info=True)
            if self.ds == "Done":
                await self.ctx.message.add_reaction("✅")
                await self.ctx.send(f'A __***{self.save_name}***__ mentés törölve.')
            else:
                await self.ctx.message.add_reaction("💥")
                await self.ctx.send('*** A {self.save_name} törlése SIKERTELEN! ***')
                await self.ctx.send('Ellenőrizd hogy az adott játékos rendelkezik-e ilyen nevű mentéssel!')

        except Exception as error:
            await self.ctx.message.add_reaction("💥")
            await self.ctx.send('*** A {self.save_name} törlése SIKERTELEN! ***')
            await self.ctx.send('Úgy tűnik valamilyen DB probléma léphetett fel. Szólj DeeSnow-nak')
            self.logger.error('Delete roster {} save for user {} is Failed '.format( self.save_name, self.discord_id, exc_info=True))
            self.logger.error('-------dump--------')
            self.logger.error(error)
            self.logger.error('-------dump--------')




    @del_save.error
    async def del_save_error(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!", error)
            await self.ctx.send('⛔ - NINCS MEGFELELŐ JOGOSULTSÁGOD!!!')
        

    #---------------------------------------------------------------------------------------
        
    
    #NOW COMMAND
    @commands.command(aliases= ['now', 'fejlodes'],pass_context = True, name='Fejlődés')    
    #@commands.has_any_role('Master') # User need this role to run command (can have multiple)
    async def getnow(self, ctx, user, save1, filter=None):
        self.ctx = ctx
        self.save1 = save1
        self.diff = rosterdf.RosterDf(self.bot)
        #self.save_name = 'xxnowxx'
        await self.ctx.message.add_reaction("🐍")

        self.filter = filter
        self.server_id = ctx.message.guild.id

        self.result = self.bot.loop.create_task(self.mdb.get_team(self.filter, self.server_id))
        await self.result
        self.team_dict = self.result._result
        self.team = []
        if self.team_dict is not None:
            for char in self.team_dict['Ids']:
                self.team.append(char[0])
        
        

        if user != "me":
            self.user_id = self.ctx.message.mentions[0].id
            
        else:
            self.user_id = self.ctx.author.id

        self.allycode = db.get_allycode(self.user_id)
        if self.allycode != "Failed":
            self.msg1 = await ctx.send(f'🔎 Allycode a játékoshoz azonosítva, adatok lekérdezése ... \nEz a folyamat az API terheltség függvényében akár 1-2 percet is igénybe vehet.')
            await ctx.message.add_reaction("⏳")

            #get diff dataframe
            if len(self.team) == 5:
                self.diff_df = await self.diff.save_now_compare(self.allycode, self.save1, self.team)
            else:
                self.diff_df = await self.diff.save_now_compare(self.allycode, self.save1)

            

            
            if "Error" not in self.diff_df:
                
                
                self.embed_msg_list = self.eg.embed_roster(self.diff_df)

                for self.msg in self.embed_msg_list:
                    await self.ctx.send(embed=self.msg)

            else:
                self.error_msg = self.diff_df['Error']
                await ctx.send(f'`💥 - {self.error_msg}`')


        else:
            if 'Error' in self.allycode:
                self.error_msg = self.allycode['Error']
                await ctx.send(f'`💥 - {self.error_msg}`')
            else:
                await self.ctx.send('Nem található allycode! A játékos regisztrálva van? Regisztráld így - snk reg <discord_user> <ally-code>')
        



    @getnow.error
    async def now_error(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!")
            await self.ctx.send('⛔ - You don\'t have the right permission!!!')
    


    #---------------------------------------------------------------------------------------

    # SAVE mentioned user date to local DB
    @commands.command(aliases= ['list', 'ls'],pass_context = True, name='MentésLista')
    #@commands.has_any_role('Master') # User need this role to run command (can have multiple)
    async def listsaves(self, ctx, user):
        self.ctx = ctx
        self.user = user
        await self.ctx.message.add_reaction("🐍")
        if user != "me":
            self.user_id = self.ctx.message.mentions[0].id
            
        else:
            self.user_id = self.ctx.author.id

        self.roster_saves = db.listsaves(self.user_id)

        

        if self.roster_saves == None:
            await self.ctx.send('`💥 - Úgy tűnik nincs még mentésed. Regisztrálva vagy?`')

        elif 'Error' in self.roster_saves.keys():
            self.error = self.roster_saves['Error']
            await self.ctx.send(f'`💥 - {self.error}`')

        
        else:

        
        
            self.embed = discord.Embed(
                title = 'Roster Mentések',
                description = f'Mentett állapotok listája: \n **<Mentés név>**\n <Mentés dátuma>',
                color = discord.Color.dark_blue()
                )

            self.embed.set_footer(text = 'Are these droids you are looking for?')
            self.embed.add_field(name='--------------------', value='--------------------' , inline=False)
            if self.roster_saves != None:
                for self.item, self.item_date in self.roster_saves.items():
                    self.embed.add_field(name=self.item , value=self.item_date , inline=False)
                
                await self.ctx.send(embed=self.embed)

        
            


    

# --------------------------------
def setup(bot):
    bot.add_cog(SaveRoster(bot))
