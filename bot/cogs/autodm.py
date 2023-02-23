import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
import json
import os
import random
from google_images_search import GoogleImagesSearch
from setup.lists import oldmems

class autodm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """    @commands.command()
    @commands.has_role('staff')
    async def accept(self, ctx, *, member: discord.Member):
        message = ctx.message
        embed = discord.Embed(title="Congrats, you got into Chroma!", description="**Read the rules before joining the Chroma discord!**", color=0x303136)
        embed.add_field(name="\u200b", value="thank you for joining chroma!!\nwe are honored to have you in our grp\n\n**GRP RULES:**\n- WATERMARK your logos with your USERNAME (make it unstealable)\n- NEVER share our logos and mega link for our logos to anyone\n- always use #헰헵헿헼헺헮헴헿헽\n- make sure you’re following @aelestic @electric.aep_ @manglxd @rqinflow @starrys.aep and @chromagrp at all times\n\n**CHAT RULES:**\n- try to stay active\n- set your discord nickname to “name | username” format\n- no impersonation\n- only spam in the spam channels\n- only self promote in the self-promo channel\n- no nudity/inappropriate content allowed\n- no offensive jokes\n- no negative comments about others\n- no inappropriate songs/videos in music bots\n- if you ever decide to leave/quit, pls dm @chromagrp\n- do not share the discord invite link with others\n\nif you have any problems with the link you have access to a channel called #members-help in the scout server where you can let us know!")
        embed.set_thumbnail(url="https://scontent-ort2-1.cdninstagram.com/v/t51.2885-19/83646915_193095065216493_3896196118190489600_n.jpg?_nc_ht=scontent-ort2-1.cdninstagram.com&_nc_ohc=GOALPaSRkDQAX97VJL3&edm=AKralEIAAAAA&ccb=7-4&oh=8a2292d20ac8c4908322e4e4598b5aa9&oe=609D5D70&_nc_sid=5e3072")
        await member.send(embed=embed)
        channl = self.bot.get_channel(694010549532360726)
        channel = channl
        chanl = self.bot.get_channel(835837557036023819)
        msgchannel = chanl
        roleid = 835838435067297823
        role = ctx.guild.get_role(roleid)
        membr = member.display_name
        link = await channel.create_invite(max_age = 86400, max_uses = 1)
        embed2 = discord.Embed(description=f"**you accepted {membr} // {member}!**", color=0x303136)
        await member.send(f"**Here's the link! <3**\n{link}")
        await member.add_roles(role)
        await message.add_reaction('✅')
        await msgchannel.send(embed=embed2)"""

    """@commands.command()
    @commands.has_role('staff')
    async def accept(self, ctx, *, member: discord.Member):
        sendch = self.bot.get_channel(836677673681944627)
        message = ctx.message
        embed = discord.Embed(title="Congrats, you got into Chroma!", description="**Read the rules before joining the Chroma discord!**", color=0x303136)
        embed.add_field(name="\u200b", value="thank you for joining chroma!!\nwe are honored to have you in our grp\n\n**GRP RULES:**\n- WATERMARK your logos with your USERNAME (make it unstealable)\n- NEVER share our logos and mega link for our logos to anyone\n- always use #헰헵헿헼헺헮헴헿헽\n- make sure you’re following @qtplum @rqinflow @94suga @ratwhore.mp4 and @chromagrp at all times\n\n**CHAT RULES:**\n- try to stay active\n- set your discord nickname to “name | username” format\n- no impersonation\n- only spam in the spam channels\n- only self promote in the self-promo channel\n- no nudity/inappropriate content allowed\n- no offensive jokes\n- no negative comments about others\n- no inappropriate songs/videos in music bots\n- if you ever decide to leave/quit, pls dm @chromagrp\n- do not share the discord invite link with others\n\nmessage a lead on discord if you encounter any problems!")
        embed.set_thumbnail(url="https://scontent-ort2-1.cdninstagram.com/v/t51.2885-19/83646915_193095065216493_3896196118190489600_n.jpg?_nc_ht=scontent-ort2-1.cdninstagram.com&_nc_ohc=GOALPaSRkDQAX97VJL3&edm=AKralEIAAAAA&ccb=7-4&oh=8a2292d20ac8c4908322e4e4598b5aa9&oe=609D5D70&_nc_sid=5e3072")
        channl = self.bot.get_channel(694010549532360726)
        channel = channl
        membr = member.display_name
        llist = membr.split("|")
        name1 = llist[1]
        name = name1.replace(" ", "")
        await member.send(embed=embed)
        link = await channel.create_invite(max_age = 86400, max_uses = 1)
        await member.send(f"**Here's the link! <3**\n{link}")
        chanl = self.bot.get_channel(835837557036023819)
        msgchannel = chanl
        roleid = 898539592553222144
        role = ctx.guild.get_role(roleid)
        await member.add_roles(role)
        embed2 = discord.Embed(description=f"**you accepted {name} [{member}]!**", color=0x303136)
        embed2.set_footer(text="you've accepted {} people so far!".format(len(role.members)))
        await message.add_reaction('✅')
        await msgchannel.send(embed=embed2)
        with open("members.json", "r") as file:
            data = json.load(file)
            data.append(name)
        with open("members.json", "w") as file:
            json.dump(data, file)
        await sendch.send(f"**you need to follow:**\nhttps://instagram.com/{name}")"""
        
    @commands.command()
    async def answer(self, ctx, *, response):
        msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        channel = self.bot.get_channel(862617899356651531)
        if "^" in msg.content:
                message = msg.content.split("^ ")
                question = message[0]
                asker = message[1]
        else:
                return
        user = await self.bot.fetch_user(asker)
        embed = discord.Embed(title="chroma scout q&a", color=0x303136, description=f"**q: {question}**\na: {response}")
        embed.set_footer(text=f"asked by {user.display_name} | answered by {ctx.author.display_name}")
        await channel.send(f"{user.mention}")
        await channel.send(embed=embed)

    """@commands.command()
    @commands.has_role('staff')
    async def totalmembers(self, ctx):
        with open("members.json", "r") as file:
            data = json.load(file)
        membs = '\n'.join(data)
        amnt = len(data)
        await ctx.reply(f"**these are the people you have accepted:**\n{membs}")
        await ctx.send(f"you've accepted {amnt} people!")

    @commands.command()
    @commands.has_role('staff')
    async def acceptpw(self, ctx):
        embed = discord.Embed(title="Congrats, you got into Chroma!", description="**Read the rules before joining the Chroma discord!**", color=0x36393f)
        embed.add_field(name="\u200b", value="thank you for joining chroma!!\nwe are honored to have you in our grp\n\nGRP RULES:\n- WATERMARK your logos with your USERNAME (make it unstealable)\n- NEVER share our logos and mega link for our logos to anyone\n- always use #헰헵헿헼헺헮헴헿헽\n- make sure you’re following @aelestic @electric.aep_ @manglxd @rqinflow and @starrys.aep at all times\n\nCHAT RULES:\n- try to stay active\n- set your discord nickname to “name | username” format\n- no impersonation\n- only spam in the spam channels\n- only self promote in the self-promo channel\n- no nudity/inappropriate content allowed\n- no offensive jokes\n- no negative comments about others\n- no inappropriate songs/videos in music bots\n- if you ever decide to leave/quit, pls dm @chromagrp\n- do not share the discord invite link with others\n\nif you have any problems with the link you have access to a channel called #members-help in the scout server where you can let us know!")
        embed.set_thumbnail(url="https://scontent-ort2-1.cdninstagram.com/v/t51.2885-19/83646915_193095065216493_3896196118190489600_n.jpg?_nc_ht=scontent-ort2-1.cdninstagram.com&_nc_ohc=GOALPaSRkDQAX97VJL3&edm=AKralEIAAAAA&ccb=7-4&oh=8a2292d20ac8c4908322e4e4598b5aa9&oe=609D5D70&_nc_sid=5e3072")
        await ctx.send(embed=embed)"""

    @commands.command(aliases=['ia'])
    async def inactive(self, ctx, *, value):
        stored_guild_id = 694010548605550675
        if ctx.guild.id == stored_guild_id:
            channel = self.bot.get_channel(849707778380922910)
            embed = discord.Embed(title="inactivity", description=f"{value}", color=0x32D052)
            embed.set_footer(text=f"message from; {ctx.author.display_name}")
            await ctx.reply("okay! i sent ur message to the staff")
            await channel.send(embed=embed)
        else:
            return

    @commands.command()
    async def qna(self, ctx, *, question):
        guild_id = 835495688832811039
        channel = self.bot.get_channel(862615059355271188)         
        q = await ctx.reply("asked!")
        await channel.send(f"{question} ^ {ctx.author.id}")
        await asyncio.sleep(2)
        await ctx.message.delete()
        await q.delete()
              
              
    @commands.command()
    async def answer(self, ctx, *, response):
        msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        channel = self.bot.get_channel(862617899356651531)
        if "^" in msg.content:
            message = msg.content.split(" ^ ")
            question = message[0]
            asker = message[1]
        else:
            return
        user = self.bot.get_user(int(asker))
        embed = discord.Embed(title="chroma scout q&a", color=0x303136, description=f"**q: {question}**\na: {response}")
        embed.set_footer(text=f"asked by {user.display_name} | answered by {ctx.author.display_name}")
        await channel.send(f"{user.mention}")
        await channel.send(embed=embed)

    @commands.command(aliases=['ae'])
    async def addedit(self, ctx, edit=None):
        if edit == None:
            await ctx.reply("you need to enter a streamable url!")
        else:
            with open("edits.json", "r") as file:
                data = json.load(file)
                data.append(edit)
                with open("edits.json", "w") as file:
                    json.dump(data, file)
            await ctx.reply("added your edit!") 

    @commands.command()
    async def publicedits(self, ctx, arg=None):
        if arg == None:
            async with ctx.typing():
                with open("edits.json", "r") as file:
                    data = json.load(file)
                    await ctx.reply(random.choice(data))
            return
        if arg == "count":
            async with ctx.typing():
                with open("edits.json", "r") as file:
                    data = json.load(file)
                    amnt = len(data)
                    await ctx.reply(f"there are currently {amnt} edits uploaded!")
            return
        else:
            return

    @commands.command()
    @commands.has_role('staff')
    async def membercheck(self, ctx, username):
        message = ctx.message
        if username in oldmems:
            await message.add_reaction('✅')
        else:
            await message.add_reaction('❌')


async def setup(bot):
    await bot.add_cog(autodm(bot))
