import os
import sys
import platform

import signal
import asyncio

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context

from dotenv import load_dotenv

from edge.helper.DBFunctions import AutoDBMgr
from edge.helper.fileRead import FileHandler
from edge.helper.aiohttpSessionFactory import SessionFactory

from edge.registry.colors import EmbedColors
from edge.registry.version import Version

from edge.status.StatusManager import StatusDecider

from edge.logger.context import db_logger, cockatoo_logger

intents = discord.Intents.default()
intents.message_content = True

class CockatooEdge(commands.Bot): # main class
    def __init__(self) -> None:
        super().__init__(
            command_prefix="/", # use slash as prefix
            intents=intents,
            help_command=None,
            status=discord.Status.online, # set default online status
        )

        self.logger = cockatoo_logger
        self.db_logger = db_logger

    async def load_cogs(self) -> None:
        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/commands"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"commands.{extension}")
                    self.logger.info(f"Loaded command module '{extension}'")

                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    self.logger.error(f"Failed to load command module {extension}\n{exception}")

    @tasks.loop(minutes=5.0)
    async def status_task(self) -> None:
        await self.change_presence(activity=discord.Activity(type = discord.ActivityType.watching, name = await StatusDecider.decide_content()))

        #.change_presence(activity=discord.Game(name="a game"))
        #.change_presence(activity=discord.Streaming(name="stream name", url=twitch_url))
        #.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))
        #.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))

    @status_task.before_loop
    async def before_task(self) -> None:
        await self.wait_until_ready()
        self.logger.info(f"Waiting for background tasks to start up...")

    async def setup_hook(self) -> None:

        self.logger.info("Initializing bot...")
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(f"Running on: {platform.platform()} {platform.release()} ({os.name}) | Arch: {platform.machine()}")

        self.logger.info(f"Version: {Version.version} ({Version.version_raw}) | Commit: {await FileHandler.fetch_latest_git_commit()}")

        self.logger.info("-------------------\n")

        await AutoDBMgr.init_db() #initializes database instances, configured by edge.registry.database

        await SessionFactory().create_session() #initialize aiohttp session pool for global use

        await self.load_cogs()

        self.status_task.start()

        self.logger.info("Initialization complete.")

    # events ----------------------------------------------------------

    async def on_ready(self):
        self.logger.info(f"Bot initialized.")
        await self.wait_until_ready()

        self.logger.info(f"Syncing command tree...")
        await self.tree.sync()
        self.logger.info(f"Command tree has been synchronized.")

    # discord api hooks -----------------------------------------------

    # ==================================================================================================================

    async def on_member_join(self, member: discord.Member): #on member join
        pass

    async def on_member_ban(self, guild: discord.Guild, member: discord.User): #on member ban
        pass

    async def on_member_unban(self, guild: discord.Guild, member: discord.User): #on member unban
        pass

    async def on_member_update(self, before, after):
        pass

    # ==================================================================================================================

    async def on_message(self, message: discord.Message) -> None: #on message

        if message.author == self.user or message.author.bot:
            return
        
        #add message processing here
    
    async def on_message_delete(self, message: discord.Message): #on message delete
        pass

    async def on_message_edit(self, before: discord.Message, after: discord.Message): #on message edit
        pass

    # ==================================================================================================================

    async def on_command_completion(self, context: Context) -> None:

        full_command_name = context.command.qualified_name
        ref_url = context.message.jump_url
        if context.guild is not None:
            log_content = f"Executed `{full_command_name}` command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})\n[Jump to message]({ref_url})"
            
        else:
            log_content = f"Executed `{full_command_name}` command in DMs by {context.author} (ID: {context.author.id})"
        
        self.logger.info(log_content)

    async def on_command_error(self, context: Context, error) -> None:

        if isinstance(error, commands.CommandOnCooldown):

            self.logger.warning(f"{context.author} (ID: {context.author.id}) tried to execute the command `{context.command.qualified_name}` in the guild {context.guild.name} (ID: {context.guild.id}), but is on cooldown.")

        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                description="This command is owner only!", color=EmbedColors.red,
            )
            await context.send(embed=embed)

            if context.guild:
                self.logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the guild {context.guild.name} (ID: {context.guild.id}), but the user is not an owner of the bot."
                )
            else:
                self.logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the bot's DMs, but the user is not an owner of the bot."
                )

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="You are missing the permission(s) `" + ", ".join(error.missing_permissions) + "` to execute this command!",
                color=EmbedColors.red,
            )
            await context.send(embed=embed)

            self.logger.warning(
                f"{context.author} (ID: {context.author.id}) tried to execute the command `{context.command.qualified_name}` in the guild {context.guild.name} (ID: {context.guild.id}), but is missing the permission(s) {', '.join(error.missing_permissions)}."
            )

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                description="Cockatoo Edge is missing permission(s) `" + ", ".join(error.missing_permissions) + "` to fully perform this command!",
                color=EmbedColors.red,
            )

            await context.send(embed=embed)

            self.logger.warning(
                f"{context.author} (ID: {context.author.id}) tried to execute the command `{context.command.qualified_name}` in the guild {context.guild.name} (ID: {context.guild.id}), but the bot is missing the permission(s) {', '.join(error.missing_permissions)}."
            )

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Error!",
                description=str(error).capitalize(),
                color=EmbedColors.red,
            )
            await context.send(embed=embed)

            self.logger.warning(
                f"{context.author} (ID: {context.author.id}) tried to execute the command `{context.command.qualified_name}` in the guild {context.guild.name} (ID: {context.guild.id}), but is missing the required argument(s) {', '.join(error.missing_arguments)}."
            )

        else:

            embed = discord.Embed(
                title="Error!",
                description="Looks like we have an expected error. Please try again later!",
                color=EmbedColors.red,
            )

            await context.send(embed=embed)

            self.logger.error(
                f"An error occurred while executing the command `{context.command.qualified_name}` in the guild {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id}).",
                exc_info=error,
            )

load_dotenv()


# register signal handler for graceful shutdown on ctrl c
def signal_handler(_sig, _frame):
    try:
        cockatoo_logger.info("Shutting down. Bye!")
        loop = asyncio.get_running_loop()

        loop.create_task(SessionFactory().close_session()) #close aiohttp session
        loop.create_task(bot.close())
        loop.call_later(1, loop.stop)

    except Exception as e:
        cockatoo_logger.error(f"Error during shutdown procedure: {e}")
        sys.exit(1) #force exit if error occurs

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    bot = CockatooEdge()
    bot.run(os.getenv("TOKEN"))