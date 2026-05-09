# Poser Monorepo

This repository is now organized as a monorepo with applications under `apps/*`.

## Apps

- `apps/python-api` — Python/FastAPI render orchestration for ComfyUI.
- `apps/pose-api` — Next.js deterministic pose resolver API.

## Development focus

When actively developing the Next.js app, Python tests are not required.

## Web app (pose-api)

```bash
npm install
npm run dev:web
```

Pose resolve endpoint:

- `POST /api/v1/pose/resolve`

Behavior:

- deterministic regex/rule parsing
- deterministic fuzzy scoring
- hard fail with `POSE_NOT_FOUND` when no pose meets threshold

## Python app (comfy/render)

Python sources and tests are isolated in `apps/python-api`.

Run manually when needed:

```bash
cd apps/python-api
python -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'
uvicorn poser.api.app:app --reload
```
