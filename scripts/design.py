"""Original pkOS design assets. MIT; no downloaded theme or vendor artwork."""
from pathlib import Path
import shutil

BG = '#10151b'
SURFACE = '#17212b'
ACCENT = '#8babc0'
TEXT = '#edf2f7'
BORDER = '#33434f'

def svg(elements, width=1024, height=1024):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">' + ''.join(elements) + '</svg>\n'

def frame(prefix, x=0, y=0, radius=12, color=SURFACE, opacity=1, border=BORDER, dot=False, hover=False, margins=8):
    """Nine-slice frame: solid fills, 1px outline, no shadow or gradients."""
    r = max(radius, 1)
    pieces=[]
    stem=prefix+'-' if prefix else ''
    for name, dx, dy, width, height in [('center',r,r,64,64),('top',r,0,64,r),('bottom',r,r+64,64,r),('left',0,r,r,64),('right',r+64,r,r,64)]:
        fill=color
        alpha=opacity
        detail=''
        if dot:
            fill=SURFACE if hover and name=='center' else BG
            alpha=0.45 if hover and name=='center' else 0
            if name=='bottom':
                detail=f'<circle cx="32" cy="{r/2}" r="2" fill="{ACCENT}"/>'
        elif border:
            if name=='top': detail=f'<path d="M0 .5H64" stroke="{border}"/>'
            if name=='bottom': detail=f'<path d="M0 {r-.5}H64" stroke="{border}"/>'
            if name=='left': detail=f'<path d="M.5 0V64" stroke="{border}"/>'
            if name=='right': detail=f'<path d="M{r-.5} 0V64" stroke="{border}"/>'
        pieces.append(f'<g id="{stem}{name}" transform="translate({x+dx} {y+dy})"><rect width="{width}" height="{height}" fill="{fill}" fill-opacity="{alpha}"/>{detail}</g>')
    for name,dx,dy,rotation in [('topleft',0,0,0),('topright',r+64,0,90),('bottomright',r+64,r+64,180),('bottomleft',0,r+64,270)]:
        # Corner paths have exact r x r bounds. Rotate around their centres.
        shape=f'M0 {r} A{r} {r} 0 0 1 {r} 0 V{r} Z'
        alpha=0 if dot else opacity
        outline='' if dot or not border else f'<path d="M.5 {r} A{r-.5} {r-.5} 0 0 1 {r} .5" fill="none" stroke="{border}"/>'
        pieces.append(f'<g id="{stem}{name}" transform="translate({x+dx} {y+dy})"><g transform="rotate({rotation} {r/2} {r/2})"><path d="{shape}" fill="{color}" fill-opacity="{alpha}"/>{outline}</g></g>')
    for side in ['top','bottom','left','right']:
        pieces.append(f'<rect id="{stem}hint-{side}-margin" x="{x+100}" y="{y+100}" width="{margins}" height="{margins}" fill="#000"/>')
    # Stretch the strips once; tiling them exposes raster seams every 64px.
    pieces.append(f'<rect id="{stem}hint-stretch-borders" x="{x+112}" y="{y+112}" width="1" height="1"/>')
    return pieces

def deploy(root):
    root=Path(root)
    def write(dest, text):
        p=root/dest
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(text)
    def tree(source,dest):
        shutil.copytree(source,root/dest,dirs_exist_ok=True)
    tree('branding/aurorae','usr/share/aurorae/themes/pkos')
    write('usr/share/aurorae/themes/pkos/decoration.svg', svg(frame('decoration',color=SURFACE,margins=1)+frame('decoration-inactive',x=128,color=SURFACE,margins=1)))
    for name,color in [('close','#d27b83'),('minimize','#c7ac76'),('maximize','#8cae98'),('restore','#8cae98')]:
        elements=[]
        for i,state in enumerate(['active','inactive','hover','hover-inactive','pressed','pressed-inactive','deactivated','deactivated-inactive']):
            fill='#596674' if state.startswith('deactivated') else color
            alpha='.65' if state=='inactive' else '1'
            mark=''
            if state.startswith(('hover','pressed')):
                path={'close':'M6 6l4 4m0-4-4 4','minimize':'M5 8h6','maximize':'M5 8h6m-3-3v6','restore':'M5 8h6'}[name]
                mark=f'<path d="{path}" stroke="{BG}" stroke-width="1.2" stroke-linecap="round"/>'
            elements.append(f'<g id="{state}-center" transform="translate({i*24} 0)"><rect width="16" height="16" fill="{BG}" fill-opacity="0"/><circle cx="8" cy="8" r="6" fill="{fill}" opacity="{alpha}"/>{mark}</g>')
        write(f'usr/share/aurorae/themes/pkos/{name}.svg',svg(elements,192,16))
    tree('branding/plasma-style','usr/share/plasma/desktoptheme/pkos')
    tree('branding/wordmark-applet','usr/share/plasma/plasmoids/org.pkos.wordmark')
    for selector,alpha in [('',.94),('opaque/',1),('solid/',1),('translucent/',.94)]:
        elements=frame('',opacity=alpha)+frame('north',x=128,radius=1,opacity=alpha,margins=4)+frame('south',x=256,opacity=alpha,margins=8)
        write('usr/share/plasma/desktoptheme/pkos/'+selector+'widgets/panel-background.svg',svg(elements))
    elements=[]
    prefixes=['normal','focus','minimized','attention','hover','normal-hover','focus-hover','minimized-hover','attention-hover','launcher-hover']
    for i,prefix in enumerate(prefixes):
        elements+=frame(prefix,x=(i%5)*128,y=(i//5)*128,radius=8,dot=prefix!='launcher-hover',hover='hover' in prefix,border=None,margins=8)
    elements+=frame('progress',x=0,y=384,radius=8,color=ACCENT,opacity=.15,border=None,margins=8)
    write('usr/share/plasma/desktoptheme/pkos/widgets/tasks.svg',svg(elements))
    colors=root/'usr/share/color-schemes/pkOS.colors'
    shutil.copy2(colors,root/'usr/share/plasma/desktoptheme/pkos/colors')
    css='''/* pkOS overrides, MIT. Breeze supplies the GTK widget engine. */
@define-color theme_bg_color #17212b;
@define-color theme_fg_color #edf2f7;
@define-color theme_base_color #10151b;
@define-color theme_text_color #edf2f7;
@define-color theme_selected_bg_color #8babc0;
@define-color theme_selected_fg_color #10151b;
@define-color borders #33434f;
* { font-family: Inter; }
window, dialog, headerbar, menubar, toolbar, .titlebar { background-color: #17212b; background-image: none; color: #edf2f7; box-shadow: none; }
entry, textview, treeview, .view { background-color: #10151b; color: #edf2f7; }
button { background-image: none; background-color: #17212b; color: #edf2f7; border: 1px solid #33434f; border-radius: 8px; box-shadow: none; }
button:hover, button:checked { background-color: #33434f; }
selection { background-color: #8babc0; color: #10151b; }
*:focus { border-color: #8babc0; }
'''
    write('usr/share/themes/pkOS/gtk-3.0/gtk.css','@import url("/usr/share/themes/Breeze-Dark/gtk-3.0/gtk.css");\n'+css)
    write('usr/share/themes/pkOS/index.theme','[Desktop Entry]\nName=pkOS\nType=X-GNOME-Metatheme\n[X-GNOME-Metatheme]\nGtkTheme=pkOS\nIconTheme=Papirus-Dark\nCursorTheme=breeze_cursors\n')
    write('etc/skel/.config/gtk-3.0/gtk.css',css)
    # GTK4's native base style remains, with the same palette and typography.
    write('etc/skel/.config/gtk-4.0/gtk.css',css)

