from datetime import datetime
import json
import os

from discord import Embed
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
									"verification_role": None,
									"reporting_channel": None,
									"reports": {}
								}
			# Save to config file
			json.dump(config, open('config.json', 'w'), indent=2, separators=(',', ': '))


@bot.event
async def on_message(message):
	if message.guild is None:
		await bot.process_commands(message)
		return
	config_full = json.loads(open('config.json', 'r').read())
	config = config_full[str(message.guild.id)]
	verification_enabled = True if config["verification_channel"] is not None else False
	if message.author != bot.user and verification_enabled:
		# Check if the user is attempting to verify, if not then delete the message and send them a notice in DM
		verify_channel = config['verification_channel']
		unverified_role = get(message.author.guild.roles, name="Unverified")
		if unverified_role in message.author.roles and (message.channel.id != verify_channel and message.content != "b!verify"):
			await message.channel.purge(limit=1)
			await message.author.send(
				"You have not verified your account, please type 'b!verify' in your server's verification channel")
	await bot.process_commands(message)


@bot.event
async def on_member_join(member):
	config_full = json.loads(open('config.json', 'r').read())
	config = config_full[str(member.guild.id)]
	verification_enabled = True if config["verification_channel"] is not None else False
	if verification_enabled and not member.bot:
		role = get(member.guild.roles, id=config["verification_role"])
		await member.add_roles(role)

	# Prepare welcome embed
	embed = Embed(
					color=0x9370DB,
					description=f'Welcome to the server! You are member number {len(list(member.guild.members))}'
				)
	embed.set_thumbnail(url=member.avatar_url)
	embed.set_author(name=member.name, icon_url=member.avatar_url)
	embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
	embed.timestamp = datetime.utcnow()

	# Get the server message channel and send welcome message there
	channel = bot.get_channel(id=member.guild.system_channel.id)

	await channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
	# Prepare goodbye embed
	embed = Embed(color=0x9370DB, description=f'Goodbye! Thank you for spending time with us!')
	embed.set_thumbnail(url=member.avatar_url)
	embed.set_author(name=member.name, icon_url=member.avatar_url)
	embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
	embed.timestamp = datetime.utcnow()

	# Get the server message channel and send goodbye message there
	channel = bot.get_channel(id=member.guild.system_channel.id)

	await channel.send(embed=embed)


@bot.event
async def on_guild_join(guild):
	config = json.loads(open('config.json', 'r').read())
	# Create configuration dict to store in JSON
	config[str(guild.id)] = {
		"verification_channel": None,
		"verification_role": None,
		"reporting_channel": None,
		"reports": {}
	}
	# Save to config file
	json.dump(config, open('config.json', 'w'), indent=2, separators=(',', ': '))


@bot.event
async def on_guild_remove(guild):
	config = json.loads(open('config.json', 'r').read())
	config.pop(str(guild.id))
	json.dump(config, open('config.json', 'w'), indent=2, separators=(',', ': '))


if __name__ == '__main__':
	token = None
	try:
		# Attempt to fetch the token from config.json
		token = json.loads(open('config.json', 'r').read())['token']
	except FileNotFoundError:
		# If config.json does not exist, it must be the first time starting the bot, run through configuration
		token = input('It appears this is the first time running the bot. Please enter your bot\'s token: ')
		initial_config = {"token": token}
		json.dump(initial_config, open('config.json', 'w'), indent=2, separators=(',', ': '))
		os.mkdir('./assets/network_charts')
		os.mkdir('./assets/role_charts')
	finally:
		for file in os.listdir('./cogs'):
			if file.endswith('.py'):
				bot.load_extension(f'cogs.{file[:-3]}')
		bot.run(token)

