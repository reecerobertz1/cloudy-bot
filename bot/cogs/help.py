import discord
import json
from discord.ext import commands


class helpcmd(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
            embed1 = discord.Embed(color=0x9E74FF)
            emoji = '⏮'
            emoji2 = '◀️'
            emoji3 = '▶️'
            emoji4 = '⏭'
            try:
                with open("prefixes.json", "r") as f:
                    prefixes = json.load(f)
                fix = prefixes[str(ctx.guild.id)]
            except AttributeError: # I added this when I started getting dm error messages
                fix = '+' # This will return "+" as a prefix. You can change it to any default prefix.

            embed1.set_author(name='cloudy', icon_url='https://cdn.discordapp.com/attachments/799984745772875786/800015677653909504/yaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.png')
            embed1.add_field(name="HELP", value="Help for cloudy is put into different categories so it's easier for you to find what you're looking for. In the following categories the command will be listed next to a number and what it does will be described below. These are the different catagories:", inline=False)
            embed1.add_field(name='**1. Editing**', value="Includes the commands you would wanna use for editing!", inline=False)
            embed1.add_field(name='**2. Chroma**', value='Includes the commands associated with [Chroma group](https://www.instagram.com/chromagrp) and its members!', inline=False) 
            embed1.add_field(name="**3. Fun**", value='Includes commands you can use for fun!', inline=False)
            embed1.add_field(name="**4. Custom commands**", value='Includes information on how to make custom commands with cloudy!', inline=False)
            embed1.add_field(name="**5. Tags**", value="Includes information on how to use tags with cloudy!", inline=False)
            embed1.add_field(name='**6. Other**', value='Includes other information on cloudy!')
            embed1.set_footer(icon_url='https://cdn.discordapp.com/icons/694010548605550675/a_250164731b9ec08b3060309d3c20ee93.gif?size=256', text='to see the categories use the arrows below')

            embed2 = discord.Embed(title='Commands for editing:', color=0x9E74FF, description=f"`{fix}effect`\nSends an After Effects effect\n\n`{fix}transition`\nSends a transition\n\n`{fix}audio [badass | soft]`\nSends an editing audio")
            embed2.set_author(name='HELP', icon_url='https://cdn.discordapp.com/attachments/798221090555297792/798221191151222844/chroma_logo_blue.png')
            embed2.set_footer(text='Category 1 | Editing')

            embed3 = discord.Embed(title='Chroma commands:', color=0x9E74FF, description=f"`{fix}member`\nSends an instagram link to a random Chroma member\n\n`{fix}memberinfo <discord user>`\nSends info on a member of the discord server\n\n`{fix}edit`\nSends an edit made by a random Chroma member")
            embed3.set_author(name='HELP', icon_url='https://cdn.discordapp.com/attachments/798221090555297792/798221191151222844/chroma_logo_blue.png')
            embed3.set_footer(text='Category 2 | Chroma')

            embed6 = discord.Embed(title='**About Cloudy:**', color=0x6bb5ff)
            embed6.set_author(name='HELP', icon_url='https://cdn.discordapp.com/attachments/798221090555297792/798221191151222844/chroma_logo_blue.png')
            embed6.add_field(name='**Basics:**', value=f"Cloudy's prefix for this server is {fix}, which means you have to put {fix} before you use a command, e.g. ``{fix}edits`` If you want to change the prefix type ``{fix}newprefix <new prefix>``", inline=False)
            embed6.add_field(name='**About the coding of cloudy**:', value="Cloudy is coded using Python. The specific version it's developed on is Python 3.8. Some of the commands the bot has are from suggestions by members of Chroma. If you have any ideas for commands or any further questions or enconter problems while using Cloudy mention <@!728597655156162600> in the Chroma server or message them on Discord!", inline=False)
            embed6.set_footer(text='Category 5 | made by alex<3#0017 with love')

            embed4 = discord.Embed(title='Fun commands:', color=0x9E74FF, description=f"`{fix}imgur <search>`\nSends photo from imgur\n\n`{fix}gif [search]`\nSends a GIF from GIPHY\n\n`{fix}hug [mention]`\nGive a hug to a friend, or get a hug from Cloudy\n\n`{fix}kiss [mention]`\nKiss someone, or get a kiss from Cloudy\n\n`{fix}ship <person> <person2>`\nCloudy tells you whether it ships or not!\n\n`{fix}slap <mention>`\nSlap someone")
            embed4.set_author(name='HELP', icon_url='https://cdn.discordapp.com/attachments/798221090555297792/798221191151222844/chroma_logo_blue.png')
            embed4.set_footer(text='Category 3 | Fun')

            embed5 = discord.Embed(title='Custom commands:', color=0x9E74FF, description=f"`{fix}newcmd`\nCreates a command\n\n`{fix}removecmd <commandname>`\nPermanently deletes a custom command\n\n`{fix}customcmds`\nSends a list of your guild's custom commands")
            embed5.set_author(name='HELP', icon_url='https://cdn.discordapp.com/attachments/798221090555297792/798221191151222844/chroma_logo_blue.png')
            embed5.set_footer(text='Category 4 | Custom commands')

            embed45 = discord.Embed(title='Fun commands:', color=0x9E74FF, description=f"`{fix}dm <mention> <message>`\nSends the inputted message to the mentioned user's messages\n\n`{fix}dm_me <message>`\nSends you the inputted message\n\n`{fix}choose <choice1> <choice2>`\nChooses one of the two options\n\n`{fix}number`\nOutputs a random number within your range\n\n`{fix}embed <message>`\nEmbeds your message\n\n`{fix}clock <continent/city>`\nSends the current time in the specified city\n\n")
            embed45.set_footer(text='Category 3.5 | Fun')
            
            embed7 = discord.Embed(title='Tag commands:', color=0x9E74FF, description=f"`{fix}tag <tag_name>`\nResponds with the tag's response\n\n`{fix}tag create <tag_name> <tag response>`\nMakes you a custom tag\n\n`{fix}tag info <tag_name>`\nGives you info on a tag\n\n`{fix}tag view`\nSends a list of all commands in the server\n\n`{fix}tag list [mention]`\nSends the tags owned by the given user\n\n`{fix}tag edit <tag_name> <response>`\nEdits the given tag to say your new input\n\n`{fix}tag delete <tag_name>`\nDeletes the given tag")
            embed7.set_author(name='HELP', icon_url='https://cdn.discordapp.com/attachments/798221090555297792/798221191151222844/chroma_logo_blue.png')

            pages = [embed1, embed2, embed3, embed4, embed45, embed5, embed7, embed6]

            message = await ctx.send(embed=embed1)
            await message.add_reaction(emoji)
            await message.add_reaction(emoji2)
            await message.add_reaction(emoji3)
            await message.add_reaction(emoji4)

            def check(reaction, user):
                return user == ctx.author

            i = 0
            reaction = None

            while True:
                if str(reaction) == '⏮':
                    i = 0
                    await message.edit(embed = pages[i])
                elif str(reaction) == '◀️':
                    if i > 0:
                        i -= 1
                        await message.edit(embed = pages[i])
                elif str(reaction) == '▶️':
                    if i < 7:
                        i += 1
                        await message.edit(embed = pages[i])
                elif str(reaction) == '⏭':
                    i = 7
                    await message.edit(embed = pages[i])
            
                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout = 60.0, check = check)
                    await message.remove_reaction(reaction, user)
                except:
                    break

            await message.clear_reactions()

def setup(client):
    client.add_cog(helpcmd(client))
