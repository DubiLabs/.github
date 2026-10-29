"""Generate outlined SVG profile artwork. Requires PySide6 and Be Vietnam Pro TTFs."""
from pathlib import Path
import argparse,html,math
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase,QFont,QFontMetricsF,QPainterPath,QImage,QPainter
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
 dark=theme=='dark';bg='#0C0C15' if dark else '#FAF8FF';panel='#151520' if dark else '#FFFFFF';fg='#F7F4FF' if dark else '#251D38';muted='#AAA3BD' if dark else '#766B88';purple='#B49AFF' if dark else '#7953DD';border='#302B40' if dark else '#E5DCF4';soft='#262035' if dark else '#F1EBFA'
 def svg(w,h,title):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(title,quote=True)}"><title>{html.escape(title)}</title>'
 def mark(x,y,scale,first,second):return f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke-width="6" stroke-linecap="round"><path d="M44 14H23C13 14 9 20 9 26S14 36 22 36H32" stroke="{first}"/><path d="M12 44H33C43 44 47 38 47 32S42 22 34 22H24" stroke="{second}"/></g>'
 s=svg(1280,420,'DubiSub — Translate. Dub. Create. Một video. Mọi ngôn ngữ.')
 s+=f'<defs><radialGradient id="aura"><stop stop-color="{purple}" stop-opacity=".22"/><stop offset="1" stop-color="{bg}" stop-opacity="0"/></radialGradient><radialGradient id="orb" cx="35%" cy="25%"><stop stop-color="#43316D"/><stop offset="1" stop-color="#191329"/></radialGradient><linearGradient id="ribbon"><stop stop-color="#DACDFF"/><stop offset="1" stop-color="#8D66FF"/></linearGradient><linearGradient id="white"><stop stop-color="#FFFFFF"/><stop offset="1" stop-color="#D1BEFF"/></linearGradient></defs><rect x="1" y="1" width="1278" height="418" rx="28" fill="{bg}" stroke="{border}"/><ellipse cx="1020" cy="210" rx="430" ry="300" fill="url(#aura)"/>'
 s+=mark(50,35,.58,fg,purple)+txt('A WORLD OF STORIES. YOUR VOICE.',96,59,12,muted,500)
 font=QFont('Be Vietnam Pro');font.setPixelSize(104);font.setWeight(QFont.Weight.DemiBold);advance=QFontMetricsF(font).horizontalAdvance('Dubi')
 s+=txt('Dubi',50,198,104,fg,600)+txt('Sub',50+advance,198,104,purple,600)
 s+=txt('Translate. Dub. Create.',56,253,30,fg,500)+txt('Một video. Mọi ngôn ngữ. Dấu ấn của bạn.',56,299,20,muted,400)
 for x,w,label in [(56,105,'PHỤ ĐỀ'),(173,133,'LỒNG TIẾNG'),(318,121,'BIÊN TẬP')]:
  s+=f'<rect x="{x}" y="337" width="{w}" height="32" rx="16" fill="{soft}" stroke="{border}"/>'+txt(label,x+17,358,12,purple,500)
 # Signature illustration uses the original DubiSub ribbon geometry.
 s+=f'<ellipse cx="990" cy="213" rx="220" ry="97" transform="rotate(-33 990 213)" fill="none" stroke="{purple}" opacity=".18"/><circle cx="990" cy="213" r="164" fill="none" stroke="{border}"/><circle cx="990" cy="213" r="141" fill="url(#orb)" stroke="#604882" stroke-opacity=".45"/>'
 s+=mark(855,84,4.8,'url(#white)','url(#ribbon)')
 for x,y,r in [(798,197,3),(1169,259,4),(1080,57,3)]:s+=f'<circle cx="{x}" cy="{y}" r="{r}" fill="{purple}"/>'
 s+=f'<rect x="795" y="59" width="155" height="48" rx="15" fill="{panel}" stroke="{border}"/>'+txt('EN',814,89,16,muted,500)+txt('→',855,89,18,purple,500)+txt('VI',894,89,16,fg,600)
 s+=f'<rect x="1050" y="314" width="169" height="58" rx="17" fill="{panel}" stroke="{border}"/>'
 for i in range(20):
  h=4+abs(math.sin(i*.7))*27;s+=f'<rect x="{1068+i*3.9:.1f}" y="{343-h/2:.1f}" width="2.2" height="{h:.1f}" rx="1.1" fill="{purple}"/>'
 s+=txt('VOICE',1156,347,10,muted,500)+'</svg>';save(f'hero-{theme}.svg',s,1280,420)
 features=[('translate','Dịch & lồng tiếng',['Thêm ngôn ngữ mới','cho video của bạn.']),('edit','Biên tập phụ đề',['Câu chữ và thời gian,','đúng theo ý bạn.']),('workflow','Một nơi, mọi dự án',['Từng video hoặc hàng loạt.','Theo dõi tiến độ tập trung.'])]
 for idx,(name,title,lines) in enumerate(features):
  c=svg(360,262,title+'. '+' '.join(lines));c+=f'<rect x="1" y="1" width="358" height="260" rx="22" fill="{panel}" stroke="{border}"/><rect x="15" y="15" width="330" height="119" rx="15" fill="{soft}"/>'
  if name=='translate':
   c+=f'<path d="M143 67C160 43 204 43 220 67" fill="none" stroke="{purple}" stroke-width="1.5"/><path d="M212 61L221 67L224 57" fill="none" stroke="{purple}" stroke-width="1.5"/><rect x="41" y="37" width="117" height="44" rx="12" fill="{panel}" stroke="{border}"/><rect x="201" y="71" width="117" height="44" rx="12" fill="{panel}" stroke="{purple}"/>'+txt('Hello.',67,65,17,fg,500)+txt('Xin chào.',218,99,17,purple,500)
  elif name=='edit':
   for y,x,w,label in [(37,36,288,'Chỉnh từng câu chữ'),(76,64,232,'Giữ trọn nhịp câu chuyện')]:
    c+=f'<rect x="{x}" y="{y}" width="{w}" height="28" rx="7" fill="{panel}"/>'+txt(label,x+13,y+19,13,fg,400)
   c+=f'<path d="M42 115H319" stroke="{border}"/><path d="M191 30V120" stroke="{purple}"/><circle cx="191" cy="30" r="3" fill="{purple}"/>'
  else:
   for i,y in enumerate([33,64,95]):
    c+=f'<rect x="39" y="{y}" width="19" height="19" rx="5" fill="{panel}" stroke="{border}"/>'
    if i<2:c+=f'<path d="M43 {y+9}L47 {y+13}L54 {y+5}" fill="none" stroke="{purple}" stroke-width="1.8"/>'
    c+=f'<rect x="74" y="{y+6}" width="{129-i*19}" height="7" rx="3.5" fill="{purple}" opacity="{.55-i*.12}"/><rect x="248" y="{y+5}" width="67" height="9" rx="4.5" fill="{panel}"/>'
  c+=txt(f'0{idx+1}',24,166,11,purple,500)+txt(title,24,198,23,fg,600)+txt(lines[0],24,226,16,muted,400)+txt(lines[1],24,248,16,muted,400)+'</svg>';save(f'feature-{name}-{theme}.svg',c,360,262)
print('Generated signature ribbon hero and illustrated feature cards.')
