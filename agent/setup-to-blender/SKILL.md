---
name: setup-to-blender
description: Create metric experimental optical figures using the generic library, locked laptop POV, versioned illumination and approved final exports.
---

# Experimental setup to Blender

Identify the active repository by library/, docs/assets.json and examples/paper-setup/. Read root AGENTS.md, docs/assets.json, docs/figure-workflow.md and [organization-and-process.md](references/organization-and-process.md). Do not infer the root from an installed agent location.

Interpret the supplied component sequence and source images; record facts, assumptions, missing dimensions, collection mappings and beam paths before building. Use only authored GE_ assets, native meter units and collection instances. Never import manufacturer CAD or treat indicative geometry as a certified mechanical fit. Generic lens shapes do not encode focal lengths. Rejected orders retain the source red hue at lower brightness.

For the bundled example, replay examples/paper-setup/source.blend using scripts/build_generic_example.py. Use the saved experimental-table-front-left camera exactly. Preserve the laptop transform and both screen images. Do not add floating panels, switch to a schematic camera, generate a plan view or run a camera search. For new geometry, recompute projected label anchors and content bounds without changing the locked camera; report clipping rather than silently reframing.

Save one dated figure folder with type folders and _vXX filenames. Create an illumination revision after replaying the locked POV. Keep optics, camera, laptop and beam materials unchanged while tuning lights. Use scripts/export_example.py for the unchanged example, inspect the render and SVG pair, then run scripts/finalize_figure.py only after explicit owner approval. Keep reference fixtures separate from newly approved results.

Verify asset identities, units, apertures, beam endpoints, laptop images, packed dependencies, SVG dimensions and editable lettering. Record only checks actually performed. If Blender cannot run, preserve the source and disclose that rendering is unverified. Close only task-opened windows. Run scripts/validate_structure.py before distribution; exclude local figures and revision history.
