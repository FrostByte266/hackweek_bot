from asyncio import sleep

from discord.ext import commands
from discord import Member


class Messages(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int, target: Member = None):
        """Remove the specified amount of messages"""
        if target is None:
            await ctx.message.channel.purge(limit=limit+1)
        else:
            await ctx.message.channel.purge(limit=limit, check=lambda message: message.author == target)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.delete()
            message = await ctx.send("You are missing the manage messages permission!")
            await sleep(3)
            await message.delete()


def setup(bot):
    bot.add_cog(Messages(bot))
