"""Sống vui mỗi ngày - dựng Reel song ngữ (1 slide: câu nói vui + tiếng cười + câu đố) rồi đăng Facebook.
Mỗi lần chạy = 1 Reel. Sau khi đăng Reel mới, bình luận ĐÁP ÁN của Reel trước.
Biến môi trường: PAYLOAD (json: page_id, force, preview), FB_PAGE_TOKEN_SVMN, FB_PAGE_ID (dự phòng), DRY_TTS=1 (thử cục bộ, không gọi TTS)."""
import os, sys, io, json, math, random, time, wave, struct, asyncio, subprocess, textwrap, urllib.request
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, 'assets', 'fonts')
STATE_PATH = os.path.join(ROOT, 'state.json')
W, H = 1080, 1920
GV = 'https://graph.facebook.com/v23.0'
WORK = os.environ.get('WORK_DIR', '/tmp/svmn')
os.makedirs(WORK, exist_ok=True)

P = json.loads(os.environ.get('PAYLOAD') or '{}') or {}
PREVIEW = str(P.get('preview', os.environ.get('IN_PREVIEW') or os.environ.get('PREVIEW', ''))).lower() in ('1', 'true', 'yes')
FORCE = str(P.get('force', os.environ.get('IN_FORCE', ''))).lower() in ('1', 'true', 'yes')
DRY_TTS = os.environ.get('DRY_TTS') == '1'
PAGE_ID = str(P.get('page_id') or os.environ.get('FB_PAGE_ID') or '').strip()
TOKEN = os.environ.get('FB_PAGE_TOKEN_SVMN', '').strip()

# ---------------------------------------------------------------- phông chữ (tải từ Google Fonts nếu thiếu)
GF = 'https://raw.githubusercontent.com/google/fonts/main/ofl/'
FONTS = {
    'Pacifico.ttf': 'pacifico/Pacifico-Regular.ttf', 'Lobster.ttf': 'lobster/Lobster-Regular.ttf',
    'Baloo2.ttf': 'baloo2/Baloo2%5Bwght%5D.ttf', 'PatrickHand.ttf': 'patrickhand/PatrickHand-Regular.ttf',
    'Mali-Bold.ttf': 'mali/Mali-Bold.ttf', 'Comfortaa.ttf': 'comfortaa/Comfortaa%5Bwght%5D.ttf',
    'BeVietnamPro-ExtraBold.ttf': 'bevietnampro/BeVietnamPro-ExtraBold.ttf',
    'DancingScript.ttf': 'dancingscript/DancingScript%5Bwght%5D.ttf', 'Lemonada.ttf': 'lemonada/Lemonada%5Bwght%5D.ttf',
    'Nunito.ttf': 'nunito/Nunito%5Bwght%5D.ttf', 'PlaypenSans.ttf': 'playpensans/PlaypenSans%5Bwght%5D.ttf',
    'Grandstander.ttf': 'grandstander/Grandstander%5Bwght%5D.ttf', 'Itim.ttf': 'itim/Itim-Regular.ttf',
    'Sriracha.ttf': 'sriracha/Sriracha-Regular.ttf', 'Pattaya.ttf': 'pattaya/Pattaya-Regular.ttf',
    'ChakraPetch-Bold.ttf': 'chakrapetch/ChakraPetch-Bold.ttf', 'Oswald.ttf': 'oswald/Oswald%5Bwght%5D.ttf',
}


def ensure_fonts():
    os.makedirs(FONT_DIR, exist_ok=True)
    for name, path in FONTS.items():
        dest = os.path.join(FONT_DIR, name)
        if os.path.exists(dest) and os.path.getsize(dest) > 10000:
            continue
        for _ in range(3):
            try:
                data = requests.get(GF + path, timeout=60).content
                if len(data) > 10000:
                    open(dest, 'wb').write(data); break
            except Exception as e:
                print('Tải phông lỗi', name, e); time.sleep(2)


_fc = {}


def font(name, size, weight=None):
    k = (name, size, weight)
    if k in _fc: return _fc[k]
    f = ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    if weight:
        try: f.set_variation_by_axes([weight])
        except Exception: pass
    _fc[k] = f
    return f


# ---------------------------------------------------------------- 17 giao diện (mỗi tin một kiểu chữ + màu khác nhau)
# (tên phông, độ đậm, nền trên, nền dưới, màu khung, màu chữ, màu nhấn, bộ biểu tượng nền)
THEMES = [
    ('Pacifico.ttf', None, '#FFD54A', '#FF8A3D', '#FFF9E6', '#5B2A00', '#D6336C', '😂🌞🍋'),
    ('Baloo2.ttf', 700, '#7EE8C7', '#2BB6D9', '#F1FFFB', '#063B4A', '#0B7285', '🤣🐬🌊'),
    ('Lobster.ttf', None, '#FF9ECF', '#9B5DE5', '#FFF0FA', '#4A1259', '#C2185B', '😆🦄🎀'),
    ('Mali-Bold.ttf', None, '#C6F36B', '#2BAE66', '#F7FFE8', '#164B1E', '#E8590C', '😄🍀🐸'),
    ('Comfortaa.ttf', 700, '#4FACFE', '#00F2FE', '#F0FBFF', '#0B3C5D', '#E67700', '😁☁️🎈'),
    ('BeVietnamPro-ExtraBold.ttf', None, '#FF6A88', '#FFB347', '#FFF5EE', '#4A1C1C', '#1971C2', '🤪🍉🌴'),
    ('DancingScript.ttf', 700, '#CBB2FF', '#7AA2FF', '#F7F3FF', '#2B1B5A', '#D6336C', '😹🌈💜'),
    ('Lemonada.ttf', 700, '#FF9966', '#FF5E62', '#FFF7F0', '#4D1F10', '#0B7285', '😂🍊🔥'),
    ('Nunito.ttf', 800, '#89F7FE', '#66A6FF', '#FFFFFF', '#12355B', '#D9480F', '😆🐳⭐'),
    ('PlaypenSans.ttf', 700, '#FFF176', '#FFB74D', '#FFFDE7', '#3E2723', '#AD1457', '🤣🍌🐥'),
    ('Grandstander.ttf', 800, '#B388FF', '#FF80AB', '#FFF3FB', '#311B92', '#E8590C', '😝🍇🎉'),
    ('PatrickHand.ttf', None, '#1E1B4B', '#4338CA', '#FFFDF2', '#1E1B4B', '#F59F00', '😂🌙✨'),
    ('Itim.ttf', None, '#FFDEE9', '#B5FFFC', '#FFFFFF', '#3B2F63', '#E64980', '😊🍭🧁'),
    ('Sriracha.ttf', None, '#F857A6', '#FF5858', '#FFF5F7', '#4B0F23', '#1C7ED6', '🤭🍒💖'),
    ('Pattaya.ttf', None, '#11998E', '#38EF7D', '#F3FFF8', '#04362F', '#D6336C', '😄🌿🦜'),
    ('ChakraPetch-Bold.ttf', None, '#0F2027', '#2C5364', '#F5FBFF', '#0B2530', '#E8590C', '😆🚀🤖'),
    ('Oswald.ttf', 600, '#43E97B', '#38F9D7', '#F2FFF9', '#073B3A', '#C2255C', '😁🥑🏄'),
]
TAGFONT = 'BeVietnamPro-ExtraBold.ttf'
LAUGH_EMOJI = '😂🤣😆😹😄'
THINK_EMOJI = '🧩🤔💡🧠'
EXTRA_EMOJI = '🎉✨🌈🍀😜🎈🥳💥'


def hexrgb(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(c): return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


# ---------------------------------------------------------------- biểu tượng cảm xúc (Noto Color Emoji)
EMOJI_FONT = None
for _p in ('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', '/usr/share/fonts/noto/NotoColorEmoji.ttf'):
    if os.path.exists(_p): EMOJI_FONT = _p
_ec = {}


def emoji_img(ch, size):
    if not EMOJI_FONT: return None
    key = (ch, size)
    if key in _ec: return _ec[key]
    try:
        f = ImageFont.truetype(EMOJI_FONT, 109)
        im = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
        bb = im.getbbox()
        if not bb: return None
        im = im.crop(bb)
        s = size / max(im.size)
        im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
    except Exception as e:
        print('Emoji lỗi', ch, e); im = None
    _ec[key] = im
    return im


def paste_emoji(canvas, ch, cx, cy, size, rot=0, alpha=1.0):
    im = emoji_img(ch, size)
    if im is None: return
    if rot: im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    if alpha < 1:
        a = im.getchannel('A').point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    canvas.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


# ---------------------------------------------------------------- vẽ chữ
def wrap(text, f, maxw):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if f.getlength(t) <= maxw or not cur: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines


def lh(f): a, d = f.getmetrics(); return int((a + d) * 1.08)


def fit_block(vi, en, fname, weight, w, h, gap=26):
    for s in range(70, 28, -2):
        fv, fe = font(fname, s, weight), font(fname, int(s * 0.72), weight)
        lv, le = wrap(vi, fv, w), wrap(en, fe, w)
        tot = len(lv) * lh(fv) + gap + len(le) * lh(fe)
        if tot <= h and max(fv.getlength(x) for x in lv) <= w: break
    return fv, fe, lv, le, tot, gap


def draw_lines(d, lines, f, cx, y, fill):
    for ln in lines:
        d.text((cx - f.getlength(ln) / 2, y), ln, font=f, fill=fill); y += lh(f)
    return y


def panel_layer(x, y, w, h, fill, accent, tag_text, tag_emoji, vi, en, th, rng):
    """Một khung nội dung (RGBA toàn màn hình) gồm bóng, khung, nhãn, chữ Việt + Anh."""
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x + 6, y + 14, x + w + 6, y + h + 14), 54, fill=(0, 0, 0, 90))
    layer.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((x, y, x + w, y + h), 54, fill=hexrgb(fill) + (245,), outline=hexrgb(accent), width=7)
    # nhãn
    tf = font(TAGFONT, 34)
    tw = tf.getlength(tag_text) + 120
    tx = x + (w - tw) / 2
    d.rounded_rectangle((tx, y - 36, tx + tw, y + 36), 36, fill=hexrgb(accent))
    d.text((tx + 84, y - 22), tag_text, font=tf, fill=(255, 255, 255))
    paste_emoji(layer, tag_emoji, tx + 46, y, 56)
    # chữ
    fname, weight = th[0], th[1]
    ink, ink2 = hexrgb(th[5]), hexrgb(th[6])
    area_y, area_h = y + 70, h - 100
    fv, fe, lv, le, tot, gap = fit_block(vi, en, fname, weight, w - 110, area_h)
    cy = area_y + (area_h - tot) / 2
    d = ImageDraw.Draw(layer)
    cy = draw_lines(d, lv, fv, x + w / 2, cy, ink)
    cy += gap
    draw_lines(d, le, fe, x + w / 2, cy, ink2)
    return layer


def render_frame(th, quote, riddle, counter, active, count=None):
    """active: 'quote' | 'riddle' | 'cta' (một slide, chỉ đổi phần nổi bật)."""
    rng = random.Random(counter * 7919 + 13)
    top, bot = hexrgb(th[2]), hexrgb(th[3])
    ys = np.linspace(0, 1, H)[:, None, None]
    arr = (np.array(top)[None, None, :] * (1 - ys) + np.array(bot)[None, None, :] * ys)
    arr = np.repeat(arr, W, axis=1).astype(np.uint8)
    img = Image.fromarray(arr, 'RGB').convert('RGBA')
    dark = lum(top) < 110
    # hoạ tiết biểu tượng nền
    for i, ch in enumerate(th[7] * 12):
        pass
    emos = [c for c in th[7] if not c.isspace()]
    gx, gy = 220, 240
    for r in range(-1, H // gy + 2):
        for c in range(-1, W // gx + 2):
            e = emos[(r * 3 + c) % len(emos)]
            ox = (gx // 2 if r % 2 else 0)
            paste_emoji(img, e, c * gx + ox + 30, r * gy + 40, 78, rot=((r * 5 + c * 3) % 5 - 2) * 9, alpha=0.20)
    # biểu tượng lớn ngẫu nhiên (cười vui) - chỉ ở vùng trống phía dưới
    spots = [(110, 1835), (970, 1835), (540, 1855)]
    for (sx, sy) in (spots[:2] if count is not None else spots):
        paste_emoji(img, rng.choice(LAUGH_EMOJI + EXTRA_EMOJI), sx, sy, rng.randint(120, 170), rot=rng.randint(-25, 25))
    d = ImageDraw.Draw(img)
    tcol = (255, 255, 255) if dark else hexrgb(th[5])
    # tiêu đề (tự thu nhỏ cho vừa), hai biểu tượng cười hai bên
    title = 'Sống vui mỗi ngày'
    for sz in range(84, 40, -2):
        ft = font(th[0], sz, th[1])
        if ft.getlength(title) <= 700: break
    d.text((W / 2 - ft.getlength(title) / 2, 70), title, font=ft, fill=tcol)
    fs = font(TAGFONT, 32); sub = 'Live happy · Laugh every day'
    d.text((W / 2 - fs.getlength(sub) / 2, 70 + lh(ft) + 6), sub, font=fs, fill=tcol)
    paste_emoji(img, rng.choice(LAUGH_EMOJI), 105, 150, 110, rot=-12)
    paste_emoji(img, rng.choice(LAUGH_EMOJI), 975, 150, 110, rot=12)
    # hai khung
    qx, qw = 60, W - 120
    rlayer = panel_layer(qx, 330, qw, 560, th[4], th[6], 'ĐỐ VUI · RIDDLE', rng.choice(THINK_EMOJI),
                         riddle['vi_q'], riddle['en_q'], th, rng)
    qlayer = panel_layer(qx, 980, qw, 560, th[4], th[6], 'CÂU NÓI VUI · FUNNY QUOTE', rng.choice(LAUGH_EMOJI),
                         quote['vi'], quote['en'], th, rng)
    def dim(layer, a):
        if a >= 1: return layer
        l = layer.copy(); l.putalpha(layer.getchannel('A').point(lambda v: int(v * a))); return l
    img.alpha_composite(dim(qlayer, 1.0 if active in ('quote', 'cta') else 0.40))
    img.alpha_composite(dim(rlayer, 1.0 if active in ('riddle', 'cta') else 0.40))
    # băng chữ cuối
    by = 1590
    banner = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(banner)
    bd.rounded_rectangle((90, by, W - 90, by + 150), 60, fill=hexrgb(th[6]) + (255,))
    f1, f2 = font(TAGFONT, 44), font(TAGFONT, 34)
    t1, t2 = '💬 Bình luận đáp án của bạn nhé!', 'Comment your answer · Đáp án có ở tin sau'
    t1 = t1.replace('💬 ', '')
    bd.text((W / 2 - f1.getlength(t1) / 2 + 30, by + 28), t1, font=f1, fill=(255, 255, 255))
    bd.text((W / 2 - f2.getlength(t2) / 2, by + 90), t2, font=f2, fill=(255, 255, 255))
    paste_emoji(banner, '💬', W / 2 - f1.getlength(t1) / 2 - 18, by + 52, 58)
    if count is None:
        img.alpha_composite(dim(banner, 1.0 if active == 'cta' else 0.55))
    else:  # đếm ngược 5 → 1 giây: giữ người xem đến hết
        cl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cd = ImageDraw.Draw(cl)
        cx, cy, R = W // 2, 1665, 105
        cd.ellipse((cx - R - 14, cy - R - 14, cx + R + 14, cy + R + 14), fill=(255, 255, 255, 235))
        cd.ellipse((cx - R, cy - R, cx + R, cy + R), fill=hexrgb(th[6]) + (255,))
        fnum = font(th[0], 150, th[1]); ns = str(count)
        cd.text((cx - fnum.getlength(ns) / 2, cy - lh(fnum) / 2 - 6), ns, font=fnum, fill=(255, 255, 255))
        fq = font(TAGFONT, 36); tq = 'Đoán nhanh! · Quick, guess!'
        cd.text((cx - fq.getlength(tq) / 2, cy + R + 28), tq, font=fq, fill=tcol)
        img.alpha_composite(cl)
    return img.convert('RGB')


# ---------------------------------------------------------------- âm thanh
SR = 44100


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


# Tiếng cười THẬT của trẻ em (BigSoundBank, giấy phép CC0 - miễn phí, không cần ghi nguồn).
LAUGH_IDS = ['0980']  # Laughing Boy of 16 Months - tiếng cười nhẹ nhàng
def fetch_laughs(dest):
    """Tải mẫu tiếng cười thật (chạy được trên GitHub Actions). Lỗi mạng -> bỏ qua, dùng tiếng cười tổng hợp."""
    try:
        import requests
        os.makedirs(dest, exist_ok=True)
        for i in LAUGH_IDS:
            f = os.path.join(dest, f'bsb_{i}.mp3')
            if os.path.exists(f) and os.path.getsize(f) > 5000:
                continue
            try:
                r = requests.get(f'https://bigsoundbank.com/UPLOAD/mp3/{i}.mp3', timeout=25,
                                 headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://bigsoundbank.com/'})
                if r.status_code == 200 and len(r.content) > 5000 and r.content[:3] in (b'ID3', b'\xff\xfb', b'\xff\xf3', b'\xff\xf2'):
                    open(f, 'wb').write(r.content)
                else:
                    print('laugh', i, 'bỏ qua', r.status_code, len(r.content))
            except Exception as e:
                print('laugh', i, 'lỗi', e)
    except Exception as e:
        print('fetch_laughs lỗi', e)

def synth_laugh(seed):
    """Tiếng cười 'ha ha ha' tổng hợp (không dính bản quyền): nhiều đợt hơi, cao độ giảm dần, lọc nguyên âm /a/."""
    rng = np.random.default_rng(seed)
    f0_base = float(rng.choice([205, 235, 300, 330]))
    n = int(rng.integers(7, 11))
    total = np.zeros(int(SR * 3.4))
    t_cur = 0.05
    for i in range(n):
        dur = 0.15 + 0.03 * rng.random()
        L = int(SR * dur)
        t = np.arange(L) / SR
        f0 = f0_base * (1.28 - 0.05 * i) * (1 + 0.04 * rng.standard_normal())
        f0 = f0 * (1 + 0.10 * np.exp(-t * 14))  # nhấn đầu tiếng
        ph = 2 * np.pi * np.cumsum(f0) / SR
        src = sum(np.sin(k * ph) / k ** 0.9 for k in range(1, 28))
        src += 0.55 * rng.standard_normal(L) * 0.35  # hơi thở
        spec = np.fft.rfft(src)
        fr = np.fft.rfftfreq(L, 1 / SR)
        shape = lambda c, bw, g: g * np.exp(-0.5 * ((fr - c) / bw) ** 2)
        F1, F2 = 780 + 40 * rng.random(), 1250 + 90 * rng.random()
        H_ = shape(F1, 130, 1.0) + shape(F2, 200, 0.7) + shape(2650, 350, 0.35) + 0.03
        y = np.fft.irfft(spec * H_, L)
        env = np.minimum(1, t / 0.012) * np.exp(-t * 11) * (0.95 ** i)
        y = y * env
        y = y / (np.max(np.abs(y)) + 1e-9) * (0.9 - 0.04 * i)
        s = int(t_cur * SR)
        e = min(len(total), s + L)
        total[s:e] += y[:e - s]
        t_cur += 0.205 + 0.01 * i * 0.3 + 0.02 * rng.random()
        if t_cur * SR + L >= len(total): break
    end = int(min(len(total), (t_cur + 0.25) * SR))
    total = total[:end]
    # lớp thứ hai lệch nhẹ để thành "nhóm người cười"
    shift = int(0.035 * SR)
    mix = total.copy(); mix[shift:] += 0.55 * total[:-shift]
    mix = np.tanh(mix * 1.1)
    mix /= (np.max(np.abs(mix)) + 1e-9)
    fade = int(0.12 * SR); mix[-fade:] *= np.linspace(1, 0, fade)
    return mix * 0.85


def synth_ticks(sec):
    out = np.zeros(int(SR * sec))
    k = 0
    t = 0.12
    while t < sec - 0.1:
        f = 1900 if k % 2 == 0 else 1350
        L = int(SR * 0.045); tt = np.arange(L) / SR
        c = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 90) * 0.5
        s = int(t * SR); out[s:s + L] += c[:len(out) - s]
        t += 0.5; k += 1
    for sec_i in range(int(sec)):  # nhấn mạnh nhịp mỗi giây
        s0 = int(sec_i * SR); L = int(SR * 0.09); tt = np.arange(L) / SR
        b = np.sin(2 * np.pi * 880 * tt) * np.exp(-tt * 45) * 0.45
        out[s0:s0 + L] += b[:len(out) - s0]
    return out


def silence(sec): return np.zeros(int(SR * sec))


def read_wav(path):
    with wave.open(path, 'rb') as w:
        n = w.getnframes(); raw = w.readframes(n)
        return np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32767.0


def to_wav(src, dst):
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-ar', str(SR), '-ac', '1', dst])


VI_VOICES = ['vi-VN-HoaiMyNeural', 'vi-VN-NamMinhNeural']
EN_VOICES = ['en-US-AriaNeural', 'en-US-GuyNeural', 'en-US-JennyNeural', 'en-US-AndrewNeural', 'en-GB-SoniaNeural', 'en-AU-NatashaNeural']


def tts(text, voice, rate, out_wav, tag):
    text = ' '.join(text.replace('…', '...').split())
    if not text or text in ('Riddle time!',):
        write_wav(out_wav, np.zeros(int(SR * 0.1))); return
    if DRY_TTS:
        n = max(1.2, len(text) / 14.0)
        write_wav(out_wav, np.zeros(int(SR * n))); return
    import edge_tts
    mp3 = f'{WORK}/{tag}.mp3'
    last = None
    for k in range(4):
        try:
            asyncio.run(edge_tts.Communicate(text, voice, rate=rate).save(mp3))
            if os.path.getsize(mp3) > 1000:
                to_wav(mp3, out_wav); return
        except Exception as e:
            last = e; print('TTS lỗi', tag, k, e); time.sleep(2 + k * 2)
    raise RuntimeError(f'TTS thất bại ({tag}): {last}')


# ---------------------------------------------------------------- trạng thái + chọn nội dung
def load_state():
    try: return json.load(open(STATE_PATH, encoding='utf8'))
    except Exception: return {'counter': 0, 'last_time': 0, 'pending': [], 'history': []}


def save_state(st):
    json.dump(st, open(STATE_PATH, 'w', encoding='utf8'), ensure_ascii=False, indent=1)


def pick(lst, counter, salt):
    n = len(lst); cyc, i = divmod(counter, n)
    order = list(range(n)); random.Random(salt * 1000003 + cyc).shuffle(order)
    return lst[order[i]]


def main():
    ensure_fonts()
    data = json.load(open(os.path.join(ROOT, 'data', 'content.json'), encoding='utf8'))
    st = load_state()
    c = int(os.environ.get('COUNTER') or st.get('counter', 0))
    now = time.time()
    if not PREVIEW and not FORCE and now - float(st.get('last_time', 0)) < 40 * 60:
        print('Vừa đăng cách đây dưới 40 phút, bỏ qua (dùng force để ép).'); return
    if P.get('quote_vi') and P.get('r_vq'):  # nội dung do Apps Script chọn từ Google Sheet
        ids = str(P.get('ids') or 'sheet/sheet').split('/')
        quote = {'id': ids[0], 'vi': str(P['quote_vi']).strip(), 'en': str(P.get('quote_en') or '').strip()}
        riddle = {'id': ids[-1], 'vi_q': str(P['r_vq']).strip(), 'vi_a': str(P.get('r_va') or '').strip(),
                  'en_q': str(P.get('r_eq') or '').strip(), 'en_a': str(P.get('r_ea') or '').strip()}
    else:
        quote = pick(data['quotes'], c, 11)
        riddle = pick(data['riddles'], c, 29)
    th = THEMES[(c * 5) % len(THEMES)]
    vi_voice = VI_VOICES[c % 2]
    en_voice = EN_VOICES[(c * 5 + 1) % len(EN_VOICES)]
    print('Tin số', c, quote['id'], riddle['id'], 'phông', th[0], vi_voice, en_voice)

    # 1) giọng đọc + tiếng cười
    segs = [('qv', quote['vi'], vi_voice, '+0%'), ('qe', quote['en'], en_voice, '+0%')]
    wavs = {}
    for tag, text, voice, rate in segs:
        p = f'{WORK}/{tag}.wav'; tts(text, voice, rate, p, tag); wavs[tag] = read_wav(p)
    laugh_dir = os.path.join(ROOT, 'assets', 'laugh')
    fetch_laughs(laugh_dir)
    custom = [os.path.join(laugh_dir, f) for f in sorted(os.listdir(laugh_dir))] if os.path.isdir(laugh_dir) else []
    custom = [f for f in custom if f.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg'))]
    def get_laugh(k, maxsec, start=0.0):
        if custom:
            src = custom[k % len(custom)]; to_wav(src, f'{WORK}/laugh{k}.wav'); lg = read_wav(f'{WORK}/laugh{k}.wav')[int(SR * start):int(SR * (start + maxsec))]
            n = min(len(lg), int(SR * 0.15)); lg = lg.copy(); lg[-n:] *= np.linspace(1, 0, n); lg[:n] *= np.linspace(0, 1, n)
            return lg / (np.max(np.abs(lg)) + 1e-9) * 0.75
        return synth_laugh(k + 5)
    laugh1 = get_laugh(c, 3.0)       # cười sau câu nói tiếng Việt
    laugh2 = get_laugh(c + 3, 2.5, 3.0 if custom and len(custom) == 1 else 0.0)   # cười sau câu nói tiếng Anh
    for tag, text, voice, rate in [
        ('rv', riddle['vi_q'], vi_voice, '+0%'),
        ('re', riddle['en_q'], en_voice, '+0%'),
        ('cv', 'Bình luận đáp án nhé!', vi_voice, '+5%'),
        ('ce', 'Comment your answer!', en_voice, '+5%')]:
        p = f'{WORK}/{tag}.wav'; tts(text, voice, rate, p, tag); wavs[tag] = read_wav(p)
    parts, t = [], 0.0
    def add(x, name=None):
        nonlocal t
        parts.append(x); t += len(x) / SR
    # câu đố lên trước, đếm ngược 5 giây, rồi câu nói vui kèm tiếng cười, cuối cùng là lời kêu gọi bình luận
    add(silence(0.3)); add(wavs['rv']); add(silence(0.25)); add(wavs['re']); add(silence(0.2))
    t_read = t
    add(synth_ticks(5.0))
    t_count_end = t
    add(silence(0.2))
    add(wavs['qv']); add(silence(0.2)); add(laugh1); add(silence(0.25))
    add(wavs['qe']); add(silence(0.2)); add(laugh2); add(silence(0.3))
    t_cta = t
    add(wavs['cv']); add(silence(0.25)); add(wavs['ce']); add(silence(0.7))
    audio = np.concatenate(parts)
    write_wav(f'{WORK}/audio.wav', audio)
    total = t
    durs = [t_read, 1.0, 1.0, 1.0, 1.0, 1.0, t_cta - t_count_end, total - t_cta]
    print('Thời lượng', [round(x, 1) for x in durs], 'tổng', round(total, 1))

    # 2) khung hình: một slide, ba trạng thái nhấn
    imgs = []
    plan = [('riddle', None), ('riddle', 5), ('riddle', 4), ('riddle', 3), ('riddle', 2), ('riddle', 1), ('quote', None), ('cta', None)]
    for i, (act, cn) in enumerate(plan):
        im = render_frame(th, quote, riddle, c, act, cn); p = f'{WORK}/f{i}.png'; im.save(p); imgs.append(p)
    if os.environ.get('SAVE_FRAMES'):
        for i, p in enumerate(imgs): Image.open(p).save(os.path.join(os.environ['SAVE_FRAMES'], f'frame{i}.png'))
    segs_v = []
    for i, p in enumerate(imgs):
        s = f'{WORK}/s{i}.mp4'; n = int(durs[i] * 30)
        vf = f"scale=1188:2112,zoompan=z='min(zoom+0.0004,1.04)':d={n}:s=1080x1920:fps=30,format=yuv420p"
        subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', p, '-vf', vf, '-t', f'{durs[i]:.2f}',
                               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22', s])
        segs_v.append(s)
    open(f'{WORK}/list.txt', 'w').write(''.join(f"file '{s}'\n" for s in segs_v))
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{WORK}/list.txt', '-c', 'copy', f'{WORK}/video.mp4'])
    out = f'{WORK}/final.mp4'
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{WORK}/video.mp4', '-i', f'{WORK}/audio.wav',
                           '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', out])
    print('Đã dựng', out, os.path.getsize(out) // 1024, 'KB')

    hooks = [
        ("⏱️ Thử thách 5 giây: bạn đoán ra câu đố này không?",
         "5-second challenge: can you solve this riddle?"),
        ("🤔 Nghe thì dễ, nhưng nhiều người nghĩ mãi! Bạn thì sao?",
         "Sounds easy, but it trips up a lot of people! How about you?"),
        ("😄 Bạn đoán nhanh cỡ nào? Thử ngay trong 5 giây!",
         "How fast can you guess? Try it in 5 seconds!"),
        ("🧠 Đố bạn trả lời được ngay! Gõ đáp án xuống bình luận nhé.",
         "Bet you can solve it! Type your answer in the comments."),
        ("🔥 Ai đoán đúng đầu tiên nào? Đáp án bên dưới video sau!",
         "Who gets it right first? The answer comes in the next video!"),
    ]
    h_vi, h_en = hooks[c % len(hooks)]
    caption = (f"{h_vi}\n{h_en}\n\n"
               f"🧩 ĐỐ VUI / RIDDLE:\n{riddle['vi_q']}\n{riddle['en_q']}\n\n"
               f"💬 Bình luận đáp án ngay nhé! Đáp án sẽ có ở video tiếp theo.\n"
               f"💬 Comment your answer below! The answer will be in the next video.\n\n"
               f"#SongVuiMoiNgay #CauDoVui #Riddle #FunnyQuotes #BilingualVietnameseEnglish")
    open(f'{WORK}/caption.txt', 'w', encoding='utf8').write(caption)
    if PREVIEW:
        print('PREVIEW: không đăng, không đổi trạng thái.'); return
    if not (PAGE_ID and TOKEN):
        sys.exit('Thiếu page_id hoặc secret FB_PAGE_TOKEN_SVMN')

    # 3) đăng Reel
    r = requests.post(f'{GV}/{PAGE_ID}/video_reels', data={'upload_phase': 'start', 'access_token': TOKEN}, timeout=60)
    print(r.status_code, r.text[:300]); r.raise_for_status()
    vid, up = r.json()['video_id'], r.json()['upload_url']
    size = os.path.getsize(out)
    with open(out, 'rb') as fh:
        u = requests.post(up, headers={'Authorization': 'OAuth ' + TOKEN, 'offset': '0', 'file_size': str(size)}, data=fh, timeout=600)
    print(u.status_code, u.text[:200]); u.raise_for_status()
    fin = requests.post(f'{GV}/{PAGE_ID}/video_reels', data={'upload_phase': 'finish', 'video_id': vid, 'access_token': TOKEN,
                        'video_state': 'PUBLISHED', 'description': caption}, timeout=120)
    print(fin.status_code, fin.text[:300]); fin.raise_for_status()
    post_id = (fin.json() or {}).get('post_id') or ''
    for _ in range(12):
        s = requests.get(f'{GV}/{vid}', params={'fields': 'status', 'access_token': TOKEN}, timeout=30).json()
        print(s)
        if (s.get('status') or {}).get('video_status') in ('ready', 'error'): break
        time.sleep(10)

    # 4) cập nhật trạng thái NGAY (tránh đăng trùng nếu bước sau lỗi), rồi bình luận đáp án của tin trước
    heads = ['✅ ĐÁP ÁN / ANSWER', '💡 Đáp án đây rồi! / Here is the answer!', '🎯 Bạn đoán đúng chưa? / Did you get it?',
             '🔎 Cùng xem đáp án nhé! / Let us check the answer!']
    answer_text = (heads[c % len(heads)] + '\n'
                   f"❓ {riddle['vi_q']}\n👉 {riddle['vi_a']}\n\n"
                   f"❓ {riddle['en_q']}\n👉 {riddle['en_a']}")
    pend = list(st.get('pending', []))
    st['counter'] = c + 1; st['last_time'] = now
    st['history'] = (st.get('history', []) + [{'n': c, 'q': quote['id'], 'r': riddle['id'], 'post': post_id, 'video': vid,
                                               't': time.strftime('%Y-%m-%d %H:%M', time.gmtime(now))}])[-60:]
    st['pending'] = pend
    save_state(st)
    new_pending = []
    for item in pend:
        ok = False
        for target in dict.fromkeys([x for x in (item.get('post'), item.get('video')) if x]):
            try:
                cm = requests.post(f'{GV}/{target}/comments', data={'message': item['text'], 'access_token': TOKEN}, timeout=60)
                print('Bình luận đáp án', target, cm.status_code, cm.text[:200])
                if cm.ok: ok = True; break
            except Exception as e:
                print('Bình luận lỗi', e)
        if not ok:
            item['tries'] = item.get('tries', 0) + 1
            if item['tries'] < 6: new_pending.append(item)
    new_pending.append({'post': post_id, 'video': vid, 'text': answer_text, 'tries': 0})
    st['pending'] = new_pending[-8:]
    save_state(st)
    print('Xong tin', c)


if __name__ == '__main__':
    main()
