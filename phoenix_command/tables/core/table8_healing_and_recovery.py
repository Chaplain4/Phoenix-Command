import random

from phoenix_command.models.enums import MedicalAid
from phoenix_command.models.recovery import Recovery


class Table8HealingAndRecovery:

    @classmethod
    def get_incapacitation_time_8b(cls, physical_damage_total: int) -> int:
        """Return incapacitation time in phases (fully self-contained version)."""

        INC_TABLE = {
            50: [4, 15, 29, 47, 73, 120],
            100: [25, 90, 150, 270, 420, 750],
            200: [90, 330, 630, 690, 1590, 2880],
            300: [600, 1980, 3780, 7200, 10800, 18000],
            450: [750, 2550, 10800, 14400, 25200, 43200],
            600: [1500, 10800, 18000, 32400, 50400, 90000],
            750: [7200, 21600, 39600, 68400, 104400, 190800],
            1000: [18000, 61200, 115200, 190800, 295200, 259200],
        }

        row_key = max(k for k in INC_TABLE.keys() if k <= physical_damage_total)

        r = random.randint(0, 9)
        if r == 0:
            col = 0
        elif 1 <= r <= 2:
            col = 1
        elif 3 <= r <= 5:
            col = 2
        elif 6 <= r <= 7:
            col = 3
        elif r == 8:
            col = 4
        else:  # r == 9
            col = 5

        return INC_TABLE[row_key][col]

    @classmethod
    def get_critical_time_period_and_recovery_chance_8a(cls, physical_damage: float, target_health: float) -> Recovery:
        # Конвертеры
        H = 1800  # 1 hour in pulses
        D = 43200  # 1 day in pulses
        M = 30  # 1 minute in pulses
        P = 1  # pulse stays pulse

        # Таблица уже в pulses
        TABLE = [
            (5, 17, 79 * H, 94, 25 * D, 96, 99 * D, 99, 99 * D, 99, 25 * D, 99),
            (10, 25, 75 * H, 89, 25 * D, 92, 99 * D, 99, 99 * D, 99, 25 * D, 99),
            (15, 30, 72 * H, 85, 25 * D, 89, 99 * D, 99, 99 * D, 99, 25 * D, 99),
            (20, 35, 68 * H, 81, 25 * D, 86, 25 * D, 96, 99 * D, 99, 25 * D, 99),
            (25, 38, 65 * H, 77, 25 * D, 82, 25 * D, 95, 99 * D, 99, 25 * D, 99),
            (30, 41, 62 * H, 73, 25 * D, 79, 25 * D, 94, 99 * D, 99, 25 * D, 99),
            (35, 43, 59 * H, 69, 25 * D, 76, 25 * D, 93, 25 * D, 97, 25 * D, 99),
            (40, 44, 56 * H, 66, 25 * D, 73, 25 * D, 92, 25 * D, 96, 25 * D, 99),
            (45, 46, 53 * H, 63, 25 * D, 70, 25 * D, 91, 25 * D, 96, 25 * D, 99),
            (50, 47, 51 * H, 60, 25 * D, 68, 25 * D, 90, 25 * D, 95, 25 * D, 99),
            (60, 48, 46 * H, 54, 25 * D, 63, 25 * D, 89, 25 * D, 94, 25 * D, 99),
            (70, 50, 41 * H, 49, 25 * D, 58, 25 * D, 87, 25 * D, 94, 25 * D, 99),
            (80, 51, 37 * H, 44, 25 * D, 54, 25 * D, 85, 25 * D, 92, 25 * D, 97),
            (90, 52, 34 * H, 40, 25 * D, 50, 25 * D, 83, 25 * D, 91, 25 * D, 96),
            (100, 53, 31 * H, 36, 25 * D, 46, 25 * D, 82, 25 * D, 90, 25 * D, 96),
            (200, 61, 11 * H, 12, 23 * D, 21, 25 * D, 67, 25 * D, 82, 25 * D, 92),
            (300, 65, 4 * H, 4, 19 * D, 10, 25 * D, 55, 25 * D, 74, 25 * D, 89),
            (400, 68, 93 * M, 1, 16 * D, 4, 25 * D, 45, 25 * D, 67, 25 * D, 85),
            (500, 70, 35 * M, 0, 13 * D, 2, 25 * D, 37, 25 * D, 61, 25 * D, 82),
            (600, 72, 13 * M, 0, 10 * D, 1, 25 * D, 30, 25 * D, 55, 25 * D, 79),
            (700, 73, 6 * M, 0, 8 * D, 0, 25 * D, 25, 25 * D, 50, 25 * D, 76),
            (800, 75, 5 * M, 0, 7 * D, 0, 25 * D, 20, 25 * D, 45, 25 * D, 73),
            (900, 76, 4 * M, 0, 6 * D, 0, 25 * D, 16, 25 * D, 41, 25 * D, 70),
            (1000, 77, 90 * P, 0, 5 * D, 0, 25 * D, 13, 25 * D, 37, 25 * D, 67),
            (2000, 84, 85 * P, 0, 15 * H, 0, 6 * D, 2, 25 * D, 13, 25 * D, 45),
            (3000, 88, 81 * P, 0, 2 * H, 0, 21 * H, 0, 5 * D, 5, 18 * H, 30),
            (4000, 91, 76 * P, 0, 22 * M, 0, 4 * H, 0, 18 * H, 2, 72 * H, 20),
            (5000, 93, 71 * P, 0, 6 * M, 0, 63 * M, 0, 5 * H, 1, 21 * H, 13),
            (6000, 95, 67 * P, 0, 4 * M, 0, 36 * M, 0, 3 * H, 0, 12 * H, 9),
            (7000, 96, 62 * P, 0, 87 * P, 0, 29 * M, 0, 2 * H, 0, 10 * H, 6),
            (8000, 98, 57 * P, 0, 75 * P, 0, 25 * M, 0, 2 * H, 0, 8 * H, 4),
            (9000, 99, 52 * P, 0, 67 * P, 0, 22 * M, 0, 2 * H, 0, 7 * H, 3),
            (12000, 102, 38 * P, 0, 57 * P, 0, 19 * M, 0, 95 * M, 0, 6 * H, 1),
            (16000, 105, 25 * P, 0, 44 * P, 0, 15 * M, 0, 75 * M, 0, 5 * H, 0),
        ]

        lookup = physical_damage * 10.0 / target_health

        closest_row = min(TABLE, key=lambda r: abs(r[0] - lookup))

        (
            dmg, healing_days,
            no_ctp, no_rr,
            fa_ctp, fa_rr,
            as_ctp, as_rr,
            fh_ctp, fh_rr,
            tc_ctp, tc_rr
        ) = closest_row

        aid_map = {
            MedicalAid.NO_AID: (no_ctp, no_rr),
            MedicalAid.FIRST_AID: (fa_ctp, fa_rr),
            MedicalAid.AID_STATION: (as_ctp, as_rr),
            MedicalAid.FIELD_HOSPITAL: (fh_ctp, fh_rr),
            MedicalAid.TRAUMA_CENTER: (tc_ctp, tc_rr),
        }

        return Recovery(float(healing_days), aid_map)
