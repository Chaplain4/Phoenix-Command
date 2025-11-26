import random

from phoenix_command.models.enums import TargetExposure, AdvancedHitLocation


class Table1AdvancedDamageHitLocation:

    @classmethod
    def get_hit_location_front_rear(cls, exposure: TargetExposure) -> AdvancedHitLocation:
        """
        Generates a random roll internally and determines hit location.

        Logic:
        1. Looking/Firing Over Cover -> Uses specific d100 columns.
        2. Head/Body/Legs -> Uses "In The Open" column but restricts the random range
           to focus on those areas (Invented Logic based on table distribution).
        3. Other -> Uses full "In The Open" d1000 column (0-999).
        """

        # ---------------------------------------------------------
        # 1. LOGIC FOR COVER (d100 Tables)
        # ---------------------------------------------------------
        if exposure == TargetExposure.LOOKING_OVER_COVER:
            roll = random.randint(0, 99)
            if 0 <= roll <= 11: return AdvancedHitLocation.HEAD_GLANCE
            if 12 <= roll <= 77: return AdvancedHitLocation.FOREHEAD
            if 78 <= roll <= 99: return AdvancedHitLocation.EYE_NOSE
            return AdvancedHitLocation.MISS

        elif exposure == TargetExposure.FIRING_OVER_COVER:
            roll = random.randint(0, 99)
            if 0 <= roll <= 2: return AdvancedHitLocation.HEAD_GLANCE
            if 3 <= roll <= 16: return AdvancedHitLocation.FOREHEAD
            if 17 <= roll <= 21: return AdvancedHitLocation.EYE_NOSE
            if 22 <= roll <= 32: return AdvancedHitLocation.MOUTH
            if 33 <= roll <= 34: return AdvancedHitLocation.NECK_FLESH
            if 35 <= roll <= 36: return AdvancedHitLocation.NECK_THROAT
            if 37 <= roll <= 42: return AdvancedHitLocation.SHOULDER_GLANCE_LEFT
            if 43 <= roll <= 48: return AdvancedHitLocation.SHOULDER_GLANCE_RIGHT
            if 49 <= roll <= 52: return AdvancedHitLocation.SHOULDER_SOCKET_LEFT
            if 53 <= roll <= 56: return AdvancedHitLocation.SHOULDER_SOCKET_RIGHT
            if 57 <= roll <= 58: return AdvancedHitLocation.SHOULDER_LEFT
            if 59 <= roll <= 60: return AdvancedHitLocation.SHOULDER_RIGHT
            if 61 <= roll <= 61: return AdvancedHitLocation.ARM_GLANCE_LEFT
            if 62 <= roll <= 62: return AdvancedHitLocation.ARM_GLANCE_RIGHT
            if 63 <= roll <= 63: return AdvancedHitLocation.ARM_GLANCE_SHOULDER_LEFT
            if 64 <= roll <= 65: return AdvancedHitLocation.ARM_GLANCE_SHOULDER_RIGHT
            if 66 <= roll <= 66: return AdvancedHitLocation.ARM_FLESH_LEFT
            if 67 <= roll <= 68: return AdvancedHitLocation.ARM_FLESH_RIGHT
            if 69 <= roll <= 69: return AdvancedHitLocation.ARM_FLESH_SHOULDER_LEFT
            if 70 <= roll <= 71: return AdvancedHitLocation.ARM_FLESH_SHOULDER_RIGHT
            if 72 <= roll <= 72: return AdvancedHitLocation.ARM_BONE_SHOULDER_LEFT
            if 73 <= roll <= 74: return AdvancedHitLocation.ARM_BONE_SHOULDER_RIGHT
            if 75 <= roll <= 76: return AdvancedHitLocation.ELBOW_SHOULDER_LEFT
            if 77 <= roll <= 78: return AdvancedHitLocation.ELBOW_SHOULDER_RIGHT
            if 79 <= roll <= 79: return AdvancedHitLocation.FOREARM_FLESH_LUNG_LEFT
            if 80 <= roll <= 81: return AdvancedHitLocation.FOREARM_FLESH_LUNG_RIGHT
            if 82 <= roll <= 847: return AdvancedHitLocation.FOREARM_BONE_LUNG_LEFT
            if 85 <= roll <= 86: return AdvancedHitLocation.FOREARM_BONE_LUNG_RIGHT
            if 88 <= roll <= 90: return AdvancedHitLocation.HAND_BASE_OF_NECK_LEFT
            if 91 <= roll <= 93: return AdvancedHitLocation.HAND_BASE_OF_NECK_RIGHT
            if 94 <= roll <= 99: return AdvancedHitLocation.WEAPON_CRITICAL
            return AdvancedHitLocation.MISS

        # ---------------------------------------------------------
        # 2. LOGIC FOR "IN THE OPEN" (d1000 Table)
        # ---------------------------------------------------------
        else:
            # Determine the range for the random roll based on target
            if exposure == TargetExposure.HEAD:
                # Table 000-059 represents head/neck area
                roll = random.randint(0, 59)
            elif exposure == TargetExposure.BODY:
                # Table 060-533 represents shoulders, arms, torso, pelvis
                roll = random.randint(60, 533)
            elif exposure == TargetExposure.LEGS:
                # Table 534-999 represents hips and legs
                roll = random.randint(534, 999)
            elif exposure == TargetExposure.ARMS:
                # Table 060-166 represents shoulders, hands and arms with weapon
                roll = random.randint(60, 166)
            else:
                # Full table for general exposure
                roll = random.randint(0, 999)

            # Mapping Logic (Left column usually 1st range, Right column 2nd range)

            if 0 <= roll <= 4: return AdvancedHitLocation.HEAD_GLANCE
            if 5 <= roll <= 27: return AdvancedHitLocation.FOREHEAD
            if 28 <= roll <= 35: return AdvancedHitLocation.EYE_NOSE
            if 36 <= roll <= 53: return AdvancedHitLocation.MOUTH
            if 54 <= roll <= 56: return AdvancedHitLocation.NECK_FLESH
            if 57 <= roll <= 59: return AdvancedHitLocation.NECK_THROAT

            # Split Ranges Start Here
            if 60 <= roll <= 69: return AdvancedHitLocation.SHOULDER_GLANCE_LEFT
            if 70 <= roll <= 80: return AdvancedHitLocation.SHOULDER_GLANCE_RIGHT

            if 81 <= roll <= 87: return AdvancedHitLocation.SHOULDER_SOCKET_LEFT
            if 88 <= roll <= 94: return AdvancedHitLocation.SHOULDER_SOCKET_RIGHT

            if 95 <= roll <= 97: return AdvancedHitLocation.SHOULDER_LEFT
            if 98 <= roll <= 100: return AdvancedHitLocation.SHOULDER_RIGHT

            if 101 == roll: return AdvancedHitLocation.ARM_GLANCE_LEFT
            if 102 <= roll <= 103: return AdvancedHitLocation.ARM_GLANCE_RIGHT

            if 104 <= roll <= 105: return AdvancedHitLocation.ARM_GLANCE_SHOULDER_LEFT
            if 106 <= roll <= 108: return AdvancedHitLocation.ARM_GLANCE_SHOULDER_RIGHT

            if 109 <= roll <= 110: return AdvancedHitLocation.ARM_FLESH_LEFT
            if 111 <= roll <= 113: return AdvancedHitLocation.ARM_FLESH_RIGHT

            if 114 <= roll <= 115: return AdvancedHitLocation.ARM_FLESH_SHOULDER_LEFT
            if 116 <= roll <= 117: return AdvancedHitLocation.ARM_FLESH_SHOULDER_RIGHT

            if 118 <= roll <= 119: return AdvancedHitLocation.ARM_BONE_SHOULDER_LEFT
            if 120 <= roll <= 121: return AdvancedHitLocation.ARM_BONE_SHOULDER_RIGHT

            if 122 <= roll <= 124: return AdvancedHitLocation.ELBOW_SHOULDER_LEFT
            if 125 <= roll <= 128: return AdvancedHitLocation.ELBOW_SHOULDER_RIGHT

            if 129 <= roll <= 130: return AdvancedHitLocation.FOREARM_FLESH_LUNG_LEFT
            if 131 <= roll <= 132: return AdvancedHitLocation.FOREARM_FLESH_LUNG_RIGHT

            if 133 <= roll <= 137: return AdvancedHitLocation.FOREARM_BONE_LUNG_LEFT
            if 138 <= roll <= 143: return AdvancedHitLocation.FOREARM_BONE_LUNG_RIGHT

            if 144 <= roll <= 148: return AdvancedHitLocation.HAND_BASE_OF_NECK_LEFT
            if 149 <= roll <= 154: return AdvancedHitLocation.HAND_BASE_OF_NECK_RIGHT

            if 155 <= roll <= 166: return AdvancedHitLocation.WEAPON_CRITICAL
            if 167 <= roll <= 194: return AdvancedHitLocation.TORSO_GLANCE
            if 195 <= roll <= 207: return AdvancedHitLocation.BASE_OF_NECK
            if 208 <= roll <= 223: return AdvancedHitLocation.LUNG_RIB
            if 224 <= roll <= 241: return AdvancedHitLocation.LUNG
            if 242 <= roll <= 251: return AdvancedHitLocation.HEART
            if 252 <= roll <= 264: return AdvancedHitLocation.LIVER_RIB
            if 265 <= roll <= 272: return AdvancedHitLocation.LIVER
            if 273 <= roll <= 283: return AdvancedHitLocation.STOMACH_RIB
            if 284 <= roll <= 290: return AdvancedHitLocation.STOMACH
            if 291 <= roll <= 303: return AdvancedHitLocation.STOMACH_SPLEEN
            if 304 <= roll <= 312: return AdvancedHitLocation.STOMACH_KIDNEY
            if 313 <= roll <= 334: return AdvancedHitLocation.LIVER_KIDNEY
            if 335 <= roll <= 348: return AdvancedHitLocation.LIVER_SPINE
            if 349 <= roll <= 389: return AdvancedHitLocation.INTESTINES
            if 390 <= roll <= 416: return AdvancedHitLocation.SPINE
            if 417 <= roll <= 533: return AdvancedHitLocation.PELVIS

            # Legs split ranges
            if 534 <= roll <= 547: return AdvancedHitLocation.HIP_SOCKET_LEFT
            if 548 <= roll <= 561: return AdvancedHitLocation.HIP_SOCKET_RIGHT

            if 562 <= roll <= 583: return AdvancedHitLocation.LEG_GLANCE_LEFT
            if 584 <= roll <= 605: return AdvancedHitLocation.LEG_GLANCE_RIGHT

            if 606 <= roll <= 680: return AdvancedHitLocation.THIGH_FLESH_LEFT
            if 681 <= roll <= 755: return AdvancedHitLocation.THIGH_FLESH_RIGHT

            if 756 <= roll <= 774: return AdvancedHitLocation.THIGH_BONE_LEFT
            if 775 <= roll <= 793: return AdvancedHitLocation.THIGH_BONE_RIGHT

            if 794 <= roll <= 814: return AdvancedHitLocation.KNEE_LEFT
            if 815 <= roll <= 835: return AdvancedHitLocation.KNEE_RIGHT

            if 836 <= roll <= 855: return AdvancedHitLocation.SHIN_FLESH_LEFT
            if 856 <= roll <= 876: return AdvancedHitLocation.SHIN_FLESH_RIGHT

            if 877 <= roll <= 905: return AdvancedHitLocation.SHIN_BONE_LEFT
            if 906 <= roll <= 935: return AdvancedHitLocation.SHIN_BONE_RIGHT

            if 936 <= roll <= 967: return AdvancedHitLocation.FOOT_LEFT
            if 968 <= roll <= 999: return AdvancedHitLocation.FOOT_RIGHT

            return AdvancedHitLocation.MISS
