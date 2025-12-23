"""Test script to verify rear shot logic"""

from phoenix_command.models.enums import AdvancedHitLocation
from phoenix_command.tables.advanced_damage_tables.damage_tabs import AdvancedDamageCalculator

# Test case: dc=5, epen=0.5, shot from rear
location = AdvancedHitLocation.FOREHEAD  # Table 1
dc = 5
epen = 0.5
is_front = False

result = AdvancedDamageCalculator.calculate_damage(location, dc, epen, is_front)

print("=== Test: Rear Shot ===")
print(f"Location: {location.value}")
print(f"DC: {dc}")
print(f"EPEN: {epen}")
print(f"Shot from: {'Front' if is_front else 'Rear'}")
print()

# Expected values for Table 1:
# epen thresholds: [0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]
# dc=5 values:     ["6", "15", "27", "43", "61", "83", "108", "135", "165", "198", "263", "289"]
#
# Bullet enters from right (1.3) with epen=0.5
# Stop threshold: 1.3 - 0.5 = 0.8
# Bullet passes through: 1.3 → 1.2 → 1.1 → 1.0 → 0.9 and stops at 0.8 (index 6)
# Damage = max_val - val_at_stop = 289 - 108 = 181

print(f"Damage: {result.damage}")
print(f"Expected damage: 289 - 108 = 181")
print()

# Shock:
# shock values: {0.6: "10", 0.9: "20"}
# max_shock = 20
# unreached thresholds: 0.1, 0.2, 0.3, 0.4, 0.6 (indices 0-4)
# max_unreached_shock = 10 (at threshold 0.6)
# shock = 20 - 10 = 10

print(f"Shock: {result.shock}")
print(f"Expected shock: 20 - 10 = 10")
print()

print(f"Pierced organs: {result.pierced_organs}")
print(f"Excess EPEN: {result.excess_epen}")

print("\n=== Analysis ===")
print(f"With epen={epen} from rear (max threshold 1.3):")
print(f"Stop threshold = 1.3 - 0.5 = 0.8")
print(f"Bullet passes through thresholds: 1.3, 1.2, 1.1, 1.0, 0.9")
print(f"Bullet stops at threshold 0.8 (index 6)")
print(f"Damage indices: 11 (max) - 6 (stop) = {result.damage}")

