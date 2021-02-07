# https://github.com/greeneyedsoandso/chewie
"""bot for fielding wookieepedia queries"""
import os
from numpy import random
from discord.ext import commands
from wiki import wikia_summary, wikia_link

# commands start with / because having to hit shift is dumb
bot = commands.Bot(command_prefix='/')
token = os.getenv("DISCORD_BOT_TOKEN")


# FATE dice utility functions


def calc_dice(n):
    results = list(random.choice(["+", "-", " "], n))
    total = results.count("+") - results.count("-")
    return results, total


def dice_to_emoji(dice_list):
    rt_emojis = []
    for die in dice_list:
        if die == "+":
            rt_emojis.append("<:pluskey:807768315669643314>")
        elif die == "-":
            rt_emojis.append("<:minuskey:807768315577237595>")
        elif die == " ":
            rt_emojis.append("<:voidkey:807768315635826718>")
    return ' '.join(rt_emojis)
# Bot actions


@bot.event
# command line confirmation that the bot is running
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(name='hello', help='This is a test. Requires a name after the command.')
# if you type '/hello Han' Chewie says 'Hello Han!'
async def greeting(ctx, args):
    hello = f'Hello {args}!'
    await ctx.send(hello)


@bot.command(help='Dumb test that repeats a word you type')
# an extra-dumb test: if you type '$test something` Chewie says `something`
async def test(ctx, arg):
    await ctx.send(arg)


@bot.command(name='fate', help='Follow with the number of dice to roll. Example /fate 4')
async def dice(ctx, n_dice):
    """Rolls FATE dice"""
    result = calc_dice(int(n_dice))
    emojis = dice_to_emoji(result[0])
    user_id = ctx.message.author
    # player = user_id.commands.clean_content(use_nicknames=True)
    if result == 1:
        await ctx.send(f"{str(user_id)} rolls {n_dice} die.\n"
                       f"{emojis}\nTotal result: {str(result[1])}")
    else:
        await ctx.send(f"{str(user_id)} rolls {n_dice} dice.\n"
                       f"{emojis}\nTotal result: {str(result[1])}")


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
