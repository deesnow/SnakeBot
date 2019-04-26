import pymongo
import json
import os
import os
import json
import logging
import logging.config
import discord
from discord.ext import commands
from discord import Game

import db_handler as mongo

def setup_logging(
    default_path='logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)



logger = logging.getLogger(__name__)
setup_logging()

#Setup base Discord Bot
BOT_PREFIX = ("?", "!")
TOKEN = "NTU4MjI0MDYyMTY2MzM1NTA5.D3TwfA.O8FZKYREf8DCy8BniYQeEfuei4A"
SERVER_ID = "558221252024598539"

bot = commands.Bot(command_prefix = 'snk ')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=Game(name="Under Development"))
        
@bot.command()
async def load(ctx, extension):
    try:
        bot.load_extension(extension)
        await ctx.message.add_reaction("✅")

    except Exception as error:
        await ctx.message.add_reaction("💥")
        await ctx.send('{} cannot be loaded. [{}]'.format(extension, error))
        logger.exception ('{} cannot be loaded. [{}]'.format(extension, error))

@bot.command()
async def unload(ctx, extension):
    try:
        bot.unload_extension(extension)
        await ctx.message.add_reaction("✅")

    except Exception as error:
        await ctx.message.add_reaction("💥")
        await ctx.send('{} cannot be unloaded. [{}]'.format(extension, error))
        logger.exception ('{} cannot be unloaded. [{}]'.format(extension, error))
    
extensions = ['cmdReg', 'cmdEmbed']       

# -----------------------------------------
if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print ('{} is loaded.'.format(extension))
        except Exception as error:
            print ('{} cannot be loaded. [{}]'.format(extension, error))



bot.run(TOKEN)