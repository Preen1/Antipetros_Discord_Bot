import pytest
from discord.ext import commands
from antipetros_discordbot.engine.antipetros_bot import AntiPetrosBot


@pytest.fixture
def test_bot():
    return AntiPetrosBot(is_test=True)


@pytest.fixture
def base_import_path():
    return "antipetros_discordbot.cogs"
