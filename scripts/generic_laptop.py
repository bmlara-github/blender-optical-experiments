import bpy, math
from mathutils import Vector

def build_laptop():
 c=bpy.data.collections.new('GE_Laptop')
 def mat(name,col,metal=0):
  m=bpy.data.materials.new(name);m.diffuse_color=(*col,1);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*col,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.32;return m
 silver=mat('Laptop aluminium',(.32,.38,.44),.8);black=mat('Laptop dark keys',(.012,.018,.025));glass=mat('Laptop screen',(.009,.014,.022))
 def box(name,loc,size,m):
  bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  for col in list(o.users_collection):col.objects.unlink(o)
  c.objects.link(o);o.data.materials.append(m);be=o.modifiers.new('Soft edges','BEVEL');be.width=.001;be.segments=3;return o
 box('Laptop base',(0,0,.006),(.285,.185,.012),silver)
 for row in range(5):
  for col in range(13):box('Laptop key',(-.12+col*.019,.055-row*.015,.013),(.016,.011,.002),black)
 box('Laptop space bar',(0,-.021,.013),(.095,.011,.002),black)
 box('Laptop trackpad',(0,-.060,.0123),(.086,.042,.001),black)
 # Screen is tilted back 12 degrees from vertical, front faces local -Y.
 angle=math.radians(12)
 def pos(x,z,front=0):return (x,.081+math.sin(angle)*z-front,.014+math.cos(angle)*z)
 lid=box('Laptop screen housing',pos(0,.092),(.285,.008,.184),silver);lid.rotation_euler.x=-angle
 def plane(name,x0,x1,z0,z1,m):
  mesh=bpy.data.meshes.new(name);mesh.from_pydata([pos(x0,z0,.0046),pos(x1,z0,.0046),pos(x1,z1,.0046),pos(x0,z1,.0046)],[],[(0,1,2,3)]);mesh.update()
  uv=mesh.uv_layers.new()
  for loop,co in zip(uv.data,[(0,0),(1,0),(1,1),(0,1)]):loop.uv=co
  o=bpy.data.objects.new(name,mesh);c.objects.link(o);o.data.materials.append(m)
  if 'display' in name:o.location.y=-.0002
  return o
 plane('Laptop black bezel',-.135,.135,.009,.175,glass)
 # Square source images: matched square display areas, no aspect distortion.
 plane('Laptop CCD display',-.125,-.005,.032,.152,glass)
 plane('Laptop SLM display',.005,.125,.032,.152,glass)
 c.asset_mark();c.asset_data.catalog_id='e95172ba-ec95-4bd4-a543-01399c327402';c.asset_data.author='B. M. Rodriguez-Lara; J. Escamilla Angeles';c.asset_data.description='Generic laptop with two replaceable image display planes; meters; width 285 mm. Local front -Y, up Z.'
 return c
