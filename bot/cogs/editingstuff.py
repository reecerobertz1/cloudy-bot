import discord
from discord.ext import commands
import random

class Editingstuff(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(aliases=['audios'])
    async def audio(self, ctx, arg = None):
        if arg == 'badass':
            badass = ["https://soundcloud.app.goo.gl/2XB16Bu8Mv5wdKKW8", "https://soundcloud.app.goo.gl/eATHisrSUwxp3RDF8", "https://soundcloud.app.goo.gl/PNaPKuKjkuLzVYNj7", "https://soundcloud.app.goo.gl/6jGh8uT1ef2z55zB9", "https://soundcloud.app.goo.gl/n8cjHmkU9gtGLWL8A", "https://soundcloud.app.goo.gl/uahHbHpTvekQiugeA", "https://soundcloud.app.goo.gl/DXUAoYkbJkZUYP448", "https://soundcloud.app.goo.gl/QpKSx9aejCVVVLS47", "https://soundcloud.app.goo.gl/zxszrszh2E1NX9h99", "https://soundcloud.app.goo.gl/NQjF9PYScXu3Ug2K7", "https://soundcloud.app.goo.gl/dRahrtsH5HPMJksv7", "https://soundcloud.app.goo.gl/oZ85qMLb4azKLj7H6", "https://soundcloud.app.goo.gl/iWroyH9NKDKBxWwW6", "https://soundcloud.app.goo.gl/wceXiQYEJ6PyhRP68", "https://soundcloud.app.goo.gl/PydxxboAZzNV6i9RA", "https://soundcloud.app.goo.gl/fLaVavrfsZWvybZa6", "https://soundcloud.app.goo.gl/wuDGfKfegXvHWsxT6", "https://soundcloud.app.goo.gl/2NMVhRyzHCkmb7yJ9", "https://soundcloud.app.goo.gl/rWxJrvG6jh3cinaJ9", "https://soundcloud.app.goo.gl/H7dHwaoCKRabNsu4A", "https://soundcloud.app.goo.gl/UT9gTDYMH3VDm9AQ7", "https://soundcloud.app.goo.gl/JbwxN5DqPZdgCob97", "https://soundcloud.app.goo.gl/jDNrK6UV8GsFXB8z5", "https://soundcloud.app.goo.gl/NnSswveHQ1Hyv7my5", "https://soundcloud.app.goo.gl/37o76ftAw6z37siK7", "https://soundcloud.app.goo.gl/eHHcggfmdb8tS7ga8", "https://soundcloud.app.goo.gl/Sh1rpsi6KfbQbT3d8", "https://soundcloud.app.goo.gl/uRMHjTUFZg6fSJ9t7", "https://soundcloud.app.goo.gl/4ubRXPMd3Si5aCYo8", "https://soundcloud.app.goo.gl/5dd3tMRBQk66tsxdA", "https://soundcloud.app.goo.gl/piAjMLpJp2vv5uzW6", "https://soundcloud.app.goo.gl/1mRf9ne4ECL6cZ8i8", "https://soundcloud.app.goo.gl/95XH4jm23hYYmLtB9", "https://soundcloud.app.goo.gl/yNPzJ2DLXHgimAq16", "https://soundcloud.app.goo.gl/ugQzxDJoaiijAwCQ6", "https://soundcloud.app.goo.gl/ThYrQCiGeEGXZfN26", "https://soundcloud.app.goo.gl/Bnd5tWKkfyb8QEu47", "https://soundcloud.app.goo.gl/8wQ6ApgbanJxY8fBA", "https://soundcloud.app.goo.gl/RbsB64TGMCBJxueo8", "https://soundcloud.app.goo.gl/zMRskqYEQufNEuwe7", ]
            ranbadass = random.choice(badass)
            await ctx.reply(ranbadass)
            await ctx.send('Remember to credit whoever made the audio!')
        if arg == None:
            choices = ["https://www.instagram.com/p/CF7dzFWjvpB/?utm_source=ig_web_copy_link", "https://www.instagram.com/p/CFU92rcjjLw/?utm_source=ig_web_copy_link", "https://www.instagram.com/p/CFmyFBuDQNL/?utm_source=ig_web_copy_link", "https://www.instagram.com/p/CFkMUoWIOEh/?utm_source=ig_web_copy_link", "https://soundcloud.com/aelestic/why", "https://soundcloud.com/aelestic/when-you-walk-away", "https://soundcloud.com/aelestic/mind-games-sickick", "https://soundcloud.com/squarxd/sugar", "https://soundcloud.com/squarxd/fashion-killer", "https://soundcloud.com/squarxd/9am", "https://www.instagram.com/p/CE_rImAnMs_/?utm_source=ig_web_copy_link", "https://www.instagram.com/p/CEvPjWOJwY0/?utm_source=ig_web_copy_link", "https://www.instagram.com/p/CAaUxiJHVoW/?utm_source=ig_web_copy_link", "https://soundcloud.com/squarxd/night-out", "https://soundcloud.com/user-911721740/et-1", "https://soundcloud.com/user-911721740/cant-stop-dancing", "https://www.instagram.com/p/CFz_I2Hh9iA/?utm_source=ig_web_copy_link", "https://www.instagram.com/p/CFsT7EGD0ro/?utm_source=ig_web_copy_link", "https://www.instagram.com/p/CFm43Zwj9ip/?utm_source=ig_web_copy_link", "https://soundcloud.com/tessaedit/eastside", "https://soundcloud.com/tessaedit/walking-solo", "https://soundcloud.com/tessaedit/lifetime-in-repeat-1"]
            ranaudio = random.choice(choices)
            await ctx.reply(ranaudio)
            await ctx.send('Remember to credit whoever made the audio!')
        if arg == 'soft':
            choices = ["https://soundcloud.app.goo.gl/KwDPUjU5sJaJmF4N9", "https://soundcloud.app.goo.gl/1Q8NMEkAZgAojuo68", "https://soundcloud.app.goo.gl/Qmvstfza3vefkZ6F7", "https://soundcloud.app.goo.gl/T8XDP3vA4HRonDBdA", "https://soundcloud.app.goo.gl/SorLTqSTrT3fU4Xa8", "https://soundcloud.app.goo.gl/NpYYLvCoFgRSPnbs7", "https://soundcloud.app.goo.gl/Wzm2Ztsw9g23Ug9GA", "https://soundcloud.app.goo.gl/Lo34yGDBMHLuNhYc7", "https://soundcloud.app.goo.gl/qBeGhUqjmn5nVhEj8", "https://soundcloud.app.goo.gl/uHBZdRVzPjESUpMUA", "https://soundcloud.app.goo.gl/CNHPLsZpPpeur5gu9", "https://soundcloud.app.goo.gl/a9khxRAi59jzVLL29", "https://soundcloud.app.goo.gl/1uDSuteEg68hhzMf7", "https://soundcloud.app.goo.gl/3KcYFMehiWpve3GR6", "https://soundcloud.app.goo.gl/65pcZMcUo1oGcHGZA", "https://soundcloud.app.goo.gl/A83TLtWgRAHLKoSU9", "https://soundcloud.app.goo.gl/WzEzzVt3odYvB36t6", "https://soundcloud.app.goo.gl/62r4MoPURXmZY7kq5", "https://soundcloud.app.goo.gl/Yo2Zvhr5EUpMzAeLA", "https://soundcloud.app.goo.gl/XsWEm96Nn7SZYMD78", "https://soundcloud.app.goo.gl/uZvaiDc84Bmi75y36", "https://soundcloud.app.goo.gl/MgRCTFsZfETzNcoJ7", "https://soundcloud.app.goo.gl/Lc1ZF6Tp9Di2yMLb8", "https://soundcloud.app.goo.gl/BniZ3qnpynnLDAak8", "https://soundcloud.app.goo.gl/VRAZSoAwoPArVs1o7", "https://soundcloud.app.goo.gl/1ssK6nrie7WpT9Q2A", ]
            ransoft = random.choice(choices)
            await ctx.reply(ransoft)
            await ctx.send('Remember to credit whoever made the audio!')

    @commands.command(aliases=['effects'])
    async def effect(self, ctx):
        choices = ["4-Color Gradient", "S_HalfTone", "Gradient Ramp", "S_PseudoColor", "S_FlysEyeHex", "S_WipeTiles", "S_EdgeRays", "S_WipeMoire", "S_WipeDots", "S_WipePixelate", "S_WipePlasma", "S_WipeFlux", "S_GlowDist", "S_Glint", "Glow", "Turbulent Displace"]
        raneffect = random.choice(choices)
        await ctx.reply(raneffect)

    @commands.command(aliases=['transitions'])
    async def transition(self, ctx):
        await ctx.reply(random.choice([
                                          "cc flo motion + tile rotation",
                                          "s_flyseyehex rotation",
                                          "zoom in",
                                          "rotation",
                                          "warp",
                                          "middle tile rotation",
                                          "zoom out",
                                          "skew",
                                          "timeslice slide",
                                          "butterfly overlay",
                                          "fisheye warp",
                                          "2 split cube",
                                          "3 split cube",
                                          "go to kiki's acc and get transition ideas :)",
                                          "go to sienna's acc and get transition ideas",
                                          "split slide rotation",
                                          "y rotation",
                                          "x rotation",
                                          "vr rotate sphere",
                                          "cube expand w something on the inside",
                                          "scale stretch",
                                          "do something w a cube, dont be lazy",
                                          "do something 3d",
                                          "shatter",
                                          "inside cube rotation",
                                          "card wipe",
                                          "cube split",
                                          "tile rotation",
                                          "wipe rings (+turb)",
                                          "hexagon tile spin",
                                          "zoom in + rotation",
                                          "zoom out + rotation",
                                          "mirror stretch",
                                          "3D tunnel",
                                          "torn paper transition",
                                          "wipe overlay",
                                          "3D flip",
                                          "slide + rotation",
                                          "vr reorient",
                                          "cube rotatiton",
                                          "s_warpcornerpin",
                                          "s_wipeblobs",
                                          "s_flyseyehex corner spin",
                                          "s_flyseyerect anchored point rotation",
                                          "stretch slide",
                                          "cc scale wipe",
                                          "s_warppuddle",
                                          "vortex spin",
                                          "cube shatter",
                                          "warp squeeze",
                                          "ink splash"]))

def setup(client):
    client.add_cog(Editingstuff(client))