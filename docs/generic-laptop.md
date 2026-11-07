# Generic laptop

GE_Laptop in Generic_Experimental_Laptop.blend. Original generic geometry with aluminium chassis, keyboard, trackpad, and a screen tilted 12 degrees back. Native meters; 285 mm wide. Front is local -Y, up is Z. Two square UV-mapped display planes accept CCD and SLM textures in a scene. No manufacturer CAD or branding. The library file has neutral screen materials; figure-specific images are packed in the scene.

## Rebuild and use

Run `blender --background --python scripts/build_generic_laptop.py` from the project root. Append or instance the `GE_Laptop` collection at unit scale. The reusable library contains no experimental images. Assign an image-texture emission material to `Laptop CCD display` and `Laptop SLM display` in your scene; their UV coordinates cover the full square image. For images of another aspect ratio, fit them to a square canvas without stretching. Make a local copy of the collection before customizing screens independently for multiple laptops.
