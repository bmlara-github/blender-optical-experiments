Read agent/setup-to-blender/SKILL.md and generate this figure.

Create a realistic-looking optical experiment on a generic
750 x 750 mm perforated breadboard, without table legs.
Use this project's generic library and collection instances
at unit scale (1 Blender unit = 1 meter). Set the optical
axis 120 mm above the tabletop. Use posts, holders and lens
mounts to support the components.

The beam follows this sequence:
Laser -> P -> L1P -> L2P -> SLM -> L2 -> SF -> L1 -> CCD.

P is a circular pupil, not a polarizer. L1P and L2P are the
two lenses before the reflective spatial light modulator
(SLM). At the SLM, fold the path toward L2, SF, L1 and CCD.
L2 is the lens nearest the SLM; L1 is nearest the CCD.
SF is a spatial filter: transmit the +1 diffraction order
toward L1 and CCD; stop the 0 and -1 orders at SF.
Do not add a beam splitter or a polarizer.

Use generic biconvex lenses. Focal lengths are unspecified;
do not invent them. For this illustration use a 4 mm pupil
and a 1 mm filter opening. Use examples/paper-setup/layout.json
for coordinates and orientations, not as measured data.
Draw continuous red beams. Make rejected orders dimmer in
the same red hue. Do not add direction arrows.

Include the two images in
examples/paper-setup/reference-images/:
- slm_hologram.png: a flat framed panel beside the SLM.
- ccd_intensity.png: a flat framed panel beside the CCD.
Put both panels along the front table edge, at the same
height and with their centers at Y = -0.25 m. Preserve
aspect ratios and pack the images in the Blender file.
Do not draw connector lines or invent replacement images.

Use scripts/build_generic_example.py for this example and
scripts/export_example.py for the SVGs. Locate Blender and
check the exporter's Pillow dependency before running.
Save in a new Figures/YYYY-MM-DD-FIgNN/ folder using my
local date and the next unused number. Preserve prior files.

Render perspective and overhead views at 2000 x 1600 pixels,
40 Cycles samples, with denoising. Deliver the editable
Blender scene, repeatable source, clean and lettered PNGs,
and paired SVGs with/without editable text at 86 mm width.
Keep the optical render raster and the SVG text editable.
Inspect both views. Report missing files or failures, and
record assumptions and checks in the figure README.
Generate the files now and give me links to the outputs.
