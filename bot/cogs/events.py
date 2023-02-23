import discord
from discord.ext import commands
import json
from typing import Optional

class chromacom(commands.Cog):
    def __init__(self,client):
        self.client = client

    async def get_user_data(self, userid):
        query = "SELECT * FROM user_info WHERE user_id = $1;"
        info = await self.bot.db.fetchrow(query, userid)
        return info

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.mentions[0] == self.client.user:

                if 'help' in message.content:

                    with open("prefixes.json", "r") as f:
                        prefixes = json.load(f)

                    pre = prefixes[str(message.guild.id)] 

                    await message.channel.send(f"My prefix for this server is {pre}")
                else:
                    return

        except:
            pass

        stored_guild_id = 694010548605550675
        scout_guild_id = 835495688832811039

        if message.author.bot:
            return
        if 'starrys.aep' in message.content:
            await message.channel.send("yes starry is the best and the love of alex's life mwah <:iheartstarrysaep:962016301344243802>")
        if 'stan kiki' in message.content:
            await message.channel.send('we stan kiki yup')
        if 'ana grandily' in message.content:
            await message.channel.send('ana is so grandily!')
        if 'hi martine' in message.content:
            await message.channel.send('oh no, not martine-')
        if message.content.lower() == 'cloudy':
            await message.channel.send('hi im cloudy and i love u mwah')
        if 'alex bae' in message.content:
            await message.channel.send('stan alex :)')
        if 'leeron bae' in message.content:
            await message.channel.send('lee is bae mwah')
        if 'leonie bae' in message.content:
            await message.channel.send('i love leonie omg')
        if 'freya bae' in message.content:
            await message.channel.send('i love freya bae')
        if 'zara bae' in message.content:
            await message.channel.send('hi i love zara')
        if 'leeroni' in message.content:
            await message.channel.send('i want roni and leeron to get married!')
        if 'ariel bae' in message.content:
            await message.channel.send('i luv ari')
        if 'nancy luhvbott' in message.content:
            await message.channel.send('i love nancy so so much mwah <3')
        if 'kay 94suga' in message.content:
            await message.channel.send("yoongi and cloudy loves kay confirmed")
        if "Anis" in message.content:
            await message.channel.send("You have now summoned the toji simp")
        if "kijn" in message.content:
            await message.channel.send("kay and tijn are soulmates!!!")
        if message.content.lower() == 'chroma':
            author = message.author.mention
            await message.channel.send(f'{author} loves chroma <a:c9:784237655545610290>')
        if "MessageType.premium_guild" in str(message.type):
                if "|" in message.author.display_name:
                    name0 = message.author.display_name.split("|")
                    display = name0[0]
                else:
                    display = message.author.display_name
                embed = discord.Embed(title=f"thanks for boosting, {display}!", description="- your boost is greatly appreciated by the chroma community!\n- you can get your perks in <#865516313065947136>\n- thanks for supporting chroma, we love u! <3", color=0x303136)
                embed1 = discord.Embed(title=f"thanks for boosting, {display}!", description="- your boost is greatly appreciated!\n- you can get your perks in <#853241710658584586>\n- you can also claim perks by doing `+claimperks` in <#822422177612824580>\n- thanks for supporting chroma <3", color=0xDECAB2)
                if message.guild.id == stored_guild_id:
                    await message.channel.send(f"{message.author.mention}")
                    await message.channel.send(embed=embed1)
                elif message.guild.id == scout_guild_id:
                    await message.channel.send(f"{message.author.mention}")
                    await message.channel.send(embed=embed)
                else:
                    pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        public = 835498963418480650
        role = 836244165637046283
        stored_guild_id = 694010548605550675
        scout_guild_id = 835495688832811039
        if member.guild.id == stored_guild_id:
            embed = discord.Embed(title='Welcome to Chroma!', color=0xff3dc8, description=f"{member.mention} has joined the sever!\n• read the <#725373131220320347> and get your <#838298608704815114>\n• introduce yourself in <#727875317439528982>\n• questions? ask a <@&753678720119603341> or <@&739513680860938290>!\n• enjoy your time here in chroma! <3")
            embed.set_footer(text='thank you for joining!', icon_url=member.display_avatar.url)
            channel = self.client.get_channel(725389930607673384)
            embed.set_thumbnail(url='https://rqinflow.com/static/chroma_pfp.png')
            await channel.send(f'{member.mention}')
            await channel.send(embed=embed)
        elif member.guild.id == scout_guild_id:
            guild = self.client.get_guild(694010548605550675)
            guild2 = self.client.get_guild(835495688832811039)
            embed2 = discord.Embed(title="welcome!", color=0x303136, description=f"{member.mention} has joined the server!\n\n• read the <#835495896727814164>!\n• get editing help in <#862656708059594782>\n• talk to other editors <#836647673595428925>")
            embed2.set_footer(text='thanks for wanting to join chroma! <3', icon_url=member.display_avatar.url)
            channel2 = self.client.get_channel(836251337649160256)
            await channel2.send(f'{member.mention}')
            await channel2.send(embed=embed2)
            member2 = guild.get_member(member.id)
            if member2 is None:
                await member.add_roles(member.guild.get_role(public))
            else:
                await member.add_roles(member.guild.get_role(role))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        stored_guild_id = 694010548605550675
        if member.guild.id == stored_guild_id:
            embed = discord.Embed(title="Member left!", color=0x96bfff, description=f"{member.mention} has left the discord.")
            embed.set_thumbnail(icon_url=member.display_avatar.url)
            embed.set_footer(text='i hope to see you again!', icon_url='https://cdn.discordapp.com/attachments/799984745772875786/800015677653909504/yaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.png')
            channel = self.client.get_channel(725389930607673384)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):


        with open("./prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = "+"

        with open("./prefixes.json", "w") as f:
            json.dump(prefixes,f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open("./prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open("./prefixes.json", "w") as f:
            json.dump(prefixes,f, indent=4)

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        connection = await self.bot.pgdb.acquire()
        if "offline" in after.status:
            async with connection.transaction():
                try:
                    user_info_query = "INSERT INTO user_info (user_id, last_seen, online_since) VALUES ($1, $2, $3)"
                    await self.bot.pgdb.execute(user_info_query, after.id, discord.utils.utcnow(), None)
                except Exception as e:
                    if e.message == 'duplicate key value violates unique constraint "user_info_pkey"':
                        update_query = '''UPDATE user_info SET last_seen = $1, online_since = $2 WHERE user_id = $3'''
                        await self.bot.pgdb.execute(update_query, discord.utils.utcnow(), None, after.id)
                    else:
                        print(e)
        elif "offline" in before.status:
            async with connection.transaction():
                try:
                    user_info_query = "INSERT INTO user_info (user_id, last_seen, online_since) VALUES ($1, $2, $3)"
                    await self.bot.pgdb.execute(user_info_query, after.id, None, discord.utils.utcnow())
                except Exception as e:
                    if e.message == 'duplicate key value violates unique constraint "user_info_pkey"':
                        update_query = '''UPDATE user_info SET last_seen = $1, online_since = $2 WHERE user_id = $3'''
                        await self.bot.pgdb.execute(update_query, None, discord.utils.utcnow(), after.id)
                    else:
                        print(e)
        await self.bot.pgdb.release(connection)

async def setup(client):
    await client.add_cog(chromacom(client))