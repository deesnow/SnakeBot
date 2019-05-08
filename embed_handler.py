import discord
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

def embed(title, description, messeages):
    embed = discord.Embed(
            title = 'Command Title',
            description = 'This is a description',
            color = discord.Color.dark_blue()
    
    embed.set_footer(text = 'I hope you are happy with this')
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/558224062166335509/430849dd3a3d2b9179aaa0006ca22d88.png')

    if type(messeages) is dict:
        pass