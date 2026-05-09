from poser.backends.comfyui.adapter import ComfyUIAdapter
from poser.backends.base import BackendJobSpec


def test_comfyui_adapter_mock_mode():
    adapter = ComfyUIAdapter(execute_live=False)
    result = adapter.execute(BackendJobSpec(workflow={"a": 1}))
    assert result.metadata["executed"] is False
    assert result.metadata["backend"] == "comfyui"


def test_comfyui_adapter_live_mode(monkeypatch):
    adapter = ComfyUIAdapter(execute_live=True)

    class FakeClient:
        def __init__(self, base_url: str):
            self.base_url = base_url

        def prompt(self, workflow: dict) -> dict:
            return {"prompt_id": "abc123", "workflow": workflow}

    monkeypatch.setattr("poser.backends.comfyui.adapter.ComfyUIClient", FakeClient)
    result = adapter.execute(BackendJobSpec(workflow={"b": 2}))
    assert result.metadata["executed"] is True
    assert result.metadata["response"]["prompt_id"] == "abc123"
