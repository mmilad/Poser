import json
from pathlib import Path

from poser.backends.comfyui.workflow_builder import build_workflow
from poser.domain.scene_schema import SceneRequest
from poser.planning.compiler import build_render_plan


def test_workflow_matches_expected_fixture():
    payload = json.loads(Path("tests/fixtures/scenes/minimal_scene.json").read_text())
    expected = json.loads(Path("tests/fixtures/expected_workflows/minimal_workflow.json").read_text())
    scene = SceneRequest.model_validate(payload)
    plan = build_render_plan(scene)
    actual = build_workflow(plan)
    assert actual == expected
