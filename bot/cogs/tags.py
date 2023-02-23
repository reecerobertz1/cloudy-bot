import discord
from discord.errors import HTTPException
from discord.ext import commands
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import datetime

class tag(commands.Cog, name="Tags", description="Includes information on how to use tags with cloudy!"):
    def __init__(self,bot):
        self.bot = bot

        #with open('badwords.txt', 'r') as f:
        #    global badwords 
        #    words = f.read()
        #    badwords = words.split()

    @commands.group(invoke_without_command=True, aliases=['t'])
    async def tag(self, ctx, tag_name):
        """Cloudy's tag commands"""
        try:
            guildid = ctx.guild.id
            ref_response = db.reference(f"/tags/{tag_name}/{guildid}/response")
            if ctx.message.reference is not None:
                msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                await msg.reply(ref_response.get())
            else:
                await ctx.send(ref_response.get())
            ref_number = db.reference(f"/tags/{tag_name}/{guildid}/usage")
            number = ref_number.get()
            newnumber = int(number) + 1
            ref = db.reference(f"/tags/{tag_name}/{guildid}")
            ref.update({
                "usage": newnumber
            })
        except discord.HTTPException:
            await ctx.reply(f"there is no tag named **{tag_name}**!")

    @tag.command()
    async def create(self, ctx, tag_name=None, *, response=None):
        """Creates a tag"""
        guildid = ctx.guild.id
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        tagname = tag_name
        msg = ctx.message.content
        owner = ctx.author.id
        #for word in badwords:
        #    if word in msg:
        #        await ctx.reply("you used one or more words that aren't allowed to use in tags.")
        #        return await ctx.message.delete()
        #    else:
        #        pass
        if tag_name == None:
            await ctx.send("you need a tag name")
        elif response == None:
            await ctx.send("you need a response for your tag")
        else:
            try:
                ref = db.reference(f"/tags/{tag_name}/{guildid}")
                ref_owner = db.reference(f"/tags/{tag_name}/{guildid}/owner")
                author = ref_owner.get()
                if author == owner:
                    await ctx.reply(f"you already own the command named **{tag_name}**! to edit it, please use *tag edit")
                elif author == None:
                    ref = db.reference(f"/tags/{tag_name}")
                    ref.update({
                        guildid: {
                                "response": str(response),
                                "owner": ctx.author.id,
                                "created": date, 
                                "usage": "0"
                            }
                    })
                    return await ctx.reply("done!")
                elif author != owner:
                    return await ctx.reply(f"the command **{tag_name}** already exists!")    
            except HTTPException:
                ref = db.reference("/tags/")
                ref.update({
                    tagname: {
                        guildid: {
                            "response": str(response),
                            "owner": ctx.author.id,
                            "created": date, 
                            "usage": "0"
                        }
                    }
                })
                await ctx.reply("done!")
        return

    @tag.command()
    async def info(self, ctx, tag_name):
        """Sends info about a specific tag"""
        guildid = ctx.guild.id
        ref = db.reference(f"/tags/{tag_name}/{guildid}/owner/")
        embed = discord.Embed(title=f"**{tag_name}**")
        embed.add_field(name="owner", value=f"<@!{ref.get()}>")
        ref2 = db.reference(f"/tags/{tag_name}/{guildid}/created/")
        embed.add_field(name="created", value=f"{ref2.get()}")
        ref3 = db.reference(f"/tags/{tag_name}/{guildid}/usage/")
        embed.add_field(name="used", value=f"{ref3.get()} times")
        await ctx.reply(embed=embed)

    @tag.command()
    async def view(self, ctx):
        """Sends a list consisting all the tags in the current guild"""
        ref = db.reference("/tags/")
        all = ref.get()
        listt = []
        for element in all:
            if str(ctx.guild.id) in all[element]:
                listt.append(element)
        before = str(listt)
        mid = before.replace("[", " ")
        last = mid.replace("]", " ")
        fin = last.replace("'", "`")
        title1 = ctx.guild.name
        title = title1.lower()
        embed = discord.Embed(title=f"{title}'s tags", description=fin)
        embed.set_footer(text="for info on a specific tag, do *tag info <tagname>")
        await ctx.send(embed=embed)

    @tag.command()
    async def list(self, ctx, member: discord.User=None):
        """Sends a list of the tags owned by the specified member"""
        guilid = ctx.guild.id
        if member == None:
            id = ctx.author.id
            name = ctx.author.display_name
        else:
            id = member.id
            name = member.display_name
        ref = db.reference("/tags/")
        tags_dict = ref.get()
        lst = []
        for i in tags_dict:
            for j, k in tags_dict[i].items():
                owner = k["owner"]
                if int(guilid) == int(j) and int(owner) == int(id):
                    lst.append(i)
        cmds = ',\n'.join(lst)
        embed = discord.Embed(title=f"{name}'s tags", description=cmds)
        embed.set_footer(text="for info on a specific tag, do *tag info <tagname>")
        await ctx.send(embed=embed)

    @tag.command()
    async def delete(self, ctx, tag_name):
        """Deletes a tag"""
        guildid = ctx.guild.id
        owner = ctx.author.id
        ref = db.reference(f"/tags/{tag_name}/")
        ref_owner = db.reference(f"/tags/{tag_name}/{guildid}/owner")
        author = ref_owner.get()
        if author == owner:
            delete_ref = ref.child(f"{guildid}")
            delete_ref.delete()
            await ctx.send(f"deleted your tag named **{tag_name}**")
        else:
            await ctx.send("you can't delete a tag that you don't own!")

    @tag.command()
    async def edit(self, ctx, tag_name=None, *, response=None):
        """Edit a tag"""
        if tag_name == None:
            await ctx.send("you need to specify which tag you want to edit!")
        elif response == None:
            await ctx.send("you need a response for your tag!")
        guildid = ctx.guild.id
        owner = ctx.author.id
        ref = db.reference(f"/tags/{tag_name}/")
        ref_owner = db.reference(f"/tags/{tag_name}/{guildid}/owner")
        author = ref_owner.get()
        if author == owner:
            ref.update({
                f"{guildid}/response": f'{str(response)}'
            })
            return await ctx.reply(f"**{tag_name}** was edited!")
        elif author == None:
            return await ctx.reply(f"you cannot edit **{tag_name}**, as it does not exist")
        elif author != owner:
            return await ctx.reply(f"you cannot edit **{tag_name}**, because you don't own it!")

async def setup(bot):
    await bot.add_cog(tag(bot))