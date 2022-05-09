import discord
from discord.ext import commands, tasks
from discord.utils import get
import random
import asyncio
import os
from imgurpython import ImgurClient
import giphy_client
from giphy_client.rest import ApiException
from datetime import datetime
import pytz
from utils.lists import *
import matplotlib.pyplot as plt
import seaborn as sns
import os
from setup.config import *
from utils.functions import gif_embed
import aiohttp


# accessing from setup.config
imgur = ImgurClient(imgur_id, imgur_secret)

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hug(self, ctx, user:str=None):
        author = ctx.message.author.mention
        embed = discord.Embed(description=f"{author} gave {user} a hug!", color=0x9A5FF2)
        urls = ['https://cdn.discordapp.com/attachments/804482120671821865/814085524548878346/download_1.gif', "https://cdn.discordapp.com/attachments/804482120671821865/814083420194996224/download.gif", "https://cdn.discordapp.com/attachments/804482120671821865/814086607997108254/tenor.gif", "https://cdn.discordapp.com/attachments/804482120671821865/814087205039243274/tenor_1.gif", "https://cdn.discordapp.com/attachments/804482120671821865/814087528906620968/tenor_2.gif"]
        embed.set_image(url=(random.choice(urls)))
        if user == None:
            await ctx.reply(f"Cloudy gave {author} a hug <:bearhug:800042518477013053>")
        else:
            await ctx.send(embed=embed)

    @commands.command()
    async def hbd(self, ctx, user:str=None):
        author = ctx.message.author.mention
        if user == None:
            await ctx.reply(f"Cloudy wishes {author} a happy birthday! <:cake:804020293416517672>")
        else:
            await ctx.send(f'Happy birthday {user}! <:cake:804020293416517672>')
    
    @commands.command()
    async def kiss(self, ctx, user:str=None):
        author = ctx.message.author.mention
        kiss = self.client.get_emoji(804022318992719922)
        embed = discord.Embed(description=f"{author} kissed {user} <3 i ship!")
        hugs = ['https://cdn.discordapp.com/attachments/804482120671821865/814095974611681280/37f9f27715e7dec6f2f4b7d63ad1af13.gif', 'https://cdn.discordapp.com/attachments/804482120671821865/814096796582019082/39fe167bdab90223bcc890bcb067b761.gif', 'https://cdn.discordapp.com/attachments/804482120671821865/814097411525836851/5f5afb51884af7c58e8d46c90261f990.gif', 'https://cdn.discordapp.com/attachments/804482120671821865/814097832494759936/tenor_1.gif', 'https://cdn.discordapp.com/attachments/804482120671821865/814098373228625970/tenor_2.gif']
        embed.set_image(url=(random.choice(hugs)))
        if user == None:
            await ctx.reply(f"Cloudy kissed {author}! {kiss}")
        else:
            await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, user:str=None):
        author = ctx.message.author.mention
        embed = discord.Embed(description=f'{author} slapped {user}!', color=0x2a3387)
        embed.set_image(url='https://cdn.discordapp.com/attachments/804482120671821865/814100958463524884/nK.gif')
        if user == None:
            await ctx.reply(f"Cloudy slapped {author}! sorry!!!!")
        else:
            await ctx.send(embed=embed)
    
    @commands.command()
    async def ship(self, ctx, *, user:str=None):
        choices = ["I ship", "I don't ship"]
        if user == None:
            await ctx.reply("There's nobody to ship!")
        else:
            message = await ctx.send("{} {}!" .format(random.choice(choices), user))
            if "don't" in message.content:
                await message.add_reaction('💔')
            else:
                await message.add_reaction('💞')

    @commands.command()
    async def dm(self, ctx, user: discord.User, *, value):
        message = ctx.message
        await user.send(f'{value}\n``sent from {ctx.author.display_name}``')
        await message.add_reaction('💌')

    @commands.command()
    async def dm_me(self, ctx, *, message:str):
        await ctx.author.send(message)

    @commands.command()
    async def embed(self, ctx, *, message:str):
        colors = [0x99e9ff, 0xac58ed, 0xff7ab6, 0x7cf7a3, 0xf1ff94, 0x978aff]
        randomcolor = random.choice(colors) 
        embed = discord.Embed(title=f'{message}', colour=randomcolor)
        embed.set_footer(text=f'-{ctx.author}', icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def embed2(self, ctx, *, message:str):
        colors = [0x99e9ff, 0xac58ed, 0xff7ab6, 0x7cf7a3, 0xf1ff94, 0x978aff]
        randomcolor = random.choice(colors) 
        embed = discord.Embed(colour=randomcolor, description=f'{message}')
        await ctx.send(embed=embed)

    @commands.command()
    async def greet(self, ctx):
        await ctx.reply("Say hello!")

        def check(m):
            return m.content == "hello"

        msg = await self.client.wait_for("message", check=check)
        await ctx.reply(f"Hello {msg.author}!")

    @commands.command()
    async def createembed(self, ctx):
        await ctx.message.delete()
        first = await ctx.send("What title do you want your embed to have?")

        title1 = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
        title = title1.content
        await title1.delete()
        await first.delete()
        second = await ctx.send('Okay! What do you want your description to be?')

        desc1 = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
        desc = desc1.content
        await desc1.delete()
        await second.delete()

        col = await ctx.send('What color do you want your embed to be? (in hex; eg., 303136)')
        color = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
        await col.delete()
        await color.delete()

        third = await ctx.send('Are you finished with your embed? Say ``yes`` if you are and ``no`` if you arent!')
        answer1 = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
        if 'yes' in answer1.content:
            await answer1.delete()
            await third.delete()
            embed0 = discord.Embed(title=f'{title}', description=f'{desc}', colour=int(color.content, 16))
            await ctx.send(embed=embed0)
        else:
            four = await ctx.send('OK! What do you want the name of the first field to be!')

            name0 = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
            name1 = name0.content
            await name0.delete()
            await four.delete()
            five = await ctx.send('Cool! What do you want your value to be?')

            value0 = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
            value1 = value0.content
            await value0.delete()
            await five.delete()
            embed = discord.Embed(title=f'{title}', description=f'{desc}', colour=0x60e5fc)
            embed.add_field(name=f'{name1}', value=f'{value1}')
            await ctx.send(embed=embed)

    @commands.command()
    async def number(self, ctx):
        await ctx.reply('What do you want your lowest possible number to be?')
        number1 = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
        number1 = int(number1.content)
        await ctx.reply('OK, noted! What do you want the highest number to be?')
        number2 = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
        number2 = int(number2.content)
        await ctx.reply(random.randrange(number1, number2))

    @commands.command()
    async def choose(self, ctx, *choices: commands.clean_content(fix_channel_mentions=False)):
        choice = list(choices)
        lst = ' '.join(choice)
        choose1 = lst.split()
        await ctx.reply(random.choice(choose1))

    @commands.command(name='8ball')
    async def ball(self, ctx):
        message = ctx.message
        options = ['It is certain.', 'It is decidedly so.', 'Without a doubt.', 'Yes, definitely.', 'You may rely on it.', 'As I see it, yes.', 'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.', "Don't count on it.", 'My reply is no.', 'My sources say no.', 'Outlook not so good.', 'Very doubtful.']
        async with ctx.typing():
            await asyncio.sleep(2)
        await message.add_reaction('🎱')
        await asyncio.sleep(0.7)
        await ctx.reply(random.choice(options))

    @commands.command(aliases = ['image', 'images'])
    async def photo2(self, ctx, arg = None):
        if arg == 'halsey':
            image = os.listdir('./photos/halseyphotos/')
            imgString = random.choice(image)
            path = "./photos/halseyphotos/" + imgString
            await ctx.send(file=discord.File(path))
        if arg == 'valkyrae':
            image = os.listdir('./photos/valkyrae/')
            imgString = random.choice(image)
            path = "./photos/valkyrae/" + imgString
            await ctx.send(file=discord.File(path))
        if arg == 'raven':
            image = os.listdir('./photos/raven/')
            imgString = random.choice(image)
            path = "./photos/raven/" + imgString
            await ctx.send(file=discord.File(path))
        if arg == 'jennie':
            image = os.listdir('./photos/jennie/')
            imgString = random.choice(image)
            path = "./photos/jennie/" + imgString
            await ctx.send(file=discord.File(path))            
        if arg == 'kiara':
            image = os.listdir('./photos/keeahwah/')
            imgString = random.choice(image)
            path = "./photos/keeahwah/" + imgString
            await ctx.send(file=discord.File(path))
        if arg == 'nai':
            image = os.listdir('./photos/nai/')
            imgString = random.choice(image)
            path = "./photos/nai/" + imgString
            await ctx.send(file=discord.File(path))
        if arg == 'camila':
            image = os.listdir('./photos/camila/')
            imgString = random.choice(image)
            path = "./photos/camila/" + imgString
            await ctx.send(file=discord.File(path)) 
        if arg == 'lauren':
            image = os.listdir('./photos/lauren/')
            imgString = random.choice(image)
            path = "./photos/lauren/" + imgString
            await ctx.send(file=discord.File(path)) 
        if arg == 'halren':
            image = os.listdir('./photos/halren/')
            imgString = random.choice(image)
            path = "./photos/halren/" + imgString
            await ctx.send(file=discord.File(path))             
        if arg == None:
            await ctx.send('Hey! Want a photo of someone? You have to specifiy who, by doing `+photo <person>`! For a list of people the command works with do `+photo help`')
        if arg == 'help':
            embed = discord.Embed(
                title='Photos',
                description='**Current celebs the photo command works with:**\n• Nailea Devora (Nai)\n• Jennie Kim (Jennie)\n• Raven | inyourdre4mz (Raven)\n• Kiara | keeahwah (Kiara)\n• Rachel Hofstetter | Valkyrae (Valkyrae)\n• Lauren Jauregui (Lauren)\n• Camila Cabello (Camila)\n• Ashley Frangipane | Halsey (Halsey)\n• Halsey & Lauren Jauregui (Halren)',
                color=0xd7ff9e
            )
            await ctx.send(embed=embed)

    @commands.command(name='imgur', pass_context=True)
    async def imgur(self, ctx, *text: str):
        """Allows the user to search for an image from imgur"""
        rand = random.randint(0, 29)
        try:
            if text == ():
                await ctx.send('Remember to put what you want to search for!')
            elif text[0] != ():
                items = imgur.gallery_search(" ".join(text[0:len(text)]), advanced=None, sort='viral', window='all',page=0)
                await ctx.send(items[rand].link)

        except IndexError:
                await ctx.reply("Sorry, I couldn't find a photo of that on imgur!")
    
    @commands.command()
    async def gif(self, ctx, searchterm=None):

        giphyApi=""

        if searchterm == None:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.giphy.com/v1/gifs/trending?api_key={giphyApi}&limit=25&rating=g") as api:
                    json = await api.json()
                    elements = json["data"]
                    results = elements[random.choice(range(0, 24))]
                    embed = await gif_embed(results, searchterm)
                    await ctx.send(embed=embed)
        # if there is a search term it fetches the api for the search term specified
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.giphy.com/v1/gifs/search?api_key={giphyApi}&q={searchterm}&limit=25&offset=0&rating=g&lang=en") as api:
                    json = await api.json()
                    elements = json["data"]
                    results = elements[random.choice(range(0, 24))]
                    embed = await gif_embed(results, searchterm)
                    await ctx.send(embed=embed)

    @commands.command()
    async def clock(self, ctx, *, place):
        text = place.replace(" ", "_")
        country_time_zone = pytz.timezone(text)
        country_time = datetime.now(country_time_zone)
        place1, place2 = place.split("/")
        place = place2.title()
        embed = discord.Embed(title=f"Current date & time | {place1.title()}", description=(country_time.strftime(f"In {place} it is currently %I:%M %p (%B %d)")), color=discord.Colour.random())
        await ctx.reply(embed=embed)


    @commands.command()
    async def color(ctx, args):
        ranpal = random.choice(palettes)
        palette = sns.color_palette(ranpal, int(args))
        pal = sns.palplot(palette)
        plt.savefig("palette.png")
        file=discord.File("palette.png")
        embed = discord.Embed(title="color palette",color=0x303136)
        embed.set_image(url="attachment://palette.png")
        await ctx.send(file=file, embed=embed)
        palfile = "palette.png"
        os.remove(palfile)
        return

    @commands.command(help="sends a cat photo")
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thecatapi.com/v1/images/search") as api:
                json = await api.json()
                elements = json[0]
                await ctx.send(elements["url"])

def setup(client):
    client.add_cog(Fun(client))
