"""Original parametric visualization geometry. No CAD imports or manufacturer tracing.
Run with Blender --background --python scripts/build_generic_library.py.
Units are meters. Geometry describes illustrations, not fabrication specifications.
"""
import bpy, math, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from gaussian_beam import create_gaussian_segment
LIB='Generic_Experimental_Optics.blend'
CAT='e95172ba-ec95-4bd4-a543-01399c327402'
bpy.ops.wm.read_factory_settings(use_empty=True)
S=bpy.context.scene;S.unit_settings.system='METRIC';S.unit_settings.scale_length=1
assets=[];meta=[];C=None

def mat(name,color,metal=0,rough=.3,trans=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;p.inputs['Transmission Weight'].default_value=trans;p.inputs['IOR'].default_value=1.46
 return m
black=mat('Generic satin black',(.018,.024,.033),.55,.3)
silver=mat('Generic brushed aluminum',(.48,.55,.61),.85,.28)
glass=mat('Generic optical glass',(.84,.95,1),0,.08,.95)
reflect=mat('Generic reflective coating',(.78,.85,.9),1,.075)
active=mat('Generic SLM active surface',(.13,.09,.19),.7,.19)
sensor=mat('Generic detector surface',(.035,.20,.24),.5,.18)

def asset(name,desc,axis='Z up; bottom at Z=0',**params):
 global C
 C=bpy.data.collections.new('GE_'+name);C.asset_mark();C.asset_data.author='B. M. Rodriguez-Lara; J. Escamilla Angeles';C.asset_data.description=desc;C.asset_data.catalog_id=CAT
 C['provenance']='Original procedural geometry; no imported manufacturer CAD';C['license']='CC-BY-4.0';C['meters_per_blender_unit']=1;C['axis']=axis
 assets.append(C);meta.append({'index':len(assets),'collection':C.name,'library':LIB,'description':desc,'axis':axis,'parameters_mm':params,'provenance':C['provenance'],'license':'CC-BY-4.0'})
 return C

def link(o,name,m):
 o.name=name
 for c in list(o.users_collection):c.objects.unlink(o)
 C.objects.link(o)
 if m:o.data.materials.append(m)
 return o

def box(name,loc,size,m=black,bevel=.001):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=link(bpy.context.object,name,m);o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  mod=o.modifiers.new('Soft edges','BEVEL');mod.width=bevel;mod.segments=2;o.modifiers.new('Normals','WEIGHTED_NORMAL')
 return o

def cyl(name,loc,r,h,m=silver,axis='Z'):
 rot={'Z':(0,0,0),'Y':(math.pi/2,0,0),'X':(0,math.pi/2,0)}[axis]
 bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=r,depth=h,location=loc,rotation=rot);o=link(bpy.context.object,name,m)
 for f in o.data.polygons:f.use_smooth=len(f.vertices)==4
 return o

def ring(name,outer,inner,depth,m=black,center=(0,0,0),axis='Y'):
 n=64;verts=[];faces=[]
 for y,r in [(-depth/2,outer),(depth/2,outer),(-depth/2,inner),(depth/2,inner)]:
  for i in range(n):
   x,z=r*math.cos(i*math.tau/n),r*math.sin(i*math.tau/n);v=(x,y,z) if axis=='Y' else (x,z,y);verts.append(tuple(v[k]+center[k] for k in range(3)))
 for i in range(n):
  j=(i+1)%n;faces.extend([(i,j,n+j,n+i),(2*n+j,2*n+i,3*n+i,3*n+j),(j,i,2*n+i,2*n+j),(n+i,n+j,3*n+j,3*n+i)])
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);C.objects.link(o);me.materials.append(m)
 for f in me.polygons:f.use_smooth=f.index%4<2
 return o

def knob(loc,axis='X',r=.006):cyl('Generic locking knob',loc,r,.009,black,axis)

# A true perforated thin plate: tessellated square annuli, no boolean copies of CAD.
def board(width,pitch=.025,thickness=.010):
 n=round(width/pitch);verts=[];faces=[];seg=16;r=.003
 for ix in range(n):
  for iy in range(n):
   cx=(ix+.5)*pitch-width/2;cy=(iy+.5)*pitch-width/2;base=len(verts)
   for z,inner in [(0,False),(-thickness,False),(0,True),(-thickness,True)]:
    for k in range(seg):
     a=k*math.tau/seg;rr=r if inner else pitch/2/max(abs(math.cos(a)),abs(math.sin(a)))
     verts.append((cx+rr*math.cos(a),cy+rr*math.sin(a),z))
   for k in range(seg):
    j=(k+1)%seg;faces.extend([(base+k,base+j,base+2*seg+j,base+2*seg+k),(base+seg+j,base+seg+k,base+3*seg+k,base+3*seg+j),(base+2*seg+k,base+2*seg+j,base+3*seg+j,base+3*seg+k)])
 # outer boundary skin
 for a,b in [((-width/2,-width/2),(width/2,-width/2)),((width/2,-width/2),(width/2,width/2)),((width/2,width/2),(-width/2,width/2)),((-width/2,width/2),(-width/2,-width/2))]:
  q=len(verts);verts.extend([(a[0],a[1],0),(b[0],b[1],0),(b[0],b[1],-thickness),(a[0],a[1],-thickness)]);faces.append((q,q+1,q+2,q+3))
 me=bpy.data.meshes.new('Perforated plate mesh');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Perforated aluminum plate',me);C.objects.link(o);me.materials.append(silver)
 import bmesh
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=1e-7);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(me);bm.free()
for mm in [300,450,750]:
 asset('Breadboard_'+str(mm),f'Original {mm} mm square perforated plate, 10 mm thick; 25 mm pitch, 6 mm through-holes.','Z up; top surface Z=0',width=mm,thickness=10,hole_pitch=25,hole_diameter=6);board(mm/1000)
for mm in [50,100]:
 asset('Table_Support_'+str(mm),f'Generic short cylindrical support, {mm} mm tall.',height=mm,diameter=60);cyl('Support',(0,0,mm/2000),.03,mm/1000,black);cyl('Foot',(0,0,.004),.04,.008)
for mm in [25,40,60,80,100,150]:
 asset('Post_'+str(mm),f'Generic 12 mm post, {mm} mm long.',height=mm,diameter=12);cyl('Post',(0,0,mm/2000),.006,mm/1000);cyl('Unthreaded mounting stud',(0,0,mm/1000+.002),.0025,.004)
for mm in [30,50,70]:
 asset('Post_Holder_'+str(mm),f'Generic sleeve for 12 mm posts, {mm} mm overall height. Illustrative clearance.',height=mm,bore=12.4)
 box('Mounting base',(0,0,.004),(.05,.035,.008));ring('Sleeve',.012,.0062,mm/1000-.008,center=(0,0,(mm/1000+.008)/2),axis='Z');knob((.015,0,mm/1000-.012))
for deg in [0,45,90]:
 asset('Post_Clamp_'+str(deg),f'Generic post collar with {deg}-degree arm; no manufacturer interface claimed.',arm_angle=deg)
 ring('Post collar',.012,.0062,.016,center=(0,0,.008),axis='Z');o=box('Clamp arm',(.022,0,.008),(.026,.012,.016));o.rotation_euler.z=math.radians(deg);knob((0,-.015,.008),'Y')
asset('Base_Bracket','Generic right-angle support bracket.')
box('Base',(0,0,.004),(.05,.04,.008));box('Upright',(0,.016,.026),(.05,.008,.044))
for mm in [12,25,50]:
 asset('Lens_Mount_'+str(mm),f'Generic {mm} mm clear-bore lens ring; post seat below center.','Optical axis +Y; aperture at origin',clear_bore=mm,seat_offset=mm/2+6)
 ring('Lens retaining ring',mm/2000+.005,mm/2000,.008);box('Post seat',(0,0,-mm/2000-.003),(.014,.010,.006));knob((mm/2000+.007,0,0),r=.003)
for mm in [12,25,50]:
 asset('Mirror_Mount_'+str(mm),f'Generic two-plate adjustable mirror support for {mm} mm optics.','Face +Y; optical center at origin',optic_diameter=mm)
 size=mm/1000+.014
 box('Backplate',(0,-.014,0),(size,.005,size));ring('Front retaining ring',mm/2000+.004,mm/2000,.004,center=(0,-.002,0))
 for x,z in [(-size*.38,-size*.38),(size*.38,-size*.38),(-size*.38,size*.38)]:cyl('Adjustment screw',(x,-.010,z),.002,.020,axis='Y');knob((x,-.023,z),'Y',.004)
asset('XY_Stage','Generic stacked XY translation platform. Illustrative travel controls.',size=60)
box('Base',(0,0,.004),(.07,.07,.008));box('X slide',(0,0,.012),(.06,.055,.008),silver);box('Y slide',(0,0,.020),(.05,.05,.008));knob((.040,0,.012));knob((0,.037,.020),'Y')
asset('Rotation_Stage','Generic circular manual platform; no precision specification.',diameter=60)
cyl('Rotation base',(0,0,.005),.035,.010,black);cyl('Turntable',(0,0,.013),.030,.006);knob((.040,0,.008))
asset('Iris','Generic fixed-pose iris visualization, 8 mm opening; not a working mechanism.','Optical axis +Y; aperture at origin',opening=8)
ring('Iris housing',.023,.019,.008)
ring('Blade envelope',.019,.004,.001,silver)
for i in range(8):
 a=i*math.tau/8;o=box('Blade seam',(.011*math.cos(a),.0008,.011*math.sin(a)),(.016,.0003,.00025),black,0);o.rotation_euler.y=-a
cyl('Iris control lever',(.024,0,0),.002,.018,black,'X')
# Original generic optical surfaces: shape controls, never focal-length-specific assets.
for shape,signs in [('Biconvex',(1,1)),('Biconcave',(-1,-1)),('Plano_Convex',(0,1)),('Plano_Concave',(0,-1)),('Meniscus',(-1,1))]:
 asset(shape,'Generic '+shape.replace('_',' ').lower()+' lens, 50 mm diameter; focal length unspecified.','Optical axis +Y; center at origin',diameter=50)
 n=64;nr=16;vs=[];fs=[]
 for side,sgn in enumerate(signs):
  for j in range(nr+1):
   rr=.025*max(j/nr,.00001);sag=.0025*(1-(rr/.025)**2);y=(-1 if side==0 else 1)*(.004+sgn*sag)
   for i in range(n):vs.append((rr*math.cos(i*math.tau/n),y,rr*math.sin(i*math.tau/n)))
 for side in [0,1]:
  base=side*(nr+1)*n
  for j in range(nr):
   for i in range(n):a=base+j*n+i;b=base+j*n+(i+1)%n;fs.append((a,b,b+n,a+n))
 for i in range(n):a=nr*n+i;b=nr*n+(i+1)%n;fs.append((a,b,b+(nr+1)*n,a+(nr+1)*n))
 me=bpy.data.meshes.new(shape);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(shape,me);C.objects.link(o);me.materials.append(glass)
 import bmesh
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(me);bm.free()
 for f in me.polygons:f.use_smooth=True
asset('Plane_Mirror','Generic 25 mm plane mirror.','Reflective face +Y at origin',diameter=25);cyl('Mirror',(0,-.0015,0),.0125,.003,reflect,'Y')
asset('Laser_Head','Generic cylindrical laser housing, 140 mm long.','Output +Y at origin',length=140)
cyl('Laser body',(0,-.07,0),.018,.14,black,'Y');ring('Output bezel',.018,.003,.004,center=(0,-.002,0),m=silver)
for y in [-.04,-.10]:ring('Support collar',.021,.018,.012,center=(0,y,0))
asset('CCD_Camera','Generic detector housing with illustrative active area.','Receiving face +Y at origin')
box('Camera body',(0,-.025,0),(.045,.05,.040));ring('Camera bezel',.014,.010,.006,center=(0,-.003,0),m=silver);box('Sensor',(0,-.007,0),(.016,.001,.012),sensor,0)
asset('Reflective_SLM','Generic rectangular SLM housing with illustrative active area.','Reflective face +Y at origin')
box('SLM housing',(0,-.012,0),(.07,.024,.045));box('SLM bezel',(0,0,0),(.024,.001,.018),silver);box('Active area',(0,.0006,0),(.020,.0004,.014),active,0)
for name,diam in [('Aperture_Plate',4),('Spatial_Filter',1)]:
 asset(name,f'Generic 50 mm plate with {diam} mm circular opening.','Optical axis +Y; aperture at origin',outer_diameter=50,opening=diam);ring(name,.025,diam/2000,.0015)
asset('Gaussian_Beam','Reusable red Gaussian visualization envelope and continuous core; not propagation simulation.','Beam axis +Y; start at origin')
create_gaussian_segment('Generic beam',(0,0),(0,.1),.0012,.0012,C,0,False)
ROOT.joinpath('library').mkdir(exist_ok=True);ROOT.joinpath('docs').mkdir(exist_ok=True)
bpy.data.libraries.write(str(ROOT/'library'/LIB),set(assets),fake_user=True,compress=True)
(ROOT/'docs/assets.json').write_text(json.dumps({'asset_count':len(meta),'units':'meters','assets':meta},indent=2)+'\n')
(ROOT/'library/blender_assets.cats.txt').write_text('VERSION 1\n'+CAT+':Generic Experimental Optics:Generic Experimental Optics\n')
print('GENERIC_LIBRARY_COMPLETE',len(meta),flush=True)
