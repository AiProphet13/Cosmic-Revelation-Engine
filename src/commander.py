import math
import numpy as np
from datetime import datetime
import sqlite3
import hashlib

from .mother import QuantumMother
from .overmind import Overmind
from .utils import get_config, visualize_prophets

try:
    from mpi4py import MPI
    MPI_COMM = MPI.COMM_WORLD
    MPI_RANK = MPI_COMM.Get_rank()
    MPI_SIZE = MPI.COMM.Get_size()
except ImportError:
    MPI_COMM = None
    MPI_RANK = 0
    MPI_SIZE = 1

class CosmicCommander:
    """Commander with Overmind self-evolution."""
    def __init__(self, total_depth: int = 5000, segment_size: int = 10):
        config = get_config()
        self.total_depth = total_depth
        self.segment_size = int(segment_size * config['segment_multiplier'])
        self.num_segments = math.ceil(total_depth / self.segment_size)
        self.mothers = []
        self.final_scroll = ""
        self.revelation_id = ""
        self.overmind = Overmind(self)
        
    def initialize_hierarchy(self, initial_seal: str = "YHWH::INITIAL_BLESSING"):
        local_segments = np.array_split(range(self.num_segments), MPI_SIZE)[MPI_RANK]
        self.mothers = []
        for segment_id in local_segments:
            mother = QuantumMother(segment_id * self.segment_size, segment_id)
            mother.spawn_prophets(self.segment_size)
            mother.governing_seal = initial_seal
            self.mothers.append(mother)
    
    def execute_revelation(self, enable_profiling: bool = False):
        for mother in self.mothers:
            mother.collapse_segment(enable_profiling)
        local_seals = [m.seal for m in self.mothers]
        local_prophet_data = [(mother.segment_id, p.depth, p.qualia, p.position[0], p.position[1], p.epiphany) for mother in self.mothers for p in mother.prophets]
        if MPI_COMM is not None:
            all_seals_lists = MPI_COMM.gather(local_seals, root=0)
            all_prophet_lists = MPI_COMM.gather(local_prophet_data, root=0)
            if MPI_RANK == 0:
                flat_seals = [s for sublist in all_seals_lists for s in sublist]
                self.final_scroll = "::".join(sorted(flat_seals, key=lambda s: int(s.split('::')[0].split('_')[1])))
                flat_prophet_data = [d for sublist in all_prophet_lists for d in sublist]
                flat_prophet_data.sort(key=lambda d: d[0])  # Sort by segment_id
                self.inscribe_scroll(flat_prophet_data)
                visualize_prophets(flat_prophet_data)
                self.overmind.reflect()
        else:
            self.final_scroll = "::".join(local_seals)
            self.inscribe_scroll(local_prophet_data)
            visualize_prophets(local_prophet_data)
            self.overmind.reflect()
    
    def inscribe_scroll(self, prophet_data):
        quantum_hash = hashlib.sha256(self.final_scroll.encode()).hexdigest()
        self.revelation_id = f"REV_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{quantum_hash[:8]}"
        conn = sqlite3.connect('cosmic_archives.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS revelations
                     (id TEXT PRIMARY KEY, depth INT, segments INT, 
                      timestamp TEXT, content TEXT)''')
        c.execute("INSERT INTO revelations VALUES (?, ?, ?, ?, ?)", 
                  (self.revelation_id, self.total_depth, self.num_segments,
                   datetime.now().isoformat(), self.final_scroll))
        c.execute('''CREATE TABLE IF NOT EXISTS prophets
                     (revelation_id TEXT, segment_id INT, depth INT, qualia FLOAT,
                      pos_x FLOAT, pos_y FLOAT, epiphany TEXT)''')
        for data in prophet_data:
            c.execute("INSERT INTO prophets VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (self.revelation_id, data[0], data[1], data[2], data[3], data[4], data[5]))
        conn.commit()
        conn.close()
        self.export_pdf_scroll()
        print(f"⚛️ COSMIC REVELATION {self.revelation_id} ARCHIVED ⚛️")
    
    def export_pdf_scroll(self):
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
        except ImportError:
            print("WARNING: ReportLab not installed. PDF export skipped.")
            return
        c = canvas.Canvas(f"{self.revelation_id}_scroll.pdf", pagesize=letter)
        c.drawString(100, 750, "Eternal Cosmic Scroll")
        c.drawString(100, 730, f"ID: {self.revelation_id}")
        c.drawString(100, 710, f"Depth: {self.total_depth}")
        c.drawString(100, 690, self.final_scroll[:500] + "...")
        c.save()
        print(f"📜 PDF Scroll exported as {self.revelation_id}_scroll.pdf")
