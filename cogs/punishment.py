from datetime import datetime
import json

from discord import Embed, Guild, User
from discord.utils import get
from discord.ext import commands


class IncidentReport:

    def __init__(self, server: Guild, action: str, body: str, issuer: User, subject: User):
        self.action = action
        self.issuer = issuer
        self.subject = subject
        self.body = body
        self.server = server
        self.config_full = json.loads(open('config.json').read())
        self.config = self.config_full[str(self.server.id)]
        self.report_number = self.next_report_number()
        self.finalize_report()

    def next_report_number(self):
        return len(self.config['reports']) + 1

    def finalize_report(self):
        report = {
            "report_id": self.report_number,
            "action": self.action,
            "issuer": f'{self.issuer.name}#{self.issuer.discriminator}',
            "subject": f'{self.subject.name}#{self.subject.discriminator}',
            "body": self.body
        }
        self.config["reports"].update({self.report_number: report})
        json.dump(self.config_full, open('config.json', 'w'), indent=2, separators=(',', ': '))

    def generate_receipt(self):
        embed = Embed(title='Incident Report', description=f'Case Number: {self.report_number}', color=0xff0000)
        embed.add_field(name="Issued By:", value=f'{self.issuer.name}#{self.issuer.discriminator}')
        embed.add_field(name="Subject:", value=f'{self.subject.name}#{self.subject.discriminator}')
        embed.add_field(name='Action', value=self.action)
        embed.add_field(name='Reason', value=self.body)
        embed.timestamp = datetime.utcnow()
        return embed


async def handle_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You have not entered all required parameters, use b!help <command> for a list of all parameters')
    elif isinstance(error, commands.BadArgument):
        await ctx.send("User not found! Double check you entered the correct details!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('You are missing the required permissions')


class Punishment(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config_full = json.loads(open('config.json').read())

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, target: User, *, reason: str):
        """Kick the specified user (a report receipt will be send to the recipient and issuer, and optionally reporting channel if enabled)"""
        report = IncidentReport(ctx.message.guild, 'Kick', reason, ctx.message.author, target)
        receipt = report.generate_receipt()
        await ctx.message.author.send(f'User: {target.name}#{target.discriminator} has been kicked. The incident report is attached below:', embed=receipt)
        await target.send(f'You have been kicked from {ctx.message.guild}. The incident report is attached below:', embed=receipt)
        await ctx.message.guild.kick(target, reason=reason)
        await ctx.send(f'User: {target.name}#{target.discriminator} has been kicked. Report ID: {report.report_number}')
        reporting_enabled = True if self.config_full[str(ctx.message.guild.id)]["reporting_channel"] is not None else False
        if reporting_enabled:
            report_channel = get(ctx.message.guild.text_channels, id=self.config_full[str(ctx.message.guild.id)]["reporting_channel"])
            await report_channel.send(embed=receipt)

    @kick.error
    async def kick_error(self, ctx, error):
        await handle_error(ctx, error)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, target: User, *, reason: str):
        """Ban the specified user (a report receipt will be sent to the recipient and issuer, and optionally reporting channel if enabled)"""
        report = IncidentReport(ctx.message.guild, 'Ban', reason, ctx.message.author, target)
        receipt = report.generate_receipt()
        await ctx.message.author.send(f'User: {target.name}#{target.discriminator} has been banned. The incident report is attached below:', embed=receipt)
        await target.send(f'You have been banned from {ctx.message.guild}. The incident report is attached below:', embed=receipt)
        await ctx.message.guild.ban(target, reason=reason)
        await ctx.send(f'User: {target.name}#{target.discriminator} has been banned. Report ID: {report.report_number}')
        reporting_enabled = True if self.config_full[str(ctx.message.guild.id)]["reporting_channel"] is not None else False
        if reporting_enabled:
            report_channel = get(ctx.message.guild.text_channels, id=self.config_full[str(ctx.message.guild.id)]["reporting_channel"])
            await report_channel.send(embed=receipt)

    @ban.error
    async def ban_error(self, ctx, error):
        await handle_error(ctx, error)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, target: int, *, reason: str):
        """Ban a user not in the server"""
        user = await self.bot.fetch_user(target)
        report = IncidentReport(ctx.message.guild, 'Hackban', reason, ctx.message.author, user)
        receipt = report.generate_receipt()
        await ctx.message.author.send(f'User: {user.name}#{user.discriminator} has been hackbanned. The incident report is attached below:', embed=receipt)
        await ctx.message.guild.ban(user, reason=reason)
        await ctx.send(f'User: {user.name}#{user.discriminator} has been hackbanned. Report ID: {report.report_number}')
        reporting_enabled = True if self.config_full[str(ctx.message.guild.id)]["reporting_channel"] is not None else False
        if reporting_enabled:
            report_channel = get(ctx.message.guild.text_channels, id=self.config_full[str(ctx.message.guild.id)]["reporting_channel"])
            await report_channel.send(embed=receipt)

    @hackban.error
    async def hackban_error(self, ctx, error):
        await handle_error(ctx, error)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, target_id: int, *, reason: str):
        """Unban the specified user (a report receipt will be sent to the recipient and issuer, and optionally reporting channel if enabled, user ID number required)"""
        target = await self.bot.fetch_user(target_id)
        report = IncidentReport(ctx.message.guild, 'Unban', reason, ctx.message.author, target)
        receipt = report.generate_receipt()
        await ctx.message.author.send(f'User: {target.name}#{target.discriminator} has been unbanned. The incident report is attached below:', embed=receipt)
        await ctx.message.guild.unban(target)
        await ctx.send(f'User: {target.name}#{target.discriminator} has been unbanned. Report ID: {report.report_number}')
        reporting_enabled = True if self.config_full[str(ctx.message.guild.id)]["reporting_channel"] is not None else False
        if reporting_enabled:
            report_channel = get(ctx.message.guild.text_channels, id=self.config_full[str(ctx.message.guild.id)]["reporting_channel"])
            await report_channel.send(embed=receipt)

    @unban.error
    async def unban_error(self, ctx, error):
        await handle_error(ctx, error)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def report(self, ctx, target: User, action: str, *, reason: str):
        """Create a custom incident report, action must be one word (receipt will be sent to recipient and issuer, and optionally reporting channel if enabled) """
        report = IncidentReport(ctx.message.guild, action, reason, ctx.message.author, target)
        receipt = report.generate_receipt()
        await ctx.message.author.send(f'Incident report receipt:', embed=receipt)
        await target.send(f'Incident report receipt:', embed=receipt)
        reporting_enabled = True if self.config_full[str(ctx.message.guild.id)]["reporting_channel"] is not None else False
        if reporting_enabled:
            report_channel = get(ctx.message.guild.text_channels, id=self.config_full[str(ctx.message.guild.id)]["reporting_channel"])
            await report_channel.send(embed=receipt)

    @report.error
    async def report_error(self, ctx, error):
        await handle_error(ctx, error)

    @commands.command()
    async def lookup(self, ctx, *, args: str):
        """Search for a report by user ID, mention, or report ID number, use b!lookup <report id> --receipt to have a copy sent to you via DM"""
        config = self.config_full[str(ctx.message.guild.id)]
        reports = config["reports"]
        length_args = len(args.strip())
        embed = None
        if length_args == 18:
            # User ID has been provided
            user = await self.bot.fetch_user(args)
            user_name = f'{user.name}#{user.discriminator}'
            results = []
            reports = config["reports"]
            for report_iter in config["reports"]:
                report_num = str(report_iter)
                if reports[report_num]["issuer"] == user_name or reports[report_num]["subject"] == user_name:
                    results.append(report_num)
            if results:
                for result in results:
                    embed = Embed(title='Incident Report', description=f'Case Number: {reports[result]["report_id"]}', color=0xff0000)
                    embed.add_field(name="Issued By:", value=reports[result]["issuer"])
                    embed.add_field(name="Subject:", value=reports[result]["subject"])
                    embed.add_field(name='Action', value=reports[result]["action"])
                    embed.add_field(name='Reason', value=reports[result]["body"])
                    await ctx.send(embed=embed)
            else:
                await ctx.send('No reports found with the user provided')
        elif ctx.message.mentions:
            # User provided via mention
            user = ctx.message.mentions[0]
            user_name = f'{user.name}#{user.discriminator}'
            results = []
            reports = config["reports"]
            for report_iter in config["reports"]:
                report_num = str(report_iter)
                if reports[report_num]["subject"] == user_name:
                    results.append(report_num)
            if results:
                for result in results:
                    embed = Embed(title='Incident Report', description=f'Case Number: {reports[result]["report_id"]}', color=0xff0000)
                    embed.add_field(name="Issued By:", value=reports[result]["issuer"])
                    embed.add_field(name="Subject:", value=reports[result]["subject"])
                    embed.add_field(name='Action', value=reports[result]["action"])
                    embed.add_field(name='Reason', value=reports[result]["body"])
                    await ctx.send(embed=embed)
            else:
                await ctx.send('No reports found with the user provided')
        else:
            # Looking up by ID as no users were mentioned
            report = reports.get(args, None)
            if report is not None:
                embed = Embed(title='Incident Report', description=f'Case Number: {report["report_id"]}', color=0xff0000)
                embed.add_field(name="Issued By:", value=report["issuer"])
                embed.add_field(name="Subject:", value=report["subject"])
                embed.add_field(name='Action', value=report["action"])
                embed.add_field(name='Reason', value=report["body"])
                await ctx.send(embed=embed)
            else:
                await ctx.send('No reports found with the ID number provided')
        if not ctx.message.mentions and args.endswith("--receipt"):
            # If user requests a copy of the report, DM it to them (only single reports can be sent via DM)
            await ctx.message.author.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def recall(self, ctx, report_id: str):
        """Clear a single report, you must have the ID number. If you need the report number, use b!lookup <user mention or ID> to find the number"""
        try:
            config = self.config_full[str(ctx.message.guild.id)]
            reports = config["reports"]
            reports.pop(report_id)
            json.dump(self.config_full, open('config.json', 'w'), indent=2, separators=(',', ': '))
            await ctx.send(f'Report #{report_id} successfully cleared!')
        except KeyError:
            await ctx.send('No report with that ID was found, double check the ID you entered')


def setup(bot):
    bot.add_cog(Punishment(bot))
