import json
from pathlib import Path

from poser.domain.normalization import scene_hash
from poser.domain.scene_schema import SceneRequest


def test_scene_hash_is_stable():
    payload = json.loads(Path("tests/fixtures/scenes/minimal_scene.json").read_text())
    s1 = SceneRequest.model_validate(payload)
    s2 = SceneRequest.model_validate(payload)
    assert scene_hash(s1) == scene_hash(s2)
