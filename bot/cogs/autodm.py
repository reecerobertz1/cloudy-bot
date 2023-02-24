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

    @commands.command()
    async def qna(self, ctx, *, question):
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
