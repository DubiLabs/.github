"""Generate outlined SVG profile artwork. Requires PySide6 and Be Vietnam Pro TTFs."""
from pathlib import Path
import argparse,html,math
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase,QFont,QPainterPath,QImage,QPainter
from PySide6.QtSvg import QSvgRenderer
parser=argparse.ArgumentParser();parser.add_argument('--fonts',type=Path,required=True);args=parser.parse_args()
app=QApplication([])
root=Path(__file__).resolve().parents[1];out=root/'profile/assets';out.mkdir(parents=True,exist_ok=True)
for f in args.fonts.glob('BeVietnamPro-*.ttf'):QFontDatabase.addApplicationFont(str(f))
def txt(label,x,y,size,color,weight=500):
 f=QFont('Be Vietnam Pro');f.setPixelSize(size);f.setWeight(QFont.Weight(weight));p=QPainterPath();p.addText(x,y,f,label);d=[];i=0
 while i<p.elementCount():
  a=p.elementAt(i)
  if a.isMoveTo():d.append(f'M{a.x:.2f},{a.y:.2f}')
  elif a.isLineTo():d.append(f'L{a.x:.2f},{a.y:.2f}')
  elif a.isCurveTo():
   b=p.elementAt(i+1);c=p.elementAt(i+2);d.append(f'C{a.x:.2f},{a.y:.2f} {b.x:.2f},{b.y:.2f} {c.x:.2f},{c.y:.2f}');i+=2
  i+=1
 return f'<path fill="{color}" d="'+''.join(d)+'"/>'
def save(name,s,w,h):
 (out/name).write_text(s,encoding='utf-8');im=QImage(w,h,QImage.Format.Format_ARGB32);im.fill(0);p=QPainter(im);QSvgRenderer(s.encode()).render(p);p.end();im.save(str(root/(Path(name).stem+'-preview.png')))
for theme in ['dark','light']:
 dark=theme=='dark';bg='#0D0E17' if dark else '#F9F8FE';panel='#181925' if dark else '#FFFFFF';fg='#F5F2FF' if dark else '#211A36';muted='#AAA6BF' if dark else '#706782';purple='#AF95FF' if dark else '#7650E8';border='#343043' if dark else '#E0D8F1';soft='#262137' if dark else '#F0EAFB'
 def svg(w,h,title):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(title,quote=True)}"><title>{html.escape(title)}</title>'
 s=svg(1280,420,'DubiSub — Đưa câu chuyện đi xa hơn. Dịch video, phụ đề và lồng tiếng.')
 s+=f'<defs><radialGradient id="glow"><stop stop-color="{purple}" stop-opacity=".23"/><stop offset="1" stop-color="{bg}" stop-opacity="0"/></radialGradient><linearGradient id="ink"><stop stop-color="{purple}"/><stop offset="1" stop-color="{fg}"/></linearGradient></defs><rect x="1" y="1" width="1278" height="418" rx="28" fill="{bg}" stroke="{border}"/><ellipse cx="1080" cy="125" rx="450" ry="350" fill="url(#glow)"/>'
 for x in range(700,1260,24):
  for y in range(30,400,24):s+=f'<circle cx="{x}" cy="{y}" r=".8" fill="{purple}" opacity=".11"/>'
 s+=f'<g transform="translate(47 37) scale(.88)"><path d="M44 14H23C13 14 9 20 9 26S14 36 22 36H32" fill="none" stroke="{fg}" stroke-width="6" stroke-linecap="round"/><path d="M12 44H33C43 44 47 38 47 32S42 22 34 22H24" fill="none" stroke="{purple}" stroke-width="6" stroke-linecap="round"/></g>'
 s+=txt('Dubi',107,78,36,fg,600)+txt('Sub',189,78,36,purple,600)
 s+=txt('YOUR STORY. EVERY LANGUAGE.',56,137,12,purple,600)
 s+=txt('Đưa câu chuyện',52,214,57,fg,600)+txt('đi xa hơn.',52,280,57,'url(#ink)',600)
 s+=txt('Dịch video. Phụ đề. Lồng tiếng.',56,326,22,muted,400)
 s+=f'<path d="M56 368H89" stroke="{purple}" stroke-width="2"/>'+txt('DUBISUB-DESKTOP',103,373,12,muted,500)
 # Illustration: original layered media workspace with a translation label and voice card.
 s+=f'<g transform="rotate(-4 970 214)"><rect x="746" y="110" width="444" height="234" rx="18" fill="{soft}" stroke="{border}"/><rect x="733" y="96" width="444" height="234" rx="18" fill="{panel}" stroke="{border}"/><path d="M733 130H1177" stroke="{border}"/>'
 for i,c in enumerate([purple,muted,border]):s+=f'<circle cx="{753+12*i}" cy="113" r="3" fill="{c}"/>'
 s+=f'<rect x="752" y="147" width="406" height="99" rx="10" fill="{soft}"/><circle cx="955" cy="196" r="24" fill="{purple}"/><path d="M948 183L968 196L948 209Z" fill="{bg}"/>'
 for y,width in [(264,273),(279,192),(294,315)]:s+=f'<rect x="783" y="{y}" width="{width}" height="7" rx="3.5" fill="{purple}" opacity="{.8 if y==279 else .3}"/>'
 s+=txt('V',754,270,10,muted)+txt('S',754,285,10,muted)+txt('A',754,300,10,muted)
 s+=f'<path d="M1016 253V310" stroke="{fg}" stroke-width="1.4"/><circle cx="1016" cy="253" r="3" fill="{fg}"/></g>'
 s+=f'<rect x="1057" y="53" width="152" height="54" rx="14" fill="{soft}" stroke="{border}"/>'+txt('Aa',1075,87,24,purple,600)+txt('→',1114,85,20,muted)+txt('VI',1148,85,20,purple,600)
 # Voice card overlaps the media panel, with no fabricated numeric progress.
 s+=f'<rect x="698" y="304" width="236" height="79" rx="17" fill="{panel}" stroke="{border}"/>'
 for i in range(24):
  h=5+abs(math.sin(i*.59))*30;s+=f'<rect x="{718+i*5:.1f}" y="{344-h/2:.1f}" width="2.8" height="{h:.1f}" rx="1.4" fill="{purple}"/>'
 s+=txt('VOICE',856,348,11,muted,600)
 s+='</svg>';save(f'hero-{theme}.svg',s,1280,420)
 features=[('translate','Dịch & lồng tiếng',['Thêm ngôn ngữ mới','cho video của bạn.']),('edit','Biên tập phụ đề',['Chỉnh câu chữ và thời gian','theo cách bạn muốn.']),('workflow','Làm việc liền mạch',['Một video hoặc hàng loạt.','Tiến độ luôn trong tầm mắt.'])]
 for idx,(name,title,lines) in enumerate(features):
  card=svg(360,204,title+'. '+' '.join(lines));card+=f'<rect x="1" y="1" width="358" height="202" rx="20" fill="{panel}" stroke="{border}"/><circle cx="322" cy="30" r="75" fill="{purple}" opacity=".045"/><rect x="24" y="24" width="42" height="42" rx="13" fill="{soft}"/>'
  if name=='translate':icon='<circle cx="45" cy="45" r="11"/><ellipse cx="45" cy="45" rx="5" ry="11"/><path d="M34 45H56"/>'
  elif name=='edit':icon='<path d="M36 53L38 46L50 34L56 40L44 52Z M47 37L53 43 M35 57H56"/>'
  else:icon='<rect x="34" y="35" width="22" height="21" rx="4"/><path d="M39 32V38 M51 32V38 M34 42H56 M40 48L44 52L51 45"/>'
  card+=f'<g fill="none" stroke="{purple}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round">{icon}</g>'+txt(f'0{idx+1}',303,49,12,muted,500)+txt(title,24,107,23,fg,600)+txt(lines[0],24,144,17,muted,400)+txt(lines[1],24,171,17,muted,400)+'</svg>'
  save(f'feature-{name}-{theme}.svg',card,360,204)
print('Generated themed hero and feature cards.')
