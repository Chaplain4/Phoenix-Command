"""Test script to verify damage calculation for all EPEN values"""

from phoenix_command.models.enums import AdvancedHitLocation
from phoenix_command.tables.advanced_damage_tables.damage_tabs import AdvancedDamageCalculator

# Test DC=5 for all EPEN values
location = AdvancedHitLocation.HEAD_GLANCE  # Table 1
dc = 5

# Table 1 data for reference
epen_thresholds = [0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]
dc5_values = [6, 15, 27, 43, 61, 83, 108, 135, 165, 198, 263, 289]
shock_values = {0.6: 10, 0.9: 20}

print("=" * 80)
print("DC=5, Table 1 (HEAD_GLANCE)")
print("=" * 80)
print()

print("Reference data:")
print(f"EPEN thresholds: {epen_thresholds}")
print(f"DC5 values:      {dc5_values}")
print(f"Shock values:    {shock_values}")
print()

# Test from FRONT
print("=" * 80)
print("SHOT FROM FRONT (LEFT TO RIGHT)")
print("=" * 80)
print(f"{'EPEN':<8} | {'Damage':<8} | {'Shock':<8} | {'Organs':<30} | {'Excess':<8}")
print("-" * 80)

for epen in epen_thresholds + [1.4, 1.5]:  # Add values beyond max to test pass-through
    result = AdvancedDamageCalculator.calculate_damage(location, dc, epen, is_front=True)
    organs_str = ", ".join(result.pierced_organs) if result.pierced_organs else "None"
    print(f"{epen:<8.1f} | {result.damage:<8} | {result.shock:<8} | {organs_str:<30} | {result.excess_epen:<8.2f}")

print()

# Test from REAR
print("=" * 80)
print("SHOT FROM REAR (RIGHT TO LEFT)")
print("=" * 80)
print(f"{'EPEN':<8} | {'Damage':<8} | {'Shock':<8} | {'Organs':<30} | {'Excess':<8}")
print("-" * 80)

for epen in epen_thresholds + [1.4, 1.5]:  # Add values beyond max to test pass-through
    result = AdvancedDamageCalculator.calculate_damage(location, dc, epen, is_front=False)
    organs_str = ", ".join(result.pierced_organs) if result.pierced_organs else "None"
    print(f"{epen:<8.1f} | {result.damage:<8} | {result.shock:<8} | {organs_str:<30} | {result.excess_epen:<8.2f}")

print()
print("=" * 80)
print("DETAILED ANALYSIS FOR EPEN=0.5 (REAR SHOT)")
print("=" * 80)
result = AdvancedDamageCalculator.calculate_damage(location, dc, 0.5, is_front=False)
print(f"EPEN: 0.5")
print(f"Bullet enters from right (threshold 1.3)")
print(f"Stop threshold: 1.3 - 0.5 = 0.8")
print(f"Bullet passes through thresholds: 1.3, 1.2, 1.1, 1.0, 0.9")
print(f"Bullet stops at threshold 0.8 (index 6)")
print(f"")
print(f"Expected damage: 289 (max) - 108 (at index 6) = 181")
print(f"Actual damage: {result.damage}")
print(f"")
print(f"Expected shock: 20 (max) - 10 (max unreached at 0.6) = 10")
print(f"Actual shock: {result.shock}")
print(f"")
print(f"Pierced organs: {result.pierced_organs}")
print(f"Excess EPEN: {result.excess_epen}")
