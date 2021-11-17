import discord
from discord.ext import commands, tasks
from discord.utils import get

class Administration(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command() 
    @commands.has_permissions(manage_guild=True)
    async def inv(self, ctx):
        link = await ctx.channel.create_invite(max_age = 300)
        await ctx.send(link)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def say(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send("{}" .format(msg))

def setup(client):
    client.add_cog(Administration(client))