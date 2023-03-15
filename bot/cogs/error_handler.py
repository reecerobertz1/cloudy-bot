import discord
import traceback
import sys
from discord.ext import commands
import aiohttp
from setup.config import webhook_url
from utils.subclasses import Context

class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.webhook = discord.Webhook.from_url(webhook_url, session = aiohttp.ClientSession())
        self.color = 0xe63241

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: commands.CommandError):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(title="Error", description=f"```py\nDisabled Command```\nThis command is disabled.", color=self.color)
            await ctx.reply(embed=embed, mention_author=False) 

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Error", description=f"```py\nMissing Required Argument: {error.param.name}```\nTo see the required argument for your current command do {ctx.prefix}help {ctx.command.qualified_name}", color=self.color)
            await ctx.reply(embed=embed, mention_author=False)

        elif isinstance(error, commands.MissingRole):
            embed = discord.Embed(title="Error", description=f"```py\nMissing Role```\nYou don't have the required role(s) to run this command!", color=self.color)
            await ctx.reply(embed=embed, mention_author=False)

        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(title="Error", description=f"```py\nNot owner```\nTo run this command you have to be the owner of the bot.", color=self.color)
            await ctx.reply(embed=embed, mention_author=False)

        elif isinstance(error, commands.UserNotFound):
            embed = discord.Embed(title="Error", description=f"```py\nUser Not Found```\nI can't find that user!", color=self.color)
            await ctx.reply(embed=embed, mention_author=False)

        elif isinstance(error, commands.UserNotFound):
            embed = discord.Embed(title="Error", description=f"```py\nMember Not Found```\nI can't find that member!", color=self.color)
            await ctx.reply(embed=embed, mention_author=False)

        else:
            await ctx.send(f"I'm sorry! I ran into an error while trying to execute `{ctx.command}`, the developer has been notified!")
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            err = ''.join(traceback.format_exception(None, error, error.__traceback__))
            e = discord.Embed(title=f"Error occured while attempting to execute {ctx.command}", description=f"```py\n{err}```", color=0x303136)
            await self.webhook.send(embed=e)

async def setup(bot):
    await bot.add_cog(CommandErrorHandler(bot))