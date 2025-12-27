"""
Tests for TABLES_DATA structure validation.
"""
import pytest
from phoenix_command.tables.advanced_damage_tables.tables_data import TablesData
from phoenix_command.tables.advanced_damage_tables.advanced_damage_calculator import AdvancedDamageCalculator


class TestTablesDataStructure:
    """Test the structure and consistency of TABLES_DATA."""

    @pytest.fixture
    def tables_data(self):
        """Get TABLES_DATA for testing."""
        return TablesData.TABLES_DATA

    def test_epen_values_are_unique_and_strictly_increasing(self, tables_data):
        """Test that epen values don't repeat and strictly increase."""
        for table_id, table in tables_data.items():
            epen = table["epen"]

            # Check no duplicates
            assert len(epen) == len(set(epen)), \
                f"Table {table_id}: epen contains duplicate values"

            # Check strictly increasing
            for i in range(len(epen) - 1):
                assert epen[i] < epen[i + 1], \
                    f"Table {table_id}: epen values not strictly increasing at index {i}: {epen[i]} >= {epen[i + 1]}"

    def test_epen_length_matches_dc_length(self, tables_data):
        """Test that length of epen equals length of each dc array."""
        for table_id, table in tables_data.items():
            epen_length = len(table["epen"])
            dc_dict = table["dc"]

            for dc_level, dc_values in dc_dict.items():
                assert len(dc_values) == epen_length, \
                    f"Table {table_id}, DC {dc_level}: length mismatch - epen has {epen_length} values, dc has {len(dc_values)} values"

    def test_dc_values_do_not_decrease(self, tables_data):
        """Test that dc values don't decrease when parsed."""
        for table_id, table in tables_data.items():
            dc_dict = table["dc"]

            for dc_level, dc_values in dc_dict.items():
                parsed_values = [AdvancedDamageCalculator.parse_val(val) for val in dc_values]

                for i in range(len(parsed_values) - 1):
                    assert parsed_values[i] <= parsed_values[i + 1], \
                        f"Table {table_id}, DC {dc_level}: values decrease at index {i}: {dc_values[i]} ({parsed_values[i]}) > {dc_values[i + 1]} ({parsed_values[i + 1]})"

    def test_shock_keys_correspond_to_epen_values(self, tables_data):
        """Test that shock keys strictly correspond to epen values."""
        for table_id, table in tables_data.items():
            shock = table["shock"]
            epen = table["epen"]

            for shock_key in shock.keys():
                assert shock_key in epen, \
                    f"Table {table_id}: shock key {shock_key} not found in epen values"

    def test_shock_values_strictly_increase(self, tables_data):
        """Test that shock values strictly increase with key increase."""
        for table_id, table in tables_data.items():
            shock = table["shock"]

            if len(shock) < 2:
                continue  # Skip tables with 0 or 1 shock value

            sorted_keys = sorted(shock.keys())
            shock_values = [AdvancedDamageCalculator.parse_val(shock[key]) for key in sorted_keys]

            for i in range(len(shock_values) - 1):
                assert shock_values[i] < shock_values[i + 1], \
                    f"Table {table_id}: shock values not strictly increasing - key {sorted_keys[i]} has value {shock[sorted_keys[i]]} ({shock_values[i]}), key {sorted_keys[i + 1]} has value {shock[sorted_keys[i + 1]]} ({shock_values[i + 1]})"

    def test_organ_boundaries_correspond_to_epen(self, tables_data):
        """Test that organ start/end boundaries correspond to epen values."""
        for table_id, table in tables_data.items():
            organs = table["organs"]
            epen = table["epen"]

            for start, end, name, is_critical in organs:
                assert start in epen, \
                    f"Table {table_id}, organ '{name}': start boundary {start} not found in epen"
                assert end in epen, \
                    f"Table {table_id}, organ '{name}': end boundary {end} not found in epen"

    def test_organ_boundaries_do_not_overlap(self, tables_data):
        """Test that organ boundaries don't overlap (start of one != end of another)."""
        for table_id, table in tables_data.items():
            organs = table["organs"]

            # Collect all start and end boundaries
            starts = {start for start, end, name, is_critical in organs}
            ends = {end for start, end, name, is_critical in organs}

            # Check that no start coincides with an end (except if it's the same organ segment)
            overlaps = starts & ends

            # Need to verify these are not actual overlaps
            for overlap_point in overlaps:
                # Find organs that end at this point
                organs_ending = [(start, end, name) for start, end, name, _ in organs if end == overlap_point]
                # Find organs that start at this point
                organs_starting = [(start, end, name) for start, end, name, _ in organs if start == overlap_point]

                # It's only okay if it's a continuous segment of the same organ
                for end_start, end_end, end_name in organs_ending:
                    for start_start, start_end, start_name in organs_starting:
                        if end_name != start_name or end_end != start_start:
                            # This is a real overlap between different organs
                            assert False, \
                                f"Table {table_id}: organ '{end_name}' ends at {overlap_point} where organ '{start_name}' starts"

    def test_every_epen_value_falls_in_exactly_one_organ_range(self, tables_data):
        """Test that each epen value falls into exactly one organ range."""
        for table_id, table in tables_data.items():
            epen = table["epen"]
            organs = table["organs"]

            for epen_value in epen:
                matching_organs = []

                for start, end, name, is_critical in organs:
                    if start <= epen_value <= end:
                        matching_organs.append(name)

                assert len(matching_organs) == 1, \
                    f"Table {table_id}, epen value {epen_value}: found in {len(matching_organs)} organs ({matching_organs}), expected exactly 1"

    def test_organ_ranges_are_valid(self, tables_data):
        """Test that organ start <= end."""
        for table_id, table in tables_data.items():
            organs = table["organs"]

            for start, end, name, is_critical in organs:
                assert start <= end, \
                    f"Table {table_id}, organ '{name}': invalid range - start {start} > end {end}"

    def test_all_tables_have_required_keys(self, tables_data):
        """Test that all tables have required keys."""
        required_keys = {"epen", "shock", "organs", "dc"}

        for table_id, table in tables_data.items():
            assert set(table.keys()) == required_keys, \
                f"Table {table_id}: missing or extra keys. Expected {required_keys}, got {set(table.keys())}"

    def test_dc_levels_are_valid(self, tables_data):
        """Test that DC levels are between 1 and 10."""
        for table_id, table in tables_data.items():
            dc_dict = table["dc"]

            for dc_level in dc_dict.keys():
                assert 1 <= dc_level <= 10, \
                    f"Table {table_id}: invalid DC level {dc_level}, must be between 1 and 10"

    def test_organs_tuple_structure(self, tables_data):
        """Test that organs have correct tuple structure."""
        for table_id, table in tables_data.items():
            organs = table["organs"]

            for organ_tuple in organs:
                assert len(organ_tuple) == 4, \
                    f"Table {table_id}: organ tuple has {len(organ_tuple)} elements, expected 4 (start, end, name, is_critical)"

                start, end, name, is_critical = organ_tuple

                assert isinstance(start, (int, float)), \
                    f"Table {table_id}: organ start must be numeric, got {type(start)}"
                assert isinstance(end, (int, float)), \
                    f"Table {table_id}: organ end must be numeric, got {type(end)}"
                assert isinstance(name, str), \
                    f"Table {table_id}: organ name must be string, got {type(name)}"
                assert isinstance(is_critical, bool), \
                    f"Table {table_id}: is_critical must be boolean, got {type(is_critical)}"

