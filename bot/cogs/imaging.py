import discord
from discord.ext import commands
from utils.subclasses import CloudyBot, Context
from typing import Optional, Literal
from io import BytesIO
from PIL import Image
import functools

class Imaging(commands.Cog):

    """Image related commands"""

    def __init__(self, bot: CloudyBot) -> None:
        self.bot = bot

    def prideify(self, avatar: BytesIO, option: Literal['rainbow', 'lesbian', 'gay', 'bi', 'trans', 'ace', 'pan']) -> discord.File:
        avatar.seek(0)
        pil_img = Image.open(avatar)
        pil_image = pil_img.convert('RGB')
        img = Image.open(f'./assets/{option}.png').convert('RGB').resize((256, 256))
        im3 = Image.blend(pil_image, img, 0.65)
        rb = BytesIO()
        im3.save(rb, 'png')
        rb.seek(0)
        return discord.File(rb, 'avatar.png')
    
    def put_in_jail(self, avatar: BytesIO) -> discord.File:
        avatar.seek(0)
        avatar_base = Image.open(avatar)
        avatar_image = avatar_base.convert('RGBA')
        jail_image = Image.open('./assets/cell.png').convert('RGBA').resize((256, 256))
        avatar_image.paste(jail_image, (0, 0), jail_image)
        fp = BytesIO()
        avatar_image.save(fp, 'png')
        fp.seek(0)
        return discord.File(fp, 'jail.png')
    
    @commands.command(aliases=['prison'])
    async def jail(self, ctx: Context, member: Optional[discord.Member]):
        """Put someone in jail
        
        Parameters
        ----------
        member: str, optional
            member to put in jail
        """
        member = ctx.author if not member else member
        avatar = BytesIO(await member.display_avatar.with_size(256).read())
        jail_func = functools.partial(self.put_in_jail, avatar)
        jailed = await self.bot.loop.run_in_executor(None, jail_func)
        await ctx.send(file=jailed)

    @commands.group(aliases=['rainbow'], invoke_without_command=True)
    async def pride(self, ctx: Context, member: Optional[discord.Member]):
        """Adds pride overlay to an avatar
        
        Parameters
        ----------
        member: str, optional
            member to take avatar from
        """
        if not member:
            member = ctx.author
        avatar = BytesIO(await member.display_avatar.with_size(256).read())
        make_a_rainbow = functools.partial(self.prideify, avatar, 'rainbow')
        pride = await self.bot.loop.run_in_executor(None, make_a_rainbow)
        await ctx.send(f"#pride", file=pride)

    @pride.command()
    async def lesbian(self, ctx: Context, member: Optional[discord.Member]):
        """Adds lesbian flag overlay to an avatar
        
        Parameters
        ----------
        member: str, optional
            member to take avatar from
        """
        member = ctx.author if not member else member
        avatar = BytesIO(await member.display_avatar.with_size(256).read())
        make_a_rainbow = functools.partial(self.prideify, avatar, 'lesbian')
        pride = await self.bot.loop.run_in_executor(None, make_a_rainbow)
        await ctx.send(f"#pride", file=pride)

    @pride.command()
    async def gay(self, ctx: Context, member: Optional[discord.Member]):
        """Adds gay flag overlay to an avatar
        
        Parameters
        ----------
        member: str, optional
            member to take avatar from
        """
        member = ctx.author if not member else member
        avatar = BytesIO(await member.display_avatar.with_size(256).read())
        make_a_rainbow = functools.partial(self.prideify, avatar, 'gay')
        pride = await self.bot.loop.run_in_executor(None, make_a_rainbow)
        await ctx.send(f"#pride", file=pride)

    @pride.command(aliases=['bisexual'])
    async def bi(self, ctx: Context, member: Optional[discord.Member]):
        """Adds bisexual flag overlay to an avatar
        
        Parameters
        ----------
        member: str, optional
            member to take avatar from
        """
        member = ctx.author if not member else member
        avatar = BytesIO(await member.display_avatar.with_size(256).read())
        make_a_rainbow = functools.partial(self.prideify, avatar, 'bi')
        pride = await self.bot.loop.run_in_executor(None, make_a_rainbow)
        await ctx.send(f"#pride", file=pride)

    @pride.command(aliases=['transgender'])
    async def trans(self, ctx: Context, member: Optional[discord.Member]):
        """Adds trans flag overlay to an avatar
        
        Parameters
        ----------
        member: str, optional
            member to take avatar from
        """
        member = ctx.author if not member else member
        avatar = BytesIO(await member.display_avatar.with_size(256).read())
        make_a_rainbow = functools.partial(self.prideify, avatar, 'trans')
        pride = await self.bot.loop.run_in_executor(None, make_a_rainbow)
        await ctx.send(f"#pride", file=pride)

    @pride.command(aliases=['pansexual'])
    async def pan(self, ctx: Context, member: Optional[discord.Member]):
        """Adds pansexual flag overlay to an avatar
        
        Parameters
        ----------
        member: str, optional
            member to take avatar from
        """
        member = ctx.author if not member else member
        avatar = BytesIO(await member.display_avatar.with_size(256).read())
        make_a_rainbow = functools.partial(self.prideify, avatar, 'pan')
        pride = await self.bot.loop.run_in_executor(None, make_a_rainbow)
        await ctx.send(f"#pride", file=pride)

    @pride.command(aliases=['asexual'])
    async def ace(self, ctx: Context, member: Optional[discord.Member]):
        """Adds asexual flag overlay to an avatar
        
        Parameters
        ----------
        member: str, optional
            member to take avatar from
        """
        member = ctx.author if not member else member
        avatar = BytesIO(await member.display_avatar.with_size(256).read())
        make_a_rainbow = functools.partial(self.prideify, avatar, 'ace')
        pride = await self.bot.loop.run_in_executor(None, make_a_rainbow)
        await ctx.send(f"#pride", file=pride)

async def setup(bot: CloudyBot):
    await bot.add_cog(Imaging(bot))