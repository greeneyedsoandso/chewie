# https://github.com/greeneyedsoandso/chewie
"""bot for fielding wookieepedia queries"""
from discord.ext import commands
from config import token
bot = commands.Bot(command_prefix='/')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(name='hello')
async def greeting(ctx):
    await ctx.send('Hello!')

bot.run(token)
