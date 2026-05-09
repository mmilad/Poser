import json
from pathlib import Path

from poser.domain.scene_schema import SceneRequest
from poser.planning.compiler import build_render_plan


def test_render_plan_maps_scene_to_pose_and_identity():
    payload = json.loads(Path("tests/fixtures/scenes/minimal_scene.json").read_text())
    scene = SceneRequest.model_validate(payload)
    plan = build_render_plan(scene)
    assert plan.seed == 1234
    assert plan.conditioning.pose_map.endswith("attack_02.png")
    assert plan.conditioning.identity_refs[0].endswith("refs/main.png")
