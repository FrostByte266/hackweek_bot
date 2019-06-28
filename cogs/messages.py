from asyncio import sleep

from discord import Embed, TextChannel, User
from discord.ext import commands


class Messages(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int, target: User = None):
        """Remove the specified amount of messages"""
        await ctx.message.delete()
        if target is None:
            await ctx.message.channel.purge(limit=limit)
        else:
            await ctx.message.channel.purge(limit=limit, check=lambda message: message.author == target)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.delete()
            message = await ctx.send("You are missing the manage messages permission!")
            await sleep(3)
            await message.delete()

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def move(self, ctx, count: int, target: TextChannel, copy: bool = False):
        """Move/copy specified amount of messages to target channel"""
        await ctx.message.delete()
        messages = []
        async for message in ctx.message.channel.history(limit=count):
            embed = Embed(description=message.content)
            embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
            embed.timestamp = message.created_at
            messages.append(embed)
            if not copy:
                await message.delete()

        await target.send(f'Moved from {ctx.message.channel.mention}:')

        for embed in reversed(messages):
            await target.send(embed=embed)

    @move.error
    async def move_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.delete()
            temp = await ctx.send("Error! Missing one or more of the following arguments: count, target")
            await sleep(3)
            await temp.delete()


def setup(bot):
    bot.add_cog(Messages(bot))
