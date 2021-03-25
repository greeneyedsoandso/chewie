# https://github.com/greeneyedsoandso/chewie
"""bot for fielding wookieepedia queries"""
import os
from numpy import random
from discord.ext import commands
from discord import Embed
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
    elif "-" in str_n:
        n_dice, negative = n.split("-")
        results = list(random.choice(["+", "-", " "], int(n_dice)))
        total = results.count("+") - results.count("-") - int(negative)
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


fate_points = {}


def character_check(character, dictionary):
    if character in dictionary:
        return True
    return False


def value_check(character, dictionary):
    if int(dictionary[character]) < 1:
        return False
    return True


def fate_points_add(character, dictionary):
    if character_check(character, dictionary):
        new_total = int(dictionary[character]) + 1
        dictionary[character] = str(new_total)
    else:
        return False
    return True


def fate_points_use(character, dictionary):
    if character_check(character, dictionary):
        if value_check(character, dictionary):
            new_total = int(dictionary[character]) - 1
            dictionary[character] = str(new_total)
            return True
        return False
    return False
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


@bot.command(name='make', help='Adds character to Fate point tracker. '
                               'Example: /make Han')
async def make(ctx, character):
    """Adds character to tracking"""
    if character_check(character, fate_points):
        await ctx.send(f"***{character}*** was here all along.")
    elif not character_check(character, fate_points):
        fate_points[character] = '0'
        await ctx.send(f"Welcome, ***{character}***.")


@bot.command(name='kill', help='Removes character from Fate point tracker. '
                               'Example: /kill Han')
async def kill(ctx, character):
    """Removes character from tracking"""
    if character_check(character, fate_points):
        fate_points.pop(character)
        await ctx.send(f"Goodbye, ***{character}***.")
    elif not character_check(character, fate_points):
        await ctx.send(f"***{character}***? Never heard of them.")


@bot.command(name='fate', help='Roll Fate dice and optional modifier. Examples: /fate or /fate '
                               '+1 or /fate -2')
async def dice(ctx, n_dice="4"):
    """Rolls FATE dice"""
    result = calc_dice(n_dice)
    emojis = dice_to_emoji(result[0])
    roll_text = grammar(n_dice)
    user_id = ctx.message.author.display_name
    ladder_level = ladder_text(str(result[1]), ladders)
    await ctx.send(f"***{str(user_id)}*** {roll_text}\n"
                   f"{emojis}\nTotal result: {str(result[1])}, **{ladder_level}**")


@bot.command(name='Fate', help='Error handling/shaming')
async def typo(ctx):
    """Gives an error message"""
    user_id = ctx.message.author.display_name
    await ctx.send(f"***{str(user_id)}*** please try again with lower case")


@bot.command(name='+fp', help='Grants a Fate point to the named character. Example: /+fp Han')
async def add_fate_point(ctx, character):
    """Adds Fate point to character"""
    if fate_points_add(character, fate_points):
        await ctx.send(f"***{character}*** added one Fate point")
    else:
        await ctx.send(f"***{character}***? Typo? Or did you need to /make?")


@bot.command(name='-fp', help='Named character uses a Fate point. Example: /-fp Han')
async def use_fate_point(ctx, character):
    """Removes Fate point from character"""
    if fate_points_use(character, fate_points):
        await ctx.send(f"***{character}*** used one Fate point")
    else:
        if character_check(character, fate_points):
            await ctx.send(f"***{character}*** does not have any Fate points")
        else:
            await ctx.send(f"***{character}***? Typo?")


@bot.command(name='points', help='Shows current Fate points for the named character. '
                                 'Example: /points Han')
async def current_points(ctx, character):
    """Adds Fate point to character"""
    if character_check(character, fate_points):
        await ctx.send(f"Current Fate points for ***{character}***: **{fate_points[character]}**")
    else:
        await ctx.send(f"***{character}***? Never heard of them.")


# @bot.command(name='list', help='BROKEN: Shows list of characters and Fate point totals')
# async def show_list(ctx):
#     """Lists characters"""
#     embed = Embed(title=f"__**Characters**__", color=0x0047ab)
#     # ToDo: something is wrong here, i think it doesn't like processing the dictionary? Try making
#     #  a hardcoded version with one value to see if the formatting is working? what if we did an
#     #  individual check instead of calling up the full table?
#     for key, value in fate_points:  # process embed
#         embed.add_field(name=f'**{key}**',
#                         value=f'> Fate points: {value}\n',
#                         inline=False)
#     await ctx.send(embed=embed)


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
