"""Load standalone accessory libraries and check reusable controls and UVs."""
import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
for file,key in [('Generic_Experimental_Translation.blend','GE_Linear_Translation_Stage'),('Generic_Experimental_Laptop.blend','GE_Laptop')]:
 with bpy.data.libraries.load(str(ROOT/'library'/file),link=False) as (a,b):
  assert key in a.collections
  b.collections=[key]
 c=bpy.data.collections[key];assert c.asset_data and c.asset_data.catalog_id
 bpy.context.scene.collection.children.link(c)
c=bpy.data.collections['GE_Linear_Translation_Stage']
control=next(o for o in c.objects if o.name.startswith('Travel control'))
carriage=c.objects['Moving carriage'];nominal=carriage.location.x
for mm in [-20,0,60]:
 control['travel_mm']=float(mm);control.update_tag();bpy.context.view_layer.update()
 actual=carriage.evaluated_get(bpy.context.evaluated_depsgraph_get()).matrix_world.translation.x
 assert abs(actual-(nominal-mm/1000))<1e-6,(mm,actual)
control['travel_mm']=0.
c=bpy.data.collections['GE_Laptop']
for name in ['Laptop CCD display','Laptop SLM display']:
 o=c.objects[name];assert len(o.data.uv_layers)==1 and len(o.data.uv_layers[0].data)==4
 assert o.location.y<0 # in front of bezel, avoiding coplanar surfaces
assert not [i for i in bpy.data.images if i.source=='FILE']
meta=json.loads((ROOT/'docs/assets.json').read_text())
assert meta['asset_count']==len(meta['assets'])
assert len({x['collection'] for x in meta['assets']})==len(meta['assets'])
print('PASS: standalone assets, asset catalogues, slide travel, screen UVs, no external image dependencies, metadata')
