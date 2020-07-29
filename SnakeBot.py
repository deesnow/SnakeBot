import json
import os
import logging
import logging.config
from discord.ext import commands, tasks
from discord import Game
import asyncio
from botSettings import settings


# Define logger ---------------------------------------------------------
def setup_logging(
    default_path='botSettings\\logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as log_settings:
            log_config = json.load(log_settings)
        logging.config.dictConfig(log_config)
    else:
        logging.basicConfig(level=default_level)


setup_logging()
logger = logging.getLogger(__name__)


#Setup base Discord Bot ------------------------------------------------------

class MyClient(commands.Bot):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


            self.BOT_PREFIX = ("?", "!")

            

            

        #OnReady Message
        async def on_ready(self):
            print('We have logged in as {0.user}'.format(self))
            presence = f'Version: {settings.VERSION} - Under Development'
            await self.change_presence(activity=Game(name=presence))
            logger.info('We have logged in as {0.user}'.format(self))

        
bot = MyClient(command_prefix = 'snk ')



@bot.command(aliases= ['l'])
@commands.has_any_role('BotAdmin') # User need this role to run command (can have multiple)
async def load(ctx, extension, description='Load command extension. Only person with right permission can call it'):
    try:
        bot.load_extension('expansions.'+ extension)
        await ctx.message.add_reaction("✅")

    except Exception as error:
        await ctx.message.add_reaction("💥")
        await ctx.send('{} cannot be loaded. [{}]'.format(extension, error))
        logger.exception ('{} cannot be loaded. [{}]'.format(extension, error))

@load.error
async def saveroster_error(self, ctx, error):
    self.ctx = ctx
    if isinstance(error, commands.CheckFailure):
        print("Permission error!!!")
        await self.ctx.send('⛔ - You don\'t have the right permission!!!')

@bot.command(aliases= ['u'])
@commands.has_any_role('BotAdmin') # User need this role to run command (can have multiple)
async def unload(ctx, extension, description='Unload command extension. Only person with right permission can call it'):
    try:
        bot.unload_extension('expansions.'+ extension)
        await ctx.message.add_reaction("✅")

    except Exception as error:
        await ctx.message.add_reaction("💥")
        await ctx.send('{} cannot be unloaded. [{}]'.format(extension, error))
        logger.exception ('{} cannot be unloaded. [{}]'.format(extension, error))

@unload.error
async def saveroster_error(self, ctx, error):
    self.ctx = ctx
    if isinstance(error, commands.CheckFailure):
        print("Permission error!!!")
        await self.ctx.send('⛔ - You don\'t have the right permission!!!')
    
@bot.command(aliases= ['rl'])
@commands.has_any_role('BotAdmin') # User need this role to run command (can have multiple)
async def reload(ctx, extension, description='Reload/Refresh command extension. Only person with right permission can call it'):
    try:
        bot.unload_extension('expansions.'+ extension)
        bot.load_extension('expansions.'+ extension)
        await ctx.message.add_reaction("✅")

    except Exception as error:
        await ctx.message.add_reaction("💥")
        await ctx.send('{} cannot be unloaded. [{}]'.format(extension, error))
        logger.exception ('{} cannot be unloaded. [{}]'.format(extension, error))

@reload.error
async def saveroster_error(self, ctx, error):
    self.ctx = ctx
    if isinstance(error, commands.CheckFailure):
        print("Permission error!!!")
        await self.ctx.send('⛔ - You don\'t have the right permission!!!')      

# -----------------------------------------

extensions = settings.EXTENSIONS

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension('expansions.'+ extension)
            #print ('{} is loaded.'.format(extension))
        except Exception as error:
            print ('{} cannot be loaded. [{}]'.format(extension, error))

# -----------------------------------------


bot.run(settings.TOKEN)