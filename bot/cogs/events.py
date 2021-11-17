import discord
from discord.ext import commands
import json

class chromacom(commands.Cog):
    def __init__(self,client):
        self.client = client

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
        if 'starry bae' in message.content:
            await message.channel.send('yes starry is bae mwah')
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
        if 'nancy bae' in message.content:
            await message.channel.send('i love nancy so so much mwah <3')
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
            embed.set_footer(text='thank you for joining!', icon_url=member.avatar_url)
            channel = self.client.get_channel(725389930607673384)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/799984745772875786/806921227091443762/giphy.gif')
            await channel.send(f'{member.mention}')
            await channel.send(embed=embed)
        elif member.guild.id == scout_guild_id:
            guild = self.client.get_guild(694010548605550675)
            guild2 = self.client.get_guild(835495688832811039)
            embed2 = discord.Embed(title="welcome!", color=0x303136, description=f"{member.mention} has joined the server!\n\n• read <#835495896727814164> and <#835495688832811043>!\n• join in <#835495966089281536>, good luck! <3")
            embed2.set_footer(text='thanks for wanting to join chroma! <3', icon_url=member.avatar_url)
            embed2.set_thumbnail(url=guild2.icon_url)
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
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text='i hope to see you again!', icon_url='https://cdn.discordapp.com/attachments/799984745772875786/800015677653909504/yaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.png')
            channel = self.client.get_channel(725389930607673384)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game("@cloudy♡ help"))
        print('Cloudy is now online!')

def setup(client):
    client.add_cog(chromacom(client))