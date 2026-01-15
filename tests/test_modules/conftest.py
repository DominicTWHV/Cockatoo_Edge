import pytest

import discord.ext.test as dpytest

from unittest.mock import AsyncMock

from main import CockatooEdge

@pytest.fixture
async def mock_bot():
    bot_instance = CockatooEdge()

    # config dpytest
    dpytest.configure(bot_instance)

    # explicitly run a setup_hook to get the asyncio loop going
    await bot_instance._async_setup_hook()

    #then initialize normally so databases/whatever are available
    await bot_instance.setup_hook()

    bot_instance.tree.sync = AsyncMock(return_value=[]) #mock sync to do nothing
    
    yield bot_instance 
    
    await dpytest.empty_queue()