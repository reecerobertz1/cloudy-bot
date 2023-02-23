import discord
from discord.ext import commands
from typing import Union
import asyncio
from setup.config import chroma_welc

class Recruit(commands.Cog):

    """Commands for recruit"""

    def __init__(self, bot) -> None:
        self.bot = bot

    def is_staff():
        async def predicate(ctx):
            role_id = 835549528932220938
            role = ctx.guild.get_role(role_id)
            return role in ctx.author.roles
        return commands.check(predicate)

    @commands.command()
    @is_staff()
    async def accepted(self, ctx):
        """Get a list of all users who have been accepted"""
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT * FROM applications WHERE accepted = 1")
            data = await cursor.fetchall()
            accepted = []
            for user in data:
               accepted.append(str(user[0]))
            accepted = "\n".join(accepted)
            await ctx.send(accepted)

    @commands.command()
    @is_staff()
    async def accept(self, ctx):
        """Accept a member"""
        if ctx.message.reference is not None:
            channel_id = 694010549532360726
            channel = self.bot.get_channel(channel_id)
            msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            user_id = msg.embeds[0].fields[0].value
            async with self.bot.db.cursor() as cursor:
                await cursor.execute('''UPDATE applications SET accepted = 1 WHERE user_id = ?''', (user_id,))
                await self.bot.db.commit()
                await cursor.execute('''SELECT * FROM applications WHERE user_id = ?''', (user_id,))
                row = await cursor.fetchone()
            embed = msg.embeds[0]
            embed.add_field(name="Status", value="Accepted ✅")
            member = ctx.guild.get_member(int(user_id))
            await ctx.message.add_reaction("✅")
            await msg.edit(embed=embed)
            member_embed = discord.Embed(title="Congrats, you got into Chroma!", description="**Read the rules before joining the Chroma discord!**")
            member_embed.add_field(name="\u200b", value=chroma_welc)
            embed.set_thumbnail(url="https://rqinflow.com/static/chroma_pfp.png")
            await member.send(embed=member_embed)
            link = await channel.create_invite(max_age = 86400, max_uses = 1, unique = True)
            await member.send(f"**Here's the link! <3**\n{link}")
            roleid = 836244165637046283
            role = ctx.guild.get_role(roleid)
            msgchannel = self.bot.get_channel(835837557036023819)
            sendch = self.bot.get_channel(836677673681944627)
            await member.add_roles(role)
            embed2 = discord.Embed(description=f"**you accepted {row[1]} / {member.mention}!**")
            await msgchannel.send(embed=embed2)
            await sendch.send(f"**you need to follow:**\nhttps://instagram.com/{row[1]}")
        else:
            return await ctx.send("No message reference found.")

    @commands.command(name="rc")
    @is_staff()
    async def recruit_check(self, ctx, member: discord.User):
        """Check if a user has been accepted"""
        async with self.bot.db.cursor() as cursor:
            await cursor.execute('''SELECT * FROM applications WHERE user_id = ?''', (member.id,))
            result = await cursor.fetchone()
        if result is None:
            return await ctx.send("This user has not joined the recruit")
        else:
            if result[2] == 1:
                return await ctx.send("This user has been accepted.")
            else:
                return await ctx.send("This user has not been accepted.")

    @commands.command(name="wipe")
    @commands.is_owner()
    async def wipe_recruit(self, ctx):
        """Wipe the recruit table"""
        await ctx.send("Are you sure you want to wipe the recruit table? Say `yes` to confirm.")

        def check(m) -> bool:
            return m.content == "yes" and m.author == ctx.author and m.channel == ctx.channel

        try:
            await self.bot.wait_for("message", check=check, timeout=10)

        except asyncio.TimeoutError:
            await ctx.send("Wipe cancelled!")

        else:
            async with self.bot.db.cursor() as cursor:
                await cursor.execute('''DELETE FROM applications''')
                await self.bot.db.commit()
            return await ctx.send("Recruit table wiped.")

    @commands.command(name="da")
    @is_staff()
    async def delete_app(self, ctx, member: discord.Member):
        """Delete an application"""
        async with self.bot.db.cursor() as cursor:
            await cursor.execute('''SELECT * FROM applications WHERE user_id = ?''', (member.id,))
            result = await cursor.fetchone()
            msg_id = result[3]
            channel = self.bot.get_channel(835497793703247903)
            msg = await channel.fetch_message(msg_id)
            await msg.delete()
            await cursor.execute('''DELETE FROM applications WHERE user_id = ?''', (member.id,))
            await self.bot.db.commit()
        return await ctx.send("Application deleted.")

    @commands.command(name="appinfo")
    @is_staff()
    async def appinfo(self, ctx, member: Union[discord.Member, str]):
        """Get information on an app"""
        if isinstance(member, discord.Member):
            async with self.bot.db.cursor() as cursor:
                await cursor.execute('''SELECT * FROM applications WHERE user_id = ?''', (member.id,))
                result = await cursor.fetchone()
        elif isinstance(member, str):
            async with self.bot.db.cursor() as cursor:
                await cursor.execute('''SELECT * FROM applications WHERE instagram = ?''', (member,))
                result = await cursor.fetchone()

        if result is None:
                return await ctx.send("This user has not applied.")
        else:
            embed = discord.Embed(title="App Information", description=f"{member}")
            embed.add_field(name="User ID", value=f"{result[0]}", inline=False)
            embed.add_field(name="Instagram", value=f"{result[1]}", inline=False)
            if result[2] == 1:
                embed.add_field(name="Status", value="Accepted ✅", inline=False)
            else:
                embed.add_field(name="Status", value="Pending ❌", inline=False)
            embed.add_field(name="Form Embed Link", value=f"[Click here to see the form](https://discord.com/channels/835495688832811039/835497793703247903/{result[3]})")
            return await ctx.send(embed=embed)
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Recruit(bot))