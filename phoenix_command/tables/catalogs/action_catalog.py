"""Table 7B — Action Time catalog."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ActionDef:
    """Predefined action with action-count cost."""

    id: str
    name: str
    category: str
    cost: int | str  # int or "RT" for reload time


# Table 7B — Action Time Table
BUILTIN_ACTIONS: dict[str, ActionDef] = {}

def _register(actions: list[ActionDef]) -> None:
    for action in actions:
        BUILTIN_ACTIONS[action.id] = action


_register([
    # Actions
    ActionDef("assume_firing_stance_cover", "Assume a Firing Stance - Over or Around Cover", "Actions", 2),
    ActionDef("assume_hip_firing_stance_cover", "Assume a Hip Firing Stance - Over or Around Cover", "Actions", 1),
    ActionDef("look_over_cover", "Look Over or Around Cover", "Actions", 1),
    ActionDef("duck_from_firing", "Duck from a Firing Stance or from Looking", "Actions", 1),
    ActionDef("brace_weapon", "Brace a Weapon", "Actions", 1),
    ActionDef(
        "movement_while_braced",
        "Movement While Braced",
        "Actions",
        0,  # cost computed: movement + 1 AC brace
    ),
    ActionDef("facing_change_60_120", "60 - 120 Degree Facing Change", "Actions", 1),
    ActionDef("facing_change_60_firing", "60 Degree Facing Change in Firing Stance", "Actions", 2),
    ActionDef("standing_to_kneeling", "Go from Standing to Kneeling", "Actions", 1),
    ActionDef("standing_to_prone", "Go from Standing to Prone", "Actions", 2),
    ActionDef("kneeling_to_prone", "Go from Kneeling to Prone", "Actions", 1),
    ActionDef("prone_to_kneeling", "Go from Prone to Kneeling", "Actions", 2),
    ActionDef("prone_to_standing", "Go from Prone to Standing", "Actions", 3),
    ActionDef("kick_open_door", "Kick Open a Door", "Actions", 2),
    ActionDef("open_door", "Open a Door", "Actions", 3),
    ActionDef("open_window_two_hands", "Open a Window with Two Hands", "Actions", 6),
    ActionDef("break_clear_glass", "Break and Clear Glass from a Window", "Actions", 6),
    ActionDef("climb_through_window", "Climb through a Window", "Actions", 6),
    ActionDef("get_out_trench", "Get Out of a Trench or Foxhole", "Actions", 6),
    # Reloading
    ActionDef("cock_revolver_pistol", "Cock a Revolver or Pistol", "Reloading", 1),
    ActionDef("take_bullet_magazine", "Take a Bullet or Magazine from a Pouch", "Reloading", 4),
    ActionDef("replace_bullet_magazine", "Replace a Bullet or Magazine into a Pouch", "Reloading", 6),
    ActionDef("link_belt_ammo", "Link a Belt of Ammunition", "Reloading", 8),
    ActionDef("load_round_magazine", "Load a Round into a Magazine", "Reloading", 4),
    ActionDef("load_charging_strip", "Load a Charging Strip into a Magazine", "Reloading", 7),
    ActionDef("open_hinged_ammo_can", "Open a Hinged Type Ammunition Can", "Reloading", 4),
    ActionDef("open_paper_ammo_box", "Open a Paper Box of Ammunition", "Reloading", 4),
    ActionDef("unload_weapon", "Unload a Weapon", "Reloading", "RT"),
    # Weapon Functions
    ActionDef("safety_fire_select", "Safety or Fire Select Switch", "Weapon Functions", 1),
    ActionDef("pick_up_weapon", "Pick Up or Set Down a Weapon", "Weapon Functions", 4),
    ActionDef("grab_slung_weapon", "Grab an Unheld Slung Weapon", "Weapon Functions", 3),
    ActionDef("draw_shoulder_holster", "Draw Pistol - Shoulder Holster", "Weapon Functions", 3),
    ActionDef("draw_belt_holster", "Draw Pistol - Belt Holster", "Weapon Functions", 3),
    ActionDef("draw_police_holster", "Draw Pistol - Police Holster", "Weapon Functions", 2),
    ActionDef("draw_old_west_holster", "Draw Pistol - Old West Fast Draw Holster", "Weapon Functions", 2),
    ActionDef("draw_modern_holster", "Draw Pistol - Modern Fast Draw Holster", "Weapon Functions", 1),
    ActionDef("throw_small_object", "Throw a Small Object", "Weapon Functions", 2),
    ActionDef("pick_up_grenade", "Pick up a Grenade or Small Object", "Weapon Functions", 2),
    # Equipment In/Out
    ActionDef("backpack_in", "Backpack with Quick Release - In", "Equipment", 16),
    ActionDef("backpack_out", "Backpack with Quick Release - Out", "Equipment", 7),
    ActionDef("bandolier_in", "Bandolier or Belt - In", "Equipment", 6),
    ActionDef("bandolier_out", "Bandolier or Belt - Out", "Equipment", 4),
    ActionDef("bayonet_scabbard_in", "Bayonet or Knife from Scabbard - In", "Equipment", 3),
    ActionDef("bayonet_scabbard_out", "Bayonet or Knife from Scabbard - Out", "Equipment", 2),
    ActionDef("bayonet_weapon", "Bayonet to Weapon", "Equipment", 3),
    ActionDef("bipod_in", "Bipod - In", "Equipment", 5),
    ActionDef("bipod_out", "Bipod - Out", "Equipment", 8),
    ActionDef("body_armor_in", "Body Armor (external vest) - In", "Equipment", 24),
    ActionDef("body_armor_out", "Body Armor (external vest) - Out", "Equipment", 13),
    ActionDef("climbing_harness_in", "Climbing Harness - In", "Equipment", 18),
    ActionDef("climbing_harness_out", "Climbing Harness - Out", "Equipment", 10),
    ActionDef("folding_stock_in", "Folding Stock - In", "Equipment", 6),
    ActionDef("folding_stock_out", "Folding Stock - Out", "Equipment", 4),
    ActionDef("gas_mask_in", "Gas Mask - In", "Equipment", 12),
    ActionDef("gas_mask_out", "Gas Mask - Out", "Equipment", 5),
    ActionDef("scope_in", "Optical Scope with Quick Release - In", "Equipment", 12),
    ActionDef("scope_out", "Optical Scope with Quick Release - Out", "Equipment", 4),
    ActionDef("parachute_in", "Parachute with Quick Release - In", "Equipment", 20),
    ActionDef("parachute_out", "Parachute with Quick Release - Out", "Equipment", 8),
    ActionDef("pistol_stock_in", "Pistol Shoulder Stock - In", "Equipment", 8),
    ActionDef("pistol_stock_out", "Pistol Shoulder Stock - Out", "Equipment", 6),
    ActionDef("silencer_in", "Silencer - In", "Equipment", 9),
    ActionDef("silencer_out", "Silencer - Out", "Equipment", 9),
    ActionDef("slung_weapon_in", "Slung Weapon over Shoulder - In", "Equipment", 3),
    ActionDef("slung_weapon_out", "Slung Weapon over Shoulder - Out", "Equipment", 2),
    ActionDef("tripod_in", "Tripod and Weapon - In", "Equipment", 12),
    ActionDef("tripod_out", "Tripod and Weapon - Out", "Equipment", 8),
])


@dataclass
class CustomActionDef:
    """User-defined action."""

    id: str
    name: str
    cost: int

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "cost": self.cost}

    @classmethod
    def from_dict(cls, data: dict) -> "CustomActionDef":
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            cost=int(data.get("cost", 1)),
        )


@dataclass
class ActionCatalogState:
    """Custom actions stored in session state."""

    custom_actions: dict[str, CustomActionDef] = field(default_factory=dict)

    def add_custom_action(self, name: str, cost: int, action_id: str | None = None) -> CustomActionDef:
        import uuid
        aid = action_id or f"custom_{uuid.uuid4().hex[:8]}"
        action = CustomActionDef(id=aid, name=name, cost=cost)
        self.custom_actions[aid] = action
        return action

    def get_all_actions(self) -> list[ActionDef | CustomActionDef]:
        result: list[ActionDef | CustomActionDef] = list(BUILTIN_ACTIONS.values())
        result.extend(self.custom_actions.values())
        return result

    def to_dict(self) -> dict:
        return {
            "custom_actions": {
                k: v.to_dict() for k, v in self.custom_actions.items()
            },
        }

    @classmethod
    def from_dict(cls, data: dict | None) -> "ActionCatalogState":
        if not data:
            return cls()
        return cls(
            custom_actions={
                k: CustomActionDef.from_dict(v)
                for k, v in data.get("custom_actions", {}).items()
            },
        )
