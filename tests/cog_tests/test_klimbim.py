import discord.ext.test as dpytest
from antipetros_discordbot.engine.antipetros_bot import AntiPetrosBot
import pytest


@pytest.fixture
def klimbim_loaded_bot(test_bot, base_import_path):
    klimbim_import_path = '.'.join([base_import_path, 'general_cogs', 'klimbim_cog'])
    test_bot
    return test_bot


@pytest.mark.asyncio
async def test_flip_coin():
    bot = AntiPetrosBot()
    dpytest.configure(bot)
    await dpytest.message("$$ flip_coin")
