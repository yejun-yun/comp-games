"""
Improved Pokemon Dex with Accuracy, Priority, and Recoil

Each Pokemon now has genuine strategic choices between moves!
"""

from battle_v2 import PokemonSpec, MoveSpec

DEX_V2 = [
    # Flameling - Balanced attacker with choice: reliability vs power
    PokemonSpec(
        name="Flameling",
        type="Fire",
        max_hp=60,
        attack=18,
        defense=10,
        speed=14,
        moves=[
            MoveSpec(name="Ember", type="Fire", base_power=16, accuracy=100),  # Reliable
            MoveSpec(name="Fire Blast", type="Fire", base_power=24, accuracy=85),  # Risky power
        ],
    ),
    
    # Aquaff - Balanced with choice: reliable vs disruptive
    PokemonSpec(
        name="Aquaff",
        type="Water",
        max_hp=65,
        attack=16,
        defense=12,
        speed=12,
        moves=[
            MoveSpec(name="Scald", type="Water", base_power=16, accuracy=100),  # Reliable
            MoveSpec(name="Hydro Pump", type="Water", base_power=22, accuracy=80),  # Power play
        ],
    ),
    
    # Leaflet - Setup vs immediate damage
    PokemonSpec(
        name="Leaflet",
        type="Grass",
        max_hp=55,
        attack=17,
        defense=11,
        speed=13,
        moves=[
            MoveSpec(name="Razor Leaf", type="Grass", base_power=14, accuracy=95),  # Safe
            MoveSpec(name="Solar Beam", type="Grass", base_power=26, accuracy=100),  # No drawback but strong
        ],
    ),
    
    # Bulkwall - Tank with choice: power vs coverage
    PokemonSpec(
        name="Bulkwall",
        type="Normal",
        max_hp=80,
        attack=14,
        defense=16,
        speed=8,
        moves=[
            MoveSpec(name="Body Slam", type="Normal", base_power=17, accuracy=100),  # Reliable
            MoveSpec(name="Giga Impact", type="Normal", base_power=28, accuracy=90),  # High risk/reward
        ],
    ),
    
    # Sparkit - Glass cannon with recoil vs priority
    PokemonSpec(
        name="Sparkit",
        type="Fire",
        max_hp=50,
        attack=19,
        defense=9,
        speed=16,
        moves=[
            MoveSpec(name="Flare Blitz", type="Fire", base_power=26, accuracy=100, recoil_percent=33),  # High risk
            MoveSpec(name="Quick Attack", type="Normal", base_power=8, priority=1),  # Priority finisher
        ],
    ),
    
    # Torrento - Bulky water with mixed options
    PokemonSpec(
        name="Torrento",
        type="Water",
        max_hp=70,
        attack=15,
        defense=14,
        speed=10,
        moves=[
            MoveSpec(name="Aqua Jet", type="Water", base_power=10, priority=1),  # Priority
            MoveSpec(name="Waterfall", type="Water", base_power=18, accuracy=100),  # Standard
        ],
    ),
    
    # Sprouty - Fast grass with choice
    PokemonSpec(
        name="Sprouty",
        type="Grass",
        max_hp=58,
        attack=16,
        defense=12,
        speed=15,
        moves=[
            MoveSpec(name="Bullet Seed", type="Grass", base_power=12, accuracy=100),  # Consistent
            MoveSpec(name="Wood Hammer", type="Grass", base_power=24, accuracy=100, recoil_percent=33),  # Power + recoil
        ],
    ),
    
    # Stonecub - Tank with choice between power and priority
    PokemonSpec(
        name="Stonecub",
        type="Normal",
        max_hp=75,
        attack=15,
        defense=15,
        speed=9,
        moves=[
            MoveSpec(name="Rock Slide", type="Normal", base_power=18, accuracy=90),  # Risky power
            MoveSpec(name="Mach Punch", type="Normal", base_power=10, priority=1),  # Priority
        ],
    ),
]

