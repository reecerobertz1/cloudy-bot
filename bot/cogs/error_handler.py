import discord
import traceback
import sys
from discord.ext import commands
import aiohttp
from setup.config import webhook_url

class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.webhook = discord.Webhook.from_url(webhook_url, session = aiohttp.ClientSession())

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
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
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.MissingRole):
            await ctx.send("You don't have the required role(s) to run this command!")

        elif isinstance(error, commands.NotOwner):
            await ctx.reply("This command is only for the bot owner (not you!)")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"You are missing the {error.param.name} argument! To see required arguments for your current command do {ctx.prefix}help {ctx.command.qualified_name}")

        else:
            await ctx.send(f"I'm sorry! I ran into an error while trying to execute `{ctx.command}`, the developer has been notified!")
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            err = ''.join(traceback.format_exception(None, error, error.__traceback__))
            e = discord.Embed(title=f"Error occured while attempting to execute {ctx.command}", description=f"```py\n{err}```", color=0x303136)
            await self.webhook.send(embed=e)

async def setup(bot):
    await bot.add_cog(CommandErrorHandler(bot))