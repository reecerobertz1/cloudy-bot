import discord
from discord.errors import HTTPException
from discord.ext import commands
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import datetime

class tag(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.group(invoke_without_command=True, aliases=['t'])
    async def tag(self, ctx, tag_name):
        try:
            guildid = ctx.guild.id
            ref_response = db.reference(f"/tags/{tag_name}/{guildid}/response")
            await ctx.reply(ref_response.get())
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
        guildid = ctx.guild.id
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        tagname = tag_name
        owner = ctx.author.id
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
        guildid = ctx.guild.id
        ref = db.reference(f"/tags/{tag_name}/{guildid}/owner/")
        embed = discord.Embed(title=f"**{tag_name}**", color=0x303136)
        embed.add_field(name="owner", value=f"<@!{ref.get()}>")
        ref2 = db.reference(f"/tags/{tag_name}/{guildid}/created/")
        embed.add_field(name="created", value=f"{ref2.get()}")
        ref3 = db.reference(f"/tags/{tag_name}/{guildid}/usage/")
        embed.add_field(name="used", value=f"{ref3.get()} times")
        await ctx.reply(embed=embed)

    @tag.command()
    async def view(self, ctx):
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
        embed = discord.Embed(title=f"{title}'s tags", description=fin, color=0x303136)
        embed.set_footer(text="for info on a specific tag, do *tag info <tagname>")
        await ctx.send(embed=embed)

    @tag.command()
    async def list(self, ctx, member: discord.User=None):
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
        embed = discord.Embed(title=f"{name}'s tags", description=cmds, color=0x303136)
        embed.set_footer(text="for info on a specific tag, do *tag info <tagname>")
        await ctx.send(embed=embed)

    @tag.command()
    async def delete(self, ctx, tag_name):
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

def setup(client):
    client.add_cog(tag(client))