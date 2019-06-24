import json
import os

from discord.ext import commands

bot = commands.Bot(command_prefix="b!")

config = json.loads(open('config.json', 'r').read())


@bot.event
async def on_ready():
    return


@bot.event
async def on_message(message):
    return


@bot.event
async def on_member_join(member):
    return


@bot.event
async def on_member_remove(member):
    return

for file in os.listdir("./cogs"):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run(config["token"])
