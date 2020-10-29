import discord
import logging



class EmbedGen(object):
    '''Generate different embed messages'''

    def __init__(self, bot ,logger=None):
        self.bot = bot
        self.logger = logging.getLogger(__name__)


    def embed_roster(self, diff_dict):
        
        self.diff = diff_dict
        self.embeds_list = []
        self.counter = 0
        self.page = 1
        self.new_embed = True
        # self.embed = discord.Embed(
        #     title = 'ROSTER FEJLŐDÉS - {self.page}. OLDAL',
        #     description = '📈A rostereden a következő fejleszések történtek',
        #     color = discord.Color.dark_blue()
        #     )

        # self.embed.set_footer(text = 'Are these droids you are looking for?')
        
        if len(self.diff.keys()) > 0:

            for self.character in self.diff:
                if self.new_embed:
                    self.title = f'ROSTER FEJLŐDÉS - {self.page}. OLDAL'
                    self.description = '📈A rostereden a következő fejlesztések történtek'
                    self.embed = Embed()
                    self.embed = self.embed.gen_base_embed(title=self.title, description=self.description)

                if self.counter < 800:
                    #generate embed with title + description
                   self.add_field(self.diff[self.character])
                   self.new_embed = False

                else:
                    self.add_field(self.diff[self.character])
                    self.embeds_list.append(self.embed)
                    self.counter = 0
                    self.page += 1
                    self.new_embed = True
            
            if self.page == 1:
                self.embeds_list.append(self.embed)

        
        else:
            #There is now difference in the provided saves
            self.null_roster_diff()

            self.embeds_list.append(self.embed)


        return self.embeds_list
        


    def add_field(self, char_dict):
        self.char_dict = char_dict
        self.name_line_no =  int((50 - len(self.char_dict['name']))/2)
        self.name =self.name_line_no * '-' + '   ' + self.char_dict['name'] + '   ' + self.name_line_no * '-'
        if (len(self.char_dict['name']) % 2) != 0:
            self.name += '-'
        self.value = '```xml\n'

        if self.char_dict['level_diff'] > 0:
            self.old_lvl = int(self.char_dict['old_level'])
            self.new_lvl = int(self.char_dict['new_level'])
            self.value += self.value_pos ('Level', self.old_lvl, self.new_lvl)

        if self.char_dict['rarity_diff'] > 0:
            self.old_rar = int(self.char_dict['old_rarity'])
            self.new_rar = int(self.char_dict['new_rarity'])
            self.value += self.value_pos ('Csillag', self.old_rar, self.new_rar)
            self.counter += 20

        if self.char_dict['gear_diff'] > 0:
            self.old_gear = int(self.char_dict['old_gear'])
            self.new_gear = int(self.char_dict['new_gear'])
            self.value += self.value_pos ('Gear', self.old_gear, self.new_gear)
            self.counter += 20

        if self.char_dict['relic_diff'] > 0:
            self.old_rel = int(self.char_dict['old_relic'])
            self.new_rel = int(self.char_dict['new_relic'])
            self.value += self.value_pos ('Relic', self.old_rel, self.new_rel)
            self.counter += 20

        if self.char_dict['zeta_diff'] > 0:
            self.old_zeta = int(self.char_dict['old_zeta'])
            self.new_zeta = int(self.char_dict['new_zeta'])
            self.value += self.value_pos ('Zeta', self.old_zeta, self.new_zeta)
            self.counter += 20
        
        self.value += '\n```'
        #self.value += '----------------------------------------------'

        self.embed.add_field(name=self.name, value=self.value, inline=False)
        
    def null_roster_diff(self):

        self.title = f'ROSTER FEJLŐDÉS'
        self.description = '📈A rostereden a következő fejlesztések történtek'
        self.embed = Embed()
        self.embed = self.embed.gen_base_embed(title=self.title, description=self.description)
        self.embed.add_field(name='NEM TÖRTÉNT VÁLTOZÁS A ROSTEREDBEN!', value='-------------------------------------------------------', inline=False)

    def value_pos(self, name, old, new):
        
        self.space1 = (25- len(name))* ' '
        if old < 10:
            self.space1 += ' '
        self.space2 = ' '
        if new < 10:
            self.space2 += ' '

        self.value_string = f'<{name}>:{self.space1}{old} ▶{self.space2}{new}\n'
        return self.value_string

# -------------------------------------------------------------------------------------------------------------
    def nonreg_embed(self, nonreg_list):
        #Generate embed from list of character 
        self.title = f'Nem Regisztrált Játékosok'
        self.description = '📈Regisztráld a felsorolt játékosokat a következő paranccsal:\n \
            `snk reg <discordUser> <allycode>`'
        self.embed = Embed()
        self.embed = self.embed.gen_base_embed(title=self.title, description=self.description)

        self.counter = 0
        
        self.value = '```ini\n'
        for player in nonreg_list:
            self.name = player['name']
            self.allycode = player['allycode']
            self.dashes = (20 - len(self.name)) * '-'
            self.value += f'[{self.name}]      {self.dashes}   [{self.allycode}]\n'
            self.counter += 1
            if self.counter == 10:
                self.fieldname = '-------------------- 1-10 -------------------'
                self.value += '```'
                self.embed.add_field(name=self.fieldname, value=self.value)
            if self.counter == 20:
                self.fieldname = '------------------- 11-20 -------------------'
                self.value += '```'
                self.embed.add_field(name=self.fieldname, value=self.value)
            if self.counter == 30:
                self.fieldname = '------------------- 21-30 -------------------'
                self.value += '```'
                self.embed.add_field(name=self.fieldname, value=self.value)
            if self.counter == 40:
                self.fieldname = '------------------- 31-40 -------------------'
                self.value += '```'
                self.embed.add_field(name=self.fieldname, value=self.value)
        if self.counter < 10:
            self.fieldname = '-------------------- 1-10 -------------------'
            self.value += '\n```'
            self.embed.add_field(name=self.fieldname, value=self.value)
        else:
            self.fieldname = '------------------- 41-50 -------------------'
            self.value += '```'
            self.embed.add_field(name=self.fieldname, value=self.value)

        return self.embed


            





# -------------------------------------------------------------------------------------------------------------

class Embed(object):
    '''Generate and empty embed object'''

    def __init__(self, logger=None):
        self.logger = logging.getLogger(__name__)
        

    def gen_base_embed(self, title, description,):

        self.title = title
        self.description = description
        self.embed_base = discord.Embed(
            title = self.title,
            description = description,
            color = discord.Color.dark_blue()
            )

        self.embed_base.set_footer(text = 'Are these droids you are looking for?')

        return self.embed_base
    












