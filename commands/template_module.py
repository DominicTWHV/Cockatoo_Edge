from discord.ext import commands
from discord.ext.commands import Context

from edge.registry.colors import EmbedColors

class Template(commands.Cog, name="template"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="test",
        description="A test command",
    )
    async def cmd_name(self, context: Context) -> None:

        pass

async def setup(bot) -> None:
    await bot.add_cog(Template(bot))