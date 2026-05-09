from __future__ import annotations

from poser.domain.scene_schema import SceneRequest
from poser.planning.render_plan import ConditioningInputs, RenderPlan


def build_render_plan(scene: SceneRequest) -> RenderPlan:
    first = scene.characters[0]
    return RenderPlan(
        conditioning=ConditioningInputs(
            pose_map=f"assets/characters/{first.id}/poses/{first.pose}.png",
            identity_refs=[f"assets/characters/{first.id}/refs/main.png"],
        ),
        seed=scene.render.seed,
        width=scene.render.width,
        height=scene.render.height,
        steps=scene.render.steps,
        cfg_scale=scene.render.cfg_scale,
        sampler=scene.render.sampler,
    )
