"""Blender --background --python scripts/build_generic_catalogue.py -- --output <folder>"""
import bpy,json,sys,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1]
args=sys.argv[sys.argv.index('--')+1:];out=Path(args[args.index('--output')+1]).resolve();out.mkdir(parents=True,exist_ok=True)
if (out/'catalogue.blend').exists() and '--overwrite' not in args:raise RuntimeError('Choose a new output folder')
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene
manifest=json.loads((ROOT/'docs/assets.json').read_text())
with bpy.data.libraries.load(str(ROOT/'library/Generic_Experimental_Optics.blend')) as (a,b):b.collections=[n for n in a.collections if n.startswith('GE_')]
labels=[]
for i,a in enumerate(manifest['assets']):
 c=bpy.data.collections[a['collection']];o=bpy.data.objects.new(a['collection'],None);s.collection.objects.link(o);o.instance_type='COLLECTION';o.instance_collection=c
 # Tilt upright optics toward the catalogue camera; display instances only.
 o.rotation_euler=(math.radians(48),math.radians(-10),math.radians(-24));rot=o.rotation_euler.to_matrix()
 points=[rot@(ob.matrix_basis@v.co) for ob in c.all_objects if ob.type=='MESH' for v in ob.data.vertices]
 lo=Vector(tuple(min(p[j] for p in points) for j in range(3)));hi=Vector(tuple(max(p[j] for p in points) for j in range(3)))
 k=1.35/max(hi.x-lo.x,hi.y-lo.y);o.scale=(k,)*3
 x=(i%6)*2; y=-(i//6)*2.15;o.location=(x-(lo.x+hi.x)*k/2,y-(lo.y+hi.y)*k/2,-lo.z*k)
 labels.append({'text':a['collection'][3:].replace('_',' '),'world':[x,y-.92,0]})
bpy.ops.mesh.primitive_plane_add(size=200,location=(5,-6,-.04));floor=bpy.context.object
m=bpy.data.materials.new('Background');m.diffuse_color=(.86,.88,.9,1);floor.data.materials.append(m)
s.world=bpy.data.worlds.new('World');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.8,.85,.9,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.65
for loc,power,size in [((0,0,15),1800,12),((12,-10,12),1300,10)]:
 d=bpy.data.lights.new('Softbox','AREA');d.energy=power;d.size=size;o=bpy.data.objects.new('Softbox',d);s.collection.objects.link(o);o.location=loc
 dvec=Vector((5,-6,0))-o.location;o.rotation_euler=dvec.to_track_quat('-Z','Y').to_euler()
d=bpy.data.cameras.new('Catalogue');d.type='ORTHO';d.ortho_scale=15.8;o=bpy.data.objects.new('Catalogue',d);s.collection.objects.link(o);o.location=(5,-6.5,30);s.camera=o
s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=True;s.render.resolution_x=2400;s.render.resolution_y=3000;s.render.resolution_percentage=100;s.view_settings.view_transform='AgX'
bpy.context.view_layer.update()
for l in labels:
 v=world_to_camera_view(s,o,Vector(l['world']));l.update(x=v.x*2400,y=(1-v.y)*3000)
(out/'labels.json').write_text(json.dumps(labels,indent=2));s.render.filepath=str(out/'catalogue-clean.png');bpy.ops.render.render(write_still=True);bpy.ops.wm.save_as_mainfile(filepath=str(out/'catalogue.blend'))
print('CATALOGUE_COMPLETE',flush=True)
