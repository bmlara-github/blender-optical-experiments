# Agent setup

Keep this entire agent/ folder inside the downloaded project, beside library/ and examples/. It is not a Blender add-on. Do not put it in the Blender installation folder.

## Easiest use: no installation command

Open the project folder in Codex and paste:

> Read agent/setup-to-blender/SKILL.md and use those instructions to carry out examples/paper-setup/prompt.md. Generate the example and its deliverables, using only this project.

Codex reads the agent directly, so this works without automatic skill discovery.

## Optional named-skill installation

From this project root run `python3 agent/install.py` on macOS/Linux or `py agent/install.py` on Windows. You can ask Codex to run that command. It copies the complete skill to .agents/skills/setup-to-blender/ within this project only. It leaves existing differing content untouched. No global settings are changed. Then start a new chat in the same project and ask to use `$setup-to-blender`.

Manual equivalent: copy the complete setup-to-blender folder into the project's .agents/skills folder. The final path must be .agents/skills/setup-to-blender/SKILL.md, not a second nested setup-to-blender folder. The dot-prefixed .agents folder may be hidden in your file browser.

If the named call is not recognized, use the direct read-and-run prompt above. The visible agent/ folder remains the distributed source; rerun installation only when updating a local installed copy.
