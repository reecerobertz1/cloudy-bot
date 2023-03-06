import discord
from discord.ext import commands, tasks
from discord.utils import get
import random
import asyncio
import os
from imgurpython import ImgurClient
import pytz
from setup.lists import *
from setup.config import *
import matplotlib.pyplot as plt
import seaborn as sns
import pandas
import os
import aiohttp
from utils.functions import gif_embed
import typing
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from colorthief import ColorThief
import datetime
from time import strftime, gmtime
import functools
from typing import Optional

imgur = ImgurClient(imgur_id, imgur_secret)

class Fun(commands.Cog, name="Fun", description="Includes commands you can use for fun!"):
    def __init__(self, bot):
        self.bot = bot

    def spotify_card(self, member: discord.Member, album: str):
        """Generate a Spotify Card for a member"""
        spotify = discord.utils.find(lambda a: isinstance(a, discord.Spotify), member.activities)
        ct = ColorThief(album)
        colors = ct.get_palette(4, 1)

        font = ImageFont.truetype("Karla-Bold.ttf", 60)
        font2 = ImageFont.truetype("Karla-Bold.ttf", 25)
        image = Image.new("RGBA", (1080, 400), colors[0])

        duration = spotify.duration.seconds
        duration1 = strftime("%M:%S", gmtime(spotify.duration.seconds))
        start = spotify.start
        current = datetime.datetime.now(datetime.timezone.utc)
        test = current - start
        time_left = duration - test.seconds
        time_along = duration - time_left
        duration2 = strftime("%M:%S", gmtime(time_along))
        full_time_percent = duration / 100
        left_of_current = time_along / full_time_percent

        if len(spotify.title) > 20:
            title = spotify.title[0:15] + "..." 
        else:
            title = spotify.title
        ImageDraw.Draw(image).text((20,30), f"{title}\n{spotify.artist}", colors[1], font=font)
        ImageDraw.Draw(image).line([(20, 200), (600, 200)], fill=colors[1], width=5)
        ImageDraw.Draw(image).text((20,220), f"{duration2}", colors[1], font=font2)
        ImageDraw.Draw(image).text((535,220), f"{duration1}", colors[1], font=font2)
        circle_1 = Image.open("./assets/new_circle.png").convert("RGBA")
        alpha = circle_1.getchannel('A')
        circle_3 = Image.new('RGBA', circle_1.size, color=colors[1])
        circle_3.putalpha(alpha) 
        circle = circle_3.resize((25, 25))
        ttt = left_of_current / 100 * 590
        image.paste(circle, (int(ttt), 188), circle)
        mask = Image.open("./assets/round-corners.png").convert("RGBA")
        mask = mask.resize((300, 300))
        mask_alpha = mask.getchannel('A')
        to_paste = Image.open(album)
        to_paste = to_paste.resize((300, 300))
        image.paste(to_paste, (700, 50), mask_alpha)
        buffer = BytesIO()
        image.save(buffer, "png")
        buffer.seek(0)
        return buffer

    @commands.command()
    async def spotify(self, ctx, member: Optional[discord.Member]):
        """Get a Spotify Card for the song currently playing"""
        async with ctx.typing():
            if not member:
                member = ctx.author
            spotify = discord.utils.find(lambda a: isinstance(a, discord.Spotify), member.activities)
            if not spotify:
                return await ctx.send("This user is not listening to Spotify")
            url = spotify.album_cover_url
            response = await self.bot.session.get(url)
            album = BytesIO(await response.read())
            album.seek(0)
            spotify_card = functools.partial(self.spotify_card, member, album)
            card = await self.bot.loop.run_in_executor(None, spotify_card)
            await ctx.send(file=discord.File(fp=card, filename="spotify.png"))

    @commands.command()
    async def hug(self, ctx, member: typing.Optional[discord.Member]):
        """Hug your friends or have Cloudy give you a hug"""
        author = ctx.message.author.mention
        if member == None:
            await ctx.send(f"Cloudy gave {author} a hug <:bearhug:800042518477013053>")
        else:
            embed = discord.Embed(description=f"{author} gave {member.mention} a hug!", color=0x9A5FF2)
            urls = ['https://cdn.discordapp.com/attachments/804482120671821865/814085524548878346/download_1.gif', "https://cdn.discordapp.com/attachments/804482120671821865/814083420194996224/download.gif", "https://cdn.discordapp.com/attachments/804482120671821865/814086607997108254/tenor.gif", "https://cdn.discordapp.com/attachments/804482120671821865/814087205039243274/tenor_1.gif", "https://cdn.discordapp.com/attachments/804482120671821865/814087528906620968/tenor_2.gif"]
            embed.set_image(url=(random.choice(urls)))
            await ctx.send(embed=embed)

    @commands.command()
    async def hbd(self, ctx, member: typing.Optional[discord.Member]):
        """Wish your friends a happy birthday or have Cloudy wish you a hbd"""
        author = ctx.message.author
        if member == None:
            await ctx.send(f"Cloudy wishes {author.mention} a happy birthday! <:cake:804020293416517672>")
        else:
            await ctx.send(f'Happy birthday {member.mention}! <:cake:804020293416517672>')
    
    @commands.command()
    async def kiss(self, ctx, member: typing.Optional[discord.Member]):
        """Kiss the homies good night or get a kiss from Cloudy"""
        author = ctx.message.author.mention
        kiss = self.bot.get_emoji(804022318992719922)
        if member == None:
            await ctx.reply(f"Cloudy kissed {author}! {kiss}")
        else:
            embed = discord.Embed(description=f"{author} kissed {member.mention} <3 i ship!")
            hugs = ['https://cdn.discordapp.com/attachments/804482120671821865/814095974611681280/37f9f27715e7dec6f2f4b7d63ad1af13.gif', 'https://cdn.discordapp.com/attachments/804482120671821865/814096796582019082/39fe167bdab90223bcc890bcb067b761.gif', 'https://cdn.discordapp.com/attachments/804482120671821865/814097411525836851/5f5afb51884af7c58e8d46c90261f990.gif', 'https://cdn.discordapp.com/attachments/804482120671821865/814097832494759936/tenor_1.gif', 'https://cdn.discordapp.com/attachments/804482120671821865/814098373228625970/tenor_2.gif']
            embed.set_image(url=(random.choice(hugs)))
            await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, member: typing.Optional[discord.Member]):
        """Slap your archnemesis...or make Cloudy slap you"""
        author = ctx.message.author.mention
        if member == None:
            await ctx.reply(f"Cloudy slapped {author}! sorry!!!!")
        else:
            embed = discord.Embed(description=f'{author} slapped {member.name}!', color=0x2a3387)
            embed.set_image(url='https://cdn.discordapp.com/attachments/804482120671821865/814100958463524884/nK.gif')
            await ctx.send(embed=embed)
    
    @commands.command()
    async def ship(self, ctx, *, ship:str):
        """Cloudy will tell you whether they love your favorite ship or not"""
        choices = ["I ship", "I don't ship"]
        message = await ctx.send("{} {}!" .format(random.choice(choices), ship))
        if "don't" in message.content:
            await message.add_reaction('💔')
        else:
            await message.add_reaction('💞')

    @commands.command()
    async def dm(self, ctx, member: typing.Optional[discord.Member], *, message: str):
        """Send a DM to someone via Cloudy, or get Cloudy to DM you"""
        try:
            if member == None:
                ctx.author.send(message)
            else:
                await member.send(f'{message}\n``sent from {ctx.author.display_name}``')
            message = ctx.message
            await message.add_reaction('💌')
        except discord.errors.Forbidden():
            await ctx.reply("I can't dm this user!")

    @commands.command()
    async def embed(self, ctx, *, message:str):
        """Cloudy sends your message, but in an embed"""
        colors = [0x99e9ff, 0xac58ed, 0xff7ab6, 0x7cf7a3, 0xf1ff94, 0x978aff]
        randomcolor = random.choice(colors) 
        embed = discord.Embed(title=f'{message}', colour=randomcolor)
        embed.set_footer(text=f'-{ctx.author}', icon_url=ctx.message.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def greet(self, ctx):
        """Greet Cloudy and Cloudy will greet you back"""
        await ctx.reply("Say hello!")

        def check(m):
            return m.content == "hello"

        msg = await self.bot.wait_for("message", check=check)
        await ctx.reply(f"Hello {msg.author}!")

    @commands.command()
    async def number(self, ctx):
        """Sends you a random number within your given range"""
        await ctx.reply('What do you want your lowest possible number to be?')
        number1 = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
        number1 = int(number1.content)
        await ctx.reply('OK, noted! What do you want the highest number to be?')
        number2 = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
        number2 = int(number2.content)
        await ctx.reply(random.randrange(number1, number2))

    @commands.command()
    async def choose(self, ctx, *choices: str):
        """Hard to choose what you want for dinner? Cloudy will make a choice for you!"""
        await ctx.reply(random.choice(choices))

    @commands.command(name='8ball', aliases=["8b", "b"])
    async def ball(self, ctx, *, question: str):
        """Tells you your faith or gives you advice, like all magic 8 balls do."""
        message = ctx.message
        options = ['It is certain.', 'It is decidedly so.', 'Without a doubt.', 'Yes, definitely.', 'You may rely on it.', 'As I see it, yes.', 'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.', "Don't count on it.", 'My reply is no.', 'My sources say no.', 'Outlook not so good.', 'Very doubtful.']
        async with ctx.typing():
            await asyncio.sleep(2)
        await message.add_reaction('🎱')
        await asyncio.sleep(0.7)
        await ctx.reply(f'**"{question}"**\n' + random.choice(options))

    @commands.command(name='imgur', pass_context=True)
    async def imgur(self, ctx, *text: str):
        """Will search Imgur and return an image"""
        rand = random.randint(0, 29)
        try:
            if text == ():
                await ctx.send('Remember to put what you want to search for!')
            elif text[0] != ():
                items = imgur.gallery_search(" ".join(text[0:len(text)]), advanced=None, sort='viral', window='all',page=0)
                await ctx.send(items[rand].link)

        except IndexError:
                await ctx.reply("Sorry, I couldn't find a photo of that on imgur!")
                
    
    @commands.group(invoke_without_command=True)
    async def gif(self, ctx, *, searchterm: typing.Optional[str]):

        """Searches for a GIF on Giphy"""

        try:

            if searchterm == None:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://api.giphy.com/v1/gifs/trending?api_key={giphy_api}&limit=25&rating=g") as api:
                        json = await api.json()
                        elements = json["data"]
                        results = elements[random.choice(range(0, 24))]
                        embed = await gif_embed(results, searchterm)
                        await ctx.send(embed=embed)
            # if there is a search term it fetches the api for the search term specified
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://api.giphy.com/v1/gifs/search?api_key={giphy_api}&q={searchterm}&limit=25&offset=0&rating=g&lang=en") as api:
                        json = await api.json()
                        elements = json["data"]
                        results = elements[random.choice(range(0, 24))]
                        embed = await gif_embed(results, searchterm)
                        await ctx.send(embed=embed)

        except IndexError:
            await ctx.reply("Sorry, I couldn't find enough GIFs. You can try `gif lite` or `gif mini` in order to fetch less GIFs with a bigger chance of finding a GIF!")

    @gif.command()
    async def lite(self, ctx, *, searchterm: str):

        """Searches for GIFs on Giphy while fetching less GIFs than the regular command"""

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.giphy.com/v1/gifs/search?api_key={giphy_api}&q={searchterm}&limit=25&offset=0&rating=g&lang=en") as api:
                json = await api.json()
                elements = json["data"]
                results = elements[random.choice(range(0, 12))]
                embed = await gif_embed(results, searchterm)
                await ctx.send(embed=embed)

    @gif.command()
    async def mini(self, ctx, *, searchterm: str):

        """Searches for GIFs on Giphy while fetching less GIFs than the regular and lite commands"""

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.giphy.com/v1/gifs/search?api_key={giphy_api}&q={searchterm}&limit=25&offset=0&rating=g&lang=en") as api:
                json = await api.json()
                elements = json["data"]
                results = elements[random.choice(range(0, 3))]
                embed = await gif_embed(results, searchterm)
                await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def clock(self, ctx, *, place):
        """Returns the current time in the specified place"""
        try:
            text = place.replace(" ", "_")
            country_time_zone = pytz.timezone(text)
            country_time = datetime.datetime.now(country_time_zone)
            place1, place2 = place.split("/")
            place = place2.title()
            embed = discord.Embed(title=f"Current date & time | {place1.title()}", description=(country_time.strftime(f"In {place} it is currently %I:%M %p (%B %d)")), color=discord.Colour.random())
            await ctx.reply(embed=embed)
        except pytz.UnknownTimeZoneError:
            await ctx.send("That timezone isn't formatted correctly/doesn't exist in the tz database. Make sure you use the following format: `Area/City`. To get a list of all the areas: `+clock areas`")

    @clock.command()
    async def areas(self, ctx):
        embed = discord.Embed(title="List of valid Areas", description="• Africa\n• America\n• Antarctica\n• Arctic\n• Asia\n• Atlantic\n• Australia\n• Europe\n• Indian\n• Pacific", color=discord.Colour.random())
        await ctx.send(embed=embed)

    @commands.command(help="Sends a cat photo")
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thecatapi.com/v1/images/search") as api:
                json = await api.json()
                elements = json[0]
                await ctx.send(elements["url"])

async def setup(bot):
    await bot.add_cog(Fun(bot))