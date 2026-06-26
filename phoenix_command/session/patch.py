"""Apply JSON Patch operations to nested dict state."""

from __future__ import annotations

import copy
from typing import Any


class PatchError(ValueError):
    """Invalid or inapplicable patch operation."""


def _decode_path(path: str) -> list[str]:
    if not path.startswith("/"):
        raise PatchError(f"Path must start with '/': {path!r}")
    if path == "/":
        return []
    parts = path.lstrip("/").split("/")
    return [p.replace("~1", "/").replace("~0", "~") for p in parts]


def _navigate_parent(doc: Any, parts: list[str], create: bool = False) -> tuple[Any, str]:
    if not parts:
        raise PatchError("Cannot navigate empty path for parent")
    current = doc
    for part in parts[:-1]:
        if isinstance(current, dict):
            if part not in current:
                if create:
                    current[part] = {}
                else:
                    raise PatchError(f"Missing key {part!r}")
            current = current[part]
        elif isinstance(current, list):
            idx = int(part)
            current = current[idx]
        else:
            raise PatchError(f"Cannot traverse into {type(current)}")
    return current, parts[-1]


def apply_patch(document: dict, operations: list[dict]) -> dict:
    """Apply RFC 6902-style patch operations (replace, add, remove)."""
    doc = copy.deepcopy(document)
    for op in operations:
        operation = op.get("op")
        path = op.get("path", "")
        parts = _decode_path(path)

        if operation == "replace":
            if not parts:
                if not isinstance(op.get("value"), dict):
                    raise PatchError("Root replace must be a dict")
                return copy.deepcopy(op["value"])
            parent, key = _navigate_parent(doc, parts)
            value = op["value"]
            if isinstance(parent, dict):
                parent[key] = copy.deepcopy(value)
            elif isinstance(parent, list):
                parent[int(key)] = copy.deepcopy(value)
            else:
                raise PatchError("replace target invalid")

        elif operation == "add":
            value = copy.deepcopy(op["value"])
            if not parts:
                raise PatchError("Root add not supported")
            parent, key = _navigate_parent(doc, parts[:-1], create=True) if len(parts) > 1 else (doc, parts[0])
            if isinstance(parent, dict):
                parent[key] = value
            elif isinstance(parent, list):
                idx = int(key) if key != "-" else len(parent)
                parent.insert(idx, value)
            else:
                raise PatchError("add target invalid")

        elif operation == "remove":
            if not parts:
                raise PatchError("Root remove not supported")
            parent, key = _navigate_parent(doc, parts)
            if isinstance(parent, dict):
                del parent[key]
            elif isinstance(parent, list):
                del parent[int(key)]
            else:
                raise PatchError("remove target invalid")

        else:
            raise PatchError(f"Unsupported op: {operation!r}")

    return doc
