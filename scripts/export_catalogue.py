"""python scripts/export_catalogue.py <catalogue output folder>"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys,json,base64,html
out=Path(sys.argv[1]);png=out/'catalogue-clean.png';im=Image.open(png).convert('RGB');w,h=im.size;draw=ImageDraw.Draw(im)
font=None
for name in ['Arial.ttf','DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf']:
 try:font=ImageFont.truetype(name,29);break
 except OSError:pass
if font is None:font=ImageFont.load_default(size=29)
texts=[]
for l in json.loads((out/'labels.json').read_text()):
 x,y=l['x'],l['y'];t=l['text'];draw.text((x,y),t,font=font,anchor='ms',fill='#142b38',stroke_width=1,stroke_fill='white')
 texts.append(f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="middle" font-family="Arial,sans-serif" font-size="29" fill="#142b38">{html.escape(t)}</text>')
im.save(out/'catalogue-cover.png');data=base64.b64encode(png.read_bytes()).decode()
for mode in ['lettered','unlettered']:
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="86mm" height="{86*h/w:g}mm" viewBox="0 0 {w} {h}"><title>Generic experimental optical library</title><desc>Original generic geometry. Raster optical render with editable vector lettering. Display sizes normalized, not a common physical scale.</desc><g id="raster"><image width="{w}" height="{h}" href="data:image/png;base64,{data}"/></g>'
 if mode=='lettered':svg+='<g id="lettering">'+''.join(texts)+'</g>'
 (out/f'catalogue-{mode}.svg').write_text(svg+'</svg>')
