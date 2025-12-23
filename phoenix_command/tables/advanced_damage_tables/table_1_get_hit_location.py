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

    @classmethod
    def get_hit_location_oblique(cls, exposure: TargetExposure) -> AdvancedHitLocation:
        """
        Generates a random roll for OBLIQUE fire (Table 4F).
        """

        # ---------------------------------------------------------
        # 1. LOGIC FOR COVER (d100 Tables)
        # ---------------------------------------------------------
        if exposure == TargetExposure.LOOKING_OVER_COVER:
            roll = random.randint(0, 99)
            if 0 <= roll <= 10: return AdvancedHitLocation.HEAD_GLANCE
            if 11 <= roll <= 81: return AdvancedHitLocation.FOREHEAD_SIDE
            if 82 <= roll <= 99: return AdvancedHitLocation.EYE_NOSE
            return AdvancedHitLocation.MISS

        elif exposure == TargetExposure.FIRING_OVER_COVER:
            roll = random.randint(0, 99)
            if 0 <= roll <= 2: return AdvancedHitLocation.HEAD_GLANCE
            if 3 <= roll <= 15: return AdvancedHitLocation.FOREHEAD_SIDE
            if 16 <= roll <= 19: return AdvancedHitLocation.EYE_NOSE
            if 20 <= roll <= 29: return AdvancedHitLocation.MOUTH
            if 30 <= roll <= 31: return AdvancedHitLocation.NECK_THROAT_SIDE
            if 32 <= roll <= 33: return AdvancedHitLocation.NECK_SPINE_SIDE

            # Shoulders (Split cols)
            if 34 <= roll <= 38: return AdvancedHitLocation.SHOULDER_GLANCE_LEFT
            if 39 <= roll <= 44: return AdvancedHitLocation.SHOULDER_GLANCE_RIGHT

            if 45 <= roll <= 48: return AdvancedHitLocation.SHOULDER_SOCKET_LEFT
            if 49 <= roll <= 52: return AdvancedHitLocation.SHOULDER_SOCKET_RIGHT

            if 53 <= roll <= 53: return AdvancedHitLocation.SHOULDER_LEFT
            if 54 <= roll <= 55: return AdvancedHitLocation.SHOULDER_RIGHT
            if 56 <= roll <= 58: return AdvancedHitLocation.ARM_GLANCE_LEFT
            if 59 <= roll <= 61: return AdvancedHitLocation.ARM_GLANCE_RIGHT

            # Arm Flesh (Off side / Shot Side - Oblique uses rows usually)
            if 62 <= roll <= 65: return AdvancedHitLocation.ARM_FLESH_OFF_SIDE
            if 66 <= roll <= 69: return AdvancedHitLocation.ARM_FLESH_SHOT_SIDE

            if 70 <= roll <= 71: return AdvancedHitLocation.ARM_BONE_OFF_SIDE
            if 72 <= roll <= 73: return AdvancedHitLocation.ARM_BONE_SHOT_SIDE

            if 74 <= roll <= 75: return AdvancedHitLocation.ELBOW_LEFT  # "Elbow" in table
            if 76 <= roll <= 78: return AdvancedHitLocation.ELBOW_RIGHT

            if 79 <= roll <= 79: return AdvancedHitLocation.FOREARM_FLESH_LEFT
            if 80 <= roll <= 81: return AdvancedHitLocation.FOREARM_FLESH_RIGHT

            if 82 <= roll <= 83: return AdvancedHitLocation.FOREARM_BONE_LEFT
            if 84 <= roll <= 86: return AdvancedHitLocation.FOREARM_BONE_RIGHT

            if 87 <= roll <= 88: return AdvancedHitLocation.HAND_LEFT
            if 89 <= roll <= 91: return AdvancedHitLocation.HAND_RIGHT

            if 92 <= roll <= 99: return AdvancedHitLocation.WEAPON_CRITICAL
            return AdvancedHitLocation.MISS

        # ---------------------------------------------------------
        # 2. LOGIC FOR "IN THE OPEN" (d1000 Table) - OBLIQUE
        # ---------------------------------------------------------
        else:
            # Determine the range for the random roll based on target
            if exposure == TargetExposure.HEAD:
                roll = random.randint(0, 63)
            elif exposure == TargetExposure.BODY:
                roll = random.randint(64, 498)
            elif exposure == TargetExposure.LEGS:
                roll = random.randint(499, 999)
            elif exposure == TargetExposure.ARMS:
                roll = random.randint(64, 195)
            else:
                roll = random.randint(0, 999)

            # Hit Location Mapping (Table 4F)
            if 0 <= roll <= 5: return AdvancedHitLocation.HEAD_GLANCE
            if 6 <= roll <= 29: return AdvancedHitLocation.FOREHEAD_SIDE
            if 30 <= roll <= 37: return AdvancedHitLocation.EYE_NOSE
            if 38 <= roll <= 55: return AdvancedHitLocation.MOUTH
            if 56 <= roll <= 59: return AdvancedHitLocation.NECK_THROAT_SIDE
            if 60 <= roll <= 63: return AdvancedHitLocation.NECK_SPINE_SIDE

            # Shoulders
            if 64 <= roll <= 73: return AdvancedHitLocation.SHOULDER_GLANCE_LEFT
            if 74 <= roll <= 84: return AdvancedHitLocation.SHOULDER_GLANCE_RIGHT

            if 85 <= roll <= 91: return AdvancedHitLocation.SHOULDER_SOCKET_LEFT
            if 92 <= roll <= 99: return AdvancedHitLocation.SHOULDER_SOCKET_RIGHT

            if 100 <= roll <= 101: return AdvancedHitLocation.SHOULDER_LEFT
            if 102 <= roll <= 104: return AdvancedHitLocation.SHOULDER_RIGHT

            # Arms - Glance
            if 105 <= roll <= 110: return AdvancedHitLocation.ARM_GLANCE_LEFT
            if 111 <= roll <= 116: return AdvancedHitLocation.ARM_GLANCE_RIGHT

            # Arms - Flesh/Bone (Specific to Oblique: Off Side / Shot Side)
            if 117 <= roll <= 123: return AdvancedHitLocation.ARM_FLESH_OFF_SIDE
            if 124 <= roll <= 131: return AdvancedHitLocation.ARM_FLESH_SHOT_SIDE

            if 132 <= roll <= 134: return AdvancedHitLocation.ARM_BONE_OFF_SIDE
            if 135 <= roll <= 138: return AdvancedHitLocation.ARM_BONE_SHOT_SIDE

            # Elbow
            if 139 <= roll <= 143: return AdvancedHitLocation.ELBOW_LEFT  # Mapping Left Col
            if 144 <= roll <= 148: return AdvancedHitLocation.ELBOW_RIGHT

            # Forearm
            if 149 <= roll <= 150: return AdvancedHitLocation.FOREARM_FLESH_LEFT
            if 151 <= roll <= 153: return AdvancedHitLocation.FOREARM_FLESH_RIGHT

            if 154 <= roll <= 161: return AdvancedHitLocation.FOREARM_BONE_LEFT
            if 162 <= roll <= 170: return AdvancedHitLocation.FOREARM_BONE_RIGHT

            if 171 <= roll <= 174: return AdvancedHitLocation.HAND_LEFT
            if 175 <= roll <= 179: return AdvancedHitLocation.HAND_RIGHT

            # Weapon / Torso
            if 180 <= roll <= 195: return AdvancedHitLocation.WEAPON_CRITICAL
            if 196 <= roll <= 219: return AdvancedHitLocation.TORSO_GLANCE
            if 220 <= roll <= 230: return AdvancedHitLocation.BASE_OF_NECK

            if 231 <= roll <= 243: return AdvancedHitLocation.LUNG_RIB
            if 244 <= roll <= 258: return AdvancedHitLocation.LUNG
            if 259 <= roll <= 266: return AdvancedHitLocation.HEART
            if 267 <= roll <= 276: return AdvancedHitLocation.LIVER_RIB
            if 277 <= roll <= 283: return AdvancedHitLocation.LIVER
            if 284 <= roll <= 292: return AdvancedHitLocation.STOMACH_RIB
            if 293 <= roll <= 298: return AdvancedHitLocation.STOMACH
            if 299 <= roll <= 308: return AdvancedHitLocation.STOMACH_SPLEEN
            if 309 <= roll <= 316: return AdvancedHitLocation.STOMACH_KIDNEY
            if 317 <= roll <= 334: return AdvancedHitLocation.LIVER_KIDNEY
            if 335 <= roll <= 345: return AdvancedHitLocation.LIVER_SPINE
            if 346 <= roll <= 379: return AdvancedHitLocation.INTESTINES
            if 380 <= roll <= 401: return AdvancedHitLocation.SPINE
            if 402 <= roll <= 498: return AdvancedHitLocation.PELVIS

            # Legs
            if 499 <= roll <= 509: return AdvancedHitLocation.HIP_SOCKET_LEFT
            if 510 <= roll <= 520: return AdvancedHitLocation.HIP_SOCKET_RIGHT

            if 521 <= roll <= 544: return AdvancedHitLocation.LEG_GLANCE_LEFT
            if 545 <= roll <= 568: return AdvancedHitLocation.LEG_GLANCE_RIGHT

            if 569 <= roll <= 642: return AdvancedHitLocation.THIGH_FLESH_LEFT
            if 643 <= roll <= 716: return AdvancedHitLocation.THIGH_FLESH_RIGHT

            if 717 <= roll <= 738: return AdvancedHitLocation.THIGH_BONE_LEFT
            if 739 <= roll <= 760: return AdvancedHitLocation.THIGH_BONE_RIGHT

            if 761 <= roll <= 794: return AdvancedHitLocation.KNEE_LEFT
            if 795 <= roll <= 828: return AdvancedHitLocation.KNEE_RIGHT

            # Shins (Side Tables S23, S24)
            if 829 <= roll <= 840: return AdvancedHitLocation.SHIN_FLESH_SIDE_LEFT
            if 841 <= roll <= 852: return AdvancedHitLocation.SHIN_FLESH_SIDE_RIGHT

            if 853 <= roll <= 892: return AdvancedHitLocation.SHIN_BONE_SIDE_LEFT
            if 893 <= roll <= 932: return AdvancedHitLocation.SHIN_BONE_SIDE_RIGHT

            if 933 <= roll <= 965: return AdvancedHitLocation.FOOT_LEFT
            if 966 <= roll <= 999: return AdvancedHitLocation.FOOT_RIGHT

            return AdvancedHitLocation.MISS

    @classmethod
    def get_hit_location_right_side(cls, exposure: TargetExposure) -> AdvancedHitLocation:
        """
        Generates a random roll for right SIDE fire (Table 1C / 4G).
        """

        # ---------------------------------------------------------
        # 1. LOGIC FOR COVER (d100 Tables)
        # ---------------------------------------------------------
        if exposure == TargetExposure.LOOKING_OVER_COVER:
            roll = random.randint(0, 99)
            if 0 <= roll <= 11: return AdvancedHitLocation.HEAD_GLANCE
            if 12 <= roll <= 87: return AdvancedHitLocation.SKULL_SIDE
            if 88 <= roll <= 99: return AdvancedHitLocation.EYE_SIDE
            return AdvancedHitLocation.MISS
        elif exposure == TargetExposure.FIRING_OVER_COVER:
            roll = random.randint(0, 99)
            if 0 <= roll <= 2: return AdvancedHitLocation.HEAD_GLANCE
            if 3 <= roll <= 14: return AdvancedHitLocation.SKULL_SIDE
            if 15 <= roll <= 16: return AdvancedHitLocation.EYE_SIDE
            if 17 <= roll <= 24: return AdvancedHitLocation.JAW_SIDE
            if 25 <= roll <= 32: return AdvancedHitLocation.BASE_OF_SKULL_SIDE
            if 33 <= roll <= 34: return AdvancedHitLocation.NECK_THROAT_SIDE
            if 35 <= roll <= 36: return AdvancedHitLocation.NECK_SPINE_SIDE
            # Shoulders/Arms
            if 37 <= roll <= 40: return AdvancedHitLocation.SHOULDER_GLANCE_RIGHT  # Assuming right side hit
            if 41 <= roll <= 47: return AdvancedHitLocation.SHOULDER_SOCKET_LUNG_SIDE
            if 48 <= roll <= 51: return AdvancedHitLocation.SHOULDER_SOCKET_SPINE_SIDE
            if 52 <= roll <= 58: return AdvancedHitLocation.ARM_GLANCE_RIGHT
            if 59 <= roll <= 62: return AdvancedHitLocation.ARM_FLESH_RIGHT
            if 63 <= roll <= 68: return AdvancedHitLocation.ARM_BONE_RIGHT
            if 69 <= roll <= 76: return AdvancedHitLocation.ELBOW_RIGHT
            if 77 <= roll <= 79: return AdvancedHitLocation.FOREARM_FLESH_RIGHT
            if 80 <= roll <= 89: return AdvancedHitLocation.FOREARM_BONE_RIGHT
            if 90 <= roll <= 90: return AdvancedHitLocation.HAND_RIGHT
            if 91 <= roll <= 93: return AdvancedHitLocation.HAND_WEAPON_CRITICAL
            if 94 <= roll <= 99: return AdvancedHitLocation.WEAPON_CRITICAL
            return AdvancedHitLocation.MISS
        # ---------------------------------------------------------
        # 2. LOGIC FOR "IN THE OPEN" (d1000 Table)
        # ---------------------------------------------------------
        else:
            # Range determination based on exposure
            if exposure == TargetExposure.HEAD:
                roll = random.randint(0, 77)
            elif exposure == TargetExposure.BODY:
                roll = random.randint(78, 460)
            elif exposure == TargetExposure.LEGS:
                roll = random.randint(461, 999)
            elif exposure == TargetExposure.ARMS:
                roll = random.randint(78, 209)
            else:
                roll = random.randint(0, 999)
            if 0 <= roll <= 5: return AdvancedHitLocation.HEAD_GLANCE
            if 6 <= roll <= 31: return AdvancedHitLocation.SKULL_SIDE
            if 32 <= roll <= 35: return AdvancedHitLocation.EYE_SIDE
            if 36 <= roll <= 52: return AdvancedHitLocation.JAW_SIDE
            if 53 <= roll <= 68: return AdvancedHitLocation.BASE_OF_SKULL_SIDE
            if 69 <= roll <= 73: return AdvancedHitLocation.NECK_THROAT_SIDE
            if 74 <= roll <= 77: return AdvancedHitLocation.NECK_SPINE_SIDE
            # Torso / Arms Upper
            if 78 <= roll <= 85: return AdvancedHitLocation.SHOULDER_GLANCE_RIGHT
            if 86 <= roll <= 100: return AdvancedHitLocation.SHOULDER_SOCKET_LUNG_SIDE
            if 101 <= roll <= 108: return AdvancedHitLocation.SHOULDER_SOCKET_SPINE_SIDE
            if 109 <= roll <= 115: return AdvancedHitLocation.ARM_GLANCE_LEFT  # Table shows two ranges
            if 116 <= roll <= 123: return AdvancedHitLocation.ARM_GLANCE_RIGHT
            if 124 <= roll <= 127: return AdvancedHitLocation.ARM_FLESH_LEFT
            if 128 <= roll <= 131: return AdvancedHitLocation.ARM_FLESH_RIGHT
            if 132 <= roll <= 137: return AdvancedHitLocation.ARM_BONE_LEFT
            if 138 <= roll <= 144: return AdvancedHitLocation.ARM_BONE_RIGHT
            if 145 <= roll <= 152: return AdvancedHitLocation.ELBOW_LEFT
            if 153 <= roll <= 161: return AdvancedHitLocation.ELBOW_RIGHT
            if 162 <= roll <= 164: return AdvancedHitLocation.FOREARM_FLESH_LEFT
            if 165 <= roll <= 167: return AdvancedHitLocation.FOREARM_FLESH_RIGHT
            if 168 <= roll <= 177: return AdvancedHitLocation.FOREARM_BONE_LEFT
            if 178 <= roll <= 188: return AdvancedHitLocation.FOREARM_BONE_RIGHT
            if 189 <= roll <= 190: return AdvancedHitLocation.HAND_LEFT
            if 191 <= roll <= 192: return AdvancedHitLocation.HAND_RIGHT
            if 193 <= roll <= 197: return AdvancedHitLocation.HAND_WEAPON_CRITICAL
            if 198 <= roll <= 209: return AdvancedHitLocation.WEAPON_CRITICAL
            # Organs Side (S9-S22)
            if 210 <= roll <= 234: return AdvancedHitLocation.TORSO_GLANCE
            if 235 <= roll <= 249: return AdvancedHitLocation.LUNG_RIB_SIDE
            if 250 <= roll <= 261: return AdvancedHitLocation.LUNG_SIDE
            if 262 <= roll <= 263: return AdvancedHitLocation.HEART_RIB_SIDE
            if 264 <= roll <= 265: return AdvancedHitLocation.HEART_SIDE
            if 266 <= roll <= 269: return AdvancedHitLocation.SPINE_SIDE
            if 270 <= roll <= 287: return AdvancedHitLocation.STOMACH_LIVER_RIB_SIDE
            if 288 <= roll <= 304: return AdvancedHitLocation.STOMACH_LIVER_SIDE
            if 305 <= roll <= 316: return AdvancedHitLocation.SPLEEN_LIVER_SIDE
            if 317 <= roll <= 329: return AdvancedHitLocation.KIDNEY_SPINE_SIDE
            if 330 <= roll <= 356: return AdvancedHitLocation.INTESTINES_SIDE
            if 357 <= roll <= 371: return AdvancedHitLocation.INTESTINES_SPINE_SIDE
            if 372 <= roll <= 427: return AdvancedHitLocation.PELVIS_SIDE
            if 428 <= roll <= 445: return AdvancedHitLocation.HIP_SPINE_SIDE
            if 446 <= roll <= 460: return AdvancedHitLocation.HIP_SOCKET_SIDE
            # Legs Side
            if 461 <= roll <= 484: return AdvancedHitLocation.LEG_GLANCE_LEFT
            if 485 <= roll <= 514: return AdvancedHitLocation.LEG_GLANCE_RIGHT
            if 515 <= roll <= 591: return AdvancedHitLocation.THIGH_FLESH_LEFT
            if 592 <= roll <= 638: return AdvancedHitLocation.THIGH_FLESH_RIGHT
            if 639 <= roll <= 668: return AdvancedHitLocation.THIGH_FLESH_THIGH_FLESH
            if 669 <= roll <= 680: return AdvancedHitLocation.THIGH_FLESH_THIGH_BONE
            if 681 <= roll <= 706: return AdvancedHitLocation.THIGH_BONE_LEFT

            if 707 <= roll <= 744: return AdvancedHitLocation.THIGH_BONE_RIGHT
            if 745 <= roll <= 782: return AdvancedHitLocation.KNEE_LEFT


            if 783 <= roll <= 820: return AdvancedHitLocation.KNEE_RIGHT
            if 821 <= roll <= 859: return AdvancedHitLocation.SHIN_FLESH_SIDE_LEFT
            if 860 <= roll <= 898: return AdvancedHitLocation.SHIN_FLESH_SIDE_RIGHT
            if 899 <= roll <= 917: return AdvancedHitLocation.SHIN_BONE_SIDE_LEFT
            if 918 <= roll <= 937: return AdvancedHitLocation.SHIN_BONE_SIDE_RIGHT
            if 938 <= roll <= 968: return AdvancedHitLocation.FOOT_LEFT
            if 969 <= roll <= 999: return AdvancedHitLocation.FOOT_RIGHT
            return AdvancedHitLocation.MISS

    @classmethod
    def get_hit_location_left_side(cls, exposure: TargetExposure) -> AdvancedHitLocation:
        """
        Generates a random roll for left SIDE fire (Table 1C / 4G).
        """

        # ---------------------------------------------------------
        # 1. LOGIC FOR COVER (d100 Tables)
        # ---------------------------------------------------------
        if exposure == TargetExposure.LOOKING_OVER_COVER:
            roll = random.randint(0, 99)
            if 0 <= roll <= 11: return AdvancedHitLocation.HEAD_GLANCE
            if 12 <= roll <= 87: return AdvancedHitLocation.SKULL_SIDE
            if 88 <= roll <= 99: return AdvancedHitLocation.EYE_SIDE
            return AdvancedHitLocation.MISS
        elif exposure == TargetExposure.FIRING_OVER_COVER:
            roll = random.randint(0, 99)
            if 0 <= roll <= 2: return AdvancedHitLocation.HEAD_GLANCE
            if 3 <= roll <= 14: return AdvancedHitLocation.SKULL_SIDE
            if 15 <= roll <= 16: return AdvancedHitLocation.EYE_SIDE
            if 17 <= roll <= 24: return AdvancedHitLocation.JAW_SIDE
            if 25 <= roll <= 32: return AdvancedHitLocation.BASE_OF_SKULL_SIDE
            if 33 <= roll <= 34: return AdvancedHitLocation.NECK_THROAT_SIDE
            if 35 <= roll <= 36: return AdvancedHitLocation.NECK_SPINE_SIDE
            # Shoulders/Arms
            if 37 <= roll <= 40: return AdvancedHitLocation.SHOULDER_GLANCE_LEFT  # Assuming left side hit
            if 41 <= roll <= 47: return AdvancedHitLocation.SHOULDER_SOCKET_LUNG_SIDE
            if 48 <= roll <= 51: return AdvancedHitLocation.SHOULDER_SOCKET_SPINE_SIDE
            if 52 <= roll <= 58: return AdvancedHitLocation.ARM_GLANCE_LEFT
            if 59 <= roll <= 62: return AdvancedHitLocation.ARM_FLESH_LEFT
            if 63 <= roll <= 68: return AdvancedHitLocation.ARM_BONE_LEFT
            if 69 <= roll <= 76: return AdvancedHitLocation.ELBOW_RIGHT
            if 77 <= roll <= 79: return AdvancedHitLocation.FOREARM_FLESH_LEFT
            if 80 <= roll <= 89: return AdvancedHitLocation.FOREARM_BONE_LEFT
            if 90 <= roll <= 90: return AdvancedHitLocation.HAND_LEFT
            if 91 <= roll <= 93: return AdvancedHitLocation.HAND_WEAPON_CRITICAL
            if 94 <= roll <= 99: return AdvancedHitLocation.WEAPON_CRITICAL
            return AdvancedHitLocation.MISS
        # ---------------------------------------------------------
        # 2. LOGIC FOR "IN THE OPEN" (d1000 Table)
        # ---------------------------------------------------------
        else:
            # Range determination based on exposure
            if exposure == TargetExposure.HEAD:
                roll = random.randint(0, 77)
            elif exposure == TargetExposure.BODY:
                roll = random.randint(78, 460)
            elif exposure == TargetExposure.LEGS:
                roll = random.randint(461, 999)
            elif exposure == TargetExposure.ARMS:
                roll = random.randint(78, 209)
            else:
                roll = random.randint(0, 999)
            if 0 <= roll <= 5: return AdvancedHitLocation.HEAD_GLANCE
            if 6 <= roll <= 31: return AdvancedHitLocation.SKULL_SIDE
            if 32 <= roll <= 35: return AdvancedHitLocation.EYE_SIDE
            if 36 <= roll <= 52: return AdvancedHitLocation.JAW_SIDE
            if 53 <= roll <= 68: return AdvancedHitLocation.BASE_OF_SKULL_SIDE
            if 69 <= roll <= 73: return AdvancedHitLocation.NECK_THROAT_SIDE
            if 74 <= roll <= 77: return AdvancedHitLocation.NECK_SPINE_SIDE
            # Torso / Arms Upper
            if 78 <= roll <= 85: return AdvancedHitLocation.SHOULDER_GLANCE_LEFT
            if 86 <= roll <= 100: return AdvancedHitLocation.SHOULDER_SOCKET_LUNG_SIDE
            if 101 <= roll <= 108: return AdvancedHitLocation.SHOULDER_SOCKET_SPINE_SIDE
            if 109 <= roll <= 115: return AdvancedHitLocation.ARM_GLANCE_LEFT  # Table shows two ranges
            if 116 <= roll <= 123: return AdvancedHitLocation.ARM_GLANCE_RIGHT
            if 124 <= roll <= 127: return AdvancedHitLocation.ARM_FLESH_LEFT
            if 128 <= roll <= 131: return AdvancedHitLocation.ARM_FLESH_RIGHT
            if 132 <= roll <= 137: return AdvancedHitLocation.ARM_BONE_LEFT
            if 138 <= roll <= 144: return AdvancedHitLocation.ARM_BONE_RIGHT
            if 145 <= roll <= 152: return AdvancedHitLocation.ELBOW_LEFT
            if 153 <= roll <= 161: return AdvancedHitLocation.ELBOW_RIGHT
            if 162 <= roll <= 164: return AdvancedHitLocation.FOREARM_FLESH_LEFT
            if 165 <= roll <= 167: return AdvancedHitLocation.FOREARM_FLESH_RIGHT
            if 168 <= roll <= 177: return AdvancedHitLocation.FOREARM_BONE_LEFT
            if 178 <= roll <= 188: return AdvancedHitLocation.FOREARM_BONE_RIGHT
            if 189 <= roll <= 190: return AdvancedHitLocation.HAND_LEFT
            if 191 <= roll <= 192: return AdvancedHitLocation.HAND_RIGHT
            if 193 <= roll <= 197: return AdvancedHitLocation.HAND_WEAPON_CRITICAL
            if 198 <= roll <= 209: return AdvancedHitLocation.WEAPON_CRITICAL
            # Organs Side (S9-S22)
            if 210 <= roll <= 234: return AdvancedHitLocation.TORSO_GLANCE
            if 235 <= roll <= 249: return AdvancedHitLocation.LUNG_RIB_SIDE
            if 250 <= roll <= 261: return AdvancedHitLocation.LUNG_SIDE
            if 262 <= roll <= 263: return AdvancedHitLocation.HEART_RIB_SIDE
            if 264 <= roll <= 265: return AdvancedHitLocation.HEART_SIDE
            if 266 <= roll <= 269: return AdvancedHitLocation.SPINE_SIDE
            if 270 <= roll <= 287: return AdvancedHitLocation.STOMACH_LIVER_RIB_SIDE
            if 288 <= roll <= 304: return AdvancedHitLocation.STOMACH_LIVER_SIDE
            if 305 <= roll <= 316: return AdvancedHitLocation.SPLEEN_LIVER_SIDE
            if 317 <= roll <= 329: return AdvancedHitLocation.KIDNEY_SPINE_SIDE
            if 330 <= roll <= 356: return AdvancedHitLocation.INTESTINES_SIDE
            if 357 <= roll <= 371: return AdvancedHitLocation.INTESTINES_SPINE_SIDE
            if 372 <= roll <= 427: return AdvancedHitLocation.PELVIS_SIDE
            if 428 <= roll <= 445: return AdvancedHitLocation.HIP_SPINE_SIDE
            if 446 <= roll <= 460: return AdvancedHitLocation.HIP_SOCKET_SIDE
            # Legs Side
            if 461 <= roll <= 484: return AdvancedHitLocation.LEG_GLANCE_LEFT
            if 485 <= roll <= 514: return AdvancedHitLocation.LEG_GLANCE_RIGHT
            if 515 <= roll <= 591: return AdvancedHitLocation.THIGH_FLESH_LEFT
            if 592 <= roll <= 638: return AdvancedHitLocation.THIGH_FLESH_RIGHT
            if 639 <= roll <= 668: return AdvancedHitLocation.THIGH_FLESH_THIGH_FLESH
            if 669 <= roll <= 680: return AdvancedHitLocation.THIGH_FLESH_THIGH_BONE
            if 681 <= roll <= 706: return AdvancedHitLocation.THIGH_BONE_LEFT

            if 707 <= roll <= 744: return AdvancedHitLocation.THIGH_BONE_RIGHT
            if 745 <= roll <= 782: return AdvancedHitLocation.KNEE_LEFT


            if 783 <= roll <= 820: return AdvancedHitLocation.KNEE_RIGHT
            if 821 <= roll <= 859: return AdvancedHitLocation.SHIN_FLESH_SIDE_LEFT
            if 860 <= roll <= 898: return AdvancedHitLocation.SHIN_FLESH_SIDE_RIGHT
            if 899 <= roll <= 917: return AdvancedHitLocation.SHIN_BONE_SIDE_LEFT
            if 918 <= roll <= 937: return AdvancedHitLocation.SHIN_BONE_SIDE_RIGHT
            if 938 <= roll <= 968: return AdvancedHitLocation.FOOT_LEFT
            if 969 <= roll <= 999: return AdvancedHitLocation.FOOT_RIGHT
            return AdvancedHitLocation.MISS