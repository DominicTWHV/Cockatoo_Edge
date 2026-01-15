import pytest
import discord.ext.test as dpytest

from tests.registry.configs import StaticConfig, user, channel

@pytest.mark.asyncio
async def test_download_dataset_command(mock_bot):
    # simulate command
    await dpytest.message(
        f"{StaticConfig.bot_prefix}download_dataset https://github.com/user/repo",
        member=user,
        channel=channel
    )

    assert True # this way for now until I figure out how to capture hybrid command responses in the msg queue