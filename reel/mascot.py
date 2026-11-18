"""Linh vật vẽ riêng cho Sống vui mỗi ngày: Mèo Vui và Robot Tây (vẽ bằng Pillow, không dùng emoji)."""
from PIL import Image, ImageDraw

OR, OR_D, CREAM, PINK, INK, WHITE = '#F5A04A', '#D9822B', '#FFF1DC', '#FF8FA3', '#2B2B3A', '#FFFFFF'


def _arc_eye(d, cx, cy, r, w, up=True):
    box = (cx - r, cy - r * 0.7, cx + r, cy + r * 0.9)
    d.arc(box, 200, 340, fill=INK, width=w) if up else d.arc(box, 20, 160, fill=INK, width=w)


def cat(mood='😺', k=0.0, size=270):
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
    # mũ sinh nhật
    d.polygon([f(0.40, 0.27), f(0.50, 0.00), f(0.62, 0.27)], fill='#4DABF7', outline='#1971C2')
    d.ellipse((0.47 * S, -0.015 * S, 0.53 * S, 0.045 * S), fill='#FFD43B')
    for yy in (0.12, 0.2): d.line([f(0.5 - (0.27 - yy) * 0.37, yy + 0.03), f(0.5 + (0.27 - yy) * 0.37, yy + 0.03)], fill='#FFD43B', width=7)
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
    return im.resize((size, size), Image.LANCZOS)


def bot(mood='🤖', k=0.0, size=270):
    S = 600; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = lambda x, y: (x * S, y * S)
    d.line([f(0.5, 0.26), f(0.5, 0.10)], fill='#6B7685', width=14); d.ellipse((0.43 * S, 0.02 * S, 0.57 * S, 0.14 * S), fill='#FA5252', outline='#C92A2A', width=5)
    for x0, x1 in ((0.07, 0.19), (0.81, 0.93)): d.rounded_rectangle((x0 * S, 0.44 * S, x1 * S, 0.68 * S), 24, fill='#E03131', outline='#A61E1E', width=5)
    d.rounded_rectangle((0.16 * S, 0.24 * S, 0.84 * S, 0.88 * S), 70, fill='#B8C2CF', outline='#6B7685', width=7)
    d.rounded_rectangle((0.24 * S, 0.34 * S, 0.76 * S, 0.60 * S), 44, fill='#1B2A3D')
    for x in (0.38, 0.62):
        if mood == '😸':  # mắt cười
            d.arc((x * S - 36, 0.40 * S, x * S + 36, 0.56 * S), 200, 340, fill='#66E0FF', width=12)
        else:
            d.ellipse((x * S - 30, 0.40 * S, x * S + 30, 0.54 * S + 4), fill='#66E0FF'); d.ellipse((x * S - 9, 0.43 * S, x * S + 6, 0.47 * S), fill=WHITE)
    mh = 0.05 + 0.09 * min(1, k)  # miệng lưới, mở theo lời nói
    d.rounded_rectangle((0.32 * S, 0.66 * S, 0.68 * S, (0.66 + mh) * S), 18, fill=WHITE, outline='#6B7685', width=5)
    for i in range(1, 6): d.line([f(0.32 + i * 0.06, 0.67), f(0.32 + i * 0.06, 0.66 + mh - 0.01)], fill='#9AA5B1', width=4)
    return im.resize((size, size), Image.LANCZOS)


def draw(who, mood, k, size):
    return cat(mood, k, size) if who == 'cat' else bot(mood, k, size)
