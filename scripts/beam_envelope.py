"""Reusable translucent geometric beam envelope, illustrative rather than simulated."""
import bpy, math
from mathutils import Vector

def create_envelope(name,a,b,wa,wb,collection,rejected=False):
 a,b=Vector(a),Vector(b);d=b-a; q=d.to_track_quat('Z','Y');verts=[];faces=[];n=48;steps=16
 for j in range(steps+1):
  t=j/steps;r=math.sqrt(min(wa,wb)**2+abs(wb*wb-wa*wa)*(t if wb>=wa else 1-t)**2)
  for k in range(n):
   v=a+d*t+q@Vector((r*math.cos(k*2*math.pi/n),r*math.sin(k*2*math.pi/n),0));verts.append(v)
 for j in range(steps):
  for k in range(n):faces.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);o=bpy.data.objects.new(name,me);collection.objects.link(o)
 m=bpy.data.materials.new(name+' material');m.use_nodes=True;ns=m.node_tree.nodes;ns.clear();tr=ns.new('ShaderNodeBsdfTransparent');em=ns.new('ShaderNodeEmission');em.inputs[0].default_value=(1,.008,.003,1);em.inputs[1].default_value=.336 if rejected else .7;mix=ns.new('ShaderNodeMixShader');mix.inputs[0].default_value=.14 if rejected else .21;out=ns.new('ShaderNodeOutputMaterial');ls=m.node_tree.links;ls.new(tr.outputs[0],mix.inputs[1]);ls.new(em.outputs[0],mix.inputs[2]);ls.new(mix.outputs[0],out.inputs['Surface']);me.materials.append(m);o.visible_shadow=False
 o['model']='Illustrative quadratic Gaussian-width envelope; not a diffraction calculation'
 return o
