from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from edge.registry.embedTemplates import Cog_Owner, General

class Owner(commands.Cog, name="owner"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_group(
        name='owner',
        description='Administrative commands',
    )
    async def owner(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            await context.send(embed=await General.specify_subcommand())

    @owner.command(
        name='load',
        description='Load a command module',
    )
    @app_commands.describe(cog='The name of the cog to load')
    @commands.is_owner()
    async def load(self, context: Context, cog: str) -> None:

        try:
            await self.bot.load_extension(f'cogs.{cog}')
        except Exception as e:
            await context.send(embed=await Cog_Owner.cog_load_fail(cog, str(e)))
            return
        await context.send(embed=await Cog_Owner.cog_load(cog))

    @owner.command(
        name='unload',
        description='Unloads a command module.',
    )
    @app_commands.describe(cog='The name of the cog to unload')
    @commands.is_owner()
    async def unload(self, context: Context, cog: str) -> None:
        try:
            await self.bot.unload_extension(f'cogs.{cog}')
        except Exception:
            await context.send(embed=await Cog_Owner.cog_unload_fail(cog))
            return
        await context.send(embed=await Cog_Owner.cog_unload(cog))

    @owner.command(
        name='reload',
        description='Reloads a command module.',
    )
    @app_commands.describe(cog='The name of the cog to reload')
    @commands.is_owner()
    async def reload(self, context: Context, cog: str) -> None:
        try:
            await self.bot.reload_extension(f'cogs.{cog}')
        except Exception:
            await context.send(embed=await Cog_Owner.cog_reload_fail(cog))
            return
        await context.send(embed=await Cog_Owner.cog_reload(cog))

    @owner.command(
        name='shutdown',
        description=' Shut down the bot.',
    )
    @commands.is_owner()
    async def shutdown(self, context: Context) -> None:
        embed = await Cog_Owner.shutdown()
        
        await context.send(embed=embed)
        await self.bot.close()

async def setup(bot) -> None:
    await bot.add_cog(Owner(bot))