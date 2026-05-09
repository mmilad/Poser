from __future__ import annotations

from fastapi import APIRouter

from poser.backends.comfyui.adapter import ComfyUIAdapter
from poser.domain.normalization import scene_hash
from poser.domain.scene_schema import SceneRequest
from poser.orchestration.manifest import RenderManifest
from poser.planning.compiler import build_render_plan

router = APIRouter()


@router.post("/validate-scene")
def validate_scene(scene: SceneRequest):
    return {"valid": True, "scene_hash": scene_hash(scene)}


@router.post("/render")
def render_scene(scene: SceneRequest):
    plan = build_render_plan(scene)
    backend = ComfyUIAdapter()
    job = backend.compile(plan)
    result = backend.execute(job)
    manifest = RenderManifest(
        scene_hash=scene_hash(scene),
        backend="comfyui-mock",
        model_id=plan.model_id,
        seed=plan.seed,
        width=plan.width,
        height=plan.height,
    )
    return {"job_id": manifest.scene_hash[:12], "manifest": manifest.model_dump(), "result": result.metadata}


@router.get("/render/{job_id}")
def render_status(job_id: str):
    return {"job_id": job_id, "status": "completed"}
