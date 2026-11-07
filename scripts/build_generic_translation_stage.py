import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
c=bpy.data.collections.new('GE_Linear_Translation_Stage');bpy.context.scene.collection.children.link(c)
def mat(name,col,metal):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*col,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.28;return m
black=mat('Translation stage black',(.035,.045,.055),.7);silver=mat('Translation stage steel',(.5,.55,.6),1)
control=bpy.data.objects.new('Travel control • travel_mm',None);c.objects.link(control);control['travel_mm']=0.;control.id_properties_ui('travel_mm').update(min=-20,max=60,description='Camera displacement from image plane; positive moves away from the lenses')
d=control.driver_add('location',0).driver;d.expression='-travel/1000';v=d.variables.new();v.name='travel';v.type='SINGLE_PROP';v.targets[0].id=control;v.targets[0].data_path='["travel_mm"]'
def box(name,loc,size,m,moving=False):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 for col in list(o.users_collection):col.objects.unlink(o)
 c.objects.link(o);o.data.materials.append(m);b=o.modifiers.new('Edge bevel','BEVEL');b.width=.0008;b.segments=3
 if moving:o.parent=control
box('Fixed rail base',(-.02,0,.004),(.15,.05,.008),black)
for y in [-.016,.016]:box('Guide rail',(-.02,y,.010),(.145,.006,.007),silver)
box('Moving carriage',(0,0,.016),(.045,.048,.010),black,True)
box('Travel indicator',(0,-.027,.016),(.009,.006,.004),silver,True)
for x in [-.08,-.06,-.04,-.02,0,.02,.04]:box('Travel scale tick',(x,.022,.0085),(.0006,.004,.0005),silver)
c.asset_mark();c.asset_data.catalog_id='e95172ba-ec95-4bd4-a543-01399c327402';c.asset_data.description='Generic linear translation stage, X travel -20 to +60 mm from nominal; independently authored illustrative mechanism.';c.asset_data.author='B. M. Rodriguez-Lara; J. Escamilla Angeles';c['units']='meters';c['axis']='Travel along -X; Z up';c['origin']='Nominal carriage center at board surface';c['travel_mm']=[-20,60]
bpy.data.libraries.write(str(ROOT/'library/Generic_Experimental_Translation.blend'),{c},fake_user=True)
p=ROOT/'docs/generic-assets.json'
if not p.exists():p=ROOT/'docs/assets.json'
data=json.loads(p.read_text());data['assets']=[a for a in data['assets'] if a['collection']!='GE_Linear_Translation_Stage'];data['assets'].append({'index':len(data['assets'])+1,'collection':'GE_Linear_Translation_Stage','library':'Generic_Experimental_Translation.blend','description':c.asset_data.description,'axis':'Travel -X; Z up','parameters_mm':{'length':150,'width':50,'travel':[-20,60]},'provenance':'Original procedural geometry; no manufacturer CAD','license':'CC-BY-4.0'});data['asset_count']=len(data['assets']);
for i,asset in enumerate(data['assets'],1):asset['index']=i
p.write_text(json.dumps(data,indent=2))
print('TRANSLATION_ASSET_SAVED')
