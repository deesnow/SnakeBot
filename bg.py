from discord.ext import commands
import asyncio

class BgTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def task1(self):

        channel = self.bot.get_channel(573490564646043649)
        await channel.send('Task1 started by event_loop')
        self.running = self.bot.is_ready()
        self.counter = 1
        await channel.send('Task1 - {} cycle'.format(self.counter))
        while True:
            self.counter += 1
            await channel.send('Task1 - {} cycle'.format(self.counter))
            await asyncio.sleep(60)

    
    @commands.Cog.listener()
    async def on_ready(self):
        print('BG task called')
        self.heartbeat_task = self.bot.loop.create_task(self.task1())


    @commands.command(pass_context=True)
    async def stop(self, ctx):
        self.heartbeat_task.cancel()
        await self.bot.say('Heartbeat stopped by user {}'.format(ctx.message.author.name))


def setup(bot):
    bot.add_cog(BgTask(bot))