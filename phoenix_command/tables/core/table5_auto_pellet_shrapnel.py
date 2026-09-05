import random
from typing import List, Optional

# Shared fire table data (Table 5A)
_FIRE_TABLE = {
    0.000001: ["*3", "*4", "*5", "*6", "*7", "*8", "*9", "*10", "*12", "*18", "*36", "*54", "*72", "*144"],
    0.000002: ["*3", "*4", "*5", "*5", "*6", "*7", "*8", "*9", "*11", "*16", "*33", "*49", "*65", "*131"],
    0.000003: ["*2", "*3", "*4", "*5", "*6", "*6", "*7", "*8", "*9", "*14", "*28", "*43", "*57", "*114"],
    0.2: ["*2", "*3", "*3", "*4", "*5", "*5", "*6", "*7", "*8", "*12", "*25", "*37", "*50", "*99"],
    0.200001: ["*2", "*2", "*3", "*4", "*4", "*5", "*5", "*6", "*7", "*11", "*22", "*32", "*43", "*86"],
    0.200002: ["*2", "*2", "*3", "*3", "*4", "*4", "*5", "*5", "*6", "*9", "*19", "*28", "*37", "*75"],
    0.3: ["*1", "*2", "*2", "*3", "*3", "*4", "*4", "*5", "*5", "*8", "*16", "*24", "*33", "*65"],
    0.300001: ["*1", "*2", "*2", "*2", "*3", "*3", "*4", "*4", "*5", "*7", "*14", "*21", "*28", "*57"],
    0.4: ["*1", "*1", "*2", "*2", "*2", "*3", "*3", "*3", "*4", "*6", "*12", "*18", "*25", "*49"],
    0.400001: ["89", "*1", "*1", "*2", "*2", "*2", "*3", "*3", "*4", "*5", "*11", "*16", "*21", "*43"],
    0.5: ["77", "*1", "*1", "*2", "*2", "*2", "*2", "*3", "*3", "*5", "*9", "*14", "*19", "*37"],
    0.6: ["67", "89", "*1", "*1", "*2", "*2", "*2", "*2", "*3", "*4", "*8", "*12", "*16", "*32"],
    0.7: ["58", "78", "97", "*1", "*1", "*2", "*2", "*2", "*2", "*4", "*7", "*11", "*14", "*28"],
    0.8: ["51", "67", "84", "*1", "*1", "*1", "*2", "*2", "*2", "*3", "*6", "*9", "*12", "*24"],
    0.9: ["44", "58", "73", "88", "*1", "*1", "*1", "*1", "*2", "*3", "*5", "*8", "*11", "*21"],
    1: ["38", "51", "64", "77", "89", "*1", "*1", "*1", "*2", "*2", "*5", "*7", "*9", "*19"],
    1.000001: ["33", "44", "55", "66", "78", "89", "*1", "*1", "*1", "*2", "*4", "*6", "*8", "*16"],
    1.000002: ["28", "38", "48", "58", "67", "77", "87", "97", "*1", "*2", "*3", "*5", "*7", "*14"],
    1.000003: ["25", "33", "41", "50", "58", "67", "75", "84", "*1", "*2", "*3", "*5", "*6", "*12"],
    2: ["21", "29", "36", "43", "51", "58", "65", "73", "88", "*1", "*2", "*3", "*5", "*11"],
    2.000001: ["18", "25", "31", "38", "44", "50", "57", "63", "76", "*1", "*2", "*3", "*5", "*9"],
    2.000002: ["16", "21", "27", "33", "38", "44", "49", "55", "66", "*1", "*2", "*3", "*4", "*8"],
    3: ["14", "18", "23", "28", "33", "38", "43", "48", "57", "86", "*2", "*3", "*3", "*7"],
    3.000001: ["12", "16", "20", "24", "29", "33", "37", "41", "50", "75", "*2", "*2", "*3", "*6"],
    4: ["10", "14", "17", "21", "25", "28", "32", "36", "43", "65", "*1", "*2", "*3", "*5"],
    4.000001: ["9", "12", "15", "18", "21", "25", "28", "31", "37", "56", "*1", "*2", "*2", "*5"],
    5: ["7", "10", "13", "16", "18", "21", "24", "27", "32", "49", "98", "*1", "*2", "*4"],
    5.000001: ["6", "9", "11", "13", "16", "18", "21", "23", "28", "42", "85", "*1", "*2", "*3"],
    6: ["5", "7", "10", "12", "14", "16", "18", "20", "24", "37", "74", "*1", "*2", "*3"],
    7: ["5", "6", "8", "10", "12", "14", "15", "17", "21", "32", "64", "97", "*1", "*3"],
    8: ["4", "5", "7", "9", "10", "12", "13", "15", "18", "28", "56", "84", "*1", "*2"],
    10: ["3", "5", "6", "7", "9", "10", "11", "13", "16", "24", "48", "73", "98", "*2"],
    11: ["3", "4", "5", "6", "7", "9", "10", "11", "13", "21", "42", "64", "85", "*2"],
    13: ["2", "3", "4", "5", "6", "7", "8", "9", "12", "18", "36", "55", "74", "*1"],
    15: ["2", "3", "4", "4", "5", "6", "7", "8", "10", "15", "32", "48", "64", "*1"],
    17: ["1", "2", "3", "4", "5", "5", "6", "7", "8", "13", "27", "41", "56", "*1"],
    20: ["1", "2", "2", "3", "4", "5", "5", "6", "7", "11", "24", "36", "48", "97"],
    23: ["1", "1", "2", "3", "3", "4", "4", "5", "6", "10", "20", "31", "42", "85"],
    26: ["1", "1", "2", "2", "3", "3", "4", "4", "5", "8", "18", "27", "36", "73"],
    30: ["0", "1", "1", "2", "2", "3", "3", "3", "4", "7", "15", "23", "31", "64"],
    35: ["0", "1", "1", "1", "2", "2", "3", "3", "4", "6", "13", "20", "27", "55"],
    40: ["0", "0", "1", "1", "1", "2", "2", "2", "3", "5", "11", "17", "23", "48"],
    46: ["0", "0", "0", "1", "1", "1", "2", "2", "3", "4", "10", "15", "20", "42"],
    53: ["0", "0", "0", "1", "1", "1", "1", "2", "2", "4", "8", "13", "17", "37"],
    61: ["0", "0", "0", "0", "1", "1", "1", "1", "2", "3", "7", "11", "15", "31"],
    70: ["0", "0", "0", "0", "0", "1", "1", "1", "1", "2", "6", "9", "13", "27"],
    81: ["0", "0", "0", "0", "0", "0", "1", "1", "1", "2", "5", "8", "11", "23"],
    93: ["0", "0", "0", "0", "0", "0", "0", "0", "1", "2", "4", "7", "10", "20"],
    107: ["0", "0", "0", "0", "0", "0", "0", "0", "1", "1", "4", "6", "8", "17"],
    123: ["0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "3", "5", "7", "15"],
    142: ["0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "2", "4", "6", "13"],
    163: ["0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "2", "4", "5", "11"],
    188: ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "2", "3", "4", "10"],
}
_FIRE_COLUMNS = [3, 4, 5, 6, 7, 8, 9, 10, 12, 18, 36, 54, 72, 144]
_ARC_KEYS = sorted(_FIRE_TABLE.keys())


def _arc_base_row_index(arc_of_fire: float) -> int:
    """Return the row index (into _ARC_KEYS) for a given arc of fire.

    Each arc band may have multiple sub-rows (fractional keys).  The base row
    for an arc is the *last* sub-row in that band — i.e. the row with the
    lowest Index number in the book, which is the bottom of the arc's block.
    The ``size_modifier`` shift in the caller operates from this base.
    """
    # Find first key >= arc_of_fire
    first = None
    for i, k in enumerate(_ARC_KEYS):
        if k >= arc_of_fire:
            first = i
            break
    if first is None:
        raise ValueError("arc_of_fire too large")
    # Determine the band of that key (round to 1 decimal)
    band = round(_ARC_KEYS[first], 1)
    # Advance to the last key in the same band
    last = first
    while last + 1 < len(_ARC_KEYS) and round(_ARC_KEYS[last + 1], 1) == band:
        last += 1
    return last


def _resolve_5a_cell(arc_of_fire: float, rate_of_fire: float, size_modifier: int) -> str:
    """Shared lookup: returns the raw cell string from Table 5A."""
    row_index = _arc_base_row_index(arc_of_fire)
    shifted_index = row_index - size_modifier
    shifted_index = max(0, min(len(_ARC_KEYS) - 1, shifted_index))
    row = _FIRE_TABLE[_ARC_KEYS[shifted_index]]

    rof = min(rate_of_fire, 144)
    col_key = None
    for c in _FIRE_COLUMNS:
        if rof <= c:
            col_key = c
            break
    if col_key is None:
        raise ValueError("rate_of_fire too large")
    col_index = _FIRE_COLUMNS.index(col_key)
    return row[col_index]


class Table5AutoPelletShrapnel:

    @classmethod
    def ceil_key(cls, value: float, keys):
        for k in keys:
            if value <= k:
                return k
        raise ValueError("Value too large")

    @classmethod
    def get_fire_table_value5a(cls, arc_of_fire: float, rate_of_fire: float, size_modifier: int,
                                log: Optional[List[str]] = None) -> int:
        cell = _resolve_5a_cell(arc_of_fire, rate_of_fire, size_modifier)
        if cell.startswith("*"):
            hits = int(cell[1:])
            if log is not None:
                log.append(f"  [Table 5A] Arc: {arc_of_fire}, ROF: {rate_of_fire}, Size mod: {size_modifier}")
                log.append(f"    Cell: {cell} -> {hits} guaranteed hits")
            return hits
        threshold = int(cell)
        roll = random.randint(0, 99)
        hits = 1 if roll < threshold else 0
        if log is not None:
            log.append(f"  [Table 5A] Arc: {arc_of_fire}, ROF: {rate_of_fire}, Size mod: {size_modifier}")
            log.append(f"    Cell: {cell} ({threshold}% chance), Roll: {roll} -> {hits} hits")
        return hits

    @classmethod
    def get_fire_table_probability_5a(cls, arc_of_fire: float, rate_of_fire: float, size_modifier: int) -> tuple[int, int]:
        """Get burst fire hit probability without rolling.

        Returns:
            Tuple of (guaranteed_hits, probability_percent).
        """
        if arc_of_fire > _ARC_KEYS[-1]:
            return (0, 0)
        cell = _resolve_5a_cell(arc_of_fire, rate_of_fire, size_modifier)
        if cell.startswith("*"):
            return (int(cell[1:]), 0)
        return (0, int(cell))

    @classmethod
    def get_shrapnel_pellet_hits_5a(cls, base_shrapnel_pellet_hit_chance: float, is_guaranteed: bool,
                                 size_modifier: int) -> int:
        """
        Calculates the number of shrapnel/pellet hits based on base chance, guaranteed flag, and size modifier.

        Args:
            base_shrapnel_pellet_hit_chance: Base hit chance or guaranteed hits value (0-100).
            is_guaranteed: If True, search in guaranteed (*) values; else, in probability values.
            size_modifier: Adjustment for target size (positive: larger target, move left/higher; negative: smaller, move right/lower).

        Returns:
            Number of hits (0-58), either guaranteed or probabilistic (0/1).
        """
        full_values = [58, 44, 33, 25, 19, 14, 11, 8, 6, 5, 4, 3, 2, 2, 1, 87, 65, 49, 37, 28, 21, 15, 11, 8, 6, 4, 3,
                       2, 1, 1, 0]
        num_guaranteed = 15

        base = max(0.0, min(100.0, base_shrapnel_pellet_hit_chance))  # Clamp to 0-100

        if is_guaranteed:
            candidates = range(num_guaranteed)
            max_val = 58
        else:
            candidates = range(num_guaranteed, len(full_values))
            max_val = 87

        if base > max_val:
            base_index = 0 if is_guaranteed else num_guaranteed
        elif base <= full_values[-1]:
            base_index = len(full_values) - 1
        else:
            base_index = None
            for i in reversed(list(candidates)):
                if full_values[i] >= base:
                    base_index = i
                    break
            if base_index is None:
                base_index = list(candidates)[0]

        adjusted_index = base_index - size_modifier
        adjusted_index = max(0, min(len(full_values) - 1, adjusted_index))

        final_value = full_values[adjusted_index]
        final_is_guaranteed = adjusted_index < num_guaranteed

        if final_is_guaranteed:
            return min(58, final_value)
        else:
            rand = random.randint(0, 99)
            return 1 if rand < final_value else 0

    @classmethod
    def get_pellet_hit_probability_5a(cls, base_shrapnel_pellet_hit_chance: float, is_guaranteed: bool,
                                      size_modifier: int) -> tuple[int, int]:
        """
        Calculates the pellet hit probability without rolling.

        Args:
            base_shrapnel_pellet_hit_chance: Base hit chance or guaranteed hits value (0-100).
            is_guaranteed: If True, search in guaranteed (*) values; else, in probability values.
            size_modifier: Adjustment for target size.

        Returns:
            Tuple of (guaranteed_hits, probability_percent) where:
            - guaranteed_hits: Number of guaranteed hits (0 if not guaranteed)
            - probability_percent: Probability of 1 additional hit (0-100)
        """
        # Values: guaranteed (0-14), then probabilistic (15-30)
        full_values = [58, 44, 33, 25, 19, 14, 11, 8, 6, 5, 4, 3, 2, 2, 1, 87, 65, 49, 37, 28, 21, 15, 11, 8, 6, 4, 3,
                       2, 1, 1, 0]
        num_guaranteed = 15

        base = max(0.0, min(100.0, base_shrapnel_pellet_hit_chance))

        if is_guaranteed:
            candidates = range(num_guaranteed)
            max_val = 58
        else:
            candidates = range(num_guaranteed, len(full_values))
            max_val = 87

        if base > max_val:
            base_index = 0 if is_guaranteed else num_guaranteed
        elif base <= full_values[-1]:
            base_index = len(full_values) - 1
        else:
            base_index = None
            for i in reversed(list(candidates)):
                if full_values[i] >= base:
                    base_index = i
                    break
            if base_index is None:
                base_index = list(candidates)[0]

        # Apply size modifier: subtract to move left (higher values), add to move right (lower values)
        adjusted_index = base_index - size_modifier
        adjusted_index = max(0, min(len(full_values) - 1, adjusted_index))

        final_value = full_values[adjusted_index]
        final_is_guaranteed = adjusted_index < num_guaranteed

        if final_is_guaranteed:
            return (min(58, final_value), 0)
        else:
            return (0, min(100, final_value))

    @classmethod
    def get_scatter_distance_5c(cls, sa_difference: int) -> int:
        """
        Returns scatter distance in hexes based on difference in SA (Skill Accuracy).
        
        Args:
            sa_difference: Difference in SA (1-28)
            
        Returns:
            Scatter distance in hexes
        """
        table = [
            (7, 1),
            (11, 2),
            (13, 3),
            (15, 4),
            (17, 5),
            (19, 6),
            (21, 8),
            (22, 10),
            (23, 12),
            (24, 14),
            (25, 16),
            (26, 19),
            (27, 21),
            (28, 25),
        ]
        
        for max_sa, scatter in table:
            if sa_difference <= max_sa:
                return scatter
        
        return 25
