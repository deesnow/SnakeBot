from discord.ext import commands
from handlers import mdb_handler as mdb
from botSettings import settings
import logging
from botSettings.settings import ROLES



# Discord Bot cog

class Management(commands.Cog, name='Team Management'):
    def __init__(self, bot):
        self.bot = bot
        self.mdb = mdb.mDbhandler()
        self.logger = logging.getLogger(__name__)
        self.logger.info('Init cmdManagement COG')

# ---------------------------------------------
# SEARCH character
# ---------------------------------------------

    @commands.command(aliases= ['searchchar', 'sc'])
    @commands.has_any_role(*ROLES)  # User need this role to run command
    async def search_char(self, ctx, char):
        self.char = char
        

        await ctx.message.add_reaction("🐍")
        if settings.DB_SERVER_CONNECTION:
            self.result = self.bot.loop.create_task(self.mdb.find_char(self.char))
            await self.result
            count = 1
            if len(self.result._result) ==0:
                await ctx.send(f'Did not find any character for {self.char}')
            else:
                for char in self.result._result:
                    char_id = char['base_id']
                    if 'alias' in char:
                        alias_list = char['alias']
                        await ctx.send(f'{count}.  {char_id}\n aliases: {alias_list}')
                        
                    else:
                        await ctx.send(f'{count}.  {char_id}')
                    count += 1

        else:
            await ctx.send('Database connection is DOWN!')

    @search_char.error
    async def search_char_error(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!", error)
            await self.ctx.send('⛔ - NINCS MEGFELELŐ JOGOSULTSÁGOD!!!')


# ---------------------------------------------
# Add character alias
# ---------------------------------------------
    @commands.command(aliases= ['aa'])
    @commands.has_any_role(*ROLES)  # User need this role to run command
    async def add_alias(self, ctx, id, new_alias):
        self.id = id
        self.new_alias = new_alias
        await ctx.message.add_reaction("🐍")

        if settings.DB_SERVER_CONNECTION:
            self.alias = self.bot.loop.create_task(self.mdb.get_alias(self.id))
            await self.alias
            self.alias = self.alias._result
            if self.new_alias not in self.alias:
                self.alias.append(self.new_alias)
                self.set_alias =  self.bot.loop.create_task(self.mdb.set_alias(self.id, self.alias))
                await self.set_alias
                if self.set_alias._result:
                    await ctx.send(f'{id} aliases: \n{self.alias}')
            else:
                await ctx.send(f'{self.new_alias} alias already in')

        else:
            await ctx.send('Database connection is DOWN!')

    @add_alias.error
    async def add_alias_error(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!", error)
            await self.ctx.send('⛔ - NINCS MEGFELELŐ JOGOSULTSÁGOD!!!')

# ---------------------------------------------
# Delete character alias
# ---------------------------------------------
    @commands.command(aliases= ['pop', 'pa'])
    @commands.has_any_role(*ROLES)  # User need this role to run command
    async def pop_alias(self, ctx, id, new_alias):
        self.id = id
        self.new_alias = new_alias
        await ctx.message.add_reaction("🐍")

        if settings.DB_SERVER_CONNECTION:
            self.alias = self.bot.loop.create_task(self.mdb.get_alias(self.id))
            await self.alias
            self.alias = self.alias._result
            if self.new_alias in self.alias:
                self.alias.remove(self.new_alias)
                self.set_alias =  self.bot.loop.create_task(self.mdb.set_alias(self.id, self.alias))
                await self.set_alias
                if self.set_alias._result:
                    await ctx.send(f'{id} aliases: \n{self.alias}')
            else:
                await ctx.send(f'{self.new_alias} alias Not found')

        else:
            await ctx.send('Database connection is DOWN!')

    @pop_alias.error
    async def pop_alias_error(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!", error)
            await self.ctx.send('⛔ - NINCS MEGFELELŐ JOGOSULTSÁGOD!!!')


# ---------------------------------------------
# Add Team
# ---------------------------------------------
    @commands.command(aliases= ['addteam', 'at'])
    @commands.has_any_role(*ROLES)  # User need this role to run command
    async def add_team(self, ctx, team_name, ch1=None, ch2=None, ch3=None, ch4=None, ch5=None):
        await ctx.message.add_reaction("🐍")
        self.team_members = [ch1, ch2, ch3, ch4, ch5]
        self.team_members_name = []
        self.team_members_failed = []
        self.team_ids = []
        self.all_ok = True
        self.server_id = ctx.message.guild.id


        if settings.DB_SERVER_CONNECTION:
            for ch in self.team_members:
                self.check_ch = await self.bot.loop.create_task(self.mdb.valid_char(ch))
                if self.check_ch != None:
                    self.team_ids.append(self.check_ch)
                else:
                    self.team_members_failed.append(ch)
                    self.all_ok = False
            
            if self.all_ok:
                self.team = self.bot.loop.create_task(self.mdb.add_team(team_name, self.team_members, self.team_ids, self.server_id))
                await self.team
                self.team = self.team._result
                await ctx.send(f'__**Team {team_name} created**__\n```md\n [{team_name}]  <{ch1}, {ch2}, {ch3}, {ch4}, {ch5}>\n ```')
            else:
                await ctx.send(f'Team cannot be created. The following alias(es) not assinged:\n{self.team_members_failed}')
            
            

        else:
            await ctx.send('Database connection is DOWN!')

    @add_team.error
    async def add_team_error(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!", error)
            await self.ctx.send('⛔ - NINCS MEGFELELŐ JOGOSULTSÁGOD!!!')

# ---------------------------------------------
# SEARCH Team
# ---------------------------------------------

    @commands.command(aliases= ['searchteam', 'st'])
    @commands.has_any_role(*ROLES)  # User need this role to run command
    async def search_team(self, ctx, team):
        self.team = team
        self.server_id = ctx.message.guild.id
        

        await ctx.message.add_reaction("🐍")
        if settings.DB_SERVER_CONNECTION:
            self.result = self.bot.loop.create_task(self.mdb.search_team(self.team, self.server_id))
            await self.result
            self.count = 1
            if len(self.result._result) == 0:
                await ctx.send(f'Did not find any team for {self.team}')
            else:    
                for team in self.result._result:
                    self.team_name = team['TeamName']
                    self.team_members = team['Ids']
                    if len(self.team_members)== 5:
                        ch1 = self.team_members[0][1]
                        ch2 = self.team_members[1][1]
                        ch3 = self.team_members[2][1]
                        ch4 = self.team_members[3][1]
                        ch5 = self.team_members[4][1]
                        await ctx.send(f'__**Team {self.count}:**__\n```asciidoc\n[{self.team_name}]\n= {ch1} =\n- {ch2}\n- {ch3}\n- {ch4}\n- {ch5}\n```')
                        self.count += 1
                    else:
                        await ctx.send(f'__**{self.team_name}**__ is not Complete!')
                
        else:
            await ctx.send('Database connection is DOWN!')

    @search_team.error
    async def search_team_error(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!", error)
            await self.ctx.send('⛔ - NINCS MEGFELELŐ JOGOSULTSÁGOD!!!')

# ---------------------------------------------
# LIST Team
# ---------------------------------------------

    @commands.command(aliases= ['listteam', 'lt'])
    @commands.has_any_role(*ROLES)  # User need this role to run command
    async def list_team(self, ctx):
        
        self.server_id = ctx.message.guild.id
        

        await ctx.message.add_reaction("🐍")
        if settings.DB_SERVER_CONNECTION:
            self.result = self.bot.loop.create_task(self.mdb.list_team(self.server_id))
            await self.result
            self.count = 1

            if len(self.result._result) == 0:
                await ctx.send(f'Did not find any team.')
            else:
                self.msg = '__**Team List:**__\n```md\n'    
                for team in self.result._result:
                    self.team_name = team['TeamName']
                    self.team_members = team['Members']
                    
                    if len(self.team_members)== 5:
                        ch1 = self.team_members[0]
                        ch2 = self.team_members[1]
                        ch3 = self.team_members[2]
                        ch4 = self.team_members[3]
                        ch5 = self.team_members[4]

                        self.msg += f'{self.count}. [{self.team_name}]  <{ch1}, {ch2}, {ch3}, {ch4}, {ch5}>\n'
                        self.count += 1
                    else:
                        self.msg += f'__**{self.count}. {self.team_name}**__ is not Complete!\n'
                    
                self.msg += '```'
                await ctx.send(self.msg)
                
        else:
            await ctx.send('Database connection is DOWN!')

    @list_team.error
    async def list_team_error(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!", error)
            await self.ctx.send('⛔ - NINCS MEGFELELŐ JOGOSULTSÁGOD!!!')

# ---------------------------------------------
# DELETE Team
# ---------------------------------------------

    @commands.command(aliases= ['deleteteam', 'dt'])
    @commands.has_any_role(*ROLES)  # User need this role to run command
    async def delete_team(self, ctx, team):
        self.team = team
        self.server_id = ctx.message.guild.id

        await ctx.message.add_reaction("🐍")
        if settings.DB_SERVER_CONNECTION:
            self.result = self.bot.loop.create_task(self.mdb.delete_team(self.team, self.server_id))
            await self.result
            
            
            if self.result._result.acknowledged and self.result._result.deleted_count ==1:
                await ctx.send(f'Team: __**{self.team}**__ deleted.')
            # elif self.result._result['acknowledged'] and self.result._result['delete_count' ==0] :
            #     await ctx.send(f'__**{self.result} - WRONG Team**__')
            
            else:
                await ctx.send(f'{self.team} - WRONG Team')
                
        else:
            await ctx.send('Database connection is DOWN!')

    @delete_team.error
    async def delete_team_error(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!", error)
            await self.ctx.send('⛔ - NINCS MEGFELELŐ JOGOSULTSÁGOD!!!')




# ---------------------------------------------

# ---------------------------------------------
def setup(bot):
    bot.add_cog(Management(bot))