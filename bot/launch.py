import discord

import asyncio
import logging
import logging.handlers

from utils.subclasses import CloudyBot
from setup.lists import *
from setup.config import * 

bot = CloudyBot()

@bot.tree.context_menu(name="Verify", guild=discord.Object(community_id))
async def verify(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.defer(ephemeral=True)
    try:
        embed = discord.Embed(title="Chroma Giveaway", description=ga_msg, color=0x6150ab)
        await message.author.send(embed=embed, content=ga_link)
    except discord.errors.Forbidden:
        # dms are off...
        await interaction.followup.send(f"oh no! {str(message.author).lower()} has their dms off. :/")

    await message.add_reaction("✅")
    await interaction.followup.send(f"Giveaway link has been sent to {str(message.author)} :]")

async def main():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=3,  # Rotate through 3 files
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # starts the bot
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())