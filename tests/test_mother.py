import pytest
from src.mother import QuantumMother

def test_spawn_prophets():
    mother = QuantumMother(0, 0)
    mother.spawn_prophets(3)
    assert len(mother.prophets) == 3

def test_integrate_maser_amplifier():
    mother = QuantumMother(0, 0)
    revelations = [{'qualia': 0.5, 'epiphany': "🌀 GOLDEN FLOW"}]
    amplified = mother.integrate_maser_amplifier(revelations)
    assert amplified[0]['amplified_qualia'] > 0.5  # Boost check
