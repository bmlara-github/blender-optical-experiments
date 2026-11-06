"""Build the generic experimental example using only the original GE_ library.
Blender --background --python scripts/build_generic_example.py -- --output Figures/YYYY-MM-DD-FIgNN
"""
import bpy,sys,json,math,shutil
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'library/Generic_Experimental_Optics.blend').exists())
sys.path.insert(0,str(ROOT/'scripts'))
from gaussian_beam import create_gaussian_segment
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if '--output' not in args:raise RuntimeError('Pass --output with a new figure directory')
OUT=Path(args[args.index('--output')+1]).resolve();OUT.mkdir(parents=True,exist_ok=True)
if (OUT/'example.blend').exists() and '--overwrite' not in args:raise RuntimeError('Output already exists; choose another directory')
for d in ['renders','svg','source']:(OUT/d).mkdir(exist_ok=True)
layout=json.loads((ROOT/'examples/paper-setup/layout.json').read_text())
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
with bpy.data.libraries.load(str(ROOT/'library/Generic_Experimental_Optics.blend'),link=False) as (a,b):b.collections=[n for n in a.collections if n.startswith('GE_')]
cols={}
for name in ['Hardware','Optical components','Beams','Reference images','Studio']:
 c=bpy.data.collections.new(name);s.collection.children.link(c);cols[name]=c
labels=[];instances=[]
def inst(name,key,loc,normal=None,group='Hardware'):
 o=bpy.data.objects.new(name,None);cols[group].objects.link(o);o.instance_type='COLLECTION';o.instance_collection=bpy.data.collections[key];o.location=loc
 if normal:o.rotation_euler.z=math.atan2(-normal[0],normal[1])
 instances.append({'name':name,'asset':key,'location_m':list(loc),'scale':[1,1,1]});return o

def support(name,x,y,seat):
 inst(name+' holder','GE_Post_Holder_50',(x,y,0));inst(name+' post','GE_Post_80',(x,y,seat-.080))
Z=.12
inst('Perforated aluminum tabletop','GE_Breadboard_750',(-.04,.07,0))
for item in layout['components']:
 label=item['label'];x,y=item['position_xy'];n=item['experimental_normal_xy_reference'];key=item['collection'];inst(label,key,(x,y,Z),n,'Optical components')
 if label in ['P','L1P','L2P','L2','L1','SF']:
  inst(label+' mount','GE_Lens_Mount_50',(x,y,Z),n);support(label,x,y,Z-.031)
 elif label=='Laser':
  for t in [.04,.10]:support(label+str(t),x-n[0]*t,y-n[1]*t,Z-.021)
 else:support(label,x,y,Z-(.0225 if label=='SLM' else .020))
 labels.append({'text':label,'world':[x,y,Z+.045]})
for beam in layout['beams']:
 for i,(a,b) in enumerate(zip(beam['points_xy'],beam['points_xy'][1:])):
  c=bpy.data.collections.new(beam['name']+str(i));length=math.dist(a,b)
  create_gaussian_segment(beam['name'],(0,0),(0,length),beam['visualization_radii'][i],beam['visualization_radii'][i+1],c,0,beam['rejected'])
  o=bpy.data.objects.new('Beam segment',None);cols['Beams'].objects.link(o);o.instance_type='COLLECTION';o.instance_collection=c;o.location=(*a,Z);o.rotation_euler.z=math.atan2(-(b[0]-a[0]),b[1]-a[1])
# Source images remain supplied references, not simulated data.
for item in layout['reference_images']:
 src=ROOT/item['file'];shutil.copy2(src,OUT/'source'/src.name);img=bpy.data.images.load(str(OUT/'source'/src.name));img.pack()
 x,y=item['panel_center_xy'];w=.09;h=w*img.size[1]/img.size[0]
 bpy.ops.mesh.primitive_cube_add(size=1,location=(x,y,.004));o=bpy.context.object;o.name=item['title']+' frame';o.dimensions=(w+.006,h+.006,.008);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(bpy.data.materials['Generic satin black'])
 bpy.ops.mesh.primitive_plane_add(size=1,location=(x,y,.0081));o=bpy.context.object;o.name=item['title'];o.scale=(w,h,1)
 m=bpy.data.materials.new(item['title']);m.use_nodes=True;ns=m.node_tree.nodes;ns.clear();tx=ns.new('ShaderNodeTexImage');tx.image=img;e=ns.new('ShaderNodeEmission');e.inputs[1].default_value=.85;end=ns.new('ShaderNodeOutputMaterial');m.node_tree.links.new(tx.outputs['Color'],e.inputs[0]);m.node_tree.links.new(e.outputs[0],end.inputs['Surface']);o.data.materials.append(m)
 labels.append({'text':item['title'],'world':[x,y-h/2-.018,.009],'kind':'reference'})
# Studio floor, without any manufacturer imagery or geometry.
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.013));floor=bpy.context.object;floor.name='Studio floor'
m=bpy.data.materials.new('Pale background');m.diffuse_color=(.68,.72,.76,1);floor.data.materials.append(m)
world=bpy.data.worlds.new('Neutral studio');s.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.74,.80,.9,1);world.node_tree.nodes['Background'].inputs[1].default_value=.45
center=Vector((-.04,.07,0))
for name,loc,power,size in [('Key',(-1.3,-1,2.5),75,2),('Fill',(1.5,-1,1.3),45,1.2),('Rim',(.8,1.2,2),110,1.5)]:
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(center-o.location).to_track_quat('-Z','Y').to_euler()
cams={}
for view,loc,scale in [('perspective',(-.535,-.997,1.448),1.22),('plan',(-.04,.07,3),1.1)]:
 d=bpy.data.cameras.new(view);d.type='ORTHO';d.ortho_scale=scale;d.clip_start=.001;d.clip_end=300;o=bpy.data.objects.new(view,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(center-o.location).to_track_quat('-Z','Y').to_euler();cams[view]=o
s.render.engine='CYCLES';s.cycles.samples=40;s.cycles.use_denoising=True;s.render.resolution_x=2000;s.render.resolution_y=1600;s.render.resolution_percentage=100;s.view_settings.view_transform='AgX';s.render.image_settings.file_format='PNG'
anchors={}
for view,cam in cams.items():
 s.camera=cam;bpy.context.view_layer.update();anchors[view]=[]
 for l in labels:
  v=world_to_camera_view(s,cam,Vector(l['world']));anchors[view].append({**l,'x':v.x*2000,'y':(1-v.y)*1600})
 s.render.filepath=str(OUT/'renders'/('example-'+view+'-clean.png'));bpy.ops.render.render(write_still=True)
s.camera=cams['perspective'];s.render.filepath='//renders/example-perspective-clean.png'
for image in bpy.data.images:
 if image.source=='FILE':image.filepath='//source/'+Path(image.filepath).name
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'example.blend'))
(OUT/'label_anchors.json').write_text(json.dumps(anchors,indent=2));(OUT/'setup.json').write_text(json.dumps(layout,indent=2));(OUT/'instances.json').write_text(json.dumps(instances,indent=2))
if Path(__file__).resolve() != (OUT/'build_source.py').resolve():shutil.copy2(__file__,OUT/'build_source.py')
assert all(i['asset'].startswith('GE_') for i in instances)
(OUT/'validation.json').write_text(json.dumps({'library':'Generic_Experimental_Optics.blend','hardware_instances':len(instances),'all_generic':True,'unit_scales':True,'packed_reference_images':sum(bool(i.packed_file) for i in bpy.data.images),'optical_height_m':Z,'note':'Authored layout, not optical propagation or mechanical certification.'},indent=2))
(OUT/'README.md').write_text('''# Generic optical setup

Generated solely from the original GE_ library. The paper supplied the optical topology, not these Blender models. Positions, 120 mm optical height and mounting fits are illustrative; focal lengths are unknown. Beams are visualization envelopes, not propagation simulations. The two supplied image panels are packed in the scene and placed at the same front table edge. No full-paper visual comparison was performed by this builder.

Run the saved build_source.py with Blender and --output pointing to a new figure folder beneath this project. Use scripts/export_example.py afterward to export paired 86 mm SVGs with embedded raster and editable lettering. See validation.json and instances.json for recorded scene checks.
''')
print('GENERIC_EXAMPLE_COMPLETE',OUT,flush=True)
