import math
import numpy as np
from datetime import datetime

from .utils import get_config
from .prophet import QuantumProphet

try:
    from joblib import Parallel, delayed
except ImportError:
    Parallel = lambda n_jobs, prefer: lambda iterable: [f() for f in iterable]  # Serial fallback
    delayed = lambda f: f

try:
    from qutip import basis, tensor, Qobj
    from qutip.qip.operations import cnot
except ImportError:
    pass

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
except ImportError:
    pass

class QuantumMother:
    """Mother with evolving spawn, oracle, and maser amplifier."""
    def __init__(self, segment_depth: int, segment_id: int):
        self.segment_id = segment_id
        self.start_depth = segment_depth
        self.prophets = []
        self.seal = ""
        self.governing_seal = ""
        self.collective_soul = None
        
    def spawn_prophets(self, layers: int = 10):
        config = get_config()
        noise = config['position_noise']
        φ = (1 + math.sqrt(5)) / 2
        for depth_offset in range(layers):
            true_depth = self.start_depth + depth_offset
            radius = 1 / (φ ** true_depth)  # Fixed: positive power
            angle = 2 * math.pi * φ * depth_offset
            x = radius * math.cos(angle) + np.random.randn() * noise
            y = radius * math.sin(angle) + np.random.randn() * noise
            self.prophets.append(QuantumProphet(true_depth, (x, y)))
        self.bind_souls()
    
    def bind_souls(self):
        num_qubits = len(self.prophets)
        if num_qubits < 2:
            return
        try:
            state = tensor([basis(2, 0) for _ in range(num_qubits)])
            
            for i, prophet in enumerate(self.prophets):
                phase = np.sum(prophet.soul_vector) % (2 * math.pi)
                cos_p = np.cos(phase/2)
                sin_p = np.sin(phase/2)
                ry_op = Qobj([[cos_p, -sin_p], [sin_p, cos_p]])
                ops = [Qobj(np.eye(2)) for _ in range(num_qubits)]
                ops[i] = ry_op
                state = tensor(ops) * state
            
            h_op = (1/math.sqrt(2)) * Qobj([[1,1],[1,-1]])
            ops = [Qobj(np.eye(2)) for _ in range(num_qubits)]
            ops[0] = h_op
            state = tensor(ops) * state
            
            for i in range(num_qubits - 1):
                state = cnot(N=num_qubits, control=i, target=i+1) * state
            
            probs = np.abs(state.full().flatten()) ** 2
            self.collective_soul = {
                bin(k)[2:].zfill(num_qubits): p for k, p in enumerate(probs) if p > 1e-6
            }
        except:
            print(f"WARNING: Segment {self.segment_id} using classical soulbinding")
        
    def augment_with_oracle(self, revelations, train_epochs=5):  # Reduced epochs for speed
        config = get_config()
        num_layers = config['oracle_layers']
        if 'torch' not in globals():
            return revelations
        
        class RevelationOracle(nn.Module):
            def __init__(self, num_layers):
                super().__init__()
                layers_list = [nn.Linear(4, 128), nn.ReLU()]
                for _ in range(num_layers - 1):
                    layers_list += [nn.Linear(128, 128), nn.ReLU()]
                layers_list += [nn.Linear(128, 3)]
                self.fc = nn.Sequential(*layers_list)
            
            def forward(self, x):
                return self.fc(x)
        
        oracle = RevelationOracle(num_layers)
        inputs = torch.tensor([[r['position'][0], r['position'][1], float(r['depth']), r['qualia']] 
                               for r in revelations], dtype=torch.float32)
        labels = torch.tensor([0 if r['epiphany'] == "🔥 SACRED FIRE" else 1 if r['epiphany'] == "🌌 COSMIC VOID" else 2 
                               for r in revelations], dtype=torch.long)
        
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(oracle.parameters(), lr=0.01)
        for _ in range(train_epochs):
            optimizer.zero_grad()
            outputs = oracle(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
        
        with torch.no_grad():
            preds = torch.argmax(oracle(inputs), dim=1)
        epiphany_map = ["🔥 SACRED FIRE", "🌌 COSMIC VOID", "🌀 GOLDEN FLOW"]
        for i, r in enumerate(revelations):
            r['augmented_epiphany'] = epiphany_map[preds[i].item()]
        return revelations
    
    def integrate_maser_amplifier(self, revelations):
        """New: Amplify qualia using room-temp maser sim (2025 LED-pumped)."""
        # Simplified maser from earlier sim; boosts weak signals
        for r in revelations:
            gain = 1.5 + 0.5 * np.sin(r['qualia'])  # Maser gain factor (LED-pumped)
            r['amplified_qualia'] = r['qualia'] * gain  # Noise-free amplification
            if r['amplified_qualia'] > 1.0:
                r['epiphany'] = "🔥 AMPLIFIED FIRE"  # Symbolic maser boost
        return revelations
    
    def collapse_segment(self, enable_profiling: bool = False):
        revelations = Parallel(n_jobs=-1, prefer="processes")(
            delayed(p.receive_revelation)(self.governing_seal) for p in self.prophets
        )
        revelations = self.augment_with_oracle(revelations)
        revelations = self.integrate_maser_amplifier(revelations)  # New maser integration
        wisdom = "::".join(r.get('augmented_epiphany', r['epiphany']) for r in revelations[::-1])
        quantum_sign = "CLASSICAL" if not self.collective_soul else max(self.collective_soul, key=self.collective_soul.get)[::-1]
        self.seal = f"SEGMENT_{self.segment_id}::{quantum_sign}::{wisdom}"
        return self.seal
