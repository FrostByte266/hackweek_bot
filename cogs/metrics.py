from discord.ext import commands
from discord import File
import matplotlib.pyplot as plt


class Metrics(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def plot(self,ctx):
		# Create dict of role names and the number of members in each
		roles_dict = {role: len(role.members) for role in ctx.guild.roles}
		num_roles = len(roles_dict)
		# Create plot
		plot_range = range(num_roles)
		plt.figure(figsize=(num_roles*2, 10))
		plt.bar(plot_range, list(roles_dict.values()), align='center')
		plt.xticks(plot_range, list(roles_dict.keys()))
		# One roles images per server
		image_path = f'./assets/role_charts/{ctx.guild.id}.png'
		plt.savefig(image_path)
		await ctx.message.author.send(f'{ctx.guild.name} roles chart', file=File(image_path))


def setup(bot):
	bot.add_cog(Metrics(bot))