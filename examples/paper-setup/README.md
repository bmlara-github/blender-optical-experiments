# Paper setup reconstruction (experimental)

Scientific reference: https://doi.org/10.1103/6ftp-svh8 (provided by the author). This is a **later 3D reconstruction**. The paper did not use these Blender models. The article DOI is not the DOI of this library.

## Run through the agent

Open this repository with an agent that can read local files and run Blender. Paste [prompt.md](prompt.md), or ask it to read that file and execute the request. Use `$setup-to-blender`; if discovery is unavailable, ask it to read `agent/setup-to-blender/SKILL.md` explicitly. The skill is an instruction package, not an autonomous executable or image-recognition program.

The agent runs the supplied generic example builder, exports the figures, and checks the result. For custom setups it adapts a copy of the builder. No files from the full private working copy are required. Blender and a Python interpreter are required; Pillow is required for the supplied exporter. The library files were prepared in Blender 5.2.3 LTS.

## Inputs

[layout.json](layout.json) supplies the bundled generic example builder with its authored layout. It provides the component list, collection IDs, library files, assumed coordinates and beam routes. The agent verifies collection axes and aperture alignment. The order is Laser, P, L1P, L2P, SLM, L2, SF, L1, CCD. P is a circular pupil. SF selects +1; other orders terminate at its mask.

The source figure was identified locally as manuscript Figure 6. The drawn labels put L2 nearest SLM and L1 nearest CCD; previous source notes report conflicting prose. Preserve the figure labels unless the user resolves the discrepancy. Focal lengths and physical separations were not supplied. The experimental 4 mm pupil, 1 mm filter and 120 mm optical height are authored assumptions. Schematic scale/spacing is illustrative.

The two images in [reference-images/](reference-images/) are included for the default example: the hologram goes beside SLM and the recorded intensity beside CCD. Their existing rights are documented separately; they are not Blender simulation outputs. The full paper PDF is not included. Supply a lawful sketch for an actual comparison with the complete original drawing. Without it, report that no full-sketch visual check was performed. Both panels must remain visible in both camera views, with no cable-like connectors.

## Outputs

A new dated figure folder containing build_source.py, setup.json, the Blender scene, two clean renders, paired SVGs with and without editable lettering, and a README/report. SVG optics remain raster, with vector lettering in a separate layer. Gaussian envelopes are display geometry, not simulated diffraction. Mechanical fits are not certified.
