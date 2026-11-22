"""Linh vật vẽ riêng cho Sống vui mỗi ngày: Mèo Vui và Robot Tây (vẽ bằng Pillow, không dùng emoji)."""
from PIL import Image, ImageDraw

OR, OR_D, CREAM, PINK, INK, WHITE = '#F5A04A', '#D9822B', '#FFF1DC', '#FF8FA3', '#2B2B3A', '#FFFFFF'


def _arc_eye(d, cx, cy, r, w, up=True):
    box = (cx - r, cy - r * 0.7, cx + r, cy + r * 0.9)
    d.arc(box, 200, 340, fill=INK, width=w) if up else d.arc(box, 20, 160, fill=INK, width=w)

# ------------------------------------------------------------------ bộ đồ đổi theo ngày (mũ, kính, khăn/nơ)
OUTFITS = [  # (mũ, kính, cổ)
    ('birthday', None, 'bowtie'), ('chef', None, 'scarf_red'), ('crown', 'glasses', None), ('beanie', None, 'scarf_blue'),
    ('sunhat', 'shades', None), ('grad', 'glasses', 'bowtie'), ('wizard', None, None), ('pirate', None, 'scarf_red'),
    ('cowboy', None, 'bandana'), ('cap', 'shades', None), ('flower', None, 'bowtie'), ('headphones', None, None),
    ('detective', 'glasses', None), ('beret', None, 'scarf_blue'), ('top', None, 'bowtie'), ('hardhat', None, 'bandana'),
]
NAMES_VI = {'birthday': 'mũ sinh nhật', 'chef': 'mũ đầu bếp', 'crown': 'vương miện', 'beanie': 'mũ len', 'sunhat': 'mũ cói',
            'grad': 'mũ cử nhân', 'wizard': 'mũ phù thuỷ', 'pirate': 'mũ cướp biển', 'cowboy': 'mũ cao bồi', 'cap': 'mũ lưỡi trai',
            'flower': 'vòng hoa', 'headphones': 'tai nghe', 'detective': 'mũ thám tử', 'beret': 'mũ nồi', 'top': 'mũ chóp cao', 'hardhat': 'mũ bảo hộ'}


def _hat(d, S, name, b=0.27, w=0.2, hw=0.37):
    f = lambda x, y: (x * S, y * S)
    if name == 'birthday':
        d.polygon([f(0.5 - w * 0.65, b), f(0.5, b - 0.27), f(0.5 + w * 0.65, b)], fill='#4DABF7', outline='#1971C2')
        d.ellipse((0.47 * S, (b - 0.285) * S, 0.53 * S, (b - 0.225) * S), fill='#FFD43B')
        for yy in (0.12, 0.2): d.line([f(0.5 - (0.27 - yy) * 0.37, b - 0.27 + yy + 0.03), f(0.5 + (0.27 - yy) * 0.37, b - 0.27 + yy + 0.03)], fill='#FFD43B', width=7)
    elif name == 'chef':
        for cx, cy, r in ((0.38, b - 0.13, 0.085), (0.62, b - 0.13, 0.085), (0.5, b - 0.18, 0.095)):
            d.ellipse(((cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S), fill='#FFFFFF', outline='#ADB5BD', width=4)
        d.rounded_rectangle((( 0.5 - w * 0.85) * S, (b - 0.09) * S, (0.5 + w * 0.85) * S, (b + 0.02) * S), 14, fill='#FFFFFF', outline='#ADB5BD', width=4)
    elif name == 'crown':
        pts = [(0.5 - w, b + 0.01), (0.5 - w, b - 0.15), (0.5 - w * 0.5, b - 0.07), (0.5, b - 0.19), (0.5 + w * 0.5, b - 0.07), (0.5 + w, b - 0.15), (0.5 + w, b + 0.01)]
        d.polygon([f(*q) for q in pts], fill='#FFD43B', outline='#E8A800')
        for cx, col in ((0.5 - w * 0.6, '#FF6B6B'), (0.5, '#4DABF7'), (0.5 + w * 0.6, '#51CF66')):
            d.ellipse(((cx - 0.02) * S, (b - 0.045) * S, (cx + 0.02) * S, (b - 0.005) * S), fill=col)
    elif name == 'beanie':
        d.pieslice((( 0.5 - w) * S, (b - 0.24) * S, (0.5 + w) * S, (b + 0.14) * S), 180, 360, fill='#E64980', outline='#C2255C')
        d.rounded_rectangle(((0.5 - w) * S, (b - 0.025) * S, (0.5 + w) * S, (b + 0.05) * S), 12, fill='#C2255C')
        d.ellipse((0.455 * S, (b - 0.27) * S, 0.545 * S, (b - 0.19) * S), fill='#FFFFFF', outline='#DEE2E6')
    elif name == 'sunhat':
        d.pieslice(((0.5 - w * 0.75) * S, (b - 0.22) * S, (0.5 + w * 0.75) * S, (b + 0.07) * S), 180, 360, fill='#F2D58A', outline='#C9A64E')
        d.ellipse(((0.5 - w * 1.5) * S, (b - 0.02) * S, (0.5 + w * 1.5) * S, (b + 0.08) * S), fill='#F2D58A', outline='#C9A64E', width=4)
        d.rectangle(((0.5 - w * 0.75) * S, (b - 0.06) * S, (0.5 + w * 0.75) * S, (b - 0.01) * S), fill='#FA5252')
    elif name == 'grad':
        d.rounded_rectangle(((0.5 - w * 0.6) * S, (b - 0.03) * S, (0.5 + w * 0.6) * S, (b + 0.07) * S), 10, fill='#343A40')
        d.polygon([f(0.5 - w * 1.4, b - 0.08), f(0.5, b - 0.2), f(0.5 + w * 1.4, b - 0.08), f(0.5, b + 0.02)], fill='#2B2B3A', outline='#000000')
        d.line([f(0.5 + w * 1.1, b - 0.08), f(0.5 + w * 1.1, b + 0.08)], fill='#FFD43B', width=7)
        d.ellipse(((0.5 + w * 1.1 - 0.02) * S, (b + 0.07) * S, (0.5 + w * 1.1 + 0.02) * S, (b + 0.11) * S), fill='#FFD43B')
    elif name == 'wizard':
        d.polygon([f(0.5 - w * 0.95, b + 0.01), f(0.53, b - 0.28), f(0.5 + w * 0.95, b + 0.01)], fill='#7048E8', outline='#4C2BB3')
        d.ellipse(((0.5 - w * 1.35) * S, (b - 0.025) * S, (0.5 + w * 1.35) * S, (b + 0.055) * S), fill='#5F3DC4', outline='#4C2BB3', width=4)
        for cx, cy in ((0.46, b - 0.1), (0.56, b - 0.19), (0.5, b - 0.26)): d.ellipse(((cx - 0.015) * S, (cy - 0.015) * S, (cx + 0.015) * S, (cy + 0.015) * S), fill='#FFD43B')
    elif name == 'pirate':
        d.polygon([f(0.5 - w * 1.35, b + 0.04), f(0.5 - w * 0.7, b - 0.17), f(0.5, b - 0.12), f(0.5 + w * 0.7, b - 0.17), f(0.5 + w * 1.35, b + 0.04), f(0.5, b - 0.02)], fill='#212529', outline='#000000')
        d.ellipse((0.47 * S, (b - 0.1) * S, 0.53 * S, (b - 0.04) * S), fill='#FFFFFF')
        d.line([f(0.48, b - 0.03), f(0.52, b - 0.03)], fill='#FFFFFF', width=4)
    elif name == 'cowboy':
        d.pieslice(((0.5 - w * 0.8) * S, (b - 0.2) * S, (0.5 + w * 0.8) * S, (b + 0.06) * S), 180, 360, fill='#A9744F', outline='#7A4E2D')
        d.polygon([f(0.5 - w * 1.5, b - 0.06), f(0.5 - w * 0.9, b + 0.03), f(0.5 + w * 0.9, b + 0.03), f(0.5 + w * 1.5, b - 0.06), f(0.5 + w * 1.0, b + 0.07), f(0.5 - w * 1.0, b + 0.07)], fill='#A9744F', outline='#7A4E2D')
        d.rectangle(((0.5 - w * 0.8) * S, (b - 0.04) * S, (0.5 + w * 0.8) * S, (b + 0.0) * S), fill='#5C3A21')
    elif name == 'cap':
        d.pieslice(((0.5 - w * 0.95) * S, (b - 0.22) * S, (0.5 + w * 0.95) * S, (b + 0.1) * S), 180, 360, fill='#FA5252', outline='#C92A2A')
        d.polygon([f(0.5 - w * 0.2, b - 0.01), f(0.5 + w * 1.5, b + 0.0), f(0.5 + w * 1.4, b + 0.05), f(0.5 - w * 0.2, b + 0.05)], fill='#C92A2A')
        d.ellipse((0.485 * S, (b - 0.215) * S, 0.515 * S, (b - 0.185) * S), fill='#C92A2A')
    elif name == 'flower':
        for cx, cy, col in ((0.36, b - 0.0, '#FF8FA3'), (0.5, b - 0.04, '#FFD43B'), (0.64, b - 0.0, '#74C0FC')):
            for ang in range(5):
                import math
                ax, ay = cx + 0.035 * math.cos(ang * 1.2566), cy + 0.035 * math.sin(ang * 1.2566)
                d.ellipse(((ax - 0.025) * S, (ay - 0.025) * S, (ax + 0.025) * S, (ay + 0.025) * S), fill=col)
            d.ellipse(((cx - 0.016) * S, (cy - 0.016) * S, (cx + 0.016) * S, (cy + 0.016) * S), fill='#FFFFFF')
    elif name == 'headphones':
        d.arc(((0.5 - hw) * S, (b - 0.16) * S, (0.5 + hw) * S, (b + 0.4) * S), 180, 360, fill='#343A40', width=16)
        for sx in (-1, 1):
            cx = 0.5 + sx * hw
            d.rounded_rectangle(((cx - 0.045) * S, (b + 0.07) * S, (cx + 0.045) * S, (b + 0.21) * S), 18, fill='#FA5252', outline='#C92A2A', width=4)
    elif name == 'detective':
        d.pieslice(((0.5 - w * 0.9) * S, (b - 0.2) * S, (0.5 + w * 0.9) * S, (b + 0.07) * S), 180, 360, fill='#B08968', outline='#7F5539')
        d.polygon([f(0.5 - w * 1.25, b + 0.01), f(0.5 - w * 0.6, b - 0.03), f(0.5 - w * 0.6, b + 0.05)], fill='#7F5539')
        d.polygon([f(0.5 + w * 1.25, b + 0.01), f(0.5 + w * 0.6, b - 0.03), f(0.5 + w * 0.6, b + 0.05)], fill='#7F5539')
        d.line([f(0.5, b - 0.2), f(0.5, b)], fill='#7F5539', width=5)
    elif name == 'beret':
        d.ellipse(((0.5 - w * 1.0) * S, (b - 0.13) * S, (0.5 + w * 1.15) * S, (b + 0.05) * S), fill='#C92A2A', outline='#A61E1E', width=4)
        d.ellipse((0.49 * S, (b - 0.155) * S, 0.53 * S, (b - 0.115) * S), fill='#A61E1E')
    elif name == 'top':
        d.rectangle(((0.5 - w * 0.62) * S, (b - 0.27) * S, (0.5 + w * 0.62) * S, (b - 0.0) * S), fill='#212529')
        d.rectangle(((0.5 - w * 0.62) * S, (b - 0.07) * S, (0.5 + w * 0.62) * S, (b - 0.02) * S), fill='#FA5252')
        d.ellipse(((0.5 - w * 1.1) * S, (b - 0.035) * S, (0.5 + w * 1.1) * S, (b + 0.045) * S), fill='#212529')
    elif name == 'hardhat':
        d.pieslice(((0.5 - w * 0.95) * S, (b - 0.22) * S, (0.5 + w * 0.95) * S, (b + 0.1) * S), 180, 360, fill='#FFD43B', outline='#E8A800')
        d.rounded_rectangle(((0.5 - w * 1.2) * S, (b - 0.02) * S, (0.5 + w * 1.2) * S, (b + 0.04) * S), 10, fill='#FAB005', outline='#E8A800')
        d.rectangle((0.47 * S, (b - 0.22) * S, 0.53 * S, (b - 0.0) * S), fill='#FAB005')


def _face(d, S, name, ex, ey, r=0.085):
    f = lambda x, y: (x * S, y * S)
    if name == 'glasses':
        for x in ex: d.ellipse(((x - r) * S, (ey - r) * S, (x + r) * S, (ey + r) * S), outline='#2B2B3A', width=7)
        d.line([f(ex[0] + r, ey), f(ex[1] - r, ey)], fill='#2B2B3A', width=7)
    elif name == 'shades':
        for x in ex: d.rounded_rectangle(((x - r) * S, (ey - r * 0.8) * S, (x + r) * S, (ey + r * 0.9) * S), 18, fill='#1B1B26', outline='#000000', width=4)
        d.line([f(ex[0] + r, ey - 0.02), f(ex[1] - r, ey - 0.02)], fill='#1B1B26', width=8)
        for x in ex: d.line([f(x - r * 0.5, ey - r * 0.5), f(x - r * 0.1, ey - r * 0.1)], fill='#FFFFFF', width=4)


def _neck(d, S, name, y0=0.84):
    f = lambda x, y: (x * S, y * S)
    if name == 'bowtie':
        d.polygon([f(0.5, y0 + 0.07), f(0.34, y0 + 0.01), f(0.34, y0 + 0.13)], fill='#FA5252', outline='#C92A2A')
        d.polygon([f(0.5, y0 + 0.07), f(0.66, y0 + 0.01), f(0.66, y0 + 0.13)], fill='#FA5252', outline='#C92A2A')
        d.ellipse((0.47 * S, (y0 + 0.04) * S, 0.53 * S, (y0 + 0.10) * S), fill='#C92A2A')
    elif name in ('scarf_red', 'scarf_blue'):
        c1, c2 = ('#FA5252', '#C92A2A') if name == 'scarf_red' else ('#4DABF7', '#1971C2')
        d.rounded_rectangle((0.22 * S, (y0 - 0.01) * S, 0.78 * S, (y0 + 0.08) * S), 20, fill=c1, outline=c2, width=4)
        d.rounded_rectangle((0.60 * S, (y0 + 0.04) * S, 0.72 * S, (y0 + 0.16) * S), 12, fill=c1, outline=c2, width=4)
        for xx in (0.30, 0.42, 0.54): d.line([f(xx, y0), f(xx, y0 + 0.07)], fill=c2, width=4)
    elif name == 'bandana':
        d.polygon([f(0.26, y0), f(0.74, y0), f(0.5, y0 + 0.16)], fill='#FF922B', outline='#E8590C')
        for cx, cy in ((0.4, y0 + 0.03), (0.5, y0 + 0.07), (0.6, y0 + 0.03)): d.ellipse(((cx - 0.012) * S, (cy - 0.012) * S, (cx + 0.012) * S, (cy + 0.012) * S), fill='#FFFFFF')



def cat(mood='😺', k=0.0, size=270, outfit=0):
    S = 600; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = lambda x, y: (x * S, y * S)
    # tai
    for sx in (1, -1):
        px = lambda x: 0.5 + sx * (x - 0.5)
        d.polygon([f(px(0.19), 0.42), f(px(0.25), 0.10), f(px(0.43), 0.28)], fill=OR, outline=OR_D)
        d.polygon([f(px(0.24), 0.36), f(px(0.28), 0.17), f(px(0.38), 0.29)], fill=PINK)
    # đầu
    d.ellipse((0.13 * S, 0.24 * S, 0.87 * S, 0.88 * S), fill=OR, outline=OR_D, width=6)
    for dx in (-0.07, 0, 0.07):  # vằn trán
        d.line([f(0.5 + dx, 0.25), f(0.5 + dx * 0.8, 0.36)], fill=OR_D, width=9)
    d.ellipse((0.30 * S, 0.58 * S, 0.70 * S, 0.84 * S), fill=CREAM)
    for sx in (0.22, 0.78):  # má hồng
        d.ellipse((sx * S - 34, 0.64 * S - 20, sx * S + 34, 0.64 * S + 20), fill=(255, 143, 163, 120))
    hat, face, neck = OUTFITS[outfit % len(OUTFITS)]
    _hat(d, S, hat, 0.27, 0.2, 0.37)
    ex = (0.36, 0.64); ey = 0.52
    if mood == '🙀':  # hoảng
        for x in ex:
            d.ellipse((x * S - 40, ey * S - 44, x * S + 40, ey * S + 44), fill=WHITE, outline=INK, width=6)
            d.ellipse((x * S - 11, ey * S - 11, x * S + 11, ey * S + 11), fill=INK)
    elif mood in ('😸', '😹'):  # mắt cười
        for x in ex: _arc_eye(d, x * S, ey * S + 8, 34, 11, True)
    elif mood == '😼':  # nghĩ ngợi, mắt lim dim
        for x in ex:
            d.ellipse((x * S - 27, ey * S - 30, x * S + 27, ey * S + 30), fill=INK)
            d.rectangle((x * S - 32, ey * S - 36, x * S + 32, ey * S - 4), fill=OR)
            d.line([f(x - 0.075, ey - 0.012), f(x + 0.075, ey - 0.012)], fill=INK, width=9)
            d.ellipse((x * S - 7, ey * S + 2, x * S + 3, ey * S + 12), fill=WHITE)
    else:  # vui
        for x in ex:
            d.ellipse((x * S - 27, ey * S - 36, x * S + 27, ey * S + 36), fill=INK)
            d.ellipse((x * S - 4, ey * S - 22, x * S + 12, ey * S - 6), fill=WHITE)
    d.polygon([f(0.46, 0.625), f(0.54, 0.625), f(0.5, 0.665)], fill=PINK)  # mũi
    open_ = max(k, 0.55 if mood in ('😹', '🙀') else 0.0)
    if open_ > 0.08:  # miệng mở theo lời nói
        h = 0.05 + 0.12 * min(1, open_)
        d.pieslice((0.40 * S, 0.66 * S, 0.60 * S, (0.66 + h * 2) * S), 0, 180, fill='#7A1F2B')
        d.pieslice((0.44 * S, (0.66 + h * 1.15) * S, 0.56 * S, (0.66 + h * 2) * S), 0, 180, fill=PINK)
    else:
        d.arc((0.40 * S, 0.64 * S, 0.50 * S, 0.74 * S), 10, 170, fill=INK, width=7)
        d.arc((0.50 * S, 0.64 * S, 0.60 * S, 0.74 * S), 10, 170, fill=INK, width=7)
    for sy, a in ((0.64, -0.03), (0.68, 0.0), (0.72, 0.03)):  # ria
        d.line([f(0.30, sy), f(0.10, sy + a)], fill=INK, width=4); d.line([f(0.70, sy), f(0.90, sy + a)], fill=INK, width=4)
    if mood == '😹':  # nước mắt cười
        for x in (0.25, 0.75): d.ellipse((x * S - 14, 0.60 * S, x * S + 14, 0.60 * S + 44), fill='#74C0FC')
    if face: _face(d, S, face, ex, ey)
    if neck: _neck(d, S, neck, 0.85)
    return im.resize((size, size), Image.LANCZOS)


def bot(mood='🤖', k=0.0, size=270, outfit=0):
    S = 600; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = lambda x, y: (x * S, y * S)
    d.line([f(0.5, 0.26), f(0.5, 0.10)], fill='#6B7685', width=14); d.ellipse((0.43 * S, 0.02 * S, 0.57 * S, 0.14 * S), fill='#FA5252', outline='#C92A2A', width=5)
    for x0, x1 in ((0.07, 0.19), (0.81, 0.93)): d.rounded_rectangle((x0 * S, 0.44 * S, x1 * S, 0.68 * S), 24, fill='#E03131', outline='#A61E1E', width=5)
    d.rounded_rectangle((0.16 * S, 0.24 * S, 0.84 * S, 0.88 * S), 70, fill='#B8C2CF', outline='#6B7685', width=7)
    hat, face, neck = OUTFITS[outfit % len(OUTFITS)]
    _hat(d, S, hat, 0.26, 0.22, 0.34)
    if hat in ('headphones', 'flower'): d.line([f(0.5, 0.26), f(0.5, 0.10)], fill='#6B7685', width=14); d.ellipse((0.43 * S, 0.02 * S, 0.57 * S, 0.14 * S), fill='#FA5252', outline='#C92A2A', width=5)
    d.rounded_rectangle((0.24 * S, 0.34 * S, 0.76 * S, 0.60 * S), 44, fill='#1B2A3D')
    for x in (0.38, 0.62):
        if mood == '😸':  # mắt cười
            d.arc((x * S - 36, 0.40 * S, x * S + 36, 0.56 * S), 200, 340, fill='#66E0FF', width=12)
        else:
            d.ellipse((x * S - 30, 0.40 * S, x * S + 30, 0.54 * S + 4), fill='#66E0FF'); d.ellipse((x * S - 9, 0.43 * S, x * S + 6, 0.47 * S), fill=WHITE)
    mh = 0.05 + 0.09 * min(1, k)  # miệng lưới, mở theo lời nói
    d.rounded_rectangle((0.32 * S, 0.66 * S, 0.68 * S, (0.66 + mh) * S), 18, fill=WHITE, outline='#6B7685', width=5)
    for i in range(1, 6): d.line([f(0.32 + i * 0.06, 0.67), f(0.32 + i * 0.06, 0.66 + mh - 0.01)], fill='#9AA5B1', width=4)
    if face: _face(d, S, face, (0.38, 0.62), 0.47, 0.075)
    if neck: _neck(d, S, neck, 0.85)
    return im.resize((size, size), Image.LANCZOS)


def draw(who, mood, k, size, outfit=0):
    return cat(mood, k, size, outfit) if who == 'cat' else bot(mood, k, size, outfit)
