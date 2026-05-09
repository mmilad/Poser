# Poser

Deterministic AI-assisted anime/manhwa rendering pipeline.

## Vision

Poser is a **scene compiler + neural renderer**:

- scene data is authoritative
- conditioning assets are deterministic
- backend inference is replaceable
- rendering is reproducible and testable

This repository currently contains an implementation blueprint and a minimal architecture plan oriented around local inference on a single machine.

## Core principles

- Deterministic structured inputs
- Reproducible outputs
- No prompt-centric control flow
- Scene-graph-driven rendering
- Semantic asset organization
- Modular conditioning pipeline
- Composable render passes
- Backend abstraction layer
- API-first architecture
- Local inference support
- Testability

## Initial proof-of-concept target

1. Load character references from directory structure
2. Apply pose conditioning (OpenPose / ControlNet)
3. Apply identity conditioning (IP-Adapter or equivalent)
4. Generate deterministic anime-style render
5. Minimal REST API
6. Minimal scene schema
7. Local execution
8. Basic integration tests
9. Minimal dependency footprint
10. Stable workflow generation

See `docs/architecture.md` for detailed recommendations.

## Quick start (WSL / Linux)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'
pytest
```

Run API:

```bash
uvicorn poser.api.app:app --reload
```

OpenAPI docs: `http://127.0.0.1:8000/docs`


### ComfyUI execution modes

By default, renders run in **mock mode** for deterministic development/testing without requiring a running inference service.

To use a local ComfyUI instance:

```bash
export POSER_COMFYUI_LIVE=1
export COMFYUI_BASE_URL=http://127.0.0.1:8188
pytest -q
```

This is intended for Windows users running Poser inside WSL while ComfyUI is available locally.


## Testing notes

If dependencies are missing, the test session exits early with a clear message instead of producing noisy import-trace failures.

Recommended install command:

```bash
pip install -e '.[test]'
```
