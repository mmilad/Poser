from __future__ import annotations

import hashlib
import json

from .scene_schema import SceneRequest


def normalize_scene(scene: SceneRequest) -> dict:
    payload = scene.model_dump(mode="json")
    payload["characters"] = sorted(payload["characters"], key=lambda c: c["id"])
    return payload


def scene_hash(scene: SceneRequest) -> str:
    normalized = normalize_scene(scene)
    encoded = json.dumps(normalized, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
