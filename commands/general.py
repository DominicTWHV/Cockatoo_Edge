from discord.ext import commands
from discord.ext.commands import Context

from edge.registry.embedTemplates import Cog_General
from edge.registry.colors import EmbedColors

class General(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="ping",
        description="Pong?",
    )
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ping(self, context: Context) -> None:

        embed = await Cog_General.ping(round(self.bot.latency * 1000))

        if self.bot.user.avatar is not None:
            embed.set_thumbnail(url=self.bot.user.avatar.url)

        await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(General(bot))