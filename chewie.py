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
ladders = {"Olympian": "Olympian",
           "8": "Legendary",
           "7": "Epic",
           "6": "Fantastic",
           "5": "Superb",
           "4": "Great",
           "3": "Good",
           "2": "Fair",
           "1": "Average",
           "0": "Mediocre",
           "-1": "Poor",
           "-2": "Terrible",
           "Tragedy": "Tragedy"}


def ladder_text(success_count, ladder):
    if int(success_count) > 8:
        return ladder["Olympian"]
    if int(success_count) < -2:
        return ladder["Tragedy"]
    else:
        return ladder[success_count]


def calc_dice(n):
    str_n = str(n)
    if str_n.isnumeric():
        results = list(random.choice(["+", "-", " "], int(n)))
        total = results.count("+") - results.count("-")
    elif "+" in str_n:
        n_dice, bonus = n.split("+")
        results = list(random.choice(["+", "-", " "], int(n_dice)))
        total = results.count("+") - results.count("-") + int(bonus)
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


def grammar(user_input):
    if user_input.isnumeric():
        if user_input == '1':
            roll_text = f"rolls {user_input} die."
        else:
            roll_text = f"rolls {user_input} dice."
    else:
        n_dice, bonus = user_input.split('+')
        if n_dice == '1':
            roll_text = f"rolls {n_dice} die + {bonus}."
        else:
            roll_text = f"rolls {n_dice} dice + {bonus}."
    return roll_text
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


@bot.command(name='fate', help='Roll Fate dice and optional modifier. Examples: /fate 4 or /fate '
                               '4+1 or /fate 4+-2')
async def dice(ctx, n_dice):
    """Rolls FATE dice"""
    result = calc_dice(n_dice)
    emojis = dice_to_emoji(result[0])
    roll_text = grammar(n_dice)
    user_id = ctx.message.author.display_name
    ladder_level = ladder_text(str(result[1]), ladders)
    await ctx.send(f"***{str(user_id)}*** {roll_text}\n"
                   f"{emojis}\nTotal result: {str(result[1])}, **{ladder_level}**")


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
