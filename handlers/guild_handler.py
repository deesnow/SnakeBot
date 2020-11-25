import asyncio
import json
import logging
import pandas as pd
import datetime
import random
import shortuuid
from handlers.async_swgoh_help import async_swgoh_help, settings
from botSettings import settings as mysettings
from handlers import db_handler as mongo
from handlers import cache
from handlers import rosterdf

class GuildHandles(object):
    '''Handlers functions for Guild save and Guild report commands'''

    def __init__(self, bot ,logger=None):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.db = mongo.Dbhandler()
        self.cache = cache.MyCacheLayer(self.bot)
        self.rosterdf = rosterdf
        self.cred = settings(mysettings.HELPAPI_USER, mysettings.HELPAPI_PASS)
        self.swgoh_client = async_swgoh_help(self.cred)

    async def fetch_guild(self, allycode):
        self.allycode = allycode
        raw_guild_data = self.bot.loop.create_task(self.swgoh_client.fetchGuilds(self.allycode))
        await raw_guild_data

        self.guild_member_codes = []
        for self.player in  raw_guild_data._result[0]['roster']:
            self.guild_member_codes.append(self.player['allyCode'])
        if type(self.guild_member_codes) == list:
            return self.guild_member_codes
        else:
            return {'Error': 'Hiba a Guild adatok letöltésében'}

    async def fetch_players(self, allycodes):
        '''fetch players roster data from cache layer. If not cached,
         or too old, than cachle layer will fetch if from API'''

        self.allycodes = allycodes
        self.players_data = await self.cache.get_allycode(self.allycodes, prio=1)

        return self.players_data

    def guild_save(self, data, save_name):
        self.players_SAVEdata = data
        self.save_name = save_name
        self.not_registered = []

        for player in self.players_SAVEdata:
            self.player_discordID = self.db.get_discordid(player['allyCode'])
            if self.player_discordID == 'Failed':
                player_name = player['name']
                self.not_registered.append({'name':player_name, 'allycode': player['allyCode']})
                self.fake_reg(player_name, player['allyCode'])
                

                
            elif type(self.player_discordID) == dict:
                return self.player_discordID # ERROR REtun
                break



            self.player_save = self.db.save_roster(self.player_discordID, self.save_name, player)
        
        return {'Finished': True,
                'Not_Registered' : self.not_registered}
            

    def fake_reg(self, reg_user, ally_code):
        self.fakereg = True
        while self.fakereg:
            self.player_discordID = 'xx' + shortuuid.ShortUUID().random(length=16)
            self.check_discordID = self.db.check_discordid(self.player_discordID)
            user_data = {'discord_id':self.player_discordID,
                                    'user_id':reg_user,
                                    'ally_code': ally_code }
                                
            if self.check_discordID == False:
                self.fakereg = False
                self.db.user_add(user_data)
                self.logger.info(f'Fake_Reg done for {reg_user}')

# ------------------------------------------------------------------------------------

    def guild_del(self, data, save_name):
        self.players_SAVEdata = data
        self.save_name = save_name
        self.failed_list = []
        self.done_list = []

        for self.player in self.players_SAVEdata:
            self.save_delete = self.db.delete_save_by_allycode(self.player, self.save_name)
            if self.save_delete == 'Failed':
                self.name = self.db.get_name(self.player)
                self.failed_list.append({'allyCode': self.player, 'name': self.name})
            if self.save_delete == 'Done':
                self.done_list.append(self.player)

        return {'Finished':self.done_list,
                'Failed': self.failed_list }
