from __future__ import annotations

import os
import time
from poser.backends.base import BackendJobSpec, BackendResult
from poser.backends.comfyui.client import ComfyUIClient
from poser.backends.comfyui.workflow_builder import build_workflow
from poser.planning.render_plan import RenderPlan


class ComfyUIAdapter:
    def __init__(self, base_url: str | None = None, execute_live: bool | None = None) -> None:
        self.base_url = base_url or os.getenv("COMFYUI_BASE_URL", "http://127.0.0.1:8188")
        self.execute_live = execute_live if execute_live is not None else os.getenv("POSER_COMFYUI_LIVE", "0") == "1"

    def compile(self, plan: RenderPlan) -> BackendJobSpec:
        return BackendJobSpec(workflow=build_workflow(plan))

    def execute(self, job: BackendJobSpec) -> BackendResult:
        if self.execute_live:
            response = ComfyUIClient(self.base_url).prompt(job.workflow)
            return BackendResult(artifacts=[], metadata={"backend": "comfyui", "executed": True, "response": response})

        return BackendResult(
            artifacts=["outputs/mock.png"],
            metadata={"backend": "comfyui", "executed": False, "timestamp": int(time.time()), "workflow": job.workflow},
        )

    def capabilities(self) -> dict:
        return {"pose": True, "identity": True, "depth": False, "segmentation": False}

    def healthcheck(self) -> dict:
        return {"status": "ok", "mode": "live" if self.execute_live else "mock", "base_url": self.base_url}
