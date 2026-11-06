# Optical library and figure conventions

- Add newly designed optical components and reusable beam representations to `library/`, with asset metadata and documentation. Reuse them as instances in figures.
- Save each figure under `Figures/YYYY-MM-DD-FIgNN/` using the user's local date. Keep its Blender file, source, renders, SVGs and notes together.
- Produce matching SVGs with editable lettering and without lettering. For realistic Blender materials, embed the clean raster render in the SVG and keep all lettering in a separate editable vector layer; clearly disclose that the optical rendering is raster.
- Default to 86 mm width for a single column when no size is requested. Use the user's requested width when provided. A proportional column-and-a-half is 129 mm and double column is 172 mm; use publication-specific dimensions when supplied. Preserve the aspect ratio and set explicit millimeter dimensions on the SVG root.
- Place reference images near their associated optical component. Do not draw cable-like connecting lines unless the user explicitly asks for them.
- Document visual assumptions and distinguish Gaussian visualization envelopes from simulated diffraction or measured optical behavior.

- Rejected diffraction orders use the same red hue as the source beam, distinguished by lower brightness rather than a different color.

- Keep library lenses generic by shape: biconcave, biconvex, plano-convex, plano-concave and convex-concave (meniscus). Do not create separate library assets for focal lengths. Store focal-length information in scene descriptions and metadata, and use it to inform proportional focal spans in figure layouts; measure folded spans along the beam path. Scene-specific aperture dimensions likewise do not require new library entries.

- Do not add sparse direction arrows to beam paths by default. Use continuous beam geometry; add arrows only when explicitly requested or when a consistent, purposeful annotation scheme is agreed.
