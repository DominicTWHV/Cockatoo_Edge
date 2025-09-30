import discord

from datetime import datetime, timezone

from edge.registry.colors import EmbedColors

class Owner:

    @staticmethod
    async def load_command_module_success(module: str) -> discord.Embed:
        embed = discord.Embed(
            title="Module Load",
            description=f"Successfully loaded command module `{module}`.",
            color=EmbedColors.green
        )
        embed.timestamp = datetime.now(timezone.utc)

        return embed

    @staticmethod
    async def load_command_module_failure(module: str, error: str) -> discord.Embed:
        embed = discord.Embed(
            title="Module Load",
            description=f"Failed to load command module `{module}`.\nError: {error}",
            color=EmbedColors.red
        )
        embed.timestamp = datetime.now(timezone.utc)

        return embed
    
    @staticmethod
    async def unload_command_module_success(module: str) -> discord.Embed:
        embed = discord.Embed(
            title="Module Unload",
            description=f"Successfully unloaded command module `{module}`.",
            color=EmbedColors.green
        )
        embed.timestamp = datetime.now(timezone.utc)

        return embed
    
    @staticmethod
    async def unload_command_module_failure(module: str, error: str) -> discord.Embed:
        embed = discord.Embed(
            title="Module Unload",
            description=f"Failed to unload command module `{module}`.\nError: {error}",
            color=EmbedColors.red
        )
        embed.timestamp = datetime.now(timezone.utc)

        return embed
    
    @staticmethod
    async def reload_command_module_success(module: str) -> discord.Embed:
        embed = discord.Embed(
            title="Module Reload",
            description=f"Successfully reloaded command module `{module}`.",
            color=EmbedColors.green
        )
        embed.timestamp = datetime.now(timezone.utc)

        return embed
    
    @staticmethod
    async def reload_command_module_failure(module: str, error: str) -> discord.Embed:
        embed = discord.Embed(
            title="Module Reload",
            description=f"Failed to reload command module `{module}`.\nError: {error}",
            color=EmbedColors.red
        )
        embed.timestamp = datetime.now(timezone.utc)

        return embed
    
    @staticmethod
    async def shutdown() -> discord.Embed:
        embed = discord.Embed(
            title="Shutdown",
            description="Shutting down Cockatoo Edge...",
            color=EmbedColors.orange
        )
        embed.timestamp = datetime.now(timezone.utc)

        return embed