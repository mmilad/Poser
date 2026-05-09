# Poser Architecture Blueprint (MVP)

## 1) Architecture analysis

The proposed direction is sound: treating inference as a compiler target keeps domain logic independent of tool-specific graph semantics.

Recommended split:

1. **Scene Domain Layer**
   - scene schema
   - validation
   - canonical normalization
2. **Asset Layer**
   - semantic IDs -> concrete files/metadata
   - versioning and hashing
3. **Conditioning Layer**
   - deterministic generation/loading of pose/depth/seg masks
   - consistent pre-processing
4. **Render Planning Layer**
   - scene -> render plan -> backend graph/job
5. **Backend Adapter Layer**
   - ComfyUI adapter now, Diffusers/Torch later
6. **Orchestration + API Layer**
   - REST endpoints
   - job lifecycle
   - reproducibility metadata

The key architectural move is to make **render plans backend-neutral IR** that can be compiled to any runtime.

## 2) Risks and bottlenecks

### Determinism risks
- Non-deterministic kernels/samplers across hardware/drivers
- Hidden randomness in preprocessing/transforms
- Implicit defaults in ComfyUI node configs

Mitigation:
- lock seed, sampler, scheduler, steps, CFG, resolution, model versions
- fix preprocessing algorithms + versions
- record full run manifest (including hashes)

### Coupling risks
- Business logic leaking into workflow JSON builders
- hardcoded node IDs/order assumptions

Mitigation:
- backend adapter boundary + strict contracts
- compile plan -> backend graph using symbolic node names then resolve IDs late

### Asset drift risks
- reference assets replaced without version bumps
- model file mismatch across environments

Mitigation:
- registry with content hashes
- model manifest + startup checks

### Performance risks (16GB VRAM)
- multi-character high-res scenes can OOM

Mitigation:
- capped default resolution (e.g. 768/896 longest side)
- optional tiled/highres pass disabled by default
- explicit memory profiles in backend config

## 3) Minimal viable implementation strategy

### Phase 0: Skeleton (1-2 days)
- define scene schema (Pydantic)
- define asset registry format
- define backend interface
- define render manifest format

### Phase 1: Single-character deterministic render (3-5 days)
- local asset loading
- pose map input + identity reference input
- compile backend-neutral render plan
- ComfyUI adapter compiles plan to workflow JSON and executes
- REST `/render` endpoint

### Phase 2: Integration quality bar (2-4 days)
- golden tests on workflow generation
- smoke integration tests against local ComfyUI
- deterministic replay test (same input -> same manifest + image hash tolerance policy)

### Phase 3: Composition extensions
- equipment attachments (2D anchor-based first)
- multi-character scene layering and z-order

## 4) Recommended directory structure

```text
poser/
  pyproject.toml
  README.md
  docs/
    architecture.md
    schema.md
  src/poser/
    api/
      app.py
      routes_render.py
    domain/
      scene_schema.py
      ids.py
      normalization.py
    assets/
      registry.py
      resolver.py
      models.py
    conditioning/
      pose.py
      depth.py
      segmentation.py
      identity.py
    planning/
      render_plan.py
      compiler.py
      passes.py
    backends/
      base.py
      comfyui/
        adapter.py
        workflow_builder.py
        client.py
      diffusers/
        adapter.py  # stub for migration path
    orchestration/
      renderer.py
      manifest.py
      cache.py
    utils/
      hashing.py
      image_io.py
      deterministic.py
  assets/
    characters/
      kairo/
        refs/
        embeddings/
        metadata.json
        poses/
    equipment/
      dagger_shadowfang/
        metadata.json
        masks/
    environments/
      ruined_city/
        metadata.json
    maps/
      pose/
      depth/
      seg/
  tests/
    unit/
    integration/
    fixtures/
      scenes/
      expected_workflows/
      assets/
```

## 5) Backend abstraction recommendation

Define a minimal interface:

- `compile(plan: RenderPlan) -> BackendJobSpec`
- `execute(job: BackendJobSpec) -> BackendResult`
- `capabilities() -> BackendCapabilities`
- `healthcheck() -> BackendHealth`

Rules:
- Domain/Planning layers never import ComfyUI-specific code.
- Backend returns normalized output structure:
  - image paths/bytes
  - timing
  - backend metadata
  - effective parameters used

## 6) Testing strategy

### Unit tests
- scene schema validation and normalization
- asset resolution correctness
- render plan compilation rules
- deterministic hash generation

### Contract tests
- same `RenderPlan` compiled through backend adapter yields stable workflow shape
- no prompt field becomes required for control

### Integration tests
- local ComfyUI smoke test (`/render` end-to-end)
- replay tests with frozen fixture inputs

### Determinism tests
- identical inputs + environment -> identical manifest
- image hash checks with pragmatic policy:
  - strict hash for fully deterministic modes
  - perceptual hash threshold for tolerated tiny backend variance

## 7) Workflow generation strategy

Use **template fragments + typed builder**, not giant static JSON:

1. Start from a compact canonical graph template per pipeline family.
2. Inject nodes from plan passes (pose, identity, style).
3. Resolve links symbolically.
4. Emit stable topological ordering for workflow JSON.
5. Snapshot expected workflow output in tests.

Avoid:
- manual editing node packs
- opaque mega-workflow files

## 8) Deterministic rendering practices

- fixed seed strategy (global + per-pass derived seeds)
- fixed sampler/scheduler/steps/CFG
- fixed precision and deterministic torch flags where supported
- pinned model/checkpoint/LoRA/IP-Adapter versions with SHA256
- deterministic pre-processing (resize, interpolation, normalization)
- stable filename policy derived from manifest hash
- run manifest persisted for every render:
  - scene hash
  - asset hashes
  - backend version
  - model hashes
  - effective parameters

## 9) Equipment/object attachment strategy

Start simple with 2D semantic attachment anchors:

- character skeleton anchor points (e.g. `hand_r`, `back`, `hip_l`)
- equipment metadata defines compatible anchors and offsets
- attachment compiler converts semantic attachment -> transform instructions
- transforms produce conditioning masks/overlays for backend

Data model example:

- character rig profile defines anchor coordinates per pose family
- equipment profile defines preferred anchor + offset + scale range + occlusion hint

Then evolve to:
- depth-aware occlusion ordering
- multi-layer compositing pass
- eventually 3D-aware rig inputs if needed

## 10) Migration strategy away from ComfyUI

Design migration around IR stability:

1. Freeze `RenderPlan` schema as contract.
2. Keep ComfyUI as one adapter implementation.
3. Build Diffusers adapter that consumes the same `RenderPlan`.
4. Reuse conditioning and asset layers unchanged.
5. Run cross-backend contract tests for same fixture scenes.

If a backend-specific feature is needed, gate it in `capabilities()` and keep fallback behavior explicit.

## Recommended MVP defaults (single developer, 16GB VRAM)

- Resolution default: 768x1024 portrait / 1024x768 landscape
- Single character first; multi-character behind feature flag
- One ControlNet (pose) + one identity path (IP-Adapter)
- Keep optional passes disabled unless requested
- FastAPI + Uvicorn + Pydantic only (minimal API stack)
- PyTorch + Diffusers as optional dependency group for future adapter

## Minimal API sketch

- `POST /v1/render`
  - accepts scene JSON + render options
  - returns job ID + manifest hash
- `GET /v1/render/{job_id}`
  - status + artifacts + manifest
- `POST /v1/validate-scene`
  - schema + semantic validation only

This keeps API stable for future editor/frontend integration.
