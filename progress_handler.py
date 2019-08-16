import matplotlib.pyplot as plt
import pandas as pd
from pandas.io.json import json_normalize
from pandas.tseries import converter
converter.register()
from dateutil.parser import parse
import shortuuid
import os.path
import logging

class Progresshandler(object):
    '''Stats function for the Snakebot. Contains pandas actions and plot generation.'''
    # pylint: disable=too-many-instance-attributes
    # Eight is reasonable in this case

    def __init__(self, logger=None):
        self.logger = logging.getLogger(__name__)
        
    
    def gen_df1 (self, progress_data):
        self.progress_data = progress_data
        self.data_list = []
        try:
            del self.df
        except:
            pass
        try:
            del self.df1
        except:
            pass
        try:
            del self.df3
        except:
            pass    

        for item in self.progress_data:
            self.data_list.append(self.progress_data[item])
        #genarate pandas dataframes
        self.df = json_normalize(self.data_list)
        self.df1 = self.df[[ 'arena_rank', 'pvp_battles_won', 'galactic_power', 'character_galactic_power', 'ship_galactic_power' ]]
        self.df1['fleet_rank'] = self.df['fleet_arena.rank']
        self.df1['date'] = self.df['last_updated'].astype('datetime64[ns]')
        self.df1['week'] = self.df1['date'].dt.week
        self.df1['short_date'] = self.df1['date'].dt.date
        self.df1.set_index('short_date', inplace=True)
        
        return self.df1

    def gen_df3(self, raw_df):
        self.raw_df = raw_df

        self.df2 = self.raw_df.drop_duplicates(subset='week', keep='last')
        self.df3 = self.df2.set_index('week')
        self.df3['gp_delta'] = self.df3['galactic_power'].shift(-1) - self.df3['galactic_power']
        self.df3['avggp_per_day'] = self.df3['gp_delta'] / 7 
        return self.df3

    def gen_plot(self, df1, df3, filename):


        self.fig = plt.figure(figsize=(8,7))
        self.fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.4, hspace=0.4)
        self.fig.suptitle('User Progresses', fontsize=16)
        ax1 = self.fig.add_subplot(221)
        ax1.set_xlabel('Week')
        ax1.set_ylabel('GP (k)')
        ax1.set_title('GP Progress')
        ax1.plot(df3.galactic_power/1000, color='orange')
        ax2 = self.fig.add_subplot(222)
        ax2.set_xlabel('Week')
        ax2.set_ylabel('Avg GP')
        ax2.set_title('Avg GP / day')
        ax2.bar(df3.index ,df3.avggp_per_day, color='blue')
        ax3 = self.fig.add_subplot(223)
        ax3.set_xlabel('Date')
        ax3.set_ylabel('Rank')
        ax3.set_title('Arena Rank')
        ax3.set_ylim((max(df1.arena_rank) + max(df1.arena_rank) * 0.2 ), (min(df1.arena_rank) - min(df1.arena_rank)*0.1 ))
        ax3.plot(df1.arena_rank, color="green")
        for tick in ax3.get_xticklabels():
            tick.set_rotation(90)
        ax4 = self.fig.add_subplot(224)
        ax4.set_xlabel('Date')
        ax4.set_ylabel('Rank')
        ax4.set_title('Fleet Rank')
        ax4.set_ylim(max(df1.fleet_rank) + max(df1.fleet_rank)* 0.1, (min(df1.fleet_rank) - 1))
        ax4.plot(df1.fleet_rank, color="red")
        for tick in ax4.get_xticklabels():
            tick.set_rotation(90)
        

        self.fig.savefig(filename, bbox_inches='tight')

    def get_stats(self, progress_json):
        self.progress_json = progress_json

        self.dframe1 = self.gen_df1(self.progress_json)
        self.dframe3 = self.gen_df3(self.dframe1)
        IMAGE_DIR = 'temp/'
        self.img_name = shortuuid.uuid()
        self.img_fullpath = IMAGE_DIR + self.img_name + '.png'
        self.gen_plot(self.dframe1, self.dframe3, self.img_fullpath)
        if os.path.isfile(self.img_fullpath):
            return self.img_fullpath
        else:
            return None










        

        

        
    

