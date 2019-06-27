from discord.ext import commands
from discord import File
import matplotlib.pyplot as plt

class Metrics(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	async def rolesChart(self,ctx):
		roles = ctx.guild.roles
		roles_dict = {role:0 for role in roles}
		#Generate a flat list of all roles currently attached
		current_tags = [].extend(roles for roles in [member.roles for member in ctx.guild.members])
		#abusing list comprehension
		for role in current_tags:
			roles_dict[role]+=1
		plot_range = range(len(roles_dict))
		plt.bar(plot_range, list(roles_dict.values()), align='center')
		plt.xticks(plot_range, list(roles_dict.keys()))
		#One roles images per server
		image_name = f'{ctx.guild.name}{ctx.guild.id}.png'
		plt.savefig(image_name)
		await ctx.message.author.send(f'{ctx.guild.name} roles chart', file=File(image_name))

def setup(bot):
	bot.add_cog(Metrics(bot))