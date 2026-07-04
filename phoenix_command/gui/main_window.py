"""Main window for Phoenix Command GUI."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QMessageBox,
    QFileDialog,
    QTabWidget,
)

from phoenix_command.gui.widgets.body_diagram import BodyDiagramWidget
from phoenix_command.gui.widgets.character_list import CharacterListWidget
from phoenix_command.gui.widgets.combat_log import CombatLogWidget
from phoenix_command.gui.widgets.combat_zone import CombatZoneWidget
from phoenix_command.gui.widgets.hex_map_view import HexMapView
from phoenix_command.gui.widgets.stats_display import StatsDisplayWidget
from phoenix_command.session.bridge import GameStateBridge
from phoenix_command.session.persistence import (
    default_character_filename,
    load_character_file,
    load_map_file,
    load_game_state,
    save_character_file,
    save_map_file,
    save_game_state,
)
from phoenix_command.session.game_state import GameState
from phoenix_command.session.publisher import GameStatePublisher
from phoenix_command.session.sync_protocol import (
    MessageType,
    SyncMessage,
    apply_message_to_state,
)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.characters = []
        self.setWindowTitle("Phoenix Command")

        self._session_role: str | None = None  # "host", "guest", or None
        self._p2p_host = None
        self._p2p_guest = None
        self._relay_client = None
        self._game_bridge = GameStateBridge()
        self._publisher: GameStatePublisher | None = None
        self._host_dialog = None
        self._join_dialog = None

        self._create_menu_bar()
        self._create_central_widget()
        self._create_status_bar()
        self.showMaximized()

    def _create_menu_bar(self):
        """Create menu bar."""
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")
        self._new_session_action = file_menu.addAction("&New Session")
        self._new_session_action.triggered.connect(self._new_session)
        self._save_session_action = file_menu.addAction("&Save Session")
        self._save_session_action.triggered.connect(self._save_session)
        self._load_session_action = file_menu.addAction("&Load Session")
        self._load_session_action.triggered.connect(self._load_session)
        file_menu.addSeparator()
        self._host_session_action = file_menu.addAction("&Host Session...")
        self._host_session_action.triggered.connect(self._host_session)
        self._join_session_action = file_menu.addAction("&Join Session...")
        self._join_session_action.triggered.connect(self._join_session)
        self._disconnect_action = file_menu.addAction("&Disconnect")
        self._disconnect_action.triggered.connect(self._disconnect_session)
        self._disconnect_action.setEnabled(False)
        file_menu.addSeparator()
        file_menu.addAction("E&xit", self.close)

        self.char_menu = menubar.addMenu("&Characters")
        self._add_char_action = self.char_menu.addAction("&Add Character")
        self._add_char_action.triggered.connect(self._add_character)
        self._edit_char_action = self.char_menu.addAction("&Edit Character")
        self._edit_char_action.triggered.connect(self._edit_character)
        self._remove_char_action = self.char_menu.addAction("&Remove Character")
        self._remove_char_action.triggered.connect(self._remove_character)
        self._equip_action = self.char_menu.addAction("Manage &Equipment")
        self._equip_action.triggered.connect(self._manage_equipment)
        self.char_menu.addSeparator()
        self._save_char_action = self.char_menu.addAction("&Save Character...")
        self._save_char_action.triggered.connect(self._save_character)
        self._load_char_action = self.char_menu.addAction("&Load Character...")
        self._load_char_action.triggered.connect(self._load_character)
        self.char_menu.addSeparator()
        self.char_menu.addAction("&Import Template")

        self.combat_menu = menubar.addMenu("C&ombat")
        shot_action = self.combat_menu.addAction("&Single Shot")
        shot_action.triggered.connect(self._single_shot)
        three_rb_action = self.combat_menu.addAction("&Three Round Burst")
        three_rb_action.triggered.connect(self._three_round_burst)
        burst_action = self.combat_menu.addAction("&Burst Fire")
        burst_action.triggered.connect(self._burst_fire)
        self.combat_menu.addSeparator()
        thrown_grenade_action = self.combat_menu.addAction("Thrown &Grenade")
        thrown_grenade_action.triggered.connect(self._thrown_grenade)
        explosion_action = self.combat_menu.addAction("&Explosion Damage")
        explosion_action.triggered.connect(self._explosion_damage)
        self.combat_menu.addSeparator()
        self.combat_menu.addAction("Combat &History")

        self.map_menu = menubar.addMenu("&Map")
        self._new_map_action = self.map_menu.addAction("&New Map")
        self._new_map_action.triggered.connect(self._new_map)
        self._save_map_action = self.map_menu.addAction("&Save Map...")
        self._save_map_action.triggered.connect(self._save_map)
        self._load_map_action = self.map_menu.addAction("&Load Map...")
        self._load_map_action.triggered.connect(self._load_map)
        self.map_menu.addSeparator()
        self._manage_layers_action = self.map_menu.addAction("&Manage Layers...")
        self._manage_layers_action.triggered.connect(self._manage_layers)
        self._action_catalog_action = self.map_menu.addAction("&Action Catalog...")
        self._action_catalog_action.triggered.connect(self._show_action_catalog)
        self._custom_barrier_action = self.map_menu.addAction("&Custom Barrier Material...")
        self._custom_barrier_action.triggered.connect(self._add_custom_barrier)

        help_menu = menubar.addMenu("&Help")
        help_menu.addAction("&Documentation")
        help_menu.addAction("&About")

    def _create_central_widget(self):
        """Create central widget with panels."""
        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)

        main_splitter = QSplitter(Qt.Orientation.Horizontal)

        self.character_list = CharacterListWidget()
        self.character_list.setMaximumWidth(250)
        self.character_list.setDragEnabled(True)
        self.character_list.currentRowChanged.connect(self._on_character_selected)
        main_splitter.addWidget(self.character_list)

        center_splitter = QSplitter(Qt.Orientation.Vertical)

        self._center_tabs = QTabWidget()
        self.combat_zone = CombatZoneWidget()
        self.hex_map_view = HexMapView()
        self.hex_map_view.map_changed.connect(self._on_map_changed)
        self._center_tabs.addTab(self.combat_zone, "Combat")
        self._center_tabs.addTab(self.hex_map_view, "Map")
        center_splitter.addWidget(self._center_tabs)

        self.combat_log = CombatLogWidget()
        center_splitter.addWidget(self.combat_log)

        main_splitter.addWidget(center_splitter)

        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)
        self.stats_display = StatsDisplayWidget()
        details_layout.addWidget(self.stats_display)
        self.body_diagram = BodyDiagramWidget()
        details_layout.addWidget(self.body_diagram, stretch=1)
        details_widget.setMaximumWidth(300)
        main_splitter.addWidget(details_widget)

        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 3)
        main_splitter.setStretchFactor(2, 1)

        layout.addWidget(main_splitter)

    def _create_status_bar(self):
        """Create status bar."""
        self.statusBar().showMessage("Ready")

    def _set_guest_mode(self, guest: bool) -> None:
        """Enable or disable editing when connected as guest."""
        self._add_char_action.setEnabled(not guest)
        self._edit_char_action.setEnabled(not guest)
        self._remove_char_action.setEnabled(not guest)
        self._equip_action.setEnabled(not guest)
        self._save_char_action.setEnabled(not guest)
        self._load_char_action.setEnabled(not guest)
        self.combat_menu.setEnabled(not guest)
        self._new_map_action.setEnabled(not guest)
        self._save_map_action.setEnabled(not guest)
        self._load_map_action.setEnabled(not guest)
        self._manage_layers_action.setEnabled(not guest)
        self._action_catalog_action.setEnabled(not guest)
        self._custom_barrier_action.setEnabled(not guest)
        self.hex_map_view.set_editable(not guest)
        self.character_list.setDragEnabled(not guest)
        self._host_session_action.setEnabled(not guest)
        self._join_session_action.setEnabled(not guest)
        self._new_session_action.setEnabled(not guest)

    def _notify_game_state_changed(self, domain: str = "combat", immediate: bool = False) -> None:
        if self._session_role == "host" and self._publisher:
            self._publisher.notify_changed(domain=domain, immediate=immediate)

    def _broadcast_sync_message(self, message: SyncMessage) -> None:
        if self._p2p_host:
            self._p2p_host.broadcast_message(message)
        if self._relay_client:
            self._relay_client.send_message(message)

    def _on_sync_message_received(self, message: SyncMessage) -> None:
        if self._session_role == "host":
            if message.type == MessageType.REQUEST_STATE and self._publisher:
                full = self._publisher.publish_now()
                self._broadcast_sync_message(full)
            return

        if self._session_role == "guest":
            new_state = apply_message_to_state(self._game_bridge.state, message)
            self._game_bridge.apply_remote_state(new_state, self)
            self.statusBar().showMessage(
                f"Guest: synced revision {new_state.revision}"
            )

    def _new_session(self) -> None:
        if self._session_role:
            QMessageBox.warning(
                self, "Session Active", "Disconnect before starting a new session."
            )
            return
        self.characters.clear()
        self.combat_zone.clear_all()
        self.combat_log.clear()
        self._game_bridge = GameStateBridge()
        self.hex_map_view.new_map()
        self._refresh_character_list()
        self.stats_display.clear()
        self.body_diagram.clear()
        self.statusBar().showMessage("New session")

    def _save_session(self) -> None:
        from phoenix_command.gui.dialogs.session_dialog import SaveLoadSessionDialog

        dialog = SaveLoadSessionDialog("Save Session", "session.json", parent=self)
        if not dialog.exec():
            return
        self._game_bridge.capture_from_window(self)
        save_game_state(dialog.file_path, self._game_bridge.state)
        self.statusBar().showMessage(f"Session saved: {dialog.file_path}")

    def _load_session(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Session", "", "JSON (*.json)"
        )
        if not path:
            return
        try:
            state = load_game_state(path)
            self._game_bridge.apply_remote_state(state, self)
            self.statusBar().showMessage(f"Session loaded: {path}")
            self._notify_game_state_changed(immediate=True)
        except Exception as exc:
            QMessageBox.critical(self, "Load Failed", str(exc))

    def _host_session(self) -> None:
        if self._session_role:
            QMessageBox.warning(self, "Session Active", "Disconnect first.")
            return

        from phoenix_command.gui.dialogs.session_dialog import HostSessionDialog
        from phoenix_command.session.p2p_host import P2PSessionHost

        self._host_dialog = HostSessionDialog(parent=self)
        self._p2p_host = P2PSessionHost(parent=self)
        self._publisher = GameStatePublisher(self._broadcast_sync_message)
        self._publisher.attach(self, self._game_bridge)

        self._p2p_host.invite_ready.connect(self._on_invite_ready)
        self._p2p_host.guest_connected.connect(self._on_guest_connected)
        self._p2p_host.connection_failed.connect(self._on_connection_failed)
        self._p2p_host.ice_state_changed.connect(self._on_ice_state)
        self._p2p_host.set_message_handler(self._on_sync_message_received)
        self._host_dialog.answer_submitted.connect(self._on_host_answer_submitted)

        self._session_role = "host"
        self._disconnect_action.setEnabled(True)
        self._p2p_host.start()
        self._host_dialog.show()

    def _on_invite_ready(self, code: str) -> None:
        if self._host_dialog:
            self._host_dialog.set_invite_code(code)
        self.statusBar().showMessage("Host: invite ready — send via Discord")

    def _on_guest_connected(self, guest_id: str) -> None:
        if self._host_dialog:
            self._host_dialog.set_status(f"Guest connected ({guest_id})")
        if self._publisher:
            full = self._publisher.publish_now()
            self._broadcast_sync_message(full)
        self.statusBar().showMessage(f"Host: guest {guest_id} connected")

    def _on_host_answer_submitted(self, answer: str) -> None:
        if self._p2p_host:
            self._p2p_host.submit_answer(answer)

    def _join_session(self) -> None:
        if self._session_role:
            QMessageBox.warning(self, "Session Active", "Disconnect first.")
            return

        from phoenix_command.gui.dialogs.session_dialog import JoinSessionDialog
        from phoenix_command.session.p2p_guest import P2PSessionGuest

        dialog = JoinSessionDialog(parent=self)
        if not dialog.exec():
            return

        self._join_dialog = dialog
        self._p2p_guest = P2PSessionGuest(parent=self)
        self._p2p_guest.answer_ready.connect(self._on_answer_ready)
        self._p2p_guest.connected.connect(self._on_guest_connected_to_host)
        self._p2p_guest.disconnected.connect(self._on_guest_disconnected)
        self._p2p_guest.connection_failed.connect(self._on_connection_failed)
        self._p2p_guest.state_received.connect(self._on_guest_state_received)
        self._p2p_guest.ice_state_changed.connect(self._on_ice_state)
        self._p2p_guest.set_message_handler(self._on_sync_message_received)

        self._session_role = "guest"
        self._set_guest_mode(True)
        self._disconnect_action.setEnabled(True)
        self._p2p_guest.start()
        self._p2p_guest.connect_with_invite(dialog.invite_code)
        dialog.show()

    def _on_answer_ready(self, code: str) -> None:
        if self._join_dialog:
            self._join_dialog.set_answer_code(code)
        self.statusBar().showMessage("Guest: send answer code to host via Discord")

    def _on_guest_connected_to_host(self) -> None:
        self.statusBar().showMessage("Guest: connected to host")

    def _on_guest_disconnected(self) -> None:
        self.statusBar().showMessage("Guest: disconnected")

    def _on_guest_state_received(self, message: SyncMessage) -> None:
        self._on_sync_message_received(message)

    def _on_connection_failed(self, error: str) -> None:
        QMessageBox.critical(self, "Connection Failed", error)
        self._disconnect_session()

    def _on_ice_state(self, state: str) -> None:
        role = self._session_role or "local"
        self.statusBar().showMessage(f"{role.title()}: ICE {state}")

    def _disconnect_session(self) -> None:
        if self._p2p_host:
            self._p2p_host.stop_session()
            self._p2p_host = None
        if self._p2p_guest:
            self._p2p_guest.stop_session()
            self._p2p_guest = None
        if self._relay_client:
            self._relay_client.stop_session()
            self._relay_client = None
        self._publisher = None
        self._session_role = None
        self._set_guest_mode(False)
        self._disconnect_action.setEnabled(False)
        if self._host_dialog:
            self._host_dialog.close()
            self._host_dialog = None
        if self._join_dialog:
            self._join_dialog.close()
            self._join_dialog = None
        self.statusBar().showMessage("Disconnected")

    def closeEvent(self, event) -> None:
        self._disconnect_session()
        super().closeEvent(event)

    def _on_map_changed(self) -> None:
        self._notify_game_state_changed(domain="map")

    def _new_map(self) -> None:
        self.hex_map_view.new_map()
        self._notify_game_state_changed(domain="map")

    def _save_map(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Map",
            "map.json",
            "Phoenix Command Map (*.json)",
        )
        if not path:
            return
        try:
            save_map_file(
                path,
                self.hex_map_view.get_map_state(),
                self.hex_map_view.get_token_state(),
            )
            self._game_bridge.state.map = self.hex_map_view.get_map_state()
            self._game_bridge.state.tokens = self.hex_map_view.get_token_state()
            self.statusBar().showMessage(f"Map saved: {path}")
        except Exception as exc:
            QMessageBox.critical(self, "Save Map Failed", str(exc))

    def _load_map(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Map",
            "",
            "Phoenix Command Map (*.json)",
        )
        if not path:
            return
        try:
            map_state, token_state = load_map_file(path)
            self.hex_map_view.set_map_state(map_state)
            self.hex_map_view.set_token_state(token_state)
            self.hex_map_view.set_character_names([c.name for c in self.characters])
            self._game_bridge.state.map = map_state
            self._game_bridge.state.tokens = token_state
            self._notify_game_state_changed(domain="map")
            self.statusBar().showMessage(f"Map loaded: {path}")
        except Exception as exc:
            QMessageBox.critical(self, "Load Map Failed", str(exc))

    def _save_character(self) -> None:
        current_row = self.character_list.currentRow()
        if current_row < 0:
            self.statusBar().showMessage("No character selected")
            return
        char = self.characters[current_row]
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Character",
            default_character_filename(char),
            "Phoenix Command Character (*.json)",
        )
        if not path:
            return
        try:
            save_character_file(path, char)
            self.statusBar().showMessage(f"Character saved: {path}")
        except Exception as exc:
            QMessageBox.critical(self, "Save Character Failed", str(exc))

    def _load_character(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Character",
            "",
            "Phoenix Command Character (*.json)",
        )
        if not path:
            return
        try:
            character = load_character_file(path)
            existing = {c.name for c in self.characters}
            if character.name in existing:
                reply = QMessageBox.question(
                    self,
                    "Duplicate Name",
                    f"A character named '{character.name}' already exists. Add anyway?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No,
                )
                if reply != QMessageBox.StandardButton.Yes:
                    return
            self.characters.append(character)
            self.hex_map_view.set_character_names([c.name for c in self.characters])
            self._refresh_character_list()
            self.character_list.setCurrentRow(len(self.characters) - 1)
            self._game_bridge.capture_from_window(self)
            self._notify_game_state_changed()
            self.statusBar().showMessage(f"Character loaded: {character.name}")
        except Exception as exc:
            QMessageBox.critical(self, "Load Character Failed", str(exc))

    def _manage_layers(self) -> None:
        from phoenix_command.gui.dialogs.map_dialogs import MapLayerManagerDialog
        dialog = MapLayerManagerDialog(self.hex_map_view.get_map_state(), parent=self)
        dialog.exec()
        self.hex_map_view.set_map_state(self.hex_map_view.get_map_state())
        self._notify_game_state_changed(domain="map")

    def _show_action_catalog(self) -> None:
        from phoenix_command.gui.dialogs.map_dialogs import ActionCatalogDialog
        dialog = ActionCatalogDialog(self._game_bridge.state.meta.actions, parent=self)
        dialog.exec()
        self._notify_game_state_changed(domain="meta")

    def _add_custom_barrier(self) -> None:
        from phoenix_command.gui.dialogs.map_dialogs import CustomBarrierDialog
        dialog = CustomBarrierDialog(parent=self)
        if not dialog.exec():
            return
        material = dialog.get_material()
        map_state = self.hex_map_view.get_map_state()
        map_state.custom_barriers[material.id] = material
        self.hex_map_view.set_map_state(map_state)
        self._notify_game_state_changed(domain="map")

    def _add_character(self):
        """Open character creation dialog."""
        from phoenix_command.gui.dialogs.character_dialog import CharacterDialog
        dialog = CharacterDialog(parent=self)
        if dialog.exec():
            character = dialog.get_character()
            if character:
                self.characters.append(character)
                self.hex_map_view.set_character_names([c.name for c in self.characters])
                self._refresh_character_list()
                self.statusBar().showMessage(f"Added character: {character.name}")
                self._notify_game_state_changed()

    def _refresh_character_list(self):
        """Refresh character list display."""
        self.character_list.clear()
        for char in self.characters:
            self.character_list.addItem(char.name)

    def _on_character_selected(self, index):
        """Display character details when selected."""
        if 0 <= index < len(self.characters):
            self.stats_display.set_character(self.characters[index])
            self.body_diagram.set_character(self.characters[index])
        else:
            self.stats_display.clear()
            self.body_diagram.clear()
        self._notify_game_state_changed()

    def _edit_character(self):
        """Edit selected character stats."""
        current_row = self.character_list.currentRow()
        if current_row < 0:
            self.statusBar().showMessage("No character selected")
            return

        from phoenix_command.gui.dialogs.character_dialog import CharacterDialog
        char = self.characters[current_row]
        dialog = CharacterDialog(character=char, parent=self)
        if dialog.exec():
            dialog.get_character()
            self._refresh_character_list()
            self._on_character_selected(current_row)
            self.combat_zone.refresh_cards()
            self.statusBar().showMessage(f"Updated character: {char.name}")
            self._notify_game_state_changed()

    def _remove_character(self):
        """Remove selected character from the session."""
        current_row = self.character_list.currentRow()
        if current_row < 0:
            self.statusBar().showMessage("No character selected")
            return

        char = self.characters[current_row]
        reply = QMessageBox.question(
            self,
            "Remove Character",
            f"Remove {char.name} from the session?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        self.combat_zone.remove_character(char.name)
        del self.characters[current_row]
        self.hex_map_view.set_character_names([c.name for c in self.characters])
        self._refresh_character_list()

        if self.characters:
            new_row = min(current_row, len(self.characters) - 1)
            self.character_list.setCurrentRow(new_row)
        else:
            self.stats_display.clear()
            self.body_diagram.clear()

        self.statusBar().showMessage(f"Removed character: {char.name}")
        self._notify_game_state_changed()

    def _manage_equipment(self):
        """Open equipment management dialog."""
        current_row = self.character_list.currentRow()
        if current_row < 0:
            self.statusBar().showMessage("No character selected")
            return

        from phoenix_command.gui.dialogs.equipment_dialog import EquipmentDialog
        char = self.characters[current_row]
        dialog = EquipmentDialog(character=char, parent=self)
        dialog.exec()
        self._on_character_selected(current_row)
        self.statusBar().showMessage(f"Equipment updated for {char.name}")
        self._notify_game_state_changed()

    def _after_combat_dialog(self) -> None:
        self.body_diagram.refresh()
        self.combat_zone.refresh_cards()
        self._notify_game_state_changed()

    def _single_shot(self):
        """Open single shot dialog."""
        if len(self.characters) < 2:
            self.statusBar().showMessage("Need at least 2 characters for combat")
            return

        from phoenix_command.gui.dialogs.shot_dialog import ShotDialog
        dialog = ShotDialog(characters=self.characters, parent=self)
        if dialog.exec():
            self._after_combat_dialog()

    def _three_round_burst(self):
        """Open three round burst dialog."""
        if len(self.characters) < 2:
            self.statusBar().showMessage("Need at least 2 characters for combat")
            return

        from phoenix_command.models.gear import Weapon
        has_3rb_weapon = False
        for char in self.characters:
            for item in char.equipment:
                if isinstance(item, Weapon) and item.ballistic_data and item.ballistic_data.three_round_burst:
                    has_3rb_weapon = True
                    break
            if has_3rb_weapon:
                break

        if not has_3rb_weapon:
            self.statusBar().showMessage("No character has a weapon with three round burst capability")
            return

        from phoenix_command.gui.dialogs.three_round_burst_dialog import ThreeRoundBurstDialog
        dialog = ThreeRoundBurstDialog(characters=self.characters, parent=self)
        if dialog.exec():
            self._after_combat_dialog()

    def _burst_fire(self):
        """Open burst fire dialog."""
        if len(self.characters) < 2:
            self.statusBar().showMessage("Need at least 2 characters for combat")
            return

        from phoenix_command.models.gear import Weapon
        has_full_auto_weapon = False
        for char in self.characters:
            for item in char.equipment:
                if isinstance(item, Weapon) and item.full_auto and item.full_auto_rof:
                    has_full_auto_weapon = True
                    break
            if has_full_auto_weapon:
                break

        if not has_full_auto_weapon:
            self.statusBar().showMessage("No character has a full auto capable weapon")
            return

        from phoenix_command.gui.dialogs.burst_fire_dialog import BurstFireDialog
        dialog = BurstFireDialog(characters=self.characters, parent=self)
        if dialog.exec():
            self._after_combat_dialog()

    def _explosion_damage(self):
        """Open explosion damage dialog."""
        if len(self.characters) < 1:
            self.statusBar().showMessage("Need at least 1 character")
            return

        from phoenix_command.gui.dialogs.explosion_damage_dialog import ExplosionDamageDialog
        dialog = ExplosionDamageDialog(characters=self.characters, parent=self)
        if dialog.exec():
            self._after_combat_dialog()

    def _thrown_grenade(self):
        """Open thrown grenade dialog."""
        if len(self.characters) < 1:
            self.statusBar().showMessage("Need at least 1 character")
            return

        from phoenix_command.models.gear import Grenade
        has_grenade = False
        for char in self.characters:
            for item in char.equipment:
                if isinstance(item, Grenade):
                    has_grenade = True
                    break
            if has_grenade:
                break

        if not has_grenade:
            self.statusBar().showMessage("No character has a grenade")
            return

        from phoenix_command.gui.dialogs.thrown_grenade_dialog import ThrownGrenadeDialog
        dialog = ThrownGrenadeDialog(characters=self.characters, parent=self)
        if dialog.exec():
            self._after_combat_dialog()

    def _log_shot_result(self, result):
        """Log shot result to combat log."""
        target_name = result.target.name if hasattr(result, 'target') and result.target else "Unknown"
        if result.hit:
            if result.damage_result:
                msg = f"{target_name} - {result.damage_result.location.name}: {result.damage_result.damage} damage, {result.damage_result.shock} shock"
                if result.incapacitation_effect:
                    msg += f" ({result.incapacitation_effect.name})"
                    self.combat_log.append_critical(msg)
                else:
                    self.combat_log.append_hit(msg)
            else:
                self.combat_log.append_hit(f"{target_name} - Hit")
        else:
            self.combat_log.append_miss(f"{target_name} - Miss (Roll: {result.roll} vs {result.odds}%)")
        self.body_diagram.refresh()
        self._notify_game_state_changed()
