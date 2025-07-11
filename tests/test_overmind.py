import pytest
from src.overmind import Overmind
from src.commander import CosmicCommander

def test_reflect():
    commander = CosmicCommander(5, 2)
    overmind = Overmind(commander)
    overmind.reflect()  # Should run without error
