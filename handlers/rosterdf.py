import logging
import pandas as pd
from datetime import datetime
import shortuuid

#from pandas.io.json import json_normalize

from handlers.async_swgoh_help import async_swgoh_help, settings
from handlers import db_handler as mongo
from handlers import cache

class RosterDf(object):
    '''Compare saved roster data to have progression'''
    # pylint: disable=too-many-instance-attributes
    # Eight is reasonable in this case.

    def __init__(self, bot ,logger=None):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.db = mongo.Dbhandler()
        self.cache = cache.MyCacheLayer(self.bot)



    async def save_now_compare(self, allycode, save, filter=None):
        """Compare current roster with a save and calculate the differense"""
        self.allycode = allycode
        self.save = save
        self.filter = filter

        # self.df1 = pd.DataFrame(columns=['base_id', 'name', 'old_level', 'old_rarity', 'old_gear', 'old_relic', 'old_zeta',
        #                                       'new_level', 'new_rarity', 'new_gear', 'new_relic', 'new_zeta'])

        
        #read saved roster
        self.old_roster = self.db.get_roster(self.allycode, self.save)
        #get fresh roster via cache layer
        self.new_roster = await self.cache.get_allycode(self.allycode, prio=1)

        if 'Error' in self.old_roster:
            return self.old_roster
        
        else:
            if self.old_roster is not None:
                #fill df with new data
                self.append_help_new()

                
                #add old data to df
                if self.check_if_gg(self.old_roster):
                    self.update_df_gg(self.old_roster)
                else:
                    self.update_df_help(self.old_roster)

                
                #generate diff df
                self.generate_diff()
                return self.df_to_dict(self.filter)
            else:
                self.error = {'Error': 'NINCS ILYEN MENTÉS'}
                return self.error
                

    def check_if_gg(self, roster):
        #check type of save. True if the save is done from .gg
        self.roster = roster

        if 'data' in self.roster[0]:
            return True
        else:
            return False

    def append_gg(self):

        #self.logger.info(f'DF append STARTED')

        self.units_data_list = []

        for self.units in self.old_roster:
            
            self.name = self.units['data']['name']
            self.base_id = self.units['data']['base_id']
            self.old_level = self.units['data']['level']
            self.old_rarity = self.units['data']['rarity']
            if self.units['data']['combat_type'] == 1 :
                self.old_gear = self.units['data']['gear_level']
                if 'relic_tier' in self.units['data'] and self.units['data']['relic_tier'] > 2:
                    self.old_relic = self.units['data']['relic_tier'] - 2
                else:
                    self.old_relic = 0
                self.old_zeta = len(self.units['data']['zeta_abilities'])
            
                self.unit_data = {
                        'base_id': self.base_id,
                        'name': self.name,
                        'old_level': self.old_level,
                        'old_rarity': self.old_rarity,
                        'old_gear': self.old_gear,
                        'old_relic': self.old_relic,
                        'old_zeta': self.old_zeta}
            
            else:
                self.unit_data = {
                    'base_id': self.base_id,
                    'name': self.name,
                    'old_level': self.old_level,
                    'old_rarity': self.old_rarity,
                    }
            
            self.units_data_list.append(self.unit_data)


        self.df1 = pd.DataFrame(self.units_data_list)

        self.df1.set_index('base_id', inplace=True)

        #self.logger.info(f'DF append FINISHED')
        

    def append_help(self):
        self.units_data_list = []

        for self.units in self.old_roster:
            self.name = self.units['nameKey']
            self.base_id = self.units['defId']
            self.old_level = self.units['level']
            self.old_rarity = self.units['rarity']
            if self.units['combatType'] == "CHARACTER" :
                self.old_gear = self.units['gear']
                self.old_relic = self.units['relic']['currentTier'] - 1
                self.old_zeta = 0
                for skill in self.units['skills']:
                    if skill['tiers']==skill['tier'] and skill['isZeta']:
                        self.old_zeta += 1

                self.unit_data = {
                    'base_id': self.base_id,
                    'name': self.name,
                    'old_level': self.old_level,
                    'old_rarity': self.old_rarity,
                    'old_gear': self.old_gear,
                    'old_relic': self.old_relic,
                    'old_zeta': self.old_zeta}

            else:
                self.unit_data = {
                    'base_id': self.base_id,
                    'name': self.name,
                    'old_level': self.old_level,
                    'old_rarity': self.old_rarity}

            self.units_data_list.append(self.unit_data)
        
        self.df1 = pd.DataFrame(self.units_data_list)
        
        self.df1.set_index('base_id', inplace=True)
# -------------------------------------------------------------------------------------------        

    def append_help_new(self):
            self.units_data_list = []
            if type(self.new_roster) == list and len(self.new_roster) ==1:
                self.player_name = self.new_roster[0]['name']
                
                self.new_roster = self.new_roster[0]['roster']
            
            elif type(self.new_roster) == dict:
                self.player_name = self.new_roster['name'] 
                self.guild_name =  self.new_roster['guildName']
                self.new_roster = self.new_roster['roster']

            for self.units in self.new_roster:
                self.name = self.units['nameKey']
                self.base_id = self.units['defId']
                self.new_level = self.units['level']
                self.new_rarity = self.units['rarity']
                if self.units['combatType'] == "CHARACTER" :
                    self.new_gear = self.units['gear']
                    self.new_relic = max(0, self.units['relic']['currentTier'] -2)
                    self.new_zeta = 0
                    for skill in self.units['skills']:
                        if skill['tiers']==skill['tier'] and skill['isZeta']:
                            self.new_zeta += 1

                    self.unit_data = {
                        'base_id': self.base_id,
                        'name': self.name,
                        'new_level': self.new_level,
                        'new_rarity': self.new_rarity,
                        'new_gear': self.new_gear,
                        'new_relic': self.new_relic,
                        'new_zeta': self.new_zeta}

                else:
                    self.unit_data = {
                        'base_id': self.base_id,
                        'name': self.name,
                        'new_level': self.new_level,
                        'new_rarity': self.new_rarity}

                self.units_data_list.append(self.unit_data)
            
            self.df1 = pd.DataFrame(self.units_data_list)
            
            self.df1.set_index('base_id', inplace=True)


# -------------------------------------------------------------------------------------------
    def update_df_gg(self, roster):
    
        #self.logger.info(f'DF update by .loc STARTED')
        for self.units in roster:
            self.base_id = self.units['data']['base_id']
            self.old_level = self.units['data']['level']
            self.old_rarity = self.units['data']['rarity']

            self.df1.loc[self.base_id, 'old_level'] = self.old_level
            self.df1.loc[self.base_id, 'old_rarity'] = self.old_rarity


            if self.units['data']['combat_type'] == 1 :
                self.old_gear = self.units['data']['gear_level']
                self.old_relic = max(0, self.units['data']['relic_tier'] - 2)
                self.old_zeta = len(self.units['data']['zeta_abilities'])
                
                self.df1.loc[self.base_id, 'old_gear'] = self.old_gear
                self.df1.loc[self.base_id, 'old_relic'] = self.old_relic
                self.df1.loc[self.base_id, 'old_zeta'] = self.old_zeta

        #self.logger.info(f'DF update by .loc FINISHED')

# ------------------------------------------------------------------------------------------- 
    def update_df_help(self, roster):
    
        #self.logger.info(f'DF update by .loc STARTED')
        for self.units in roster:
            self.base_id = self.units['defId']
            self.old_level = self.units['level']
            self.old_rarity = self.units['rarity']

            self.df1.loc[self.base_id, 'old_level'] = self.old_level
            self.df1.loc[self.base_id, 'old_rarity'] = self.old_rarity


            if self.units['combatType'] == "CHARACTER" :
                self.old_gear = self.units['gear']
                self.old_relic = max(0, self.units['relic']['currentTier'] - 2)
                self.old_zeta = 0
                for skill in self.units['skills']:
                    if skill['tiers']==skill['tier'] and skill['isZeta']:
                        self.old_zeta += 1
                
                self.df1.loc[self.base_id, 'old_gear'] = self.old_gear
                self.df1.loc[self.base_id, 'old_relic'] = self.old_relic
                self.df1.loc[self.base_id, 'old_zeta'] = self.old_zeta

        #self.logger.info(f'DF update by .loc FINISHED')

# ------------------------------------------------------------------------------------------- 


    def update_df(self, roster):

        #self.logger.info(f'DF update by .loc STARTED')
        for self.units in roster[0]['roster']:
            self.base_id = self.units['defId']
            self.new_level = self.units['level']
            self.new_rarity = self.units['rarity']

            self.df1.loc[self.base_id, 'new_level'] = self.new_level
            self.df1.loc[self.base_id, 'new_rarity'] = self.new_rarity


            if self.units['combatType'] == "CHARACTER" :
                self.new_gear = self.units['gear']
                self.new_relic = 0
                if self.units['relic']['currentTier'] > 2:
                    self.new_relic = self.units['relic']['currentTier'] - 2
                self.new_zeta = 0
                for skill in self.units['skills']:
                    if skill['tiers']==skill['tier'] and skill['isZeta']:
                        self.new_zeta += 1
                
                self.df1.loc[self.base_id, 'new_gear'] = self.new_gear
                self.df1.loc[self.base_id, 'new_relic'] = self.new_relic
                self.df1.loc[self.base_id, 'new_zeta'] = self.new_zeta

        #self.logger.info(f'DF update by .loc FINISHED')

# ------------------------------------------------------------------------------------------- 
# Generate Diff
# ------------------------------------------------------------------------------------------- 

    def generate_diff(self):

        self.df1.fillna(0, inplace=True)
       
        
        self.df1['level_diff'] = self.df1['new_level'] - self.df1['old_level']
        self.df1['rarity_diff'] = self.df1['new_rarity'] - self.df1['old_rarity']
        self.df1['gear_diff'] = self.df1['new_gear'] - self.df1['old_gear']
        self.df1['relic_diff'] = self.df1['new_relic'] - self.df1['old_relic']
        self.df1['zeta_diff'] = self.df1['new_zeta'] - self.df1['old_zeta']

        self.level_cond = self.df1['level_diff'] > 0
        self.rarity_cond = self.df1['rarity_diff'] > 0
        self.gear_cond = self.df1['gear_diff'] > 0
        self.relic_cond = self.df1['relic_diff'] > 0
        self.zeta_cond = self.df1['zeta_diff'] > 0

        self.diff_df = self.df1[self.level_cond | self.rarity_cond | self.gear_cond |
                                 self.relic_cond | self.zeta_cond ]

        
        
    def df_to_dict(self, filter):

        self.filter = filter

        if self.filter is None:
            return self.diff_df.to_dict('index')
        else:
            self.diff_df2 = self.diff_df[self.diff_df.index.isin(filter)]
            return self.diff_df2.to_dict('index')





# ------------------------------------------------------------------------------------------- 
# Guild level DF for for Guild Progress report
# ------------------------------------------------------------------------------------------- 

    async def guild_report (self, players_data, save, filter=None):

        self.players_data = players_data
        self.save = save
        self.filter = filter
        self.guild_diff_df = pd.DataFrame()
        self.users_with_error = [] 
        
        

        for self.player in self.players_data:
            self.player_name = self.player['name']
            print (f'***Actual Player*** - ', self.player['name'])
            if hasattr(self, 'diff_df'):
                self.diff_df = self.diff_df[0:0]
                self.df1 = self.df1[0:0]

            self.old_roster = self.db.get_roster(self.player['allyCode'], self.save)
            
            if self.old_roster is None:
                ## Need to add something to DF and highlight the player have no save
                self.users_with_error.append(self.player['name'])
                self.logger.error (f'{self.player_name} has no {self.save} save')
                continue

            else:

                if 'Error' in self.old_roster:
                    self.users_with_error.append(self.player['name'])
                    self.logger.error (f'{self.player_name} has Error to get {self.save} save')
                    continue

                else:
                    
                    self.new_roster = self.player
                    self.append_help_new()
                    #add old data to df
                    if self.check_if_gg(self.old_roster):
                        self.update_df_gg(self.old_roster)
                    else:
                        self.update_df_help(self.old_roster)
                    
                    #generate diff df
                    self.generate_diff()

                    # add name to self.diff_df
                    self.diff_df = self.diff_df.assign(player = self.player_name)
                    self.guild_diff_df = self.guild_diff_df.append(self.diff_df)

            
            
        
        # Generate Excel spredsheet
        self.date = datetime.date(datetime.today())
        self.uid = shortuuid.ShortUUID().random(length=4)
        
        self.file_name = f'temp/GuildReport - {self.date} - {self.uid}.xlsx'

        with pd.ExcelWriter(self.file_name) as writer:
            self.guild_diff_df.to_excel(writer, sheet_name='report')
            self.error_df = pd.DataFrame(self.users_with_error)
            self.error_df.to_excel(writer, sheet_name='error')

        return self.file_name


            
# ------------------------------------------------------------------------------------------- 
# Generate Diff
# ------------------------------------------------------------------------------------------- 

    def gen_guild_diff(self):
        pass

        









        

