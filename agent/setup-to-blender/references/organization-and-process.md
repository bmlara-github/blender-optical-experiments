# Experimental agent folder, data and process contract

Use `library/camera-presets/experimental-table-front-left.json` and the saved `examples/paper-setup/source.blend`. This is the front-left table view with the laptop outside the left edge. Preserve camera position, rotation, orthographic scale, shifts, resolution, laptop position and screen assignments. Do not run camera optimization, coarse/refined sampling or automatic reframing. A requested camera change requires a new explicit decision.

## Reproduce and illuminate

Run from the repository root, substituting the user's local date and next unused figure number:

```sh
blender --background --python scripts/build_generic_example.py -- --output Figures/YYYY-MM-DD-FigXX --version 1
blender --background --python scripts/build_generic_example.py -- --output Figures/YYYY-MM-DD-FigXX --source-version 1 --version 2 --light-factor 1.0 --samples 128
python3 scripts/export_example.py Figures/YYYY-MM-DD-FigXX --version 2
```

The first command replays the saved scene. The second creates an illumination revision using the existing studio rig, preserving the locked camera, geometry, laptop and beam materials. `--light-factor` multiplies current light powers; 1.0 preserves the existing illuminated appearance. Inspect the render on white. For individual light tuning, change only lights in a new version and record the settings. Avoid flattening metallic housing depth or washing out lens apertures. Do not silently alter the view to improve illumination.

The exporter requires Pillow and produces matching raster-backed SVGs with editable lettering, 86 mm width and a 0.5 mm border. Use `--width-mm 129` or `172` when requested. Its stored bounds and anchors are calibrated to this exact saved scene and resolution. If optical geometry changes, recompute bounds and projected label anchors while retaining the locked camera. A new scene must fit this view; report clipping rather than adjusting the camera automatically.

After visual inspection and explicit owner approval:

```sh
python3 scripts/finalize_figure.py Figures/YYYY-MM-DD-FigXX --stage experimental --version 2 --approved
```

This copies the selected scene and SVG pair to `FinalFigure/`, checks dimensions and hashes, and records approval. A saved POV or successful export is not final visual approval.

## Folders and records

Keep one date-FigXX folder per figure. Use `_vXX` suffixes for revisions. Place builders in `python/`, scenes in `blender/`, setup/camera/lighting/validation/export/approval JSON in `json/`, notes in `md/`, logs in `txt/`, supplied images in `source/`, PNGs in `renders/`, and SVGs in `svg/`. `FinalFigure/` stays empty until approval. Stable input image names and README indexes may be unversioned. Reusable assets stay in `library/`, helpers in `scripts/`.

Record source facts separately from assumed distances and apertures. The example uses illustrative 70/140/70 mm relay spans, metric assets, and reference images on the laptop. It does not simulate diffraction or certify mechanical fits. Both screen images retain their existing rights.

## Distribution

Distribute libraries, agents, one locked example and its reference outputs, with supporting code, documentation, licenses and citations. Do not distribute camera-search samples, user Figures/, working revisions, migration reports or manufacturer CAD. Local Figures/ are ignored by Git. Preserve local work outside the package. Close only task-opened windows after saving.

## Data contract

Write json/setup_vXX.json with source facts/provenance, assumptions, units, component-to-library mappings, transforms, routes and known folded focal spans. Write versioned camera records with transform, projection, scale, shifts and resolution; lighting records with source/output versions and light settings; validation records with outcomes and limitations; export records with dimensions/borders and raster disclosure. Approval records include explicit owner approval and final-file hashes. Use relative paths. Never mark historical validation as a fresh optical check.
