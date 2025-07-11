import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_config():
    """Load persistent cosmic configuration."""
    try:
        with open('cosmic_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'qualia_factor': 1.0,
            'oracle_layers': 2,
            'position_noise': 0.0,
            'high_threshold': 0.7,
            'segment_multiplier': 1.0
        }

def visualize_prophets(prophet_data):
    """3D visualization function (moved from commander)."""
    x = [d[3] for d in prophet_data]
    y = [d[4] for d in prophet_data]
    z = [d[2] for d in prophet_data]  # qualia
    colors = z  # Use qualia for color
    sizes = [10 * d[1] for d in prophet_data]  # Scale by depth
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c=colors, s=sizes, cmap='viridis')
    ax.set_title(f"3D Cosmic Constellation")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Qualia')
    plt.savefig("constellation_3d.png")
    plt.close()
    print("🌌 3D Visualization saved as constellation_3d.png")
