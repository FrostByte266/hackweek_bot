import json
import os

from discord.ext import commands
from discord.utils import get

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
    if message.guild is None:
        await bot.process_commands(message)
        return
    if message.author != bot.user:
        config = json.loads(open('config.json', 'r').read())
        # Check if the user is attempting to verify, if not then delete the message and send them a notice in DM
        verify_channel = config[str(message.guild.id)]['verification_channel']
        unverified_role = get(message.author.guild.roles, name="Unverified")
        if unverified_role in message.author.roles and (message.channel.id != verify_channel and message.content != "b!verify"):
            await message.channel.purge(limit=1)
            await message.author.send("You have not verified your account, please type 'b!verify' in your server's verification channel")


@bot.event
async def on_member_join(member):
    config = json.loads(open('config.json', 'r').read())
    if config[str(member.guild.id)]['verification_enabled']:
        role = get(member.guild.roles, id=config[str(member.guild.id)]["verification_role"])
        await member.add_roles(role)


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
