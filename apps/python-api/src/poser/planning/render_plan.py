from __future__ import annotations

from pydantic import BaseModel, Field


class ConditioningInputs(BaseModel):
    pose_map: str | None = None
    depth_map: str | None = None
    segmentation_map: str | None = None
    identity_refs: list[str] = Field(default_factory=list)


class RenderPlan(BaseModel):
    model_id: str = "anime-base-v1"
    conditioning: ConditioningInputs
    seed: int
    width: int
    height: int
    steps: int
    cfg_scale: float
    sampler: str
