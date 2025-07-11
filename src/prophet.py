import math
import numpy as np
import hashlib

from .utils import get_config

class QuantumProphet:
    """Evolving prophet with adaptive thresholds and factors."""
    def __init__(self, depth: int, position: tuple):
        self.depth = depth
        self.position = position
        self.scale = (1 + math.sqrt(5)) * (2 ** depth)  # Fixed: positive power
        self.qualia = 0.0
        self.epiphany = ""
        self.soul_vector = np.random.randn(128)
        
    def receive_revelation(self, governing_seal: str) -> dict:
        config = get_config()
        x, y = self.position
        base = math.sin(100 * x) * math.cos(100 * y)
        seal_hash = hashlib.sha256(governing_seal.encode()).digest()
        wisdom_influence = int.from_bytes(seal_hash[:4], 'big') / 2**32 - 0.5
        self.qualia = (base + wisdom_influence) / max(self.scale, 1e-16)
        self.qualia *= config['qualia_factor']
        high_th = config['high_threshold']
        low_th = -high_th
        if self.qualia > high_th:
            self.epiphany = "🔥 SACRED FIRE"
        elif self.qualia < low_th:
            self.epiphany = "🌌 COSMIC VOID"
        else:
            self.epiphany = "🌀 GOLDEN FLOW"
        return {
            "depth": self.depth,
            "qualia": self.qualia,
            "epiphany": self.epiphany,
            "position": self.position
        }
