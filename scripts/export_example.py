from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json,base64,html
import sys
out=Path(sys.argv[1]).resolve()
(out/'svg').mkdir(exist_ok=True)
anchors=json.loads((out/'label_anchors.json').read_text())
experimental=True
allowed={'Laser','P','L1P','L2P','SLM','L2','SF','L1','CCD','SLM hologram','Recorded intensity'}
for view in ['perspective','plan']:
 png=out/'renders'/('example-'+view+'-clean.png'); im=Image.open(png).convert('RGB');w,h=im.size;draw=ImageDraw.Draw(im);texts=[]
 for lab in anchors[view]:
  text=lab['text']
  if text not in allowed:continue
  ref=text in ['SLM hologram','Recorded intensity'];size=(28 if ref else 37) if experimental else (30 if ref else 39)
  x,y=lab['x'],lab['y']
  if experimental:
   y+=55 if ref and view=='perspective' else -15
   if text=='Laser':x-=75;y-=45
  else:
   overrides={'perspective':{'Laser':(240,300),'Recorded intensity':(500,1015),'SLM hologram':(1950,635),'SLM':(2110,1080)},'plan':{'SLM':(2070,1290),'Recorded intensity':(447,900),'SLM hologram':(1946,815)}}
   x,y=overrides[view].get(text,(x,y))
  font=None
  for candidate in ['Arial.ttf','DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf']:
   try:font=ImageFont.truetype(candidate,size);break
   except OSError:pass
  if font is None:font=ImageFont.load_default(size=size)
  draw.text((x,y),text,font=font,fill='#172c3a',anchor='ms',stroke_width=2,stroke_fill='white')
  texts.append(f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="middle" font-family="Arial, sans-serif" font-size="{size}" fill="#172c3a" stroke="white" stroke-width="3" paint-order="stroke">{html.escape(text)}</text>')
 im.save(out/'renders'/('example-'+view+'-lettered.png'))
 data=base64.b64encode(png.read_bytes()).decode()
 for mode in ['lettered','unlettered']:
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="86mm" height="{86*h/w:g}mm" viewBox="0 0 {w} {h}">\n<title>Optical setup with supplied SLM and CCD reference images</title>\n<desc>Optics and reference panels are embedded raster imagery. Lettering is editable vector text. Panels are supplied images from manuscript Figure 6, DOI 10.1103/6ftp-svh8, not simulated results. Gaussian beams are visualization only.</desc>\n<g id="raster" inkscape:groupmode="layer" inkscape:label="Raster render and reference images"><image width="{w}" height="{h}" href="data:image/png;base64,{data}"/></g>\n'
  if mode=='lettered':svg+='<g id="lettering" inkscape:groupmode="layer" inkscape:label="Editable lettering">'+'\n'.join(texts)+'</g>\n'
  (out/'svg'/f'example-{view}-{mode}-86mm.svg').write_text(svg+'</svg>')
print('Exported paired 86 mm SVGs and lettered PNGs:',out)
