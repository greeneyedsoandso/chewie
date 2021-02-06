# https://github.com/greeneyedsoandso/chewie
"""bot for fielding wookieepedia queries"""
import os
from discord.ext import commands
from wiki import wikia_summary, wikia_link
# commands start with / because having to hit shift is dumb
bot = commands.Bot(command_prefix='$')
token = os.getenv("DISCORD_BOT_TOKEN")


@bot.event
# command line confirmation that the bot is running
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(name='hello', help='This is a test. Requires a name after the command.')
# if you type '/hello Han' Chewie says 'Hello Han!'
async def greeting(ctx, args):
    hello = f'Hello {args}!'
    await ctx.send(hello)


@bot.command()
# an extra-dumb test: if you type '$test something` Chewie says `something`
async def test(ctx, arg):
    await ctx.send(arg)


@bot.listen('on_message')
async def look_up(message):
    # A wild Xexto appears!
    if message.content.find(' appears!') == -1:
        return

    else:
        int1 = message.content.find('A wild')
        end = message.content.find(' appears!')
        start = int1 + 7
        alien = message.content[start:end]
        alien_link = alien
        try:
            clean = alien.replace("'", "%27")
            alien_link = clean
        except IndexError:
            pass
        try:
            clean = alien.replace(" ", "_")
            alien = clean
            alien_link = clean
        except IndexError:
            pass
        summary = wikia_summary(alien)
        more = summary + ' ' + wikia_link(alien_link)
        await message.channel.send(more)


bot.run(token)
