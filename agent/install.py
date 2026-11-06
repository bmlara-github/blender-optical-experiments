"""Install this package's agent for this project only. Standard-library Python."""
from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
src=root/'agent/setup-to-blender';dst=root/'.agents/skills/setup-to-blender'
if not (src/'SKILL.md').is_file(): raise SystemExit('Agent source is missing. Restore the complete project folder.')
if dst.exists():
    source={p.relative_to(src):p.read_bytes() for p in src.rglob('*') if p.is_file()}
    installed={p.relative_to(dst):p.read_bytes() for p in dst.rglob('*') if p.is_file()}
    if source==installed: print('Agent is already installed for this project.')
    else: raise SystemExit('A different agent is already installed here. Preserve it before replacing; no files changed.')
else:
    dst.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(src,dst)
    print('Agent installed in .agents/skills/setup-to-blender. Start a new project chat to discover it.')
