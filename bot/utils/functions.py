import discord
import datetime

async def embedAttributes(embed_info, avatar):
    content = embed_info.split(" && ")
    title = content[0]
    description = content[1]
    color = content[2]
    embed = discord.Embed(title=title, description=description, color=int(color, 16))
    my_channel = None
    if len(content) >= 3:
        new_content = content[3:]
        for number, item in enumerate(new_content):
            if "FOOTER: " in new_content[number]:
                    footer = new_content[number].replace("FOOTER: ", "")
                    if "IMG: " in footer:
                        newfooter = footer.split("IMG: ")
                        footer_text = newfooter[0].replace("FOOTER: ", "")
                        if newfooter[1] == "AVATAR":
                            embed.set_footer(text=footer_text, icon_url=avatar)
                        else:
                            embed.set_footer(text=footer_text, icon_url=newfooter[1])
                    else:
                        embed.set_footer(text=footer)
            elif "AUTHOR: " in new_content[number]:
                author = new_content[number].replace("AUTHOR: ", "")
                if "IMG: " in author:
                        newauthor = author.split("IMG: ")
                        author_text = newauthor[0].replace("IMG: ", "")
                        if newauthor[1] == "AVATAR":
                            embed.set_author(name=author_text, icon_url=avatar)
                        else:
                            embed.set_author(name=author_text, icon_url=newauthor[1])
                else:
                    embed.set_author(name=author)
            elif "THUMBNAIL" in new_content[number]:
                thumbnail = new_content[number].replace("THUMBNAIL: ", "")
                if thumbnail == "AVATAR":
                    embed.set_thumbnail(url=avatar)
                else:
                    embed.set_thumbnail(url=thumbnail)
            elif "IMAGE" in new_content[number]:
                image = new_content[number].replace("IMAGE: ", "")
                if image == "AVATAR":
                    embed.set_image(url=avatar)
                else:
                    embed.set_image(url=image)
            elif "CHANNEL" in new_content[number]:
                my_channel = new_content[number].replace("CHANNEL: ", "")
            elif "TIMESTAMP" in new_content[number]:
                embed.timestamp = datetime.datetime.utcnow()
    return embed, my_channel

async def gif_embed(gifdata, query=None):
    if query == None:
        embed = discord.Embed(title="random gif", color=0x303136)
        embed.set_image(url=gifdata["images"]["original"]["url"])
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=gifdata["title"].lower())
    else:
        embed = discord.Embed(title=f"{query.lower()} gif", color=0x303136)
        embed.set_image(url=gifdata["images"]["original"]["url"])
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=gifdata["title"].lower())
    return embed