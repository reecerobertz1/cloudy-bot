import discord
from discord.ext import commands
from typing import Any, Type
import aiohttp
import aiosqlite
import json
from datetime import datetime
import asyncpg

from setup.lists import *
from setup.config import *

intents = discord.Intents.all()
intents.presences = True
intents.members = True

TEST_GUILD = discord.Object(id=835495688832811039)

class Context(commands.Context["CloudyBot"]):
    async def send(self, *args: Any, **kwargs: Any) -> discord.Message:
        embed = kwargs.get("embed")
        if embed and not embed.color:
            kwargs["embed"].color = self.bot.embed_color

        for embed in kwargs.get("embeds", []):
            if not embed.color:
                kwargs["embed"].color = self.bot.embed_color

        return await super().send(*args, **kwargs)

class CloudyBot(commands.Bot):
    db: aiosqlite.Connection
    session: aiohttp.ClientSession

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self._context: Type[Context]

        self._BotBase__cogs = commands.core._CaseInsensitiveDict()

        self.initial_extensions = {
            "cogs.administration",
            "cogs.autodm",
            "cogs.chroma",
            "cogs.editingstuff",
            "cogs.events",
            "cogs.fun",
            "cogs.tags",
            "cogs.help",
            "jishaku",
            "cogs.error_handler",
            "cogs.recruit",
            "cogs.misc",
            "cogs.slash"
        }

    async def get_context(self, message, *, cls=None):
            return await super().get_context(message, cls=cls or Context)

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        await self.tree.sync(guild=TEST_GUILD)
        self.session = aiohttp.ClientSession()
        self.webhook = discord.Webhook.from_url(webhook_url, session = aiohttp.ClientSession())
        self.launch_time = datetime.utcnow()
        self.embed_color = 0x2B2D31

        credentials = {"user": postgres_user, "password": postgres_password, "database": postgres_db, "host": postgres_host}
        pgdb = await asyncpg.create_pool(**credentials)
        await pgdb.execute("CREATE TABLE IF NOT EXISTS user_info (user_id bigint PRIMARY KEY , last_seen timestamp with time zone, online_since timestamp with time zone)")

        dbase = await aiosqlite.connect("utils/recruit.db")
        async with dbase.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS applications (user_id INTEGER PRIMARY KEY, instagram TEXT UNIQUE, accepted INTEGER, msg_id INTEGER)") 

        self.db = dbase
        self.pgdb = pgdb

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_ready(self):
        print('Cloudy is now online!')