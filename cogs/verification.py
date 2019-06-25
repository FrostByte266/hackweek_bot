import json

from discord.ext import commands
from discord.utils import get


class Verification(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def enable(self, ctx):
        """Enable the verification system"""
        # Create role and channel
        role = await ctx.guild.create_role(name="Unverified")
        channel = await ctx.guild.create_text_channel(name="Verification")
        config = json.loads(open('config.json', 'r').read())
        config[str(ctx.message.guild.id)].update(verification_enabled=True, verification_channel=channel.id, verification_role=role.id)
        json.dump(config, open('config.json', 'w'), indent=2, separators=(',', ': '))

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def disable(self, ctx):
        """Disable the verification system"""
        config = json.loads(open('config.json', 'r').read())
        # Delete role and channel
        await get(ctx.guild.roles, id=config[str(ctx.guild.id)]["verification_role"]).delete()
        await get(ctx.guild.text_channels, id=config[str(ctx.guild.id)]["verification_channel"]).delete()
        config[str(ctx.message.guild.id)].update(verification_enabled=False, verification_channel=None, verification_role=None)
        json.dump(config, open('config.json', 'w'), indent=2, separators=(',', ': '))


def setup(bot):
    bot.add_cog(Verification(bot))
