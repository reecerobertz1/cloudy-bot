import discord
from discord.ext import commands
import json

class HelpDropdown(discord.ui.Select):

    def __init__(self, commands: dict[commands.Cog, list[commands.Command]], bot):
        options=[discord.SelectOption(label="Home", description="Home Page")]
        super().__init__(
            placeholder='Select a category...',
            min_values=1,
            max_values=1,
            options=options
        )
        self.commands = commands
        self.bot = bot
        self.add_cog_options()

    def add_cog_options(self):
        for cog, commands in self.commands.items():
            cog_name = getattr(cog, "qualified_name", "Other")
            description = getattr(cog, "description", "Miscellaneous commands")
            if not description or len(commands) == 0 or cog_name == "Jishaku" or cog_name == "Other":
                continue
            if cog_name.capitalize() == "Chroma":
                description = "Includes the commands associated with Chroma group"
            self.add_option(label=cog_name.capitalize(), description=description)

    async def get_cog_help(self, cog):
        commands = cog.get_commands()
        embed = discord.Embed(title=f"{cog.qualified_name.capitalize()} Commands", color=0x9E74FF)
        embed.set_footer(text="Category: " + cog.qualified_name.capitalize())
        for command in commands:
            embed.add_field(name=command.qualified_name, value=command.help, inline=False)

        return embed

    def get_prefix(self, channel):
        try:
            with open("prefixes.json", "r") as f:
                prefixes = json.load(f)
            fix = prefixes[str(channel.guild.id)]
        except AttributeError:
            fix = '+'
        return fix

    async def get_init_page(self, channel, author):
        prefix = self.get_prefix(channel)
        embed = discord.Embed(title="Help", description=f"Cloudy, a multi-purpose bot made for Chroma.\nUse `{prefix}help [command|category|group]` for more info.", color=0x9E74FF)
        embed.set_thumbnail(url=channel.guild.icon)
        embed.set_footer(text=f"Requested by {author}", icon_url=author.avatar)
        for cog in self.bot.cogs:
            commands = self.bot.cogs[cog].get_commands()
            cog_name = getattr(self.bot.cogs[cog], "qualified_name", "Other")
            cog_description = getattr(self.bot.cogs[cog], "description", "Miscellaneous commands")
            if len(commands) == 0 or cog_name == "Other" or cog_name == "Jishaku" or cog_name == "Auto DM" or not cog_description:
                continue
            final_commands = []
            for command in commands:
                if command.hidden == False:
                    final_commands.append(command)
                if isinstance(command, discord.ext.commands.Group):
                    for command in command.commands:
                        final_commands.append(command)
            embed.add_field(name=f"{cog_name.capitalize()} [{len(final_commands)}]", value=cog_description, inline=False)

        return embed

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        cog_name = self.values[0].lower()
        if cog_name.lower() not in self.bot.cogs:
            channel = interaction.channel
            author = interaction.user
            embed = await self.get_init_page(channel, author)
        else:
            for name in self.bot.cogs:
                if name.lower() == cog_name.lower():
                    my_cog = self.bot.cogs[name]
            embed = await self.get_cog_help(my_cog)
        await interaction.edit_original_message(embed=embed)

class testView(discord.ui.Select):

    def __init__(self, commands: dict[commands.Cog, list[commands.Command]]):
        options=[discord.SelectOption(label="Home", description="Home Page")]
        super().__init__(
            placeholder='Select a category...',
            min_values=1,
            max_values=1,
            options=options
        )
        self.commands = commands
        self.add_my_options()

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.edit_original_message(content="hey")

class myView(discord.ui.View):
    def __init__(self, mapping, bot):
        super().__init__()
        # Adds the dropdown to our view object.
        self.add_item(HelpDropdown(mapping, bot))

class HelpCommand(commands.MinimalHelpCommand):
    
    def get_command_signature(self, command):
        channel = self.get_destination()
        try:
            with open("prefixes.json", "r") as f:
                prefixes = json.load(f)
            fix = prefixes[str(channel.guild.id)]
        except AttributeError:
            fix = '+'
        return '%s%s %s' % (fix, command.qualified_name, command.signature)

    def get_prefix(self):
        channel = self.get_destination()
        try:
            with open("prefixes.json", "r") as f:
                prefixes = json.load(f)
            fix = prefixes[str(channel.guild.id)]
        except AttributeError:
            fix = '+'
        return fix

    async def send_bot_help(self, mapping):
        prefix = self.get_prefix()
        channel = self.get_destination()
        author = self.context.author
        embed = discord.Embed(title="Help", description=f"Use `{prefix}help [command]` for more info on a command. You can also use `{prefix}help [category]` for more info on a category.\n\nThese are the different categories:", color=0x9E74FF)
        embed.set_thumbnail(url=channel.guild.icon)
        embed.set_footer(text=f"Requested by {author}", icon_url=author.avatar)
        for cog, commands in mapping.items():
            cog_name = getattr(cog, "qualified_name", "Other")
            cog_description = getattr(cog, "description", "Miscellaneous commands")
            if len(commands) == 0 or cog_name == "Auto DM" or cog_name == "Jishaku" or cog_name == "HelpCog" or cog_name == "Other" or not cog_description:
                continue
            final_commands = []
            for command in commands:
                if command.hidden == False:
                    final_commands.append(command)
                if isinstance(command, discord.ext.commands.Group):
                    for command in command.commands:
                        final_commands.append(command)
            embed.add_field(name=f"{cog_name.capitalize()} [{len(final_commands)}]", value=cog_description, inline=False)

        await channel.send(embed=embed, view=myView(mapping, self.context.bot))

    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command), color=0x9E74FF)
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_cog_help(self, cog):
        commands = cog.get_commands()
        embed = discord.Embed(title=f"{cog.qualified_name.capitalize()} Commands", color=0x9E74FF)
        for command in commands:
            embed.add_field(name=command.qualified_name, value=command.help)

        channel = self.get_destination()
        await channel.send(embed=embed)

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = HelpCommand()
        bot.help_command.cog = self
        
    def cog_unload(self):
        self.bot.help_command = self._original_help_command

async def setup(client: commands.Bot) -> None:
    await client.add_cog(HelpCog(client))