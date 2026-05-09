from __future__ import annotations

from poser.planning.render_plan import RenderPlan


def build_workflow(plan: RenderPlan) -> dict:
    return {
        "meta": {"version": 1, "kind": "poser-minimal"},
        "nodes": [
            {"id": "sampler", "type": "KSampler", "seed": plan.seed, "steps": plan.steps, "cfg": plan.cfg_scale, "sampler": plan.sampler},
            {"id": "size", "type": "EmptyLatentImage", "width": plan.width, "height": plan.height},
            {"id": "pose", "type": "LoadImage", "path": plan.conditioning.pose_map},
            {"id": "identity", "type": "LoadImage", "path": plan.conditioning.identity_refs[0] if plan.conditioning.identity_refs else None},
        ],
    }
