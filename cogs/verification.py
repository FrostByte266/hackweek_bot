import aiohttp
import json
from random import choice, choices, randint, sample

from discord import File
from discord.ext import commands
from discord.utils import get


class Verification(commands.Cog):
    # Closer the number approaches 1, the more often the word list will be refreshed. Linear


    def __init__(self, bot):
        self.bot = bot
        self.config_full = json.loads(open('config.json').read())
        self.word_list_refresh_rate = 99
        self.word_cache_size = 1000

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def verification(self, ctx, state: bool):
        """Enable or disable the verification system"""
        config = self.config_full[str(ctx.message.guild.id)]
        if state is True and config["verification_channel"] is None:
            channel = await ctx.message.guild.create_text_channel(name="Verification")
            role = await ctx.message.guild.create_role(name="Unverified")
            config.update(verification_channel=channel.id, verification_role=role.id)
            json.dump(self.config_full, open('config.json', 'w'), indent=2, separators=(',', ': '))
        elif state is False and config["verification_channel"] is not None:
            channel = get(ctx.message.guild.text_channels, id=config["verification_channel"])
            role = get(ctx.message.guild.roles, id=config["verification_role"])
            await channel.delete()
            await role.delete()
            config.update(verification_channel=None, verification_role=None)
            json.dump(self.config_full, open('config.json', 'w'), indent=2, separators=(',', ': '))

    @commands.command()
    async def verify(self, ctx):
        """Verify yourself (the bot will DM you)"""
        try:
            # Increment if use count exists
            self.verify.use_count += 1
        except AttributeError:
            # Otherwise initialize it on verify function object for persistence
            self.verify.use_count = 1
        
        if self.verify.use_count%self.word_list_refresh_rate == 1:
            # Retrieve list of words from MIT page
            async with aiohttp.ClientSession() as client:
                async with client.get("https://www.mit.edu/~ecprice/wordlist.10000") as response:
                    text = await response.text()
                    self.verify.words = sample(text.splitlines(), self.word_cache_size)
                await client.close()

        challenge_selection = randint(0, 2)
        challenge_wording = ['computation', 'phrase', 'single word basic color displayed on the pillow']

        # Some initialization
        random_phrase = '( Pillows are so comfy 😊)'
        image_selection = ['', None]
        answer_value = 0

        # Image color challenge
        if challenge_selection == 2:
            image_answer_pairing = [['blue', './assets/blue.jpg'],
                                    ['red', './assets/red.jpg'],
                                    ['white', './assets/white.jpg'],
                                    ['black', './assets/black.jpg']]
            image_selection = image_answer_pairing[randint(0, 3)]
        # Math challenge
        elif challenge_selection == 1:
            random_phrase = f'{randint(1,9)}{choice(["+","-","*"])}{randint(1,9)}{choice(["+","-","*"])}{randint(1,9)}'
            answer_value = str(eval(random_phrase))
        # Phrase challenge
        else:
            # Pick three random words and DM them to the user
            random_phrase = ' '.join(choices(self.verify.words, k=3))

        insertion_point = randint(1, len(random_phrase)-2)
        random_phrase_modded = f'{random_phrase[:insertion_point+1]}​{random_phrase[insertion_point+1:]}'.replace('o', 'ο').replace('e', 'е').replace('a', 'а').replace('i', 'і')

        expected_answer = [random_phrase, answer_value, image_selection[0]][challenge_selection]
        await ctx.message.author.send(f"Please reply with the following {challenge_wording[challenge_selection]}: {random_phrase_modded}", file=File(image_selection[1]) if challenge_selection == 2 else None)
        # Wait for 30 seconds for the user to send back the verification phrase
        await self.bot.wait_for("message", timeout=30, check=lambda message: message.content == expected_answer)
        await ctx.message.author.send("Verification complete 👍")
        # If they pass, remove the unverified role
        config = json.loads(open('config.json', 'r').read())
        role = get(ctx.guild.roles, id=config[str(ctx.guild.id)]["verification_role"])
        await ctx.message.author.remove_roles(role)

    @verify.error
    async def verify_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.message.author.send(f"Command timeout! Please rerun the command to verify. {error}")


def setup(bot):
    bot.add_cog(Verification(bot))
