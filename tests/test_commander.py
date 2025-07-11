import pytest
from src.commander import CosmicCommander

@pytest.mark.slow
def test_execute_revelation():
    commander = CosmicCommander(10, 5)
    commander.initialize_hierarchy()
    commander.execute_revelation()
    assert commander.final_scroll
