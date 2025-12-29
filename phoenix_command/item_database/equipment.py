"""Database of standard equipment items."""

from phoenix_command.models.gear import Gear

EQUIPMENT_LIST = [
    Gear(name="Bayonet", weight=1.0, description="Standard bayonet attachment"),
    Gear(name="Binoculars", weight=2.0, description="Field binoculars"),
    Gear(name="Bipod", weight=1.0, description="Weapon bipod mount"),
    Gear(name="Canteen (full)", weight=2.5, description="Full water canteen"),
    Gear(name="Clothing", weight=5.0, description="Standard field clothing"),
    Gear(name="Entrenching Tool", weight=1.5, description="Folding shovel"),
    Gear(name="Field Radio", weight=12.0, description="Portable field radio"),
    Gear(name="Fighting Harness", weight=0.6, description="Combat harness"),
    Gear(name="Headset Communication", weight=1.0, description="Communication headset"),
    Gear(name="Holster", weight=0.4, description="Weapon holster"),
    Gear(name="Magazine Pouch (2 Mags)", weight=0.2, description="Pouch for 2 magazines"),
    Gear(name="Optical Scope", weight=2.5, description="Weapon optical scope"),
    Gear(name="Sling", weight=0.4, description="Weapon sling"),
    Gear(name="Smoke Grenade", weight=1.0, description="Smoke grenade"),
]

