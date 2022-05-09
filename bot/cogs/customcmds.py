import discord
from discord.ext import commands
from setup.config import *
from firebase_admin import db

from utils.functions import embedAttributes

class CustomCommands(commands.Cog, name="customcmds"):
    def __init__(self, client):
        self.client = client

    @commands.command(help="adds a custom command to the bot")
    async def newcmd(self, ctx, name=None, *, output: commands.clean_content(fix_channel_mentions=False)=None): 
        if ctx.author.guild_permissions.manage_guild:
            if name == None:
                    embed = discord.Embed(description="**how to make custom commands**\n- to make a new command do `newcmd <commandname> <message>`, e.g. `newcmd hey how are you?`\n- the bot will then reply with **how are you?** whenever someone says hey!",color=0x303136)
                    await ctx.reply(embed=embed)
            elif output == None:
                embed = discord.Embed(description="**how to make custom commands**\n- to make a new command do `newcmd <commandname> <message>`, e.g. `newcmd hey how are you?`\n- the bot will then reply with **how are you?** whenever someone says hey!",color=0x303136)
                await ctx.reply(embed=embed)
            else:
                commands_ref = db.reference(f"/commands/{name}")
                existing_command = commands_ref.get()
                if existing_command is None and ctx.bot.get_command(name):
                    gname = ctx.guild.name
                    aname = gname.lower()
                    embed = discord.Embed(title=f"{aname} | custom commands:", description=f"there is a already a built-in command called **{name}**",color=0x303136)
                    return await ctx.reply(embed=embed)
                if existing_command:
                    self.client.remove_command(name)
                    output_ref = db.reference(f"/commands/{name}")
                    output_ref.update({
                        f"/{ctx.guild.id}": output
                    })
                    guild_ref = db.reference(f"/commands/{name}/{ctx.guild.id}")
                    cmds_dict = guild_ref.get()
                    @commands.command(name=name, help=f"custom command")
                    async def cmd(self, ctx):
                        if "!EMBED " in cmds_dict:
                            embed_info = cmds_dict.replace("!EMBED ", "")
                            embed, my_channel = await embedAttributes(embed_info, ctx.author.avatar.url)
                            channel = discord.utils.get(self.client.get_all_channels(), name=my_channel)
                            if channel == None:
                                channel = ctx.message.channel
                            await channel.send(embed=embed)
                        else:
                            if ctx.message.reference is not None:
                                msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                            else:
                                msg = ctx.message
                            await msg.reply(cmds_dict)
                    cmd.cog = self
                    # add cmd to cog and bot
                    self.__cog_commands__ = self.__cog_commands__ + (cmd,)
                    ctx.bot.add_command(cmd)
                    gname = ctx.guild.name
                    aname = gname.lower()
                    embed1 = discord.Embed(title=f"{aname} | custom commands:", description=f"edited the command **{name}**!",color=0x303136)
                    await ctx.reply(embed=embed1)
                else:
                    # add cmd to db
                    initial_ref = db.reference(f"/commands/{name}")
                    initial_ref.update ({
                        ctx.guild.id: f"{output}" 
                    })
                    guild_ref = db.reference(f"/commands/{name}/{ctx.guild.id}")
                    cmds_dict = guild_ref.get()
                    @commands.command(name=name, help=f"custom command")
                    async def cmd(self, ctx):
                        if "!EMBED " in cmds_dict:
                            embed_info = cmds_dict.replace("!EMBED ", "")
                            embed, my_channel = await embedAttributes(embed_info, ctx.author.avatar.url)
                            channel = discord.utils.get(self.client.get_all_channels(), name=my_channel)
                            if channel == None:
                                channel = ctx.message.channel
                            await channel.send(embed=embed)
                        else:
                            if ctx.message.reference is not None:
                                msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                            else:
                                msg = ctx.message
                            await msg.reply(cmds_dict)
                    cmd.cog = self
                    # add cmd to cog and bot
                    self.__cog_commands__ = self.__cog_commands__ + (cmd,)
                    ctx.bot.add_command(cmd)
                    gname = ctx.guild.name
                    aname = gname.lower()
                    embed1 = discord.Embed(title=f"{aname} | custom commands:", description=f"i added a command called **{name}**!",color=0x303136)
                    await ctx.reply(embed=embed1)
        else:
            await ctx.reply("you don't have permission to do that")

    @commands.command(help="removes a custom command from the bot")
    async def removecmd(self, ctx, name):
        if ctx.author.guild_permissions.manage_guild:
            gname = ctx.guild.name
            aname = gname.lower()
            ref = db.reference("/commands/")
            commands = ref.get()
            secondary_ref = db.reference(f"/commands/{name}/")
            guild_ref = secondary_ref.child(f"{ctx.guild.id}")
            guilds = guild_ref.get()
            if name not in commands or guilds == None:
                embed = discord.Embed(title=f"{aname} | custom commands:", description=f"i cant find a command called **{name}**",color=0x303136)
                return await ctx.reply(embed=embed)
            embed = discord.Embed(title=f"{aname} | custom commands:", description=f"i removed a command called **{name}**",color=0x303136)
            delete_ref = secondary_ref.child(f"{ctx.guild.id}")
            delete_ref.delete()
            self.client.remove_command(name)
            await ctx.reply(embed=embed)
        else:
            await ctx.reply("you don't have permission to do that")

    @commands.command(help="sends a list of all the custom commands")
    async def customcmds(self, ctx):
        ref = db.reference("/commands/")
        commands = ref.get()
        listt = []
        for element in commands:
            listt.append(element)
        custom = ', '.join(map(str, listt))
        embed = discord.Embed(title=f"{ctx.guild.name}'s custom commands", description=custom, color=0x303136)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(CustomCommands(bot))