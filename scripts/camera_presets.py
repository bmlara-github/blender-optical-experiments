"""Apply named camera presets; Blender only. Exact replay or scaled framing."""
import json
from pathlib import Path
import bpy
from mathutils import Vector

def apply_camera_preset(scene,preset_path=None,*,target=None,unit_scale=None,ortho_scale=None,resolution=None):
    path=Path(preset_path) if preset_path else Path(__file__).resolve().parents[1]/'library/camera-presets/folded-relay-front-left.json'
    data=json.loads(path.read_text())
    if data['schema_version']!=1:raise ValueError('Unsupported camera preset schema')
    factor=data['reference_meters_per_blender_unit']/scene.unit_settings.scale_length if unit_scale is None else unit_scale
    if factor<=0:raise ValueError('unit_scale must be positive')
    camera=scene.camera
    if camera is None:
        camera=bpy.data.objects.new(data['name'],bpy.data.cameras.new(data['name']));scene.collection.objects.link(camera);scene.camera=camera
    camera.rotation_mode='XYZ';camera.rotation_euler=data['rotation_euler_xyz_radians']
    anchor=Vector(data['target'])*factor if target is None else Vector(target)
    camera.location=anchor+Vector(data['offset_from_target'])*factor
    camera.data.type=data['projection'];camera.data.ortho_scale=ortho_scale if ortho_scale is not None else data['orthographic_scale']*factor
    camera.data.lens=data['lens_mm'];camera.data.clip_start=max(1e-5,data['clip_start']*factor);camera.data.clip_end=data['clip_end']*factor
    scene.render.resolution_x,scene.render.resolution_y=resolution or data['resolution'];scene.render.resolution_percentage=100
    scene.render.pixel_aspect_x,scene.render.pixel_aspect_y=data['pixel_aspect']
    camera['preset_id']=data['id'];bpy.context.view_layer.update();return camera
