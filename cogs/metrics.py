from discord.ext import commands
from discord import File
from pandas import DataFrame
from datetime import datetime
import matplotlib.pyplot as plt
import networkx as nx



class Metrics(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def networkplot(self, ctx):
		# Create dict of role names and the number of members in each
		roles = [str(role.name) for role in ctx.guild.roles]
		roles.remove('@everyone')

		df = DataFrame(columns=roles, index=roles)
		df[:] = int(0)

		for member in ctx.guild.members:
			member_roles = [role.name for role in member.roles]
			if '@everyone' in member_roles:
				member_roles.remove('@everyone')
			for role in member_roles:
				for co_role in member_roles:
						df[role][co_role] += 1
						df[co_role][role] += 1

		max_connection_weight = df.max().max()

		edge_list = []

		for index, row in df.iterrows():
			i = 0
			for col in row:
				weight = float(col) / max_connection_weight
				edge_list.append((index, df.columns[i], weight))
				i += 1

		# Remove edge if 0.0
		updated_edge_list = [x for x in edge_list if not x[2] == 0.0]

		node_list = []
		for r in roles:
			for e in updated_edge_list:
				if r == e[0] and r == e[1]:
					node_list.append((r, e[2] * 6))
		for i in node_list:
			if i[1] == 0.0:
				node_list.remove(i)

		# remove self references
		for i in updated_edge_list:
			if i[0] == i[1]:
				updated_edge_list.remove(i)

		# Create plot

		# set canvas size
		plt.subplots(figsize=(14, 14))

		# networkx graph time!
		G = nx.Graph()
		for i in sorted(node_list):
			G.add_node(i[0], size=i[1])
		G.add_weighted_edges_from(updated_edge_list)

		# check data of graphs
		# G.nodes(data=True)
		# G.edges(data = True)

		# manually copy and pasted the node order using 'nx.nodes(G)'
		# Couldn't determine another route to listing out the order of nodes for future work
		node_order = [str(x) for x in nx.nodes(G)]

		# reorder node list
		updated_node_order = []
		for i in node_order:
			for x in node_list:
				if x[0] == i:
					updated_node_order.append(x)

		# reorder edge list
		test = nx.get_edge_attributes(G, 'weight')
		updated_again_edges = []
		for i in nx.edges(G):
			for x in test.keys():
				if i[0] == x[0] and i[1] == x[1]:
					updated_again_edges.append(test[x])

		#Drawing custimization
		node_scalar = 1600
		edge_scalar = 20
		sizes = [x[1] * node_scalar for x in updated_node_order]
		widths = [x * edge_scalar for x in updated_again_edges]

		#Draw the graph
		pos = nx.spring_layout(G, k=0.42, iterations=17)
		plt.title(f'{ctx.guild.name} role co-occurance graph')
		nx.draw(G, pos, with_labels=True, font_size=8, font_weight='bold',
				node_size=sizes, width=widths)

		#One co-occurance image per server
		image_path = f'./assets/network_charts/{ctx.guild.id}.png'
		plt.savefig(image_path, format="PNG")
		await ctx.message.author.send(f'{ctx.guild.name} roles chart', file=File(image_path))

	@commands.command()
	async def plot(self,ctx):
		# Create dict of role names and the number of members in each
		roles_dict = {role.name: [len(role.members)] for role in ctx.guild.roles}
		roles_dict.pop('@everyone',None)
		num_roles = len(roles_dict)
		# Create plot
		plot_range = range(num_roles)
		data_frame = DataFrame.from_dict(roles_dict).sort_values(by=0,axis=1,ascending=False).transpose()
		sizing = len(data_frame.columns)*2
		data_frame.plot(title=f"{ctx.guild.name} roles on {datetime.today().strftime('%Y-%m-%d')}\n"
							  f"Average: {data_frame.describe().iloc[1].head(1)[0]}  Std. Dev: {round(data_frame.describe().iloc[2].head(1)[0],4)}\n"
							  f"Higher Quartile: {data_frame.describe().iloc[6].head(1)[0]}  Lower Quartile: {data_frame.describe().iloc[4].head(1)[0]}",
						kind='bar',
						width = .2,rot=90,
						fontsize=12,
						legend=False,
						figsize=(20+(sizing)*2,10+(sizing)))
		# One roles images per server
		image_path = f'./assets/role_charts/{ctx.guild.id}.png'
		plt.draw()
		plt.tight_layout()
		plt.savefig(image_path)
		await ctx.message.author.send(f'{ctx.guild.name} roles chart', file=File(image_path))


def setup(bot):
	bot.add_cog(Metrics(bot))