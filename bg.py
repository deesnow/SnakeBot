from discord.ext import commands
import asyncio

class BgTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def task1(self):

        channel = self.bot.get_channel(573490564646043649)
        await channel.send('Task1 started by event_loop')
        self.running = self.bot.is_ready()
        self.counter = 0
        while True:
            self.counter += 1
            await channel.send('Task1 - {} cycle'.format(self.counter))
            await asyncio.sleep(60)

    
    @commands.Cog.listener()
    async def on_ready(self):
        print('BG task called')
        self.bg_task = self.bot.loop.create_task(self.task1())


    @commands.command(pass_context=True)
    async def stopbg(self, ctx):
        channel = self.bot.get_channel(573490564646043649)
        self.bg_task.cancel()
        await channel.send('Task1 cycles - STOPPED')


def setup(bot):
    bot.add_cog(BgTask(bot))