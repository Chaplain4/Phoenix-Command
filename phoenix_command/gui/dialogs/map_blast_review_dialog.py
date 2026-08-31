"""Host review of auto-derived Table 5B blast modifiers before map explosion damage."""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

from phoenix_command.models.enums import BlastModifier
from phoenix_command.session.domains.token_state import TokenState
from phoenix_command.simulations.map_blast import PendingBlastPackage


class MapBlastReviewDialog(QDialog):
    """Confirm or override per-token blast modifiers after scatter placement."""

    def __init__(
        self,
        package: PendingBlastPackage,
        tokens: TokenState,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.setWindowTitle("Blast modifiers")
        self.setMinimumSize(560, 420)
        self._package = package
        self._tokens = tokens
        self._rows: dict[str, QListWidget] = {}
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        centers = []
        for i, p in enumerate(self._package.passes, start=1):
            tag = "hit" if p.hit else f"scatter {p.scatter_hexes}"
            centers.append(f"#{i} ({p.center_q},{p.center_r}) {tag}")
        layout.addWidget(QLabel("Blast center(s): " + "; ".join(centers) or "none"))

        seen: set[str] = set()
        for blast_pass in self._package.passes:
            for spec in blast_pass.victims:
                if spec.token_id in seen:
                    continue
                seen.add(spec.token_id)
                tok = self._tokens.placements.get(spec.token_id)
                name = (tok.character_name if tok else None) or spec.token_id
                layout.addWidget(
                    QLabel(
                        f"<b>{name}</b> — {spec.range_hex} hex(es) — "
                        f"auto: {', '.join(m.name for m in spec.derived_mods)}"
                    )
                )
                lst = QListWidget()
                lst.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
                derived = {m.name for m in spec.derived_mods}
                for bm in BlastModifier:
                    item = QListWidgetItem(bm.name)
                    lst.addItem(item)
                    item.setSelected(bm.name in derived)
                self._rows[spec.token_id] = lst
                layout.addWidget(lst)

        if not seen:
            layout.addWidget(QLabel("No tokens in blast radius."))

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        row = QHBoxLayout()
        row.addStretch()
        row.addWidget(buttons)
        layout.addLayout(row)

    def mod_overrides(self) -> dict[str, list[BlastModifier]]:
        by_name = {m.name: m for m in BlastModifier}
        out: dict[str, list[BlastModifier]] = {}
        for tid, lst in self._rows.items():
            mods = []
            for item in lst.selectedItems():
                bm = by_name.get(item.text())
                if bm is not None:
                    mods.append(bm)
            if not mods:
                mods = [BlastModifier.IN_THE_OPEN]
            out[tid] = mods
        return out
