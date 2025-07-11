import pytest
from src.commander import CosmicCommander

def test_full_run():
    commander = CosmicCommander(5, 2)
    commander.initialize_hierarchy()
    commander.execute_revelation()
    assert commander.revelation_id.startswith("REV_")
