from phoenix_command.models.enums import ShooterStance, TargetExposure, ExplosiveTarget


class Table2OddsOfHitting:

    @staticmethod
    def get_odds_of_hitting_2a(shot_accuracy: int, range_in_hexes: int) -> int:
        """
        Returns the odds of hitting (as int percentage) based on shot accuracy and range in hexes from the provided table.
        For intermediate shot accuracy values, selects the value corresponding to the largest shot accuracy level less than or equal to the input (floor).
        For intermediate range values, selects the value corresponding to the smallest range level greater than or equal to the input (ceiling).
        If shot_accuracy < -30, returns 0.
        If range_in_hexes > 300, returns 0.
        If range_in_hexes < 2, uses the value for range 2.
        """
        ranges = [2, 3, 4, 6, 7, 10, 20, 40, 70, 100, 200, 300]

        table = {
            -30: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            -28: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            -26: [2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            -24: [3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            -22: [5, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            -20: [7, 4, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            -18: [12, 6, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0],
            -16: [18, 9, 6, 3, 2, 1, 0, 0, 0, 0, 0, 0],
            -14: [27, 15, 9, 5, 4, 2, 0, 0, 0, 0, 0, 0],
            -12: [39, 22, 15, 7, 6, 3, 1, 0, 0, 0, 0, 0],
            -11: [46, 27, 18, 9, 7, 4, 1, 0, 0, 0, 0, 0],
            -10: [53, 33, 22, 12, 9, 5, 1, 0, 0, 0, 0, 0],
            -9: [60, 39, 27, 15, 12, 6, 2, 0, 0, 0, 0, 0],
            -8: [67, 46, 33, 18, 15, 7, 2, 1, 0, 0, 0, 0],
            -7: [74, 53, 39, 22, 18, 9, 3, 1, 0, 0, 0, 0],
            -6: [80, 60, 46, 27, 22, 12, 4, 1, 0, 0, 0, 0],
            -5: [86, 67, 53, 33, 27, 15, 5, 2, 0, 0, 0, 0],
            -4: [90, 74, 60, 39, 33, 18, 6, 2, 0, 0, 0, 0],
            -3: [94, 80, 67, 46, 39, 22, 7, 3, 1, 0, 0, 0],
            -2: [96, 86, 74, 53, 46, 27, 9, 4, 1, 0, 0, 0],
            -1: [98, 90, 80, 60, 53, 33, 12, 5, 1, 1, 0, 0],
            0: [100, 94, 86, 67, 60, 39, 15, 6, 2, 1, 0, 0],
            1: [100, 96, 90, 74, 67, 46, 18, 7, 2, 1, 0, 0],
            2: [100, 98, 94, 80, 74, 53, 22, 9, 3, 2, 0, 0],
            3: [100, 100, 96, 86, 80, 60, 27, 12, 4, 2, 0, 0],
            4: [100, 100, 98, 90, 86, 67, 33, 15, 5, 3, 1, 0],
            5: [100, 100, 100, 94, 90, 74, 39, 18, 6, 4, 1, 0],
            6: [100, 100, 100, 96, 94, 80, 46, 22, 7, 5, 1, 0],
            7: [100, 100, 100, 98, 96, 86, 53, 27, 9, 6, 2, 1],
            8: [100, 100, 100, 100, 98, 90, 60, 33, 12, 7, 2, 1],
            9: [100, 100, 100, 100, 100, 94, 67, 39, 15, 9, 3, 1],
            10: [100, 100, 100, 100, 100, 96, 74, 46, 18, 12, 4, 2],
            11: [100, 100, 100, 100, 100, 98, 80, 53, 22, 15, 5, 2],
            12: [100, 100, 100, 100, 100, 100, 86, 60, 27, 18, 6, 3],
            13: [100, 100, 100, 100, 100, 100, 90, 67, 33, 22, 7, 4],
            14: [100, 100, 100, 100, 100, 100, 94, 74, 39, 27, 9, 5],
            15: [100, 100, 100, 100, 100, 100, 96, 80, 46, 33, 12, 6],
            16: [100, 100, 100, 100, 100, 100, 98, 86, 53, 39, 15, 7],
            17: [100, 100, 100, 100, 100, 100, 100, 90, 60, 46, 18, 9],
            18: [100, 100, 100, 100, 100, 100, 100, 94, 67, 53, 22, 12],
            19: [100, 100, 100, 100, 100, 100, 100, 96, 74, 60, 27, 15],
            20: [100, 100, 100, 100, 100, 100, 100, 98, 80, 67, 33, 18],
            21: [100, 100, 100, 100, 100, 100, 100, 100, 86, 74, 39, 22],
            22: [100, 100, 100, 100, 100, 100, 100, 100, 90, 80, 46, 27],
            23: [100, 100, 100, 100, 100, 100, 100, 100, 94, 86, 53, 33],
            24: [100, 100, 100, 100, 100, 100, 100, 100, 96, 90, 60, 39],
            25: [100, 100, 100, 100, 100, 100, 100, 100, 98, 94, 67, 46],
            26: [100, 100, 100, 100, 100, 100, 100, 100, 100, 96, 74, 53],
            27: [100, 100, 100, 100, 100, 100, 100, 100, 100, 98, 80, 60],
            28: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 86, 67],
            29: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 90, 74],
            30: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 94, 80],
            31: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 96, 86],
            32: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 98, 90],
            33: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 94],
            34: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 96]
        }

        acc_levels = sorted(table.keys(), reverse=True)

        # Find floor for shot_accuracy
        floor_acc = None
        for level in acc_levels:
            if level <= shot_accuracy:
                floor_acc = level
                break

        if floor_acc is None:
            return 0

        row = table[floor_acc]

        if range_in_hexes < 2:
            range_in_hexes = 2

        for i in range(len(ranges)):
            if ranges[i] >= range_in_hexes:
                ceil_range_index = i
                break
        else:
            return 0

        return row[ceil_range_index]

    @staticmethod
    def get_multiple_hits_2b(target_range: int, rate_of_fire: int) -> int:

        """
        Returns the number of hits based on target range and rate of fire from the provided table.
        For intermediate target range values, selects the value corresponding to the smallest range level greater than or equal to the input (ceiling).
        For rate of fire:
        - If 4 <= rate_of_fire <= 8: uses the first column (Rate of Fire 4-8).
        - If 9 <= rate_of_fire <= 15: uses the second column (Rate of Fire 9-15).
        - If rate_of_fire >= 16: uses the third column (Rate of Fire 16+).
        - If rate_of_fire < 4: raises ValueError.
        If target_range < 10: uses the value for 10.
        """

        range_levels = [10, 15, 20, 25, 35, 45, 60]
        table = {
            10: [3, 5, 8],
            15: [2, 5, 7],
            20: [2, 4, 6],
            25: [2, 3, 5],
            35: [1, 2, 4],
            45: [1, 2, 3],
            60: [1, 1, 2]
        }
        # For 60+, all values are 1
        sixty_plus = [1, 1, 1]

        if rate_of_fire < 4:
            raise ValueError("Rate of fire must be at least 4.")

        # Determine column index based on rate_of_fire
        if 4 <= rate_of_fire <= 8:
            col_index = 0
        elif 9 <= rate_of_fire <= 15:
            col_index = 1
        else:  # >= 16
            col_index = 2

        # Handle target_range
        if target_range < 10:
            target_range = 10

        if target_range > 60:
            return sixty_plus[col_index]

        # Find ceiling range level
        ceil_range_index = 0
        for i in range(len(range_levels)):
            if range_levels[i] >= target_range:
                ceil_range_index = i
                break

        row = table[range_levels[ceil_range_index]]
        return row[col_index]

    @staticmethod
    def get_shot_accuracy_modifier(
            shooter_stance: ShooterStance,
            shooter_moving: bool,
            target_moving: bool,
            target_exposure: TargetExposure,  # Using exposure enum
            firing_through_smoke: bool,
            explosive_target: ExplosiveTarget | None
    ) -> int:
        """
        Calculates the total shot accuracy modifier as the sum of applicable modifiers from the table.
        If explosive_target is provided (not None), uses the explosive weapon target size modifier
        and ignores the target_exposure modifier. Assumes firing through smoke without ultrasonics (-14 penalty).
        Raises ValueError for invalid enum values.
        """
        # Validate enums
        try:
            stance_mod = shooter_stance.value
            exposure_mod = target_exposure.value
        except AttributeError:
            raise ValueError("Invalid ShooterStance or TargetExposure enum value.")

        total = stance_mod

        if shooter_moving:
            total += -10

        if target_moving:
            total += -5

        if firing_through_smoke:
            total += -14  # Assuming without ultrasonics; adjust if with ultrasonics is intended (-4)

        if explosive_target is not None:
            # Validate explosive enum
            try:
                explosive_mod = explosive_target.value
            except AttributeError:
                raise ValueError("Invalid ExplosiveTarget enum value.")
            total += explosive_mod
            # Skip target exposure when explosive_target is used
        else:
            total += exposure_mod

        return total
