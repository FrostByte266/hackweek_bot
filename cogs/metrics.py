from discord.ext import commands
from discord import File
from pandas import DataFrame
from datetime import datetime
import matplotlib.pyplot as plt



class Metrics(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def plot(self,ctx):
		# Create dict of role names and the number of members in each
		roles_dict = {role.name: [len(role.members)] for role in ctx.guild.roles}
		roles_dict.pop('@everyone',None)
		num_roles = len(roles_dict)
		# Create plot
		plot_range = range(num_roles)
		data_frame = DataFrame.from_dict(roles_dict).sort_values(ascending=False)
		data_frame.plot(title=f"{ctx.guild.name} roles on {datetime.today().strftime('%Y-%m-%d')}",kind='bar', width = .2,rot=90,range=plot_range)
		# One roles images per server
		image_path = f'./assets/role_charts/{ctx.guild.id}.png'
		plt.savefig(image_path)
		await ctx.message.author.send(f'{ctx.guild.name} roles chart', file=File(image_path))


def setup(bot):
	bot.add_cog(Metrics(bot))