from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from edge.registry.colors import EmbedColors

class SetManager(commands.Cog, name="set_manager"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="download_dataset",
        description="Download a dataset from GitHub or a URL"
    )
    @app_commands.describe(url='URL in the form of https://github.com/<user>/<repo>/ or https://domain.com/file.txt')
    async def download_dataset(self, context: Context, url: str) -> None:

        await context.send(f"This is a placeholder for the completion of the download_dataset command. URL: {url}")

async def setup(bot) -> None:
    await bot.add_cog(SetManager(bot))