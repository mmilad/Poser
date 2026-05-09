from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from poser.planning.render_plan import RenderPlan


@dataclass
class BackendJobSpec:
    workflow: dict


@dataclass
class BackendResult:
    artifacts: list[str]
    metadata: dict


class BackendAdapter(Protocol):
    def compile(self, plan: RenderPlan) -> BackendJobSpec: ...

    def execute(self, job: BackendJobSpec) -> BackendResult: ...

    def capabilities(self) -> dict: ...

    def healthcheck(self) -> dict: ...
