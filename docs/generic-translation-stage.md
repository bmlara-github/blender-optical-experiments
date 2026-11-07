# Generic linear translation stage

Asset `GE_Linear_Translation_Stage` in `library/Generic_Experimental_Translation.blend`. Original generic geometry, not manufacturer CAD. Native units are meters. The control `Travel control • travel_mm` moves the carriage along local -X; positive displacement is away from the lenses in the compact CCD scene. Default 0 mm, supported posing range -20 to +60 mm. This is an illustrative translation mechanism, not a calibrated or certified travel specification. The 150 × 50 mm base is fixed, while the carriage is driven separately. Scene-mounted cameras and posts can share the same control.

## Rebuild and use

Run `blender --background --python scripts/build_generic_translation_stage.py` from the project root. Append or instance `GE_Linear_Translation_Stage` at unit scale. Change the `travel_mm` custom property on `Travel control • travel_mm`; positive travel moves the carriage in local -X. The carriage top is 21 mm above the mounting surface. Attach your instrument to the moving control or share its driver; adding the stage alone does not move unrelated camera objects or beam geometry. Multiple independently controlled stages require independent copies of the source collection.
