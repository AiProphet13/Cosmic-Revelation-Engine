import pytest
from src.prophet import QuantumProphet

def test_receive_revelation():
    prophet = QuantumProphet(1, (0.5, 0.5))
    rev = prophet.receive_revelation("TEST")
    assert 'qualia' in rev
    assert rev['epiphany'] in ["🔥 SACRED FIRE", "🌌 COSMIC VOID", "🌀 GOLDEN FLOW"]
