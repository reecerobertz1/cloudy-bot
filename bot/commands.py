import discord
import json

from setup.lists import *
from setup.config import *

from utils.subclasses import CloudyBot

intents = discord.Intents.all()
intents.presences = True
intents.members = True

from discord.ext import commands

# Bad code moment.
def get_prefix(bot: CloudyBot, message: discord.Message):

    try:
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        return prefixes[str(message.guild.id)]
        
    except AttributeError:
        return '+' 

client = CloudyBot(
    command_prefix = get_prefix,
    intents = intents,
    case_insensitive=True,
    status = discord.Status.online,
    activity = discord.Game("@cloudy♡ help")
)

client.run(TOKEN)