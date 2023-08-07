"""
MIT License

Copyright (c) 2021-present rqinflow

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import discord
from discord.ext import commands
import datetime
from utils.subclasses import Context, CloudyBot
from asyncpg.exceptions import UniqueViolationError
from typing import TypedDict, Optional, Annotated

class TagEntry(TypedDict):
    id: int
    name: str
    content: str
    owner_id: int
    guild_id: int
    uses: int
    created_at: datetime.datetime

class Tags(commands.Cog):
    def __init__(self, bot: CloudyBot) -> None:
        self.bot = bot

    async def get_tag(self, name: str, guild_id: int) -> Optional[TagEntry]:
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                query = '''SELECT * FROM tags WHERE name = $1 AND guild_id = $2'''
                response = await conn.fetchrow(query, name, guild_id)
        return response

    @commands.group(invoke_without_command=True, aliases=['t'])
    async def tag(self, ctx: Context, name: Annotated[str, commands.clean_content]):
        """sends a tag
        
        Parameters
        ----------
        name: str
            name of the tag to send
        """
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                query = '''SELECT content, uses FROM tags WHERE name = $1 AND guild_id = $2'''
                up_query = '''UPDATE tags SET uses = $1 WHERE name = $2 AND guild_id = $3'''
                response = await conn.fetchrow(query, name, ctx.guild.id)
                if response != None:
                    if ctx.message.reference is not None:
                        msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                        await msg.reply(response['content'])
                    else:
                        await ctx.send(response['content'])
                    await conn.execute(up_query, int(response['uses'])+1, name, ctx.guild.id)
                else:
                    await ctx.send("Couldn't find the tag")

    @tag.command(extras={"examples": ["tag create example this is an example", "tag create 'with spaces' use quotation marks to make tag names with spaces in them"]})
    async def create(self, ctx: Context, name: Annotated[str, commands.clean_content], *, response: Annotated[str, commands.clean_content]):
        """create a tag
        
        Parameters
        ----------
        name: str
            name for the tag you're creating
        response: str
            the message the tag will respond with
        """
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                query = '''INSERT INTO tags (name, content, owner_id, guild_id, created_at, uses) VALUES ($1, $2, $3, $4, $5, $6)'''
                try:
                    await conn.execute(query, name, response, ctx.author.id, ctx.guild.id, discord.utils.utcnow(), 0)
                    await ctx.reply(f'Succesfully created the tag `{name}`')
                except UniqueViolationError:
                    await ctx.reply('That tag already exists!')

    @tag.command(extras={"examples": ["tag edit example this is my example tag on how to edit a tag named example"]})
    async def edit(self, ctx: Context, name: Annotated[str, commands.clean_content], *, response: Annotated[str, commands.clean_content]):
        """edit one of your tags
        
        Parameters
        ----------
        name: str
            the name of the tag to edit
        response: str
            the new message the tag will respond with
        """
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                query = '''SELECT owner_id FROM tags WHERE name = $1 AND guild_id = $2'''
                up_query = '''UPDATE tags SET content = $1 WHERE name = $2 AND guild_id = $3'''
                resp = await conn.fetchrow(query, name, ctx.guild.id)
                if not resp[0] == ctx.author.id:
                    await ctx.reply("You can't edit a tag you do not own!")
                else:
                    await conn.execute(up_query, response, name, ctx.guild.id)
                    await ctx.reply(f"Updated your tag `{name}`")

    @tag.command(extras={"examples": ["tag info sometagname"]})
    async def info(self, ctx: Context, name: str):
        """get some info on a tag
        
        Parameters
        ----------
        name: str
            name of the tag you want information about
        """
        response = await self.get_tag(name, ctx.guild.id)
        if response != None:
            embed = discord.Embed(title=f"Tag information")
            embed.add_field(name="Name", value=str(response['name']), inline=False)
            embed.add_field(name="Owner", value=f"<@!{response['owner_id']}>", inline=False)
            embed.add_field(name="Usage", value=response['uses'], inline=False)
            embed.add_field(name="Created at", value=f"{discord.utils.format_dt(response['created_at'], 'D')}", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.reply("Tag not found!")

async def setup(bot: CloudyBot) -> None:
    await bot.add_cog(Tags(bot))