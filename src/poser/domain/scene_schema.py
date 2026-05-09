from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field


class Position(BaseModel):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


class Equipment(BaseModel):
    weapon_r: str | None = None
    weapon_l: str | None = None
    back: str | None = None


class Character(BaseModel):
    id: str
    pose: str
    expression: str | None = None
    equipment: Equipment = Field(default_factory=Equipment)
    position: Position = Field(default_factory=Position)


class SceneMeta(BaseModel):
    environment: str
    time: str


class Camera(BaseModel):
    yaw: float = 0.0
    pitch: float = 0.0
    distance: float = 2.5


class RenderConfig(BaseModel):
    seed: int = 42
    width: int = 768
    height: int = 1024
    steps: int = 28
    cfg_scale: float = 6.0
    sampler: Literal["euler", "euler_a", "dpmpp_2m", "ddim"] = "dpmpp_2m"


class SceneRequest(BaseModel):
    scene: SceneMeta
    camera: Camera = Field(default_factory=Camera)
    characters: list[Character]
    render: RenderConfig = Field(default_factory=RenderConfig)
