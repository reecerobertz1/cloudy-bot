import discord
import random
import asyncio
import time
import json
import os

from discord import Intents
from random import choice
from discord import Intents
from lists import *

import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from setup.config import *

discord.Intents.all()
intents = discord.Intents.all()
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)

from discord.ext import commands, tasks
from discord.utils import get

def get_prefix(client,message):

    try:
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        return prefixes[str(message.guild.id)]
        
    except AttributeError: # I added this when I started getting dm error messages
        return '+' # This will return "." as a prefix. You can change it to any default prefix.

client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=intents)
client.remove_command('help')

@client.event
async def on_guild_join(guild):


    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "+"

    with open("prefixes.json", "w") as f:
        json.dump(prefixes,f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open("prefixes.json", "w") as f:
        json.dump(prefixes,f, indent=4)

@client.command()
@commands.has_permissions(manage_messages = True)
async def newprefix(ctx, prefix):

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes,f, indent=4)    

    embed = discord.Embed(description=f"✅ The prefix was changed to {prefix}", colour=0x70ff75)
    await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, error): 
    if isinstance(error, commands.MemberNotFound):
        await ctx.reply("i couldn't find that user!")
    # elif isinstance(error, commands.CommandInvokeError):
        # await ctx.send("I can't dm this person!")

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Loaded Cog")

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send("Unloaded Cog")

@client.command()
@commands.is_owner()
async def taload(ctx):
    client.unload_extension(f'cogs.tags')
    client.load_extension(f'cogs.tags')
    await ctx.send("Reloaded Cog")

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Reloaded Cog")

cred = credentials.Certificate(firebase_config)
databaseApp = firebase_admin.initialize_app(cred, {
    'databaseURL' : dburl
})

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[0:-3]}')
        print(f'loaded {filename}')

client.run(TOKEN)


