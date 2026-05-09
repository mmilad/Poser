from __future__ import annotations

import importlib.util
import pytest


REQUIRED_MODULES = ("pydantic",)
OPTIONAL_INTEGRATION_MODULES = ("fastapi",)


def _missing(modules: tuple[str, ...]) -> list[str]:
    return [m for m in modules if importlib.util.find_spec(m) is None]


def pytest_sessionstart(session: pytest.Session) -> None:
    missing_core = _missing(REQUIRED_MODULES)
    if missing_core:
        pytest.exit(
            "Missing required test dependencies: "
            + ", ".join(missing_core)
            + ". Install with: pip install -e '.[test]'",
            returncode=2,
        )


def pytest_configure(config: pytest.Config) -> None:
    missing_optional = _missing(OPTIONAL_INTEGRATION_MODULES)
    if missing_optional:
        config.addinivalue_line(
            "markers",
            "integration: integration tests requiring optional API dependencies",
        )
