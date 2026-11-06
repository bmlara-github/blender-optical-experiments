Use $setup-to-blender to create an experimental reconstruction of the optical setup referenced by https://doi.org/10.1103/6ftp-svh8.

Read examples/paper-setup/README.md and layout.json. This is a later visualization; the paper did not use these Blender models.

Use Laser -> P (circular pupil) -> L1P -> L2P -> reflective SLM -> L2 -> SF (transmit +1 order) -> L1 -> CCD. Show rejected 0 and -1 orders stopping at SF. Preserve the supplied labels and document the known L1/L2 disagreement with manuscript prose. Do not add a polarizer or beam splitter.

Use only this repository's library collections. Treat the supplied layout as authored assumptions, not measured distances; focal lengths are unknown. Keep generic hardware at unit metric scale and show only the tabletop. Use continuous red beams and dimmer same-hue rejected orders. Do not add arrows or cable-like connectors.

Include both bundled images listed in layout.json: slm_hologram.png beside the SLM and ccd_intensity.png beside the CCD. Use separate framed panels, preserve image aspect ratios, keep optics and beams visible, and add no connector lines. Pack textures in the saved Blender scene and check both panels in perspective and plan renders. These are supplied reference images, not Blender-generated experimental data. Read reference-images/README.md for provenance. If I supply a sketch, inspect it; otherwise record that the full original drawing was not visually checked. Do not silently omit missing images.

Save under a new Figures/YYYY-MM-DD-FIgNN/ using my local date. Deliver an editable Blender file, reproducible build_source.py and setup.json, perspective/plan PNGs, paired lettered/unlettered SVGs at 86 mm, and notes separating facts, assumptions and checks. Render at 2000 x 1600 and 40 Cycles samples. Preserve the libraries and any existing figures.

Use the supplied generic builder for this default example. Place both flat image panels at the front table edge, with matching height and Y position: SLM beside SLM, CCD beside CCD.
