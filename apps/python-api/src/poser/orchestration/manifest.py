from __future__ import annotations

from pydantic import BaseModel


class RenderManifest(BaseModel):
    scene_hash: str
    backend: str
    model_id: str
    seed: int
    width: int
    height: int
