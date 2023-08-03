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
from discord.ext import commands, tasks
from utils.subclasses import CloudyBot, Context
import asyncpg
from typing import Optional
import re

class Starboard(commands.Cog):
    def __init__(self, bot: CloudyBot) -> None:
        self.bot: CloudyBot = bot
        self._message_cache: dict[int, discord.Message] = {}
        self.spoiler_regex = re.compile(r'\|\|(.+?)\|\|')
        self.starboard_channel_id = 1090249213188784138
        self.chroma_guild_id = 694010548605550675

    def private_only():
        def predicate(ctx):
            if ctx.guild.id == 694010548605550675:
                return True
            else:
                return False
        return commands.check(predicate)

    def find_spoiler_urls(self, text: str, url: str) -> bool:
        spoilers = self.spoiler_regex.findall(text)
        spoiler_url = []
        for spoiler in spoilers:
            if url in spoiler:
                spoiler_url.append(spoiler)
        if len(spoiler_url) != 0:
            return True
        else:
            return False
    
    def starboard_embed(self, message: discord.Message, author: discord.Member):
        # creates an embed to send in starboard channel / star view command
        embed = discord.Embed(
            description=message.content,
            color=0x2B2D31
        )
        embed.set_author(
            name=author.name,
            icon_url=author.display_avatar.url
        )
        embed.add_field(
            name="Original message",
            value=f"[Jump!]({message.jump_url})",
            inline=False
        )
        if message.reference is not None:
            if message.reference.resolved:
                embed.add_field(
                    name="Replying to",
                    value=f"[{message.reference.resolved.author}]({message.reference.resolved.jump_url})",
                    inline=False
                )
        if message.embeds:
            data = message.embeds[0]
            spoiler_bool = self.find_spoilers(message.content, data.url)
            if data.url and spoiler_bool is False and data.type == "image":
                embed.set_image(url=data.url)
        if message.attachments:
            attachment = message.attachments[0]
            if attachment.url.upper().endswith(("PNG", "GIF", "JPG", "JPEG", "WEBP")) and not attachment.is_spoiler():
                embed.set_image(url=attachment.url)
            elif attachment.is_spoiler():
                embed.add_field(
                    name="Attachment",
                    value=f"||[{attachment.filename}]({attachment.url})||",
                    inline=False
                )
            else:
                embed.add_field(
                    name="Attachment",
                    value=f"[{attachment.filename}]({attachment.url})",
                    inline=False
                )
        embed.set_footer(text=f"ID: {message.id}")
        embed.timestamp = message.created_at
        return embed
    
    async def get_star_entry(self, message_id: str) -> asyncpg.Record:
        # this just gets a star entry from message_id
        query = "SELECT * FROM stars WHERE message_id = $1"
        async with self.bot.pool.acquire() as connection:
            row = await connection.fetchrow(query, message_id)
        return row
    
    async def get_recieved_stars(self, member: discord.Member):
        query = "SELECT COUNT(*) FROM stars WHERE author_id = $1"
        async with self.bot.pool.acquire() as connection:
            row = await connection.fetchrow(query, member.id)
        return row['count']
    
    async def get_given_stars(self, member: discord.Member):
        query = "SELECT COUNT(DISTINCT entry_id) FROM starrers WHERE author_id = $1"
        async with self.bot.pool.acquire() as connection:
            row = await connection.fetchrow(query, member.id)
        return row['count']

    async def get_messages_on_starboard(self, member: discord.Member):
        query = "SELECT COUNT(*) FROM stars WHERE star_embed_message_id IS NOT NULL AND author_id = $1"
        async with self.bot.pool.acquire() as connection:
            row = await connection.fetchrow(query, member.id)
        return row['count']

    async def get_message(self, channel: discord.abc.Messageable, message_id: int) -> Optional[discord.Message]:
        # gets message from cache or fetches it
        try:
            return self._message_cache[message_id]
        except KeyError:
            try:
                msg = await channel.fetch_message(message_id)
            except discord.HTTPException:
                return None
            else:
                self._message_cache[message_id] = msg
                return msg 

    async def handle_star(self, payload: discord.RawReactionActionEvent):
        # this function handles when a message is starred
        if str(payload.emoji) != "⭐": # if it's not a star reaction we can ignore
            return
        
        # if this isn't in the chroma server we don't want to act on it either
        if payload.guild_id != self.chroma_guild_id:
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        
        channel = guild.get_channel_or_thread(payload.channel_id)
        if not isinstance(channel, (discord.Thread, discord.TextChannel)):
            return # wasn't sent in a thread or text channel
        
        message = await self.get_message(channel, payload.message_id)
        if not message:
            return # message wasn't found
        
        if message.author.bot is True:
            return # we don't want bot messages to get sent in the starboard
        
        # gets the member that reacted
        # this is needed for the starrers table
        reacter = await self.fetch_or_get_member(guild, payload.user_id) 
        
        row = await self.get_star_entry(message_id=payload.message_id)
        if row is None: # message has not been starred before
            async with self.bot.pool.acquire() as connection:
                query = """
                    WITH inserting AS (
                        INSERT INTO stars (message_id, channel_id, author_id)
                        VALUES ($1, $2, $3)
                        RETURNING id
                    )
                    INSERT INTO starrers (author_id, entry_id)
                    SELECT $4, (
                        SELECT id FROM inserting
                        UNION ALL
                        SELECT id FROM stars WHERE message_id=$1
                        LIMIT 1
                    )
                """
                await connection.execute(query, message.id, channel.id, message.author.id, reacter.id)
        else: # message has been starred before
            async with self.bot.pool.acquire() as connection:
                query = "INSERT INTO starrers (author_id, entry_id) VALUES ($1, $2)"
                await connection.execute(query, reacter.id, row["id"])

                query2 = "SELECT COUNT(*) AS count FROM starrers WHERE entry_id = $1"
                reactions = await connection.fetchval(query2, row["id"])
            if reactions >= 3:
                starboard_channel = guild.get_channel(self.starboard_channel_id)
                try: # embed message already exists, let's update the reaction count
                    embed_message_id = row["star_embed_message_id"]
                    embed_msg = await self.get_message(starboard_channel, embed_message_id)
                    await embed_msg.edit(content=f"⭐ **{reactions}** <#{channel.id}>")
                except: # embed message has not been sent yet (just reached reaction requirement)
                    embed = self.starboard_embed(message, message.author)
                    msg = await starboard_channel.send(content=f"⭐ **{reactions}** <#{channel.id}>", embed=embed)
                    async with self.bot.pool.acquire() as connection:
                        query = "UPDATE stars SET star_embed_message_id = $1 WHERE id = $2"
                        await connection.execute(query, msg.id, row["id"])
            else: # reactions are less than 3, no embed message action needed
                pass

    async def handle_unstar(self, payload: discord.RawReactionActionEvent):
        if str(payload.emoji) != "⭐":
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        
        channel = guild.get_channel_or_thread(payload.channel_id)
        if not isinstance(channel, (discord.Thread, discord.TextChannel)):
            return
        
        message = await self.get_message(channel, payload.message_id)
        if not message:
            return
        
        reacter = await self.fetch_or_get_member(guild, payload.user_id) 
        
        row = await self.get_star_entry(message_id=payload.message_id)
        if row is None:
            print("This message was starred before starboard system got implemented.")
        else:
            query = """
                    SELECT COUNT(*) AS count
                    FROM starrers 
                    WHERE entry_id = ($1);
                """
            async with self.bot.pool.acquire() as connection:
                reactions = await connection.fetchval(query, row["id"])
            reactions -= 1 # we are about to remove a starrer so we need to get reactions - 1
            if reactions < 3:
                try: # embed message exists, but reactions are now less than 3 so let's delete the message.
                    starboard_channel = guild.get_channel(self.starboard_channel_id)
                    embed_message_id = row["star_embed_message_id"]
                    embed_msg = await self.get_message(starboard_channel, embed_message_id)
                    await embed_msg.delete()
                except: # doesn't exist, star remove doesn't affect anything on the discord side of things
                    pass
            # deleting the author as a starrer if they were a starrer
            # otherwise nothing will happen
            async with self.bot.pool.acquire() as connection:
                query = "DELETE FROM starrers WHERE entry_id = $1 AND author_id = $2"
                await connection.execute(query, row["id"], reacter.id)
    
    async def fetch_or_get_member(self, guild: discord.Guild, member_id: int) -> Optional[discord.Member]:
        member = guild.get_member(member_id)
        if not member:
            try:
                member = await guild.fetch_member(member_id)
            except discord.HTTPException:
                return None
        return member

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent) -> None:
        await self.handle_star(payload=payload)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent) -> None:
        await self.handle_unstar(payload=payload)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: discord.RawMessageDeleteEvent) -> None:
        # this checks if a starboard message was deleted
        # if that is the case it'll delete the entry
        if not payload.guild_id == self.chroma_guild_id:
            return
        message = await self.get_star_entry(payload.message_id)
        if message:
            async with self.bot.pool.acquire() as connection:
                query = "DELETE FROM stars WHERE star_embed_message_id = $1;"
                await connection.execute(query, message["star_embed_message_id"])

    @commands.group()
    @private_only()
    async def star(self, ctx: Context):
        pass
    
    @star.command()
    @private_only()
    async def stats(self, ctx: Context, member: Optional[discord.Member]):
        """Gets a member's starboard stats
        
        Parameters
        ----------
        member: discord.Member
            member to get stats for
        """
        member = member if member else ctx.author
        total_stars_recieved = await self.get_recieved_stars(member)
        total_stars_given = await self.get_given_stars(member)
        messages_on_sb = await self.get_messages_on_starboard(member)
        embed = discord.Embed(title=f"Starboard stats | {member.display_name}", description=f"* **Stars recieved:** {total_stars_recieved if total_stars_recieved != 0 else 'None just yet!'}\n* **Stars given to others:** {total_stars_given if total_stars_given != 0 else 'None :/'}\n* **Starboard messages:** {messages_on_sb if messages_on_sb != 0 else 'None so far!'}")
        await ctx.send(embed=embed)

    @star.command(aliases=["show", "see"])
    @private_only()
    async def view(self, ctx: Context, message_id: int):
        """View a starboard post
        
        Parameters
        ----------
        message_id: int
            ID of the starboard post
        """
        entry = await self.get_star_entry(message_id)
        channel = ctx.guild.get_channel(self.starboard_channel_id)
        if entry["star_embed_message_id"] is not None:
            message = await channel.fetch_message(entry["star_embed_message_id"])
            await ctx.reply(embed=message.embeds[0])
        else:
            await ctx.reply("Couldn't find that starboard post!")

    @tasks.loop(hours=1.5)
    async def clean_message_cache(self):
        self._message_cache.clear()

async def setup(bot):
    await bot.add_cog(Starboard(bot))