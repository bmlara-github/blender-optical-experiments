# Reusable camera and propagation accessories

## Folded Relay — Front-Left

`library/camera-presets/folded-relay-front-left.json` records the accepted orthographic view, including position, Euler rotation, quaternion, target, clipping planes, scale, resolution and reference units.

The reference camera position is **(-34, -20, 40)**, the target is **(-3, -1, 1.6)**, the orthographic scale is **36**, and the reference scene uses **0.01 metres per Blender unit**. Euler XYZ angles in radians are approximately **(0.758108318, 0, -1.020943284)**. The exact serialized numbers are authoritative.

From Blender's Python console, with the project directory substituted below:

```python
import sys
sys.path.insert(0, '/path/to/project/scripts')
from camera_presets import apply_camera_preset
apply_camera_preset(bpy.context.scene)
```

The helper adjusts distances to the scene's unit scale. To reproduce the reference coordinates literally, use `unit_scale=1`. To preserve the viewing direction while framing a metre-based table:

```python
apply_camera_preset(bpy.context.scene,
    target=(-0.08, -0.02, 0.04),
    ortho_scale=0.90, resolution=(2400, 1900))
```

`target` and `ortho_scale` are in the destination scene's Blender units. `unit_scale` is an optional explicit multiplier for reference distances. Recreate camera-facing panels after changing the camera.

## Assets and assembly

- `GE_Translation_Rail` in `Generic_Experimental_Propagation.blend`. Fixed translation rail; use with independent carriage. Native metres per unit: 1; axis: -X travel; Z up.
- `GE_Translation_Carriage` in `Generic_Experimental_Propagation.blend`. Moving carriage; use the same translation transform for the detector and its support. Native metres per unit: 1; axis: -X travel; Z up.
- `GE_Quadratic_Beam_Envelope` in `Generic_Experimental_Propagation.blend`. Translucent quadratic-width beam visualization. Not a diffraction calculation. Native metres per unit: 1; axis: +Y.

Append the asset collection and place collection instances in the scene. Keep the generic lens shapes unchanged; focal lengths and aperture settings belong in the figure metadata. The experimental rail and carriage reuse the geometry from `GE_Linear_Translation_Stage`; the original complete stage remains available with its travel control.

The beam's local axis is +Y. Its radius changes quadratically in the axial coordinate, using the endpoint radii. For a custom span, import `create_envelope` from `scripts/beam_envelope.py` and pass 3D endpoints, endpoint radii and a collection. This is an illustrative envelope, not propagation simulation or measured diffraction. Rejected orders retain the source red hue with reduced emission and opacity.

For detector translation, move the carriage, detector and detector support together. A figure may constrain travel to start at its image plane. Do not infer mechanical compatibility from the generic illustration.

## Publication export

Export paired SVGs with and without editable lettering. Embed the clean raster optical rendering and place text in a separate vector layer. Use explicit millimetre dimensions, 86 mm width for one column, and 0.5 mm clear borders when requested. Preserve the render aspect ratio. The optics inside the SVG remain raster; the lettering remains editable.
