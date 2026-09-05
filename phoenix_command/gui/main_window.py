"""Main window for Phoenix Command GUI."""

import uuid

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
    QDialog,
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
    make_intent_nack,
    make_player_intent,
)
from phoenix_command.session.domains.player_info import PlayerInfo
from phoenix_command.simulations.impulse_combat_engine import ImpulseCombatEngine


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.characters = []
        self.setWindowTitle("Phoenix Command")

        self._session_role: str | None = None  # "host", "guest", or None
        self._player_id: str = "host"
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

        options_menu = menubar.addMenu("&Options")
        from phoenix_command.gui.app_settings import get_show_blast_modifier_dialog

        self._blast_review_action = options_menu.addAction(
            "Review &blast modifiers before damage"
        )
        self._blast_review_action.setCheckable(True)
        self._blast_review_action.setChecked(get_show_blast_modifier_dialog())
        self._blast_review_action.toggled.connect(self._on_blast_review_toggled)

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
        self.hex_map_view.combat_action_requested.connect(self._on_combat_action_requested)
        self.hex_map_view.advance_impulse_requested.connect(self._on_advance_impulse)
        self.hex_map_view.map_mode_changed.connect(self._on_map_mode_changed)
        self.hex_map_view.declare_shot_requested.connect(self._on_declare_shot)
        self.hex_map_view.aim_hex_picked.connect(self._on_aim_hex_picked)
        self.hex_map_view.combat_status_hint.connect(self._on_combat_status_hint)
        self.hex_map_view.set_action_provider(self._token_available_actions)
        self._shot_preview_dialog = None
        self._center_tabs.addTab(self.combat_zone, "Combat")
        self._center_tabs.addTab(self.hex_map_view, "Map")
        center_splitter.addWidget(self._center_tabs)

        self.combat_log = CombatLogWidget()
        center_splitter.addWidget(self.combat_log)
        center_splitter.setStretchFactor(0, 4)
        center_splitter.setStretchFactor(1, 1)
        center_splitter.setSizes([560, 140])

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
        self._save_session_action.setEnabled(not guest)
        self._load_session_action.setEnabled(not guest)
        self.combat_menu.setEnabled(not guest)
        self._new_map_action.setEnabled(not guest)
        self._save_map_action.setEnabled(not guest)
        self._load_map_action.setEnabled(not guest)
        self._manage_layers_action.setEnabled(not guest)
        self._action_catalog_action.setEnabled(not guest)
        self._custom_barrier_action.setEnabled(not guest)
        self.hex_map_view.set_editable(not guest)
        if guest:
            self.hex_map_view.set_session_context("guest", self._player_id, self._game_bridge.state.meta.players)
        else:
            self.hex_map_view.set_session_context(self._session_role, self._player_id, self._game_bridge.state.meta.players)
        self.character_list.setDragEnabled(not guest)
        self._host_session_action.setEnabled(not guest)
        self._join_session_action.setEnabled(not guest)
        self._new_session_action.setEnabled(not guest)
        if hasattr(self, "combat_zone"):
            self.combat_zone.set_actions_enabled(not guest)

    def _notify_game_state_changed(self, domain: str = "combat", immediate: bool = False) -> None:
        if self._session_role == "host" and self._publisher:
            self._publisher.notify_changed(domain=domain, immediate=immediate)

    def _broadcast_sync_message(self, message: SyncMessage) -> None:
        if self._p2p_host:
            self._p2p_host.broadcast_message(message)
        if self._relay_client:
            self._relay_client.send_message(message)

    def _send_nack(self, player_id: str, intent_id: str, reason: str) -> None:
        nack = make_intent_nack(intent_id, reason, player_id=player_id)
        if self._p2p_host:
            self._p2p_host.send_to_player(player_id, nack)
        else:
            self._broadcast_sync_message(nack)

    def _on_host_sync_message(self, slot_id: str, message: SyncMessage) -> None:
        if message.type == MessageType.REQUEST_STATE and self._publisher:
            # publish_now already broadcasts via _broadcast_sync_message
            self._publisher.publish_now()
        elif message.type == MessageType.PLAYER_HELLO and message.payload:
            self._handle_player_hello(slot_id, message.payload)
        elif message.type == MessageType.PLAYER_INTENT and message.payload:
            self._handle_player_intent(message.payload)

    def _on_sync_message_received(self, message: SyncMessage) -> None:
        if self._session_role == "guest":
            if message.type == MessageType.INTENT_NACK and message.payload:
                target = message.payload.get("player_id")
                if target and target != self._player_id:
                    return
                reason = message.payload.get("reason", "Action rejected")
                if self._shot_preview_dialog is not None:
                    self._shot_preview_dialog.reject_confirm_keep_open(reason)
                self.statusBar().showMessage(f"Guest: {reason}")
                return
            new_state = apply_message_to_state(self._game_bridge.state, message)
            self._game_bridge.apply_remote_state(new_state, self)
            self._maybe_show_shot_preview()
            self._show_guest_sync_status(new_state.revision)

    def _pending_move_hint_text(self) -> str:
        """Guest hint when selected token has an unfinished move."""
        ic = self._game_bridge.state.impulse_combat
        sel = ic.selected_token_id
        if not sel:
            return ""
        rt = ic.token_runtime.get(sel)
        if rt and rt.pending_id() == "move":
            return (
                "Continue Move (Do Action → Move / pick hex) — "
                "Next Impulse does not finish pending movement"
            )
        return ""

    def _show_guest_sync_status(self, revision: int) -> None:
        """Status line after sync; keep Continue Move hint on the same line."""
        hint = self._pending_move_hint_text()
        if hint:
            self.statusBar().showMessage(f"Guest: synced r{revision} — {hint}")
        else:
            self.statusBar().showMessage(f"Guest: synced revision {revision}")

    def _maybe_hint_pending_move(self) -> None:
        """Remind guest that Next Impulse does not finish a pending move."""
        hint = self._pending_move_hint_text()
        if hint:
            self.statusBar().showMessage(f"Guest: {hint}")

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
        host_name = self._host_dialog.display_name
        self._player_id = "host"
        meta = self._game_bridge.state.meta
        meta.host_name = host_name
        meta.players = [PlayerInfo("host", host_name, is_host=True)]
        self._p2p_host = P2PSessionHost(parent=self)
        self._publisher = GameStatePublisher(self._broadcast_sync_message)
        self._publisher.attach(self, self._game_bridge)

        from PyQt6.QtCore import Qt as _Qt
        _q = _Qt.ConnectionType.QueuedConnection
        self._p2p_host.invite_ready.connect(self._on_invite_ready, _q)
        self._p2p_host.guest_connected.connect(self._on_guest_connected, _q)
        self._p2p_host.guest_disconnected.connect(self._on_host_guest_disconnected, _q)
        self._p2p_host.connection_failed.connect(self._on_connection_failed, _q)
        self._p2p_host.ice_state_changed.connect(self._on_ice_state, _q)
        self._p2p_host.set_message_handler(self._on_host_sync_message)
        self._host_dialog.answer_submitted.connect(self._on_host_answer_submitted)
        self._host_dialog.new_invite_requested.connect(self._on_new_invite_requested)

        self._session_role = "host"
        self._disconnect_action.setEnabled(True)
        self._p2p_host.start()
        self._host_dialog.show()

    def _on_invite_ready(self, slot_id: str, code: str) -> None:
        if self._host_dialog:
            self._host_dialog.set_invite_code(code, slot_id=slot_id)
        self.statusBar().showMessage(f"Host: invite ready ({slot_id}) — send via Discord")

    def _on_new_invite_requested(self) -> None:
        if self._p2p_host:
            self._p2p_host.create_invite()

    def _on_guest_connected(self, slot_id: str) -> None:
        # Do not overwrite an existing hello:* slot status (channel-open / HELLO race).
        if self._host_dialog:
            info = self._host_dialog._slots.get(slot_id) or {}
            prev = str(info.get("status") or "")
            if not prev.startswith("hello"):
                self._host_dialog.set_slot_status(slot_id, "connected")
        if self._publisher:
            # publish_now already broadcasts
            self._publisher.publish_now()
        self.hex_map_view.set_session_context(
            self._session_role, self._player_id, self._game_bridge.state.meta.players
        )
        self.statusBar().showMessage(f"Host: guest slot {slot_id} connected")
        self._maybe_qa_auto_hello(slot_id)

    @staticmethod
    def _qa_auto_hello_enabled() -> bool:
        """Opt-in only — must not default on in production."""
        import os
        return os.environ.get("PC_QA_AUTO_HELLO") == "1"

    def _maybe_qa_auto_hello(self, slot_id: str) -> bool:
        if not self._qa_auto_hello_enabled():
            return False
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(
            500,
            lambda: self._handle_player_hello(
                slot_id,
                {"player_id": "guest-0", "display_name": "GuestTester"},
            ),
        )
        return True

    def _handle_player_hello(self, slot_id: str, payload: dict) -> None:
        player_id = payload.get("player_id") or f"guest-{uuid.uuid4().hex[:8]}"
        display_name = payload.get("display_name", player_id)
        if self._p2p_host:
            self._p2p_host.bind_player(slot_id, player_id)
        meta = self._game_bridge.state.meta
        if meta.get_player(player_id) is None:
            meta.players.append(PlayerInfo(player_id, display_name, is_host=False))
        else:
            for p in meta.players:
                if p.player_id == player_id:
                    p.display_name = display_name
        meta.connected_guests = [p.display_name for p in meta.players if not p.is_host]
        self._game_bridge.state.bump_revision()
        if self._host_dialog:
            self._host_dialog.set_slot_status(slot_id, f"hello: {display_name}", player_id)
        self.hex_map_view.set_session_context(
            self._session_role, self._player_id, self._game_bridge.state.meta.players
        )
        # Auto-assign first free token only under explicit QA flag.
        if self._qa_auto_hello_enabled() and self._game_bridge.state.tokens is not None:
            tokens = self._game_bridge.state.tokens.placements
            if not any(tok.controlled_by == player_id for tok in tokens.values()):
                for tok in tokens.values():
                    if not tok.controlled_by:
                        tok.controlled_by = player_id
                        self.statusBar().showMessage(
                            f"Host: auto-assigned {tok.character_name or tok.token_id} → {display_name}"
                        )
                        break
        self.statusBar().showMessage(f"Host: hello from {display_name} ({player_id})")
        self._notify_game_state_changed(domain="meta", immediate=True)
        self._notify_game_state_changed(domain="tokens", immediate=True)

    def _handle_player_intent(self, payload: dict) -> None:
        player_id = payload.get("player_id", "")
        intent_id = payload.get("intent_id", "")
        token_id = payload.get("token_id", "")
        action = payload.get("action", "")
        args = payload.get("args") or {}
        if action == "open_shot_preview":
            ok, msg = self._host_open_shot_preview(token_id, player_id)
            if not ok:
                self._send_nack(player_id, intent_id, msg)
            else:
                self._notify_game_state_changed(domain="impulse_combat", immediate=True)
            return
        if action == "update_shot_preview":
            ok, msg = self._host_update_shot_preview(args.get("preview") or args, player_id)
            if not ok:
                self._send_nack(player_id, intent_id, msg)
            else:
                self._notify_game_state_changed(domain="impulse_combat", immediate=True)
            return
        if action == "confirm_shot":
            ok, msg = self._host_confirm_shot(player_id)
            if not ok:
                self._send_nack(player_id, intent_id, msg)
            else:
                self._notify_game_state_changed(immediate=True)
            return
        if action == "cancel_shot":
            if not self._can_edit_preview(player_id):
                self._send_nack(player_id, intent_id, "Cannot cancel this shot preview")
                return
            self._game_bridge.state.impulse_combat.shot_preview = None
            self._notify_game_state_changed(domain="impulse_combat", immediate=True)
            return
        if action == "abandon_pending":
            result = self._apply_combat_action(token_id, action, args, player_id, is_host=False)
            if not result.success:
                self._send_nack(player_id, intent_id, result.message)
            else:
                self.statusBar().showMessage(result.message)
                self.combat_log.append_system(result.message)
                self._notify_game_state_changed(domain="impulse_combat", immediate=True)
            return
        result = self._apply_combat_action(token_id, action, args, player_id, is_host=False)
        if not result.success:
            self._send_nack(player_id, intent_id, result.message)
        else:
            self.statusBar().showMessage(result.message)
            self.combat_log.append_system(result.message)
            self._notify_game_state_changed(domain="impulse_combat", immediate=True)

    def _on_host_answer_submitted(self, slot_id: str, answer: str) -> None:
        if self._p2p_host:
            self._p2p_host.submit_answer(slot_id, answer)
            if self._host_dialog:
                self._host_dialog.set_slot_status(slot_id, "answer submitted")

    def _join_session(self) -> None:
        if self._session_role:
            QMessageBox.warning(self, "Session Active", "Disconnect first.")
            return

        from phoenix_command.gui.dialogs.session_dialog import JoinSessionDialog
        from phoenix_command.session.p2p_guest import P2PSessionGuest

        dialog = JoinSessionDialog(parent=self)
        if not dialog.exec():
            return

        self._player_id = f"guest-{uuid.uuid4().hex[:8]}"
        self._guest_display_name = dialog.display_name

        self._join_dialog = dialog
        self._p2p_guest = P2PSessionGuest(parent=self)
        # Pre-register before connect so answerer already-open bootstrap can send HELLO.
        self._p2p_guest.set_hello_credentials(self._player_id, self._guest_display_name)
        from PyQt6.QtCore import Qt as _Qt
        _q = _Qt.ConnectionType.QueuedConnection
        self._p2p_guest.answer_ready.connect(self._on_answer_ready, _q)
        self._p2p_guest.connected.connect(self._on_guest_connected_to_host, _q)
        self._p2p_guest.channel_open.connect(self._on_guest_channel_open, _q)
        self._p2p_guest.disconnected.connect(self._on_guest_disconnected, _q)
        self._p2p_guest.connection_failed.connect(self._on_connection_failed, _q)
        self._p2p_guest.send_failed.connect(self._on_guest_send_failed, _q)
        self._p2p_guest.ice_state_changed.connect(self._on_ice_state, _q)
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
        self.statusBar().showMessage("Guest: ICE connected — waiting for data channel")

    def _on_guest_channel_open(self) -> None:
        self.statusBar().showMessage("Guest: connected to host")
        if self._p2p_guest:
            name = getattr(self, "_guest_display_name", None)
            if name is None and self._join_dialog:
                name = self._join_dialog.display_name
            name = name or "Player"
            # Retry HELLO only — primary send is already-open bootstrap.
            self._p2p_guest.send_player_hello(self._player_id, name)
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(
                400,
                lambda n=name: self._p2p_guest
                and self._p2p_guest.send_player_hello(self._player_id, n),
            )

    def _on_guest_send_failed(self, error: str) -> None:
        self.statusBar().showMessage(f"Guest: uplink send failed — retry ({error})")

    def _on_guest_disconnected(self) -> None:
        """ICE/channel drop on guest side — leave guest mode entirely."""
        self._disconnect_session()

    def _on_host_guest_disconnected(self, slot_id: str) -> None:
        """Guest channel closed — update slot UI and roster."""
        player_id = None
        if self._p2p_host:
            player_id = self._p2p_host.player_id_for_slot(slot_id)
        if self._host_dialog:
            self._host_dialog.set_slot_status(slot_id, "disconnected")
        meta = self._game_bridge.state.meta
        if player_id:
            meta.players = [p for p in meta.players if p.player_id != player_id]
        meta.connected_guests = [p.display_name for p in meta.players if not p.is_host]
        self._game_bridge.state.bump_revision()
        if self._publisher:
            self._publisher.publish_now()
        self.hex_map_view.set_session_context(
            self._session_role, self._player_id, meta.players
        )
        self.statusBar().showMessage(f"Host: guest slot {slot_id} disconnected")

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
        self._player_id = "host"
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

    def _characters_by_name(self) -> dict:
        return {c.name: c for c in self.characters}

    def _merge_map_characters(self, loaded: dict) -> None:
        """Import characters bundled with a map file into the session roster."""
        if not loaded:
            return
        by_name = self._characters_by_name()
        for name, char in loaded.items():
            if name in by_name:
                idx = next(i for i, c in enumerate(self.characters) if c.name == name)
                self.characters[idx] = char
            else:
                self.characters.append(char)
        self._refresh_character_list()

    def _is_combat_authority(self) -> bool:
        """Solo (None) and host may resolve combat; guests only send intents."""
        return self._session_role != "guest"

    def _combat_engine(self) -> ImpulseCombatEngine:
        tokens = self.hex_map_view.get_token_state()
        ic = self.hex_map_view.get_impulse_combat_state()
        self._game_bridge.state.tokens = tokens
        self._game_bridge.state.impulse_combat = ic
        return ImpulseCombatEngine(
            ic,
            tokens,
            self._game_bridge.state.map or self.hex_map_view.get_map_state(),
            self._characters_by_name(),
        )

    def _token_available_actions(self, token_id: str):
        actions = self._combat_engine().available_actions(token_id)
        if self._session_role == "guest":
            actions = [a for a in actions if a[0] != "set_medical_aid"]
        return actions

    def _apply_combat_action(
        self,
        token_id: str,
        action: str,
        args: dict,
        player_id: str,
        is_host: bool,
    ):
        engine = self._combat_engine()
        result = engine.apply_action(token_id, action, args, player_id, is_host)
        if result.success:
            self.hex_map_view.set_impulse_combat_state(
                self._game_bridge.state.impulse_combat, rebuild=False
            )
            if state := self._game_bridge.state.tokens:
                self.hex_map_view.set_token_state(state)
        return result

    def _on_combat_status_hint(self, message: str) -> None:
        self.statusBar().showMessage(message)
        self.combat_log.append_system(message)

    def _on_combat_action_requested(self, token_id: str, action: str, args: dict) -> None:
        from PyQt6.QtWidgets import QMessageBox

        if action == "select_weapon":
            args = dict(args)
            name = self._prompt_select_weapon(token_id)
            if not name:
                return
            args["weapon_name"] = name
        if action == "aim":
            args = dict(args)
            target_id = self._pick_enemy_token_id(token_id)
            if target_id:
                args["target_token_id"] = target_id

        ic = self.hex_map_view.get_impulse_combat_state()
        rt = ic.token_runtime.get(token_id)
        if action == "duck" and rt and rt.has_pending():
            pending = rt.pending_id() or "action"
            reply = QMessageBox.question(
                self,
                "Duck interrupts action",
                f"Duck will abandon pending {pending} and clear aim. Continue?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        if action == "abandon_pending":
            pending = (rt.pending_id() if rt else None) or "action"
            reply = QMessageBox.question(
                self,
                "Abandon pending",
                f"Abandon pending {pending}? Progress will be lost.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        if self._session_role == "guest":
            import uuid
            intent = make_player_intent(self._player_id, str(uuid.uuid4()), token_id, action, args)
            if self._p2p_guest:
                self._p2p_guest.send_message(intent)
            return
        result = self._apply_combat_action(token_id, action, args, self._player_id, is_host=True)
        if (
            not result.success
            and result.message.startswith("Abandon or continue pending")
            and rt
            and rt.has_pending()
        ):
            pending = rt.pending_id() or "action"
            reply = QMessageBox.question(
                self,
                "Pending action",
                f"{result.message}\nAbandon {pending} and retry?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                abandon = self._apply_combat_action(
                    token_id, "abandon_pending", {}, self._player_id, is_host=True
                )
                self.combat_log.append_system(abandon.message)
                if abandon.success:
                    result = self._apply_combat_action(
                        token_id, action, args, self._player_id, is_host=True
                    )
        msg = result.message if result.message else "Action applied"
        self.statusBar().showMessage(msg)
        self.combat_log.append_system(msg)
        if action == "pick_up_grenade" and result.success:
            ic = self.hex_map_view.get_impulse_combat_state()
            rt = ic.token_runtime.get(token_id)
            tok = self.hex_map_view.get_token_state().placements.get(token_id)
            if rt and rt.held_grenade_name and not rt.grenade_armed and tok and tok.character_name:
                char = self._characters_by_name().get(tok.character_name)
                arm_cost = 0
                if char:
                    from phoenix_command.models.gear import Grenade
                    for item in char.equipment:
                        if isinstance(item, Grenade) and item.name == rt.held_grenade_name:
                            arm_cost = int(item.arm_time or 0)
                            break
                if arm_cost > 0:
                    hint = f"Grenade in hand — Arm ({arm_cost} AC) then Declare Shot"
                    self.statusBar().showMessage(hint)
                    self.combat_log.append_system(hint)
        if result.success:
            self.hex_map_view._refresh_combat_ui()
            self._notify_game_state_changed(domain="impulse_combat")

    def _prompt_select_weapon(self, token_id: str) -> str | None:
        from PyQt6.QtWidgets import QInputDialog
        tokens = self.hex_map_view.get_token_state()
        tok = tokens.placements.get(token_id)
        if not tok or not tok.character_name:
            return None
        char = self._characters_by_name().get(tok.character_name)
        if not char:
            return None
        from phoenix_command.models.gear import Weapon
        names = [i.name for i in char.equipment if isinstance(i, Weapon)]
        if not names:
            return None
        choice, ok = QInputDialog.getItem(self, "Select Weapon", "Weapon:", names, 0, False)
        return choice if ok else None

    def _prompt_fire_gear(self, char, shooter_rt, interactive: bool = True):
        """Choose weapon or grenade when Declare Shot and both are available."""
        from phoenix_command.models.gear import Grenade, Weapon

        if shooter_rt.held_grenade_name:
            for item in char.equipment:
                if isinstance(item, Grenade) and item.name == shooter_rt.held_grenade_name:
                    return item, item
        weapons = [i for i in char.equipment if isinstance(i, Weapon)]
        grenades = [i for i in char.equipment if isinstance(i, Grenade)]
        if grenades and weapons:
            if not interactive:
                # Guest intent path: prefer held weapon, else first weapon.
                if shooter_rt.held_weapon_name:
                    for item in weapons:
                        if item.name == shooter_rt.held_weapon_name:
                            return item, None
                return weapons[0], None
            from PyQt6.QtWidgets import QInputDialog

            options = [f"Weapon: {w.name}" for w in weapons] + [
                f"Grenade: {g.name}" for g in grenades
            ]
            choice, ok = QInputDialog.getItem(
                self, "Declare Shot", "Fire with:", options, 0, False
            )
            if not ok:
                return None, None
            if choice.startswith("Grenade:"):
                gname = choice.split(": ", 1)[1]
                g = next(x for x in grenades if x.name == gname)
                return g, g
            wname = choice.split(": ", 1)[1]
            w = next(x for x in weapons if x.name == wname)
            return w, None
        if weapons:
            w = weapons[0]
            if shooter_rt.held_weapon_name:
                for item in weapons:
                    if item.name == shooter_rt.held_weapon_name:
                        w = item
                        break
            return w, None
        if grenades:
            return grenades[0], grenades[0]
        return None, None

    def _ammo_options_for_weapon(self, weapon) -> list[str]:
        from phoenix_command.models.gear import AmmoType

        names: list[str] = []
        for raw in getattr(weapon, "ammunition_types", None) or []:
            if isinstance(raw, AmmoType):
                names.append(raw.name)
        return names

    def _re_enrich_shot_preview(self, preview):
        from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime

        tokens = self.hex_map_view.get_token_state()
        shooter = tokens.placements.get(preview.shooter_token_id)
        if not shooter or not shooter.character_name:
            return preview
        char = self._characters_by_name().get(shooter.character_name)
        if not char:
            return preview
        weapon, ammo, _err = self._resolve_weapon_ammo(char, preview)
        ic = self.hex_map_view.get_impulse_combat_state()
        from phoenix_command.simulations.map_fire_dispatch import enrich_preview_targets

        return enrich_preview_targets(
            preview,
            shooter,
            tokens,
            self.hex_map_view.get_map_state(),
            ic.token_runtime,
            weapon,
            ammo,
        )

    def _pick_enemy_token_id(self, shooter_id: str) -> str | None:
        tokens = self.hex_map_view.get_token_state()
        shooter = tokens.placements.get(shooter_id)
        if not shooter:
            return None
        for tid, tok in tokens.placements.items():
            if tid != shooter_id and tok.character_name and tok.side_id != shooter.side_id:
                return tid
        return None

    def _on_advance_impulse(self) -> None:
        if not self._is_combat_authority():
            return
        engine = self._combat_engine()
        due_proj, due_grenades, wound_logs = engine.advance_impulse()
        ic = self._game_bridge.state.impulse_combat
        self.hex_map_view.set_impulse_combat_state(ic, rebuild=False)
        for line in wound_logs:
            self.combat_log.append_system(line)
        for proj in due_proj:
            self._resolve_pending_projectile(proj)
        for expl in due_grenades:
            self._resolve_pending_grenade_explosion(expl)
        sel = ic.selected_token_id
        rt = ic.token_runtime.get(sel or "")
        ac_txt = f" AC {rt.ac_remaining:.1f}" if rt else ""
        self.statusBar().showMessage(
            f"Impulse {ic.impulse + 1}/4 (Phase {ic.phase}){ac_txt}"
        )
        self._notify_game_state_changed(immediate=True)

    def _on_declare_shot(self, shooter_token_id: str) -> None:
        from PyQt6.QtWidgets import QMessageBox

        ic = self.hex_map_view.get_impulse_combat_state()
        rt = ic.token_runtime.get(shooter_token_id)
        if rt and rt.has_pending():
            pending = rt.pending_id() or "action"
            reply = QMessageBox.question(
                self,
                "Pending action",
                f"Token has pending {pending}. Abandon it to declare a shot?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
            if self._session_role == "guest":
                abandon_intent = make_player_intent(
                    self._player_id,
                    str(uuid.uuid4()),
                    shooter_token_id,
                    "abandon_pending",
                    {},
                )
                if self._p2p_guest:
                    self._p2p_guest.send_message(abandon_intent)
            else:
                result = self._apply_combat_action(
                    shooter_token_id, "abandon_pending", {}, self._player_id, is_host=True
                )
                self.combat_log.append_system(result.message)
                if not result.success:
                    self.statusBar().showMessage(result.message)
                    return
                self.hex_map_view._refresh_combat_ui()

        if self._session_role == "guest":
            intent = make_player_intent(
                self._player_id,
                str(uuid.uuid4()),
                shooter_token_id,
                "open_shot_preview",
                {},
            )
            if self._p2p_guest:
                self._p2p_guest.send_message(intent)
            return
        ok, msg = self._host_open_shot_preview(shooter_token_id, self._player_id)
        if not ok:
            self.statusBar().showMessage(msg)
            return
        self._notify_game_state_changed(domain="impulse_combat", immediate=True)
        self._maybe_show_shot_preview()

    def _build_preview_from_tokens(
        self, shooter_token_id: str, proposed_by: str, interactive: bool = True
    ):
        import uuid
        from phoenix_command.models.gear import AmmoType, Weapon
        from phoenix_command.session.domains.impulse_combat_state import (
            PendingShotPreview,
            TokenCombatRuntime,
        )
        from phoenix_command.simulations.map_shot_context import build_map_shot_context

        ic = self.hex_map_view.get_impulse_combat_state()
        tokens = self.hex_map_view.get_token_state()
        shooter = tokens.placements.get(shooter_token_id)
        if not shooter or not shooter.character_name:
            return None, "Shooter token missing character"
        target_id = self._pick_enemy_token_id(shooter_token_id)
        if not target_id:
            return None, "No enemy token found"
        target = tokens.placements[target_id]
        shooter_rt = ic.token_runtime.get(shooter_token_id, TokenCombatRuntime())
        target_rt = ic.token_runtime.get(target_id, TokenCombatRuntime())
        from phoenix_command.simulations.map_wounds import can_fire_weapon

        ok_fire, fire_msg = can_fire_weapon(shooter_rt)
        if not ok_fire:
            return None, fire_msg
        char = self._characters_by_name().get(shooter.character_name)
        weapon = None
        ammo_name = ""
        tof = 0
        ammo = None
        if char:
            from phoenix_command.models.gear import Grenade
            from phoenix_command.simulations.map_fire_targets import default_ammo_for_weapon

            weapon, grenade_ammo = self._prompt_fire_gear(
                char, shooter_rt, interactive=interactive
            )
            if weapon is None:
                return None, "No weapon or grenade available"
            if grenade_ammo is not None:
                ammo = grenade_ammo
                ammo_name = grenade_ammo.name
            elif isinstance(weapon, Grenade):
                ammo = weapon
                ammo_name = weapon.name
            elif getattr(weapon, "ammunition_types", None):
                from phoenix_command.models.gear import AmmoType as _AmmoType

                raw = default_ammo_for_weapon(weapon, shooter_rt.fire_mode)
                ammo = raw if isinstance(raw, _AmmoType) else None
                ammo_name = ammo.name if ammo else str(raw)

        # provisional range for PEN (refined after context)
        from phoenix_command.gui.utils.hex_geometry import axial_distance
        from phoenix_command.session.domains.map_state import rules_hexes
        map_state = self.hex_map_view.get_map_state()
        mph = map_state.grid.meters_per_hex if map_state else 1.0
        approx_range = max(
            1,
            round(rules_hexes(axial_distance(shooter.q, shooter.r, target.q, target.r) * mph)),
        )
        pen = None
        if ammo is not None and hasattr(ammo, "get_pen"):
            pen = float(ammo.get_pen(approx_range))

        ctx = build_map_shot_context(
            shooter,
            shooter_rt,
            target,
            target_rt,
            map_state,
            pen=pen,
            weapon=weapon if isinstance(weapon, Weapon) else None,
        )
        if ctx.los and ctx.los.blocked:
            return None, "No LOS to target"
        if weapon and getattr(weapon, "ballistic_data", None):
            tof = int(weapon.ballistic_data.get_time_of_flight(ctx.range_rule_hexes) or 0)

        cover = ctx.los.cover if ctx.los else None
        from phoenix_command.models.enums import WeaponType

        fire_mode = shooter_rt.fire_mode
        if (
            isinstance(weapon, Weapon)
            and weapon.full_auto
            and getattr(weapon, "weapon_type", None) == WeaponType.AUTOMATIC_GRENADE_LAUNCHER
        ):
            fire_mode = "auto"
        preview = PendingShotPreview(
            preview_id=str(uuid.uuid4()),
            shooter_token_id=shooter_token_id,
            target_token_id=target_id,
            proposed_by=proposed_by,
            status="open",
            range_hexes=ctx.range_rule_hexes,
            exposure=ctx.target_exposure.name,
            orientation=ctx.shot_params.target_orientation.name,
            stance_mods=[m.name for m in ctx.shot_params.situation_stance_modifiers],
            visibility_mods=[m.name for m in ctx.shot_params.visibility_modifiers],
            aim_time_ac=ctx.shot_params.aim_time_ac,
            fire_mode=fire_mode,
            weapon_name=weapon.name if weapon else "",
            ammo_name=ammo_name,
            visible_exposures=[e.name for e in ctx.visible_exposures],
            selected_exposure=ctx.target_exposure.name,
            tof_impulses=tof,
            notes=list(ctx.visibility_notes),
            shooter_speed=ctx.shot_params.shooter_speed_hex_per_impulse,
            target_speed=ctx.shot_params.target_speed_hex_per_impulse,
            is_front=ctx.is_front_shot,
            target_token_ids=[target_id],
            cover_notes=list(cover.notes) if cover else [],
            estimated_cover_pf=float(cover.estimated_cover_pf) if cover else 0.0,
        )
        from phoenix_command.simulations.map_fire_dispatch import enrich_preview_targets

        preview = enrich_preview_targets(
            preview,
            shooter,
            tokens,
            self.hex_map_view.get_map_state(),
            ic.token_runtime,
            weapon,
            ammo,
        )
        return preview, ""

    def _host_open_shot_preview(self, shooter_token_id: str, player_id: str):
        tokens = self.hex_map_view.get_token_state()
        tok = tokens.placements.get(shooter_token_id)
        if not tok:
            return False, "Token not found"
        engine = self._combat_engine()
        if not engine.can_control_token(player_id, tok, is_host=(player_id == "host")):
            return False, "No control of shooter"
        # Guest intents must not pop QInputDialog on the host machine.
        preview, err = self._build_preview_from_tokens(
            shooter_token_id, player_id, interactive=(player_id == "host")
        )
        if not preview:
            return False, err
        self._game_bridge.state.impulse_combat = self.hex_map_view.get_impulse_combat_state()
        self._game_bridge.state.impulse_combat.shot_preview = preview
        self.hex_map_view.set_impulse_combat_state(
            self._game_bridge.state.impulse_combat, rebuild=False
        )
        return True, ""

    def _can_edit_preview(self, player_id: str) -> bool:
        preview = self._game_bridge.state.impulse_combat.shot_preview
        if not preview:
            return False
        if player_id == "host" or self._session_role == "host":
            return True
        tokens = self.hex_map_view.get_token_state()
        tok = tokens.placements.get(preview.shooter_token_id)
        return bool(tok and tok.controlled_by == player_id)

    def _host_update_shot_preview(self, preview_data: dict, player_id: str):
        from phoenix_command.session.domains.impulse_combat_state import PendingShotPreview
        if not self._can_edit_preview(player_id):
            return False, "Cannot edit preview"
        if isinstance(preview_data, PendingShotPreview):
            preview = preview_data
        else:
            preview = PendingShotPreview.from_dict(preview_data)
        preview.status = "open"
        preview = self._re_enrich_shot_preview(preview)
        self._game_bridge.state.impulse_combat.shot_preview = preview
        self.hex_map_view.set_impulse_combat_state(
            self._game_bridge.state.impulse_combat, rebuild=False
        )
        return True, ""

    def _host_confirm_shot(self, player_id: str):
        if not self._can_edit_preview(player_id):
            return False, "Cannot confirm shot"
        preview = self._game_bridge.state.impulse_combat.shot_preview
        if not preview or preview.status != "open":
            return False, "No open preview"
        # Guest confirm must not open MapBlastReviewDialog on the host machine.
        return self._execute_confirmed_preview(preview, interactive=False)

    def _resolve_weapon_ammo(self, shooter, preview):
        from phoenix_command.models.gear import AmmoType, Grenade, Weapon

        weapon = None
        for item in shooter.equipment:
            if isinstance(item, (Weapon, Grenade)) and item.name == preview.weapon_name:
                weapon = item
                break
        if weapon is None:
            for item in shooter.equipment:
                if isinstance(item, (Weapon, Grenade)):
                    weapon = item
                    break
        if not weapon:
            return None, None, "No weapon"

        ammo = None
        if isinstance(weapon, Grenade):
            ammo = weapon
        elif preview.ammo_name:
            for a in getattr(weapon, "ammunition_types", None) or []:
                if isinstance(a, AmmoType) and a.name == preview.ammo_name:
                    ammo = a
                    break
        if ammo is None and getattr(weapon, "ammunition_types", None):
            ammo = weapon.ammunition_types[0]
        if not ammo:
            return weapon, None, "No ammo"
        return weapon, ammo, ""

    def _execute_confirmed_preview(
        self, preview, *, interactive: bool = True
    ) -> tuple[bool, str]:
        from phoenix_command.simulations.map_fire_dispatch import build_snapshot, explosive_result_to_dict
        from phoenix_command.simulations.map_fire_targets import infer_fire_kind
        from phoenix_command.simulations.map_fire_ac import (
            apply_fire_ac,
            clear_aim_state,
            clear_grenade_hand,
            plan_fire_ac,
            sync_preview_from_plan,
            validate_fire_ac,
        )
        from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime

        tokens = self.hex_map_view.get_token_state()
        shooter_tok = tokens.placements.get(preview.shooter_token_id)
        if not shooter_tok:
            return False, "Shooter token missing"
        chars = self._characters_by_name()
        shooter = chars.get(shooter_tok.character_name or "")
        if not shooter:
            return False, "Shooter character missing"

        weapon, ammo, err = self._resolve_weapon_ammo(shooter, preview)
        if err:
            return False, err

        ic = self._game_bridge.state.impulse_combat
        shooter_rt = ic.token_runtime.get(preview.shooter_token_id, TokenCombatRuntime())
        from phoenix_command.simulations.map_wounds import can_fire_weapon

        ok_fire, fire_msg = can_fire_weapon(shooter_rt)
        if not ok_fire:
            return False, fire_msg
        fire_kind = infer_fire_kind(preview.fire_mode, weapon, ammo)
        preview.fire_kind = fire_kind
        plan = plan_fire_ac(preview, shooter_rt, fire_kind, weapon)
        ok, msg = validate_fire_ac(plan, shooter_rt, fire_kind)
        if not ok:
            return False, msg

        sync_preview_from_plan(preview, plan, shooter_rt)
        apply_fire_ac(plan, shooter_rt)
        shooter_rt.fire_mode = preview.fire_mode
        clear_aim_state(shooter_rt)
        if fire_kind == "grenade":
            clear_grenade_hand(shooter_rt)

        primary_ids = preview.primary_ids()
        target_names = {}
        for tid in primary_ids:
            tok = tokens.placements.get(tid)
            if tok and tok.character_name:
                target_names[tid] = tok.character_name
        if preview.target_token_id and preview.target_token_id not in target_names:
            tok = tokens.placements.get(preview.target_token_id)
            if tok and tok.character_name:
                target_names[preview.target_token_id] = tok.character_name

        snapshot = build_snapshot(preview, shooter.name, target_names)

        ic.shot_preview = None
        self.hex_map_view.clear_fire_overlay()
        self.hex_map_view.set_impulse_combat_state(ic, rebuild=False)

        if preview.tof_impulses and preview.tof_impulses > 0:
            engine = self._combat_engine()
            engine.schedule_projectile(
                preview.shooter_token_id,
                preview.target_token_id or (primary_ids[0] if primary_ids else ""),
                preview.tof_impulses,
                snapshot,
            )
            label = ", ".join(target_names.values()) or "aim hex"
            self.combat_log.append_system(
                f"Shot in flight: {shooter.name} → {label}, TOF {preview.tof_impulses} impulse(s)"
            )
            self.statusBar().showMessage(f"Projectile in flight ({preview.tof_impulses} impulses)")
            self._notify_game_state_changed(domain="impulse_combat", immediate=True)
            return True, "scheduled"

        outcome = self._dispatch_map_fire_with_blast_review(
            preview,
            shooter,
            weapon,
            ammo,
            tokens,
            chars,
            self.hex_map_view.get_map_state(),
            ic.token_runtime,
            interactive=interactive,
        )
        if outcome.fuse_impulses > 0 and outcome.explosive_results and not outcome.blast_cancelled:
            engine = self._combat_engine()
            engine.schedule_grenade_explosion(
                preview.shooter_token_id,
                outcome.fuse_impulses,
                preview.to_dict(),
                [explosive_result_to_dict(e) for e in outcome.explosive_results],
                preview.weapon_name,
                preview.ammo_name,
                blast_mod_overrides=outcome.blast_mod_overrides,
            )
            self.hex_map_view.set_impulse_combat_state(ic, rebuild=False)
        self._apply_map_fire_outcome(outcome)
        self.hex_map_view._refresh_combat_ui()
        self._notify_game_state_changed(domain="impulse_combat", immediate=True)
        return True, "resolved"

    def _on_blast_review_toggled(self, checked: bool) -> None:
        from phoenix_command.gui.app_settings import set_show_blast_modifier_dialog

        set_show_blast_modifier_dialog(checked)

    def _dispatch_map_fire_with_blast_review(
        self,
        preview,
        shooter,
        weapon,
        ammo,
        tokens,
        chars,
        map_state,
        token_runtime,
        *,
        interactive: bool = True,
    ):
        from phoenix_command.gui.app_settings import get_show_blast_modifier_dialog
        from phoenix_command.simulations.map_fire_dispatch import (
            apply_pending_blast_damage,
            dispatch_map_fire,
            serialize_blast_mod_overrides,
        )

        review = interactive and get_show_blast_modifier_dialog()
        abs_impulse = self._combat_engine().absolute_impulse_index()
        outcome = dispatch_map_fire(
            preview,
            shooter,
            weapon,
            ammo,
            tokens,
            chars,
            map_state,
            token_runtime,
            apply_blast=not review,
            abs_impulse=abs_impulse,
        )
        package = outcome.pending_blast
        has_victims = package and any(p.victims for p in package.passes)
        fuse_deferred = outcome.fuse_impulses > 0
        if review and has_victims and outcome.blast_ammo:
            from phoenix_command.gui.dialogs.map_blast_review_dialog import (
                MapBlastReviewDialog,
            )

            dlg = MapBlastReviewDialog(package, tokens, parent=self)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                mods = dlg.mod_overrides()
                if fuse_deferred:
                    # Defer PD until fuse due; keep reviewed mods for resolve.
                    outcome.blast_mod_overrides = serialize_blast_mod_overrides(mods)
                    outcome.messages.append(
                        "Blast modifiers saved; damage deferred until fuse expires"
                    )
                else:
                    outcome.shot_results.extend(
                        apply_pending_blast_damage(
                            package,
                            outcome.blast_ammo,
                            preview,
                            tokens,
                            chars,
                            map_state,
                            token_runtime,
                            mods,
                            abs_impulse=abs_impulse,
                        )
                    )
            else:
                outcome.messages.append("Blast damage cancelled")
                if fuse_deferred:
                    outcome.blast_cancelled = True
                    outcome.fuse_impulses = 0
        return outcome

    def _apply_map_fire_outcome(self, outcome) -> None:
        for reason in outcome.miss_reasons:
            self.combat_log.append_miss(f"Miss: {reason}")
        for msg in outcome.messages:
            self.combat_log.append_system(msg)
        for expl in outcome.explosive_results:
            if expl.hit:
                self.combat_log.append_hit(
                    f"Explosive HIT (roll {expl.roll} vs {expl.odds}%)"
                )
            else:
                self.combat_log.append_miss(
                    f"Explosive miss — scatter {expl.scatter_hexes} "
                    f"({'long' if expl.is_long else 'short'})"
                )
        for result in outcome.shot_results:
            self._append_shot_result(result)
        if not outcome.shot_results and not outcome.explosive_results and not outcome.miss_reasons:
            self.combat_log.append_system(f"Fire ({outcome.kind}): no results")
        self.body_diagram.refresh()
        self.combat_zone.refresh_cards()

    def _append_shot_result(self, result) -> None:
        if result.hit:
            self.combat_log.append_hit(result.log or "Hit")
        else:
            self.combat_log.append_miss(result.log or "Miss")
        if result.log:
            self.combat_log.append_detailed(result.log)
        self.body_diagram.refresh()
        self.combat_zone.refresh_cards()

    def _resolve_pending_projectile(self, proj) -> None:
        from phoenix_command.simulations.map_fire_dispatch import (
            preview_from_snapshot,
        )
        from phoenix_command.gui.utils.hex_geometry import axial_distance
        from phoenix_command.session.domains.map_state import rules_hexes
        from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime
        from phoenix_command.simulations.map_shot_context import build_map_shot_context

        snap = proj.shot_snapshot
        tokens = self.hex_map_view.get_token_state()
        shooter_tok = tokens.placements.get(proj.shooter_token_id)
        if not shooter_tok:
            self.combat_log.append_system("In-flight shot: shooter gone — miss")
            return
        chars = self._characters_by_name()
        shooter = chars.get(snap.get("shooter_name", "") or shooter_tok.character_name or "")
        if not shooter:
            self.combat_log.append_system("In-flight shot: shooter character missing")
            return

        class _P:
            weapon_name = snap.get("weapon_name", "")
            ammo_name = snap.get("ammo_name", "")

        weapon, ammo, err = self._resolve_weapon_ammo(shooter, _P())
        if err:
            self.combat_log.append_system(f"In-flight shot: {err}")
            return

        preview = preview_from_snapshot(snap, proj.shooter_token_id, proj.target_token_id)
        ic = self.hex_map_view.get_impulse_combat_state()
        map_state = self.hex_map_view.get_map_state()

        # Refresh ranges from current positions; keep frozen shot_params from snapshot
        for tid in list(preview.primary_ids()):
            tok = tokens.placements.get(tid)
            if not tok:
                continue
            ctx = build_map_shot_context(
                shooter_tok,
                ic.token_runtime.get(proj.shooter_token_id, TokenCombatRuntime()),
                tok,
                ic.token_runtime.get(tid, TokenCombatRuntime()),
                map_state,
            )
            per = dict(preview.per_target.get(tid, {}))
            per["range_hexes"] = ctx.range_rule_hexes
            per["los_clear"] = bool(ctx.los and ctx.los.clear and not ctx.los.blocked)
            preview.per_target[tid] = per

        if preview.aim_q is not None and preview.aim_r is not None and map_state:
            mph = map_state.grid.meters_per_hex
            dist_m = axial_distance(shooter_tok.q, shooter_tok.r, preview.aim_q, preview.aim_r) * mph
            preview.range_hexes = max(1, round(rules_hexes(dist_m)))

        outcome = self._dispatch_map_fire_with_blast_review(
            preview,
            shooter,
            weapon,
            ammo,
            tokens,
            chars,
            map_state,
            ic.token_runtime,
        )
        self._apply_map_fire_outcome(outcome)

    def _resolve_pending_grenade_explosion(self, expl) -> None:
        from phoenix_command.simulations.map_fire_dispatch import (
            resolve_pending_grenade_explosion,
        )
        from phoenix_command.models.gear import Grenade

        tokens = self.hex_map_view.get_token_state()
        shooter_tok = tokens.placements.get(expl.shooter_token_id)
        if not shooter_tok:
            self.combat_log.append_system("Fused grenade: shooter gone")
            return
        chars = self._characters_by_name()
        shooter = chars.get(shooter_tok.character_name or "")
        if not shooter:
            self.combat_log.append_system("Fused grenade: shooter character missing")
            return

        class _P:
            weapon_name = expl.weapon_name
            ammo_name = expl.ammo_name

        weapon, ammo, err = self._resolve_weapon_ammo(shooter, _P())
        if err:
            self.combat_log.append_system(f"Fused grenade: {err}")
            return
        ic = self.hex_map_view.get_impulse_combat_state()
        outcome = resolve_pending_grenade_explosion(
            expl,
            shooter,
            weapon,
            ammo or weapon,
            tokens,
            chars,
            self.hex_map_view.get_map_state(),
            ic.token_runtime,
            abs_impulse=self._combat_engine().absolute_impulse_index(),
        )
        self._apply_map_fire_outcome(outcome)

    def _maybe_show_shot_preview(self) -> None:
        from phoenix_command.gui.dialogs.map_shot_preview_dialog import MapShotPreviewDialog

        preview = self._game_bridge.state.impulse_combat.shot_preview
        if not preview or preview.status != "open":
            if self._shot_preview_dialog:
                self._shot_preview_dialog.close()
                self._shot_preview_dialog = None
            self.hex_map_view.clear_fire_overlay()
            return
        editable = self._can_edit_preview(self._player_id)
        tokens = self.hex_map_view.get_token_state()
        labels = {
            tid: (tok.character_name or tok.label or tid)
            for tid, tok in tokens.placements.items()
        }
        ic = self._game_bridge.state.impulse_combat
        shooter_rt = ic.token_runtime.get(preview.shooter_token_id)
        aim_accumulated = int(shooter_rt.aim_ac_accumulated) if shooter_rt else 0
        is_hip = aim_accumulated <= 0 and preview.fire_kind not in (
            "grenade",
            "agl",
            "explosive",
        )
        ammo_options: list[str] = []
        shooter_tok = tokens.placements.get(preview.shooter_token_id)
        if shooter_tok and shooter_tok.character_name:
            char = self._characters_by_name().get(shooter_tok.character_name)
            if char:
                from phoenix_command.models.gear import Weapon

                for item in char.equipment:
                    if isinstance(item, Weapon) and item.name == preview.weapon_name:
                        ammo_options = self._ammo_options_for_weapon(item)
                        break
        if self._shot_preview_dialog is None:
            self._shot_preview_dialog = MapShotPreviewDialog(
                preview,
                editable=editable,
                token_labels=labels,
                aim_accumulated=aim_accumulated,
                is_hip_fire=is_hip,
                ammo_options=ammo_options,
                parent=self,
            )
            self._shot_preview_dialog.preview_updated.connect(self._on_preview_edited)
            self._shot_preview_dialog.confirmed.connect(self._on_preview_confirmed)
            self._shot_preview_dialog.cancelled.connect(self._on_preview_cancelled)
            self._shot_preview_dialog.pick_aim_hex_requested.connect(self._on_pick_aim_hex)
            self._shot_preview_dialog.overlay_refresh_requested.connect(
                self._on_preview_overlay
            )
            self._shot_preview_dialog.show()
        else:
            self._shot_preview_dialog._ammo_options = ammo_options
            self._shot_preview_dialog.apply_remote_preview(
                preview,
                aim_accumulated=aim_accumulated,
                is_hip_fire=is_hip,
            )
        self.hex_map_view.set_fire_overlay(preview)

    def _on_pick_aim_hex(self) -> None:
        self.statusBar().showMessage("Click a hex on the map for aim point…")
        self.hex_map_view.begin_pick_aim_hex()

    def _on_aim_hex_picked(self, q: int, r: int, layer_id: str) -> None:
        if self._shot_preview_dialog is None:
            return
        self._shot_preview_dialog.set_aim_hex(q, r, layer_id)
        self.statusBar().showMessage(f"Aim hex set to ({q}, {r})")

    def _on_preview_overlay(self, preview) -> None:
        self.hex_map_view.set_fire_overlay(preview)

    def _on_preview_edited(self, preview) -> None:
        if self._session_role == "guest":
            import uuid
            intent = make_player_intent(
                self._player_id,
                str(uuid.uuid4()),
                preview.shooter_token_id,
                "update_shot_preview",
                {"preview": preview.to_dict()},
            )
            if self._p2p_guest:
                self._p2p_guest.send_message(intent)
            return
        self._host_update_shot_preview(preview, self._player_id)
        self._notify_game_state_changed(domain="impulse_combat", immediate=True)

    def _on_preview_confirmed(self, preview) -> None:
        if self._session_role == "guest":
            # Keep dialog open until host sync clears or updates the preview.
            intent_u = make_player_intent(
                self._player_id,
                str(uuid.uuid4()),
                preview.shooter_token_id,
                "update_shot_preview",
                {"preview": preview.to_dict()},
            )
            intent_c = make_player_intent(
                self._player_id,
                str(uuid.uuid4()),
                preview.shooter_token_id,
                "confirm_shot",
                {},
            )
            if self._p2p_guest:
                self._p2p_guest.send_message(intent_u)
                self._p2p_guest.send_message(intent_c)
            self.statusBar().showMessage("Guest: shot submitted — waiting for host")
            return
        self._game_bridge.state.impulse_combat.shot_preview = preview
        preview = self._re_enrich_shot_preview(preview)
        ok, msg = self._execute_confirmed_preview(preview)
        if not ok:
            fail = f"Shot failed: {msg}"
            self.statusBar().showMessage(fail)
            self.combat_log.append_system(fail)
            preview.status = "open"
            self._game_bridge.state.impulse_combat.shot_preview = preview
            if self._shot_preview_dialog is not None:
                self._shot_preview_dialog.reject_confirm_keep_open(msg)
            return
        if self._shot_preview_dialog is not None:
            self._shot_preview_dialog.accept_after_confirm()
        self._shot_preview_dialog = None
        self.statusBar().showMessage(msg)
        self._notify_game_state_changed(immediate=True)

    def _on_preview_cancelled(self, preview_id: str) -> None:
        if self._session_role == "guest":
            import uuid
            intent = make_player_intent(
                self._player_id,
                str(uuid.uuid4()),
                "",
                "cancel_shot",
                {"preview_id": preview_id},
            )
            if self._p2p_guest:
                self._p2p_guest.send_message(intent)
            self._shot_preview_dialog = None
            return
        self._game_bridge.state.impulse_combat.shot_preview = None
        self.hex_map_view.set_impulse_combat_state(
            self._game_bridge.state.impulse_combat, rebuild=False
        )
        self._shot_preview_dialog = None
        self._notify_game_state_changed(domain="impulse_combat", immediate=True)

    def _on_map_mode_changed(self, mode: str) -> None:
        if not self._is_combat_authority():
            return
        # Sync bridge ← view first so refill mutates the same ImpulseCombatState
        engine = self._combat_engine()
        ic = self._game_bridge.state.impulse_combat
        ic.map_mode = mode
        if mode == "combat":
            engine.ensure_runtime_for_tokens()
            engine.refill_impulse_ac()
            if not ic.sides:
                ic.sides = {"alpha": "Alpha", "bravo": "Bravo"}
        self.hex_map_view.set_impulse_combat_state(ic)
        self.hex_map_view.set_editable(self._session_role != "guest")
        if mode == "combat":
            sel = ic.selected_token_id
            rt = ic.token_runtime.get(sel or "")
            ac_txt = f" — AC {rt.ac_remaining:.1f}" if rt else ""
            self.statusBar().showMessage(f"Combat mode (Impulse {ic.impulse + 1}/4){ac_txt}")
        self._notify_game_state_changed(domain="impulse_combat")

    def _map_shot_context_for_tokens(self):
        """Return MapShotContext if map combat has shooter/target tokens selected."""
        from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime
        from phoenix_command.simulations.map_shot_context import build_map_shot_context

        ic = self.hex_map_view.get_impulse_combat_state()
        tokens = self.hex_map_view.get_token_state()
        if ic.map_mode != "combat":
            return None
        shooter_id = ic.selected_token_id
        if not shooter_id:
            return None
        shooter_tok = tokens.placements.get(shooter_id)
        if not shooter_tok or not shooter_tok.character_name:
            return None
        target_tok = None
        for tid, tok in tokens.placements.items():
            if tid != shooter_id and tok.character_name and tok.side_id != shooter_tok.side_id:
                target_tok = tok
                break
        if not target_tok:
            return None
        shooter_rt = ic.token_runtime.get(shooter_id, TokenCombatRuntime())
        target_rt = ic.token_runtime.get(target_tok.token_id, TokenCombatRuntime())
        map_state = self.hex_map_view.get_map_state()
        ctx = build_map_shot_context(
            shooter_tok,
            shooter_rt,
            target_tok,
            target_rt,
            map_state,
        )
        return ctx, shooter_tok.character_name, target_tok.character_name

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
                characters=self._characters_by_name(),
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
            map_state, token_state, map_characters = load_map_file(path)
            self.hex_map_view.set_map_state(map_state)
            self.hex_map_view.set_token_state(token_state)
            self._merge_map_characters(map_characters)
            self.hex_map_view.set_character_names([c.name for c in self.characters])
            self._game_bridge.state.map = map_state
            self._game_bridge.state.tokens = token_state
            self._game_bridge.capture_from_window(self)
            self._notify_game_state_changed(domain="map")
            loaded_names = ", ".join(sorted(map_characters)) or "none"
            self.statusBar().showMessage(
                f"Map loaded: {path} (characters: {loaded_names})"
            )
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
        map_ctx = None
        shooter_name = None
        target_name = None
        ctx_pair = self._map_shot_context_for_tokens()
        if ctx_pair:
            map_ctx, shooter_name, target_name = ctx_pair
        dialog = ShotDialog(
            characters=self.characters,
            map_context=map_ctx,
            default_shooter_name=shooter_name,
            default_target_name=target_name,
            parent=self,
        )
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
