# https://github.com/greeneyedsoandso/chewie
"""bot for fielding wookieepedia queries"""
from discord.ext import commands
from config import token
from wiki import wikia_summary
# commands start with / because having to hit shift is dumb
bot = commands.Bot(command_prefix='/')


@bot.event
# command line confirmation that the bot is running
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(name='hello', help='This is a test. Requires a name after the command.')
# if you type '/hello Han' Chewie says 'Hello Han!'
async def greeting(ctx, args):
    hello = f'Hello {args}!'
    await ctx.send(hello)


@bot.event
async def on_message(message):
    # A wild Xexto appears!
    if message.content.find(' appears!') == -1:
        return

    else:
        int1 = message.content.find('A wild')
        end = message.content.find(' appears!')
        start = int1 + 6
        alien = message.content[start:end]
        summary = wikia_summary(alien)
        await message.channel.send(summary)

bot.run(token)
