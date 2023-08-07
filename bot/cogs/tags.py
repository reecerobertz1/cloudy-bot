import discord
from discord.ext import commands
import datetime
from utils.subclasses import Context, CloudyBot
from asyncpg.exceptions import UniqueViolationError
from typing import TypedDict, Optional

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
                await conn.fetchrow(query, name, guild_id)
                response = await conn.fetchrow()
        return response

    @commands.group(invoke_without_command=True, aliases=['t'])
    async def tag(self, ctx: Context, name: str):
        """Sends a tag
        
        Parameters
        ----------
        name: str
            The name of the tag to send
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

    @tag.command()
    async def create(self, ctx: Context, name: str, *, response: str):
        """Create a tag
        
        Parameters
        ----------
        name: str
            Name for the tag you're creating
        response: str
            The message the tag will respond with
        """
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                query = '''INSERT INTO tags (name, content, owner_id, guild_id, created_at, uses) VALUES ($1, $2, $3, $4, $5, $6)'''
                try:
                    await conn.execute(query, name, response, ctx.author.id, ctx.guild.id, datetime.datetime.now().timestamp(), 0)
                    await ctx.reply(f'Succesfully created the tag `{name}`')
                except UniqueViolationError:
                    await ctx.reply('That tag already exists!')

    @tag.command()
    async def edit(self, ctx: Context, name: str, *, response: str):
        """Edit one of your tags
        
        Parameters
        ----------
        name: str
            The name of the tag to edit
        response: str
            The new message the tag will respond with
        """
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                query = '''SELECT owner_id FROM tags WHERE name = $1 AND guild_id = $2'''
                up_query = '''UPDATE tags SET content = $1 WHERE name = $2 AND guild_id = $3'''
                response = await conn.fetchrow(query, name, ctx.guild.id)
                if not response[0] == ctx.author.id:
                    await ctx.reply("You can't edit a tag you do not own!")
                else:
                    await conn.execute(up_query, response, name, ctx.guild.id)
                    await ctx.reply(f"Updated your tag `{name}`")

    @tag.command()
    async def info(self, ctx: Context, name: str):
        """Gets info on the specified tag
        
        Parameters
        ----------
        name: str
            Name of the tag you want information about
        """
        response = await self.get_tag(name, ctx.guild.id)
        if response != None:
            embed = discord.Embed(title=f"Tag information", color=0x303136)
            embed.add_field(name="Name", value=str(response['name']), inline=False)
            embed.add_field(name="Owner", value=f"<@!{response['owner_id']}>", inline=False)
            embed.add_field(name="Usage", value=response['uses'], inline=False)
            embed.add_field(name="Created at", value=f"<t:{int(response['created_at'])}:D>", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.reply("Tag not found!")

async def setup(bot: CloudyBot) -> None:
    await bot.add_cog(Tags(bot))