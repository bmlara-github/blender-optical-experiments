import bpy, sys, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from generic_laptop import build_laptop
bpy.ops.wm.read_factory_settings(use_empty=True)
c=build_laptop()
bpy.data.libraries.write(str(ROOT/'library/Generic_Experimental_Laptop.blend'),{c},fake_user=True)
p=ROOT/'docs/generic-assets.json'
if not p.exists():p=ROOT/'docs/assets.json'
d=json.loads(p.read_text());d['assets']=[a for a in d['assets'] if a['collection']!='GE_Laptop']
d['assets'].append({'index':len(d['assets'])+1,'collection':'GE_Laptop','library':'Generic_Experimental_Laptop.blend','description':c.asset_data.description,'axis':'Front -Y; Z up','parameters_mm':{'width':285,'base_depth':185},'provenance':'Original procedural geometry; no manufacturer CAD','license':'CC-BY-4.0'})
d['asset_count']=len(d['assets'])
for i,asset in enumerate(d['assets'],1):asset['index']=i
p.write_text(json.dumps(d,indent=2))
print('LAPTOP_ASSET_SAVED')
