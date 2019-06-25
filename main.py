import json
import os

from discord.ext import commands

bot = commands.Bot(command_prefix="b!")


@bot.event
async def on_ready():
    print("Ready")
    config = json.loads(open('config.json', 'r').read())
    # Check if there are any new servers the bot does not have configs for
    for server in bot.guilds:
        if str(server.id) not in config:
            # Add empty config to JSON + initialize all win/loss stats for users
            config[server.id] = {
                "verification_channel": None,
                "verification_enabled": False,
                "verification_role": None
            }
            # Save to config file
            json.dump(config, open('config.json', 'w'), indent=2, separators=(',', ': '))


@bot.event
async def on_message(message):
    if message.author != bot.user:
        pass
    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    return


@bot.event
async def on_member_remove(member):
    return


@bot.event
async def on_guild_join(guild):
    config = json.loads(open('config.json', 'r').read())
    # Create configuration dict to store in JSON
    config[str(guild.id)] = {
        "verification_channel": None,
        "verification_enabled": False,
        "verification_role": None
    }
    # Save to config file
    json.dump(config, open('config.json', 'w'), indent=2, separators=(',', ': '))


@bot.event
async def on_guild_remove(guild):
    config = json.loads(open('config.json', 'r').read())
    config.pop(str(guild.id))
    json.dump(config, open('config.json', 'w'), indent=2, separators=(',', ': '))

for file in os.listdir("./cogs"):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')


token = json.loads(open('config.json', 'r').read())['token']
bot.run(token)
