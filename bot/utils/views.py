import discord
from setup.config import contribs_simple, contribs
from setup.config import community_id

class ShowGiveawayContributers(discord.ui.View):
    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True

        await self.message.edit(view=self)

    @discord.ui.button(label="Show guide", style=discord.ButtonStyle.blurple)
    async def guide_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != discord.Member:
            chroma_community = interaction.client.get_guild(community_id)
            if chroma_community == None:
                chroma_community = await interaction.client.fetch_guild(community_id)
            member = chroma_community.get_member(interaction.user.id)
            if member == None:
                member = await chroma_community.fetch_member(interaction.user.id)
        else:
            member = interaction.user
        if member is None:
            return await interaction.response.send("You need to be in the Chroma Community server to use this button")
        if member.is_on_mobile() == True:
            await interaction.response.send_message(contribs_simple, ephemeral=True)
        else:
            await interaction.response.send_message(contribs, ephemeral=True)