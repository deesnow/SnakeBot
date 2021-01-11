import asyncio
import json
import logging
import pandas as pd
import datetime
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
                return self.generate_diff(self.filter)
            else:
                self.error = {'Error': 'NINCS ILYEN MENTÉS'}
                return self.error
                

    def check_if_gg(self, roster):
        #check type of save. True if the save is done from .gg
        self.roster = roster

        try:
            self.roster[0]['data']
            return True
        except KeyError:
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

            for self.units in self.new_roster[0]['roster']:
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

    def generate_diff(self, filter):

        self.filter = filter
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

        if self.filter is None:
            return self.diff_df.to_dict('index')
        else:
            self.diff_df2 = self.diff_df[self.diff_df.index.isin(filter)]
            return self.diff_df2.to_dict('index')








        

