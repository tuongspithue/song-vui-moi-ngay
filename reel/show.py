"""Bản mới 'gameshow tí hon': Mèo Vui (tiếng Việt) + Robot Tây (tiếng Anh).
Ba loạt: KIND=meo (Mèo đố, Robot đoán sai) | odd (Tìm emoji khác biệt) | emoji (Đuổi hình bắt chữ).
Hiện chỉ DỰNG video xem thử (không đăng). Dùng lại phông, emoji, âm thanh của make.py."""
import os, sys, json, math, random, subprocess, asyncio, time
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make as M

W, H, FPS, SR, WORK = 1080, 1920, 30, M.SR, M.WORK
KIND = os.environ.get('KIND', 'meo')
C = int(os.environ.get('COUNTER', '0'))
KC = C  # số tin ĐÃ ĐĂNG của riêng loạt này (make.py truyền vào) - dùng để chọn nội dung lần lượt, không trùng khi đăng nhiều tin/ngày
CAT_VOICES = ['vi-VN-HoaiMyNeural', 'vi-VN-NamMinhNeural']
BOT_VOICES = ['en-US-GuyNeural', 'en-US-AndrewNeural', 'en-GB-SoniaNeural']
BOT_FONT = 'ChakraPetch-Bold.ttf'
BOT_FILL, BOT_FG, BOT_SUB = '#10243E', '#E6FBFF', '#7FE9FF'

THINK = 8.0  # số giây cho người xem suy nghĩ (Apps Script có thể gửi data.think để đổi)
GUESS_DEFAULT = ('Hmm... is it a banana?', 'Hừm… là quả chuối hả?')
KINDS = {  # mã: (tên Việt, tên Anh, câu Mèo hỏi)
    'TN': ('Thành ngữ', 'Vietnamese idiom', 'Đây là thành ngữ gì?'), 'TU': ('Tục ngữ', 'Vietnamese proverb', 'Đây là câu tục ngữ nào?'),
    'MA': ('Món ăn', 'Vietnamese food', 'Đây là món gì?'), 'DD': ('Địa danh', 'Place in Vietnam', 'Đây là nơi nào?'),
    'VH': ('Văn hoá', 'Vietnamese culture', 'Đây là gì?'), 'GC': ('Ghép chữ', 'Word puzzle', 'Ghép lại thành từ gì?'),
}
KIND_BY_NAME = {v[0].lower(): k for k, v in KINDS.items()}
ODD_PAIRS = [
    [('🍎', '🍅'), ('🌕', '🌝'), ('🍊', '🍑'), ('🐶', '🐺'), ('🐱', '🐯'), ('⚽', '🏐'), ('🌹', '🌷'), ('🍓', '🍒'), ('🐸', '🐢'), ('🌞', '🌻'),
     ('🐰', '🐭'), ('🦁', '🐯'), ('🍩', '🍪'), ('⭐', '🌟'), ('🐔', '🐤'), ('🍉', '🍈'), ('🚗', '🚕'), ('🎈', '🍎')],
    [('😄', '😁'), ('🙂', '🙃'), ('🐵', '🙈'), ('😉', '😜'), ('😎', '🤓'), ('😺', '😸'), ('🙈', '🙉'), ('😇', '😊'), ('😋', '😛'), ('😴', '😪'),
     ('🌛', '🌜'), ('🐼', '🐨'), ('😻', '😽'), ('😢', '😥'), ('🤗', '😊'), ('🐻', '🐹'), ('🍋', '🍐'), ('🌼', '🌻')],
    [('😮', '😯'), ('😀', '😃'), ('🕐', '🕑'), ('😃', '😄'), ('🌑', '🌚'), ('😐', '😑'), ('🙁', '😕'), ('😦', '😧'), ('🕒', '🕓'), ('😬', '😁'),
     ('😌', '😔'), ('😆', '😝'), ('🌓', '🌔'), ('😲', '😮'), ('🕕', '🕖'), ('😗', '😙'), ('🌖', '🌕'), ('😊', '☺')],
]


SCHEDULE = [(6, 30, 'odd'), (8, 30, 'tienganh'), (10, 15, 'emoji'), (11, 45, 'meo'), (14, 0, 'quyluat'), (16, 30, 'dungsai'), (19, 30, 'meo'), (21, 30, 'emoji')]  # giờ VN, khớp CFG.TIMES/KINDS trong Apps Script
KIND_VI = {'thu': 'Thử thách mới', 'odd': 'Tìm emoji khác biệt', 'meo': 'Mèo đố', 'emoji': 'Đuổi hình bắt chữ', 'tienganh': '10 giây tiếng Anh', 'quyluat': 'Quy luật nào đây', 'dungsai': 'Đúng hay sai'}


def teaser():
    """Hẹn tập kế tiếp theo lịch thật: (giờ, tên loạt)."""
    t = time.gmtime(time.time() + 7 * 3600); now = t.tm_hour * 60 + t.tm_min
    for h, m, k in SCHEDULE:
        if h * 60 + m > now + 20: return f"{h}:{m:02d}", KIND_VI[k]
    h, m, k = SCHEDULE[0]; return f"{h}:{m:02d} mai", KIND_VI[k]


def load_v2(): return json.load(open(os.path.join(M.ROOT, 'data', 'content_v2.json'), encoding='utf8'))


def truthy(v): return str(v).strip().lower() in ('1', 'true', 'yes', 'x', 'có')


# ------------------------------------------------------------------ âm thanh
def norm(x, peak=0.85):
    m = float(np.max(np.abs(x))) if len(x) else 0
    return x / m * peak if m > 1e-6 else x


def trim(x, thr=0.012):
    idx = np.where(np.abs(x) > thr)[0]
    if len(idx) == 0: return x
    return x[max(0, idx[0] - 400):min(len(x), idx[-1] + 2500)]


def say(text, voices, tag, rate='+0%', pitch='+0Hz', robot=False):
    """Đọc bằng edge-tts; lỗi thì thử giọng dự phòng (không bỏ tin)."""
    text = ' '.join(text.replace('…', '...').split())
    if M.DRY_TTS:
        return np.zeros(int(SR * max(0.9, len(text) / 15.0)))
    import edge_tts
    mp3, wav, last = f'{WORK}/{tag}.mp3', f'{WORK}/{tag}.wav', None
    for k in range(6):
        v = voices[(k // 2) % len(voices)]
        try:
            asyncio.run(edge_tts.Communicate(text, v, rate=rate, pitch=pitch).save(mp3))
            if os.path.getsize(mp3) > 1000:
                M.to_wav(mp3, wav); x = trim(M.read_wav(wav)); break
        except Exception as e:
            last = e; print('TTS lỗi', tag, v, e); time.sleep(2 + k)
    else:
        raise RuntimeError(f'TTS thất bại ({tag}): {last}')
    if robot:  # giọng hơi "máy"
        t = np.arange(len(x)) / SR
        x = 0.62 * x + 0.38 * x * np.sin(2 * np.pi * 72 * t)
    return norm(x)


def _t(d): return np.arange(int(SR * d)) / SR


def sfx_pop():
    t = _t(0.09); f = 420 + 5200 * t
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 38) * 0.5


def sfx_ting():
    t = _t(1.0)
    return sum(a * np.sin(2 * np.pi * f * t) for f, a in ((1318.5, .5), (1975.5, .3), (2637, .2))) * np.exp(-t * 5) * 0.55


def sfx_win():
    out = np.zeros(int(SR * 0.9))
    for i, f in enumerate((523.25, 659.25, 783.99, 1046.5)):
        t = _t(0.5); n = np.sin(2 * np.pi * f * t) * np.exp(-t * 7) * 0.32
        s = int(SR * 0.085 * i); out[s:s + len(n)] += n[:len(out) - s]
    return out


def sfx_buzz():
    t = _t(0.42)
    x = sum(np.sin(2 * np.pi * 138 * k * t) / k for k in (1, 3, 5, 7))
    return x * np.minimum(1, (0.42 - t) * 30) * np.minimum(1, t * 60) * 0.22


def sfx_whoosh():
    t = _t(0.3); n = np.random.default_rng(3).standard_normal(len(t))
    n = np.convolve(n, np.ones(24) / 24, 'same')
    return n * np.sin(np.pi * t / 0.3) ** 2 * 0.9


def get_laugh(k, maxsec):
    d = os.path.join(M.ROOT, 'assets', 'laugh'); M.fetch_laughs(d)
    fs = [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg'))] if os.path.isdir(d) else []
    if fs:
        M.to_wav(fs[k % len(fs)], f'{WORK}/laugh.wav'); lg = M.read_wav(f'{WORK}/laugh.wav')[:int(SR * maxsec)].copy()
        n = min(len(lg), int(SR * 0.2)); lg[-n:] *= np.linspace(1, 0, n)
        print('Tiếng cười: tệp thật', os.path.basename(fs[k % len(fs)])); return norm(lg, 0.75)
    print('Tiếng cười: tổng hợp (không tải được tệp thật)')
    return M.synth_laugh(k + 5)[:int(SR * maxsec)]


class Track:
    def __init__(self): self.items, self.speak = [], {'cat': [], 'bot': []}
    def put(self, x, at, who=None):
        self.items.append((at, x, who))
        if who: self.speak[who].append((at, at + len(x) / SR))
        return at + len(x) / SR
    def mix(self, total):
        out = np.zeros(int(SR * total) + SR); env = {}
        for who in ('cat', 'bot'):
            tr = np.zeros_like(out)
            for at, x, w in self.items:
                if w == who: s = int(at * SR); tr[s:s + len(x)] += x[:len(tr) - s]
            n = int(total * FPS) + 2; step = SR // FPS
            e = np.array([np.sqrt(np.mean(tr[i * step:(i + 1) * step] ** 2) + 1e-12) for i in range(n)])
            e = e / e.max() if e.max() > 1e-4 else None
            env[who] = e
        for at, x, w in self.items:
            s = int(at * SR); out[s:s + len(x)] += x[:len(out) - s]
        return np.clip(out[:int(SR * total)], -1, 1), env


# ------------------------------------------------------------------ hình
def ease_back(p):
    p = min(1, max(0, p)); return 1 + 2.70158 * (p - 1) ** 3 + 1.70158 * (p - 1) ** 2


def ease(p): p = min(1, max(0, p)); return 1 - (1 - p) ** 3


def gradient(c1, c2):
    a, b = np.array(M.hexrgb(c1), float), np.array(M.hexrgb(c2), float)
    t = np.linspace(0, 1, H)[:, None]
    col = (a * (1 - t) + b * t).astype(np.uint8)
    arr = np.repeat(col[:, None, :], W, axis=1)
    return Image.fromarray(np.dstack([arr, np.full((H, W), 255, np.uint8)]), 'RGBA')


def paste_c(canvas, im, cx, cy, scale=1.0, alpha=1.0):
    if scale <= 0.02 or alpha <= 0.02: return
    if abs(scale - 1) > 0.004:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if alpha < 0.995:
        im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * alpha)))
    canvas.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)),
                           ) if 0 <= cx - im.width / 2 and cx + im.width / 2 <= W and 0 <= cy - im.height / 2 and cy + im.height / 2 <= H else _paste_clip(canvas, im, cx, cy)


def _paste_clip(canvas, im, cx, cy):
    x, y = int(cx - im.width / 2), int(cy - im.height / 2)
    tmp = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); tmp.paste(im, (x, y)); canvas.alpha_composite(tmp)


def card(main, sub, fname, weight, fill, fg, subfg, w=940, maxh=620, tail=None, header=None, accent='#D6336C', top=None, max_size=88, sub_ratio=0.6):
    """Thẻ chữ bo góc (có bóng, có 'đuôi' chỉ về nhân vật đang nói). Trả về ảnh RGBA, tâm thẻ = tâm ảnh."""
    pad = 52; inner = w - 2 * pad
    hh = 70 if header else 0
    ft = M.font(M.TAGFONT, 34) if top else None
    lt = M.wrap(top, ft, inner) if top else []
    th_ = len(lt) * M.lh(ft) + 18 if top else 0
    for s in range(max_size, 30, -3):
        fm, fs = M.font(fname, s, weight), M.font(fname, max(26, int(s * sub_ratio)), weight)
        lm = M.wrap(main, fm, inner); ls = M.wrap(sub, fs, inner) if sub else []
        body = len(lm) * M.lh(fm) + ((20 + len(ls) * M.lh(fs)) if ls else 0)
        if body + hh + th_ + 2 * pad <= maxh and max(fm.getlength(x) for x in lm) <= inner: break
    h = body + hh + th_ + 2 * pad
    m, tl = 40, 56
    im = Image.new('RGBA', (w + 2 * m, h + 2 * (m + tl)), (0, 0, 0, 0))
    x0, y0 = m, m + tl
    def shape(d, dx, dy, col):
        d.rounded_rectangle((x0 + dx, y0 + dy, x0 + w + dx, y0 + h + dy), 54, fill=col)
        if tail:
            tx = x0 + (170 if tail == 'left' else w - 170) + dx
            d.polygon([(tx - 44, y0 + h + dy - 2), (tx + 44, y0 + h + dy - 2), (tx + (-60 if tail == 'left' else 60), y0 + h + tl + dy)], fill=col)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); shape(ImageDraw.Draw(sh), 0, 14, (0, 0, 0, 90))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(im); shape(d, 0, 0, fill)
    y = y0 + pad
    if header:
        fh = M.font(M.TAGFONT, 36); tw = fh.getlength(header)
        d.rounded_rectangle((x0 + w / 2 - tw / 2 - 30, y - 8, x0 + w / 2 + tw / 2 + 30, y + 50), 29, fill=accent)
        d.text((x0 + w / 2 - tw / 2, y - 2), header, font=fh, fill='#FFFFFF'); y += hh
    if top:
        y = M.draw_lines(d, lt, ft, x0 + w / 2, y, subfg) + 18
    y = M.draw_lines(d, lm, fm, x0 + w / 2, y, fg)
    if ls: M.draw_lines(d, ls, fs, x0 + w / 2, y + 20, subfg)
    return im


def pill(text, size, fill, fg, emoji=None, fname=None, weight=None):
    f = M.font(fname or M.TAGFONT, size, weight); tw = int(f.getlength(text)); e = int(size * 1.25) if emoji else 0
    w, h = tw + e + (16 if emoji else 0) + 2 * int(size * 0.8), int(size * 1.9)
    im = Image.new('RGBA', (w + 24, h + 28), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((12, 16, 12 + w, 16 + h), h // 2, fill=(0, 0, 0, 80))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    d = ImageDraw.Draw(im); d.rounded_rectangle((12, 8, 12 + w, 8 + h), h // 2, fill=fill)
    x = 12 + int(size * 0.8)
    if emoji: M.paste_emoji(im, emoji, x + e / 2, 8 + h / 2, e); x += e + 16
    a, dsc = f.getmetrics(); d.text((x, 8 + (h - a - dsc) / 2), text, font=f, fill=fg)
    return im


def ring(p, num, fg, bg, r=108):
    """Vòng đếm ngược: p = phần còn lại (1→0), num = số đang hiện."""
    S = 2; R = r * S; size = (R + 16 * S) * 2
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = size // 2
    d.ellipse((c - R, c - R, c + R, c + R), fill=bg)
    d.arc((c - R, c - R, c + R, c + R), -90, -90 + 360 * p, fill=fg, width=22 * S)
    im = im.resize((size // S, size // S), Image.LANCZOS)
    f = M.font(M.TAGFONT, 120); d = ImageDraw.Draw(im); t = str(num); tw = f.getlength(t); a, ds = f.getmetrics()
    d.text((im.width / 2 - tw / 2, im.height / 2 - (a + ds) / 2 - 4), t, font=f, fill=fg)
    return im


_MC = {}


def _mascot(who, ch, k, size):
    """Linh vật vẽ riêng (reel/mascot.py), lưu đệm theo cảm xúc và độ mở miệng."""
    import mascot
    key = (who, ch, int(min(1.0, k) * 6), size)
    if key not in _MC: _MC[key] = mascot.draw(who, ch, int(min(1.0, k) * 6) / 6.0, size)
    return _MC[key]


class Stage:
    """Nền chuyển động + thanh tiến độ + tên loạt + hai nhân vật."""
    def __init__(self, th, title, title_emoji, total, env, speak, chars=True, char_y=1330, char_size=270):
        self.th, self.total, self.env, self.speak = th, total, env, speak
        self.bg = gradient(th[2], th[3])
        rng = random.Random(C * 7 + 1)
        pool = list(th[7]) + list(M.EXTRA_EMOJI)
        self.float = [(rng.choice(pool), rng.uniform(0, W), rng.uniform(0, H), rng.uniform(40, 110), rng.uniform(70, 130), rng.uniform(0, 6.28)) for _ in range(12)]
        dark = M.lum(M.hexrgb(th[2])) < 110
        self.ink = '#FFFFFF' if dark else th[5]
        self.title = pill(title, 44, th[6], '#FFFFFF', title_emoji)
        self.chars, self.cy, self.cs = chars, char_y, char_size
        self.tag_cat = pill('Mèo Vui', 30, '#FFFFFF', th[5]); self.tag_bot = pill('Robot Tây', 30, BOT_FILL, BOT_FG)

    def talk(self, who, t):
        e = self.env.get(who); f = int(t * FPS)
        if e is not None: return float(e[min(f, len(e) - 1)])
        return abs(math.sin(t * 11)) if any(s <= t <= x for s, x in self.speak[who]) else 0.0

    def base(self, t):
        im = self.bg.copy()
        for ch, x, y, sp, sz, ph in self.float:  # emoji trôi nhẹ lên trên
            yy = (y - sp * t) % (H + 200) - 100; xx = x + 26 * math.sin(t * 0.9 + ph)
            M.paste_emoji(im, ch, xx, yy, int(sz), alpha=0.28)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((100, 150, W - 100, 164), 7, fill=(255, 255, 255, 110))
        d.rounded_rectangle((100, 150, 100 + (W - 200) * min(1, t / self.total), 164), 7, fill=self.th[6])
        paste_c(im, self.title, W / 2, 240, 0.7 + 0.3 * ease_back(t / 0.3))
        return im

    def char(self, im, who, ch, t, over=None, x=None, y=None, size=None, boost=1.0):
        x = x if x is not None else (250 if who == 'cat' else 830); y = y or self.cy; size = size or self.cs
        k = self.talk(who, t) * boost
        bob = 6 * math.sin(t * 2.2 + (0 if who == 'cat' else 1.7))
        d = ImageDraw.Draw(im); d.ellipse((x - size * 0.38, y + size * 0.47, x + size * 0.38, y + size * 0.57), fill=(0, 0, 0, 45))
        e = _mascot(who, ch, k, size)
        if e is not None:
            sx, sy = 1 + 0.05 * k, 1 + 0.13 * k
            e2 = e.resize((int(e.width * sx), int(e.height * sy)), Image.BILINEAR) if k > 0.03 else e
            im.alpha_composite(e2, (int(x - e2.width / 2), int(y + e.height / 2 - e2.height + bob - 10 * k)))
        if over:
            M.paste_emoji(im, over, x + size * 0.36, y - size * 0.55 + 8 * math.sin(t * 5), int(size * 0.42), rot=10 * math.sin(t * 4))
        paste_c(im, self.tag_cat if who == 'cat' else self.tag_bot, x, y + size * 0.72)


def confetti(im, t, seed=1, n=55):
    if t < 0 or t > 3: return
    rng = random.Random(seed); d = ImageDraw.Draw(im)
    cols = ['#FF5252', '#FFD740', '#40C4FF', '#69F0AE', '#E040FB', '#FF9100']
    for _ in range(n):
        x0 = rng.uniform(100, W - 100); vx = rng.uniform(-260, 260); vy = rng.uniform(-1300, -500); s = rng.uniform(12, 26); col = rng.choice(cols)
        x = x0 + vx * t; y = 760 + vy * t + 0.5 * 1900 * t * t
        if 0 < y < H:
            w = s * abs(math.cos(t * rng.uniform(5, 11))) + 3
            d.rectangle((x - w / 2, y - s / 2, x + w / 2, y + s / 2), fill=col)


def encode(draw, total, audio, out, shots=()):
    M.write_wav(f'{WORK}/a.wav', audio)
    if os.environ.get('SAVE_FRAMES'):
        os.makedirs(os.environ['SAVE_FRAMES'], exist_ok=True)
        for i, t in enumerate(shots): draw(t).convert('RGB').save(os.path.join(os.environ['SAVE_FRAMES'], f'{KIND}_{i}.jpg'), quality=85)
        if os.environ.get('FRAMES_ONLY'): return
    tmp = f'{WORK}/v_tmp.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for f in range(int(total * FPS)):
        p.stdin.write(draw(f / FPS).convert('RGB').tobytes())
    p.stdin.close()
    if p.wait() != 0: sys.exit('ffmpeg lỗi')
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-i', f'{WORK}/a.wav', '-map', '0:v', '-map', '1:a',
                           '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', out])
    print('Đã dựng', out, round(total, 1), 'giây', os.path.getsize(out) // 1024, 'KB')


# ------------------------------------------------------------------ Loạt 1: Mèo đố, Robot đoán sai
def make_meo(th, out, D):
    if D.get('vq'):
        r = dict(id=D.get('id', 'sheet'), vi_q=str(D['vq']).strip(), vi_a=str(D.get('va', '')).strip(), en_q=str(D.get('eq', '')).strip(),
                 en_a=str(D.get('ea', '')).strip(), g_en=str(D.get('g_en', '')).strip(), g_vi=str(D.get('g_vi', '')).strip(), vi_only=truthy(D.get('vi_only', '')))
    else:
        data = load_v2()['riddles']; rid = os.environ.get('RID')
        r = next((x for x in data if x['id'] == rid), None) or M.pick(data, C, 29)
    g_en, g_vi = (r['g_en'], r.get('g_vi', '')) if r.get('g_en') else GUESS_DEFAULT
    vo = bool(r.get('vi_only')) or not r.get('en_q')  # câu chơi chữ: chỉ hỏi bằng tiếng Việt
    ans_vi, ans_en = r['vi_a'].rstrip('.'), r['en_a'].rstrip('.')
    tr = Track()
    ask = say(r['vi_q'], CAT_VOICES, 'ask', '+6%', '+22Hz')
    gs = say(g_en, BOT_VOICES, 'guess', '+0%', '-6Hz', robot=True)
    a1 = say('Sai rồi! Đáp án là: ' + ans_vi + '.', CAT_VOICES, 'a1', '+6%', '+22Hz')
    a2 = say('Oh! Vietnamese is so tricky!' if vo else 'Oh! ' + ans_en + '!', BOT_VOICES, 'a2', '+0%', '-6Hz', robot=True)
    lg = get_laugh(C, 2.4)
    t_ask = 0.25; tr.put(sfx_pop(), 0.0); e = tr.put(ask, t_ask, 'cat')
    t_cd = e + 0.15; tr.put(M.synth_ticks(THINK), t_cd)
    t_g = t_cd + THINK; tr.put(sfx_whoosh(), t_g - 0.05); e = tr.put(gs, t_g + 0.15, 'bot')
    t_bz = e + 0.05; tr.put(sfx_buzz(), t_bz)
    t_rv = t_bz + 0.5; tr.put(sfx_ting(), t_rv); tr.put(sfx_win(), t_rv + 0.05)
    e = tr.put(a1, t_rv - 0.35, 'cat'); e = tr.put(a2, max(e, t_rv + 0.6) + 0.1, 'bot')
    t_end = e + 0.1; tr.put(lg * 0.9, t_end, 'cat'); total = t_end + 2.5
    audio, env = tr.mix(total)
    st = Stage(th, f'MÈO ĐỐ · TẬP {C + 1}', '😺', total, env, tr.speak)
    q_card = card(r['vi_q'], '' if vo else r['en_q'], th[0], th[1], th[4], th[5], th[6], tail='left')
    g_card = card(g_en, g_vi, BOT_FONT, None, BOT_FILL, BOT_FG, BOT_SUB, tail='right', maxh=480)
    a_card = card(ans_vi, ans_en, th[0], th[1], '#FFFFFF', '#0B6B3A', '#1971C2', header='ĐÁP ÁN · ANSWER', accent='#2BAE66', top=r['vi_q'], maxh=600, max_size=110)
    B = D.get('board') or {}
    if B.get('total'):  # Bảng vàng: số liệu thật từ bình luận của câu đố trước
        end_p = pill(f"Câu trước: {B['total']} bạn đoán, {B.get('correct', 0)} bạn đúng", 38, th[6], '#FFFFFF', '🏆')
        end_e = pill('Đến lượt bạn! · Your turn!', 32, '#FFFFFF', th[5])
    else:
        end_p = pill('Bạn đoán mất mấy giây?', 44, th[6], '#FFFFFF', '⏱️')
        end_e = pill(f'Tiếp theo {teaser()[0]} · {teaser()[1]}', 32, '#FFFFFF', th[5], '⏰')
    cdl = pill('Gõ đáp án vào bình luận!', 32, '#FFFFFF', th[5])
    CY = 660

    def draw(t):
        im = st.base(t)
        if t < t_g:
            paste_c(im, q_card, W / 2, CY, 0.93 + 0.07 * ease_back((t) / 0.32))
        elif t < t_rv:
            u = t - t_g; sh = 16 * math.sin((t - t_bz) * 55) * max(0, 1 - (t - t_bz) / 0.4) if t >= t_bz else 0
            paste_c(im, g_card, W / 2 + sh, CY, 0.55 + 0.45 * ease_back(u / 0.28))
            if t >= t_bz: M.paste_emoji(im, '❌', W / 2 + 350, CY - 120, int(210 * (1.6 - 0.6 * ease((t - t_bz) / 0.18))), rot=-10)
        else:
            u = t - t_rv
            paste_c(im, a_card, W / 2, CY, 0.5 + 0.5 * ease_back(u / 0.32))
            confetti(im, u, C + 3)
        if t_cd <= t < t_g:
            u = t - t_cd; n = max(1, int(math.ceil(THINK - u))); frac = u - int(u)
            rg = ring(1 - u / THINK, n, st.th[6], '#FFFFFF')
            paste_c(im, rg, W / 2, 1330, 1 + 0.16 * max(0, 1 - frac / 0.22))
            paste_c(im, cdl, W / 2, 1150)
        if t >= t_end:
            u = t - t_end
            paste_c(im, end_p, W / 2, 1050, ease_back(u / 0.3)); paste_c(im, end_e, W / 2, 1135, ease_back((u - 0.15) / 0.3))
        cat = '😺' if t < t_cd else '😼' if t < t_g else '🙀' if t < t_bz else '😸' if t < t_end else '😹'
        over = '🤔' if t_cd <= t < t_g else '💡' if t_g <= t < t_bz else '💦' if t_bz <= t < t_rv else '👏' if t >= t_rv else None
        st.char(im, 'cat', cat, t, boost=1.5 if t >= t_end else 1.0); st.char(im, 'bot', '🤖', t, over=over)
        return im

    encode(draw, total, audio, out, shots=(0.15, t_ask + 1.0, t_cd + 2.4, t_g + 0.8, t_bz + 0.25, t_rv + 0.5, t_end + 1.2))
    return (f"😺 Mèo Vui đố, 🤖 Robot Tây đoán sai mất rồi. Còn bạn thì sao?\n\n🧩 {r['vi_q']}\n" + ('' if vo else f"🧩 {r['en_q']}\n") +
            f"\n⏱️ Bạn đoán mất mấy giây? / How fast were you?\n\n#SongVuiMoiNgay #MeoDo #CauDoVui #Riddle #HocTiengAnh"), r['id']


# ------------------------------------------------------------------ Loạt 2: Tìm emoji khác biệt
def make_odd(th, out, D):
    rng = random.Random(C * 31 + 5)
    levels = []
    for li, (n, dur) in enumerate(((5, THINK - 2.5), (6, THINK - 1.5), (8, THINK - 0.5))):
        a, b = rng.choice(ODD_PAIRS[li]); levels.append({'n': n, 'dur': dur, 'a': a, 'b': b, 'pos': (rng.randrange(n), rng.randrange(n))})
    tr = Track(); t = 0.0
    lines = ['Tìm emoji khác biệt! Màn một.', 'Màn hai!', 'Màn ba. Siêu khó!']
    for li, lv in enumerate(levels):
        v = say(lines[li], CAT_VOICES, f'l{li}', '+8%', '+22Hz')
        lv['t0'] = t; tr.put(sfx_whoosh(), t); tr.put(v, t + 0.1, 'cat')
        tr.put(M.synth_ticks(lv['dur']) * 0.6, t)
        lv['t1'] = t + lv['dur']; tr.put(sfx_ting(), lv['t1']); t = lv['t1'] + 1.3
    v = say('Bạn tìm được mấy màn?', CAT_VOICES, 'end', '+6%', '+22Hz'); b = say('How many did you find?', BOT_VOICES, 'endb', '+0%', '-6Hz', robot=True)
    t_end = t; e = tr.put(v, t_end + 0.1, 'cat'); e = tr.put(b, e + 0.1, 'bot'); tr.put(get_laugh(C, 1.6) * 0.7, e, 'cat'); total = e + 1.7
    audio, env = tr.mix(total)
    st = Stage(th, f'TÌM EMOJI KHÁC BIỆT · TẬP {C + 1}', '🔍', total, env, tr.speak, char_y=1460, char_size=190)
    sub = pill('Bạn tìm ra trong vài giây?  Can you spot it?', 28, '#FFFFFF', th[5])
    GX, GY, GS = 100, 395, 880
    panel = Image.new('RGBA', (GS + 60, GS + 60), (0, 0, 0, 0)); ImageDraw.Draw(panel).rounded_rectangle((0, 0, GS + 59, GS + 59), 50, fill=(255, 255, 255, 215))
    for lv in levels:
        n = lv['n']; cs = GS / n; sz = int(cs * 0.78)
        lv['cs'], lv['sz'] = cs, sz
        full = Image.new('RGBA', (GS, GS), (0, 0, 0, 0))
        for r in range(n):
            for c in range(n):
                M.paste_emoji(full, lv['b'] if (c, r) == lv['pos'] else lv['a'], c * cs + cs / 2, r * cs + cs / 2, sz)
        lv['full'] = full
        dim = full.copy(); dim.putalpha(dim.getchannel('A').point(lambda v: int(v * 0.25))); lv['dim'] = dim
        lv['tag'] = pill(f"MÀN {levels.index(lv) + 1}/3", 40, th[6], '#FFFFFF')
    endc = card('Bạn tìm được mấy màn?', 'How many did you find?', th[0], th[1], th[4], th[5], th[6], maxh=420)
    tz = pill(f'Tiếp theo {teaser()[0]} · {teaser()[1]}', 32, '#FFFFFF', th[5], '⏰'); fz = pill('Theo dõi để không lỡ!', 36, th[6], '#FFFFFF', '🔔')

    def draw(t):
        im = st.base(t)
        paste_c(im, sub, W / 2, 322)
        if t < t_end:
            li = max(i for i, lv in enumerate(levels) if t >= lv['t0']); lv = levels[li]; u = t - lv['t0']
            im.alpha_composite(panel, (GX - 30, GY - 30))
            n, cs, sz = lv['n'], lv['cs'], lv['sz']; ox, oy = lv['pos']
            if u < 0.34 and li > 0:  # ô bật ra theo làn sóng (màn 1 hiện sẵn để khung đầu có hình)
                for r in range(n):
                    for c in range(n):
                        p = (u - (r + c) * 0.16 / (2 * n)) / 0.16
                        if p > 0: M.paste_emoji(im, lv['b'] if (c, r) == lv['pos'] else lv['a'], GX + c * cs + cs / 2, GY + r * cs + cs / 2, max(4, int(sz * ease_back(p))))
            elif t < lv['t1']:
                im.alpha_composite(lv['full'], (GX, GY))
            else:
                v = t - lv['t1']; im.alpha_composite(lv['dim'], (GX, GY))
                cx, cy = GX + ox * cs + cs / 2, GY + oy * cs + cs / 2
                d = ImageDraw.Draw(im); rr = cs * (0.62 + 0.08 * math.sin(v * 12)); d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline='#FF3B30', width=10)
                M.paste_emoji(im, lv['b'], cx, cy, int(sz * (1 + 0.35 * ease_back(v / 0.25))))
            d = ImageDraw.Draw(im); left = max(0, 1 - u / lv['dur'])  # thanh thời gian
            d.rounded_rectangle((GX, 1298, GX + GS, 1322), 12, fill=(255, 255, 255, 150))
            if left > 0: d.rounded_rectangle((GX, 1298, GX + max(24, GS * left), 1322), 12, fill='#FF3B30' if left < 0.3 else th[6])
            paste_c(im, lv['tag'], W / 2, 1460, 0.6 + 0.4 * ease_back(u / 0.3))
        else:
            paste_c(im, endc, W / 2, 800, 0.5 + 0.5 * ease_back((t - t_end) / 0.3))
            paste_c(im, tz, W / 2, 1090, ease_back((t - t_end - 0.4) / 0.3)); paste_c(im, fz, W / 2, 1175, ease_back((t - t_end - 0.6) / 0.3))
        rev = any(lv['t1'] <= t < lv['t1'] + 1.3 for lv in levels)
        st.char(im, 'cat', '😹' if t >= t_end + 2 else '😸' if rev else '😺', t, x=200); st.char(im, 'bot', '🤖', t, over='👏' if rev else '🤔', x=880)
        return im

    L = levels
    encode(draw, total, audio, out, shots=(0.2, L[0]['t0'] + 2, L[0]['t1'] + 0.6, L[1]['t0'] + 2, L[2]['t0'] + 2, L[2]['t1'] + 0.6, t_end + 1.5))
    return ("🔍 Tìm emoji khác biệt trong vài giây! 3 màn khó dần, bạn qua được mấy màn?\n"
            "Spot the odd emoji! 3 levels, how many can you find?\n\n#SongVuiMoiNgay #TimDiemKhacBiet #OddOneOut #EmojiChallenge #BrainTeaser"), 'odd-' + '-'.join(lv['a'] for lv in levels)


# ------------------------------------------------------------------ Loạt 4: Câu đố của tuần (tổng hợp 5 câu, chạy Chủ nhật)
def make_tuan(th, out, D):
    data = {x['id']: x for x in load_v2()['riddles']}
    ids = [i for i in (D.get('recap_ids') or []) if i in data and data[i].get('vi_q')]
    rng = random.Random(C * 13 + 7)
    rest = [x for x in data.values() if x['id'] not in ids and not x.get('season')]
    rng.shuffle(rest)
    rs = [data[i] for i in ids][:5]
    rs += rest[:max(0, 5 - len(rs))]
    NT = 6.0  # giây suy nghĩ mỗi câu (gọn để cả video khoảng 70-80 giây)
    tr = Track(); t = 0.0
    intro = say('Câu đố của tuần! Năm câu liên tiếp, bạn trả lời được mấy câu?', CAT_VOICES, 'in', '+6%', '+22Hz')
    tr.put(sfx_pop(), 0.0); e = tr.put(intro, 0.25, 'cat'); t = e + 0.5
    segs = []
    for i, r in enumerate(rs):
        ans_vi, ans_en = r['vi_a'].rstrip('.'), (r.get('en_a') or '').rstrip('.')
        vo = bool(r.get('vi_only')) or not r.get('en_q')
        ask = say(f"Câu {i + 1}. " + r['vi_q'], CAT_VOICES, f'q{i}', '+6%', '+22Hz')
        a1 = say('Đáp án là: ' + ans_vi + '.', CAT_VOICES, f'a{i}', '+6%', '+22Hz')
        sg = dict(r=r, vo=vo, ans_vi=ans_vi, ans_en=ans_en, t0=t)
        tr.put(sfx_whoosh(), t); e = tr.put(ask, t + 0.2, 'cat')
        sg['cd'] = e + 0.15; tr.put(M.synth_ticks(NT), sg['cd'])
        sg['rv'] = sg['cd'] + NT; tr.put(sfx_ting(), sg['rv']); tr.put(sfx_win(), sg['rv'] + 0.05)
        e = tr.put(a1, sg['rv'] + 0.1, 'cat')
        if ans_en and not vo:
            a2 = say(ans_en + '!', BOT_VOICES, f'b{i}', '+0%', '-6Hz', robot=True); e = tr.put(a2, e + 0.1, 'bot')
        sg['t1'] = e + 0.9; t = sg['t1']; segs.append(sg)
    t_end = t
    outv = say('Bạn trả lời đúng mấy câu? Hẹn gặp lại nhé!', CAT_VOICES, 'out', '+6%', '+22Hz')
    e = tr.put(outv, t_end + 0.1, 'cat'); tr.put(get_laugh(C, 1.6) * 0.8, e, 'cat'); total = e + 1.9
    audio, env = tr.mix(total)
    st = Stage(th, 'CÂU ĐỐ CỦA TUẦN', '🏅', total, env, tr.speak)
    n_ = len(segs)
    for i, sg in enumerate(segs):
        r = sg['r']
        sg['q'] = card(r['vi_q'], '' if sg['vo'] else r['en_q'], th[0], th[1], th[4], th[5], th[6], tail='left')
        sg['a'] = card(sg['ans_vi'], sg['ans_en'], th[0], th[1], '#FFFFFF', '#0B6B3A', '#1971C2', header='ĐÁP ÁN · ANSWER', accent='#2BAE66', top=r['vi_q'], maxh=600, max_size=110)
        sg['tag'] = pill(f'CÂU {i + 1}/{n_}', 40, th[6], '#FFFFFF')
    ic = card('5 câu đố của tuần', 'Weekly riddles · Can you get them all?', th[0], th[1], th[4], th[5], th[6], maxh=520)
    end_p = pill('Bạn đúng mấy câu?', 44, th[6], '#FFFFFF', '🏅'); end_e = pill(f'Tiếp theo {teaser()[0]} · {teaser()[1]}', 32, '#FFFFFF', th[5], '⏰')
    cdl = pill('Gõ đáp án vào bình luận!', 32, '#FFFFFF', th[5]); CY = 660

    def draw(t):
        im = st.base(t); cat = '😺'; over = None
        if t < segs[0]['t0']:
            paste_c(im, ic, W / 2, CY, 0.93 + 0.07 * ease_back(t / 0.32))
        elif t < t_end:
            sg = max((s_ for s_ in segs if t >= s_['t0']), key=lambda s_: s_['t0']); u = t - sg['t0']
            paste_c(im, sg['tag'], W / 2, 330, ease_back(u / 0.3))
            if t < sg['rv']:
                paste_c(im, sg['q'], W / 2, CY, 0.93 + 0.07 * ease_back(u / 0.32))
                if t >= sg['cd']:
                    v = t - sg['cd']; frac = v - int(v)
                    paste_c(im, ring(1 - v / NT, max(1, int(math.ceil(NT - v))), st.th[6], '#FFFFFF'), W / 2, 1330, 1 + 0.16 * max(0, 1 - frac / 0.22))
                    paste_c(im, cdl, W / 2, 1150); cat = '😼'; over = '🤔'
            else:
                paste_c(im, sg['a'], W / 2, CY, 0.5 + 0.5 * ease_back((t - sg['rv']) / 0.32)); confetti(im, t - sg['rv'], C + 3); cat = '😸'; over = '👏'
        else:
            u = t - t_end
            paste_c(im, end_p, W / 2, 1050, ease_back(u / 0.3)); paste_c(im, end_e, W / 2, 1135, ease_back((u - 0.15) / 0.3)); cat = '😹'
        st.char(im, 'cat', cat, t, boost=1.5 if t >= t_end else 1.0); st.char(im, 'bot', '🤖', t, over=over)
        return im

    s0, s2 = segs[0], segs[min(2, n_ - 1)]
    encode(draw, total, audio, out, shots=(0.2, s0['t0'] + 1.0, s0['cd'] + 2.4, s0['rv'] + 0.8, s2['rv'] + 0.8, t_end + 1.0))
    qs = '\n'.join(f"{i + 1}. {sg['r']['vi_q']}" for i, sg in enumerate(segs))
    return (f"🏅 Câu đố của tuần: 5 câu liên tiếp, bạn trả lời được mấy câu?\n\n{qs}\n\n⏱️ Gõ số câu bạn đoán đúng nhé! / How many did you get?\n\n"
            f"#SongVuiMoiNgay #CauDoCuaTuan #CauDoVui #Riddle #HocTiengAnh"), 'tuan-' + time.strftime('%Y%m%d', time.gmtime(time.time() + 7 * 3600))


# ------------------------------------------------------------------ Loạt thử nghiệm: Đúng hay Sai / Quy luật nào đây / 10 giây tiếng Anh
# Mỗi câu Đúng/Sai đều là kiến thức phổ thông đã được xác nhận; (câu VI, câu EN, đúng?, giải thích VI, giải thích EN)
DUNGSAI = [
    ("Cá heo thở bằng mang.", "Dolphins breathe with gills.", False, "Cá heo thở bằng phổi và phải nổi lên mặt nước để hít thở.", "Dolphins are mammals and breathe air with lungs."),
    ("Mật ong bảo quản kín có thể để rất lâu mà không hỏng.", "Properly sealed honey can last a very long time without spoiling.", True, "Mật ong rất ít nước và có tính axit nên vi khuẩn khó phát triển.", "Honey has little water and is acidic, so bacteria struggle to grow."),
    ("Quả chuối là một loại quả mọng theo thực vật học.", "Bananas are berries in botany.", True, "Theo thực vật học, chuối là quả mọng.", "Botanically, a banana is a berry."),
    ("Dâu tây là quả mọng theo thực vật học.", "Strawberries are berries in botany.", False, "Dâu tây không phải quả mọng thực sự theo thực vật học.", "Botanically, strawberries are not true berries."),
    ("Sét không bao giờ đánh hai lần vào cùng một chỗ.", "Lightning never strikes the same place twice.", False, "Sét có thể đánh nhiều lần vào cùng một nơi, nhất là chỗ cao.", "Lightning often strikes the same place again, especially tall objects."),
    ("Con người chỉ dùng 10% bộ não.", "Humans only use 10% of their brain.", False, "Đây là lầm tưởng: gần như mọi vùng não đều được sử dụng.", "It is a myth: nearly all brain regions are used."),
    ("Lạc đà trữ nước trong bướu.", "Camels store water in their humps.", False, "Bướu lạc đà chứa mỡ, không chứa nước.", "A camel's hump stores fat, not water."),
    ("Bạch tuộc có ba trái tim.", "An octopus has three hearts.", True, "Hai tim bơm máu qua mang, một tim bơm máu đi khắp cơ thể.", "Two hearts pump blood to the gills, one to the body."),
    ("Nước luôn sôi ở 100 độ C dù ở độ cao nào.", "Water always boils at 100°C at any altitude.", False, "Càng lên cao áp suất càng thấp nên nước sôi ở nhiệt độ thấp hơn.", "At higher altitude pressure drops, so water boils at a lower temperature."),
    ("Thủ đô của Úc là Sydney.", "The capital of Australia is Sydney.", False, "Thủ đô của Úc là Canberra.", "The capital of Australia is Canberra."),
    ("Thủ đô của Thổ Nhĩ Kỳ là Istanbul.", "The capital of Turkey is Istanbul.", False, "Thủ đô của Thổ Nhĩ Kỳ là Ankara.", "The capital of Turkey is Ankara."),
    ("Cá vàng chỉ nhớ được trong 3 giây.", "Goldfish only remember things for 3 seconds.", False, "Cá vàng có thể nhớ trong nhiều tháng.", "Goldfish can remember things for months."),
    ("Dơi bị mù.", "Bats are blind.", False, "Dơi nhìn được, và nhiều loài còn dùng siêu âm để định hướng.", "Bats can see, and many also use echolocation."),
    ("Mặt Trăng tự phát ra ánh sáng.", "The Moon makes its own light.", False, "Mặt Trăng chỉ phản chiếu ánh sáng Mặt Trời.", "The Moon only reflects sunlight."),
    ("Sao Kim là hành tinh gần Mặt Trời nhất.", "Venus is the closest planet to the Sun.", False, "Hành tinh gần Mặt Trời nhất là Sao Thủy.", "The closest planet to the Sun is Mercury."),
    ("Gấu trúc thuộc bộ Ăn thịt dù chủ yếu ăn tre.", "Giant pandas belong to the order Carnivora even though they mostly eat bamboo.", True, "Gấu trúc thuộc họ Gấu, bộ Ăn thịt, nhưng ăn tre là chính.", "Pandas are bears, in the order Carnivora, but mostly eat bamboo."),
    ("Mèo luôn rơi xuống bằng bốn chân an toàn từ mọi độ cao.", "Cats always land safely on their feet from any height.", False, "Mèo biết xoay người khi rơi nhưng vẫn có thể bị thương nặng.", "Cats can twist in the air but can still be badly hurt."),
    ("Vàng là kim loại dẫn điện tốt nhất.", "Gold is the best electrical conductor among metals.", False, "Bạc dẫn điện tốt nhất trong các kim loại.", "Silver is the best electrical conductor among metals."),
    ("Cá voi là loài cá.", "Whales are fish.", False, "Cá voi là động vật có vú, thở bằng phổi và nuôi con bằng sữa.", "Whales are mammals: they breathe air and nurse their young."),
    ("Cá mập là một loài cá.", "Sharks are fish.", True, "Cá mập là cá sụn, thở bằng mang.", "Sharks are cartilaginous fish and breathe with gills."),
    ("Số 0 là số chẵn.", "Zero is an even number.", True, "Số 0 chia hết cho 2 nên là số chẵn.", "Zero is divisible by 2, so it is even."),
    ("Chim cánh cụt sống ở Bắc Cực.", "Penguins live at the North Pole.", False, "Chim cánh cụt sống chủ yếu ở Nam bán cầu, không phải Bắc Cực.", "Penguins live mostly in the Southern Hemisphere, not the Arctic."),
    ("Nhện là côn trùng.", "Spiders are insects.", False, "Nhện có 8 chân, còn côn trùng có 6 chân.", "Spiders have 8 legs, insects have 6."),
    ("Ngày Nhà giáo Việt Nam là ngày 20 tháng 11.", "Vietnamese Teachers' Day is on November 20.", True, "Ngày 20/11 hằng năm là Ngày Nhà giáo Việt Nam.", "November 20 each year is Teachers' Day in Vietnam."),
    ("Ếch có thể hấp thụ nước qua da.", "Frogs can absorb water through their skin.", True, "Ếch hấp thụ nước qua da nên ít khi cần uống như chúng ta.", "Frogs take in water through their skin."),
    ("Ánh sáng đi nhanh hơn âm thanh.", "Light travels faster than sound.", True, "Vì vậy ta thấy tia chớp trước khi nghe tiếng sấm.", "That is why we see lightning before we hear thunder."),
    ("Cà chua là một loại quả theo thực vật học.", "A tomato is a fruit in botany.", True, "Cà chua có hạt và phát triển từ hoa nên là quả.", "A tomato develops from a flower and holds seeds, so it is a fruit."),
    ("Cá heo ngủ khi chỉ một nửa bộ não nghỉ.", "Dolphins sleep with only half of their brain resting.", True, "Nhờ vậy cá heo vẫn nổi lên thở khi ngủ.", "That lets them keep surfacing to breathe while asleep."),
]
ANH10 = [  # (nghĩa tiếng Việt, câu tiếng Anh, ghi chú)
    ("Bạn khỏe không?", "How are you?", ""), ("Cảm ơn bạn rất nhiều", "Thank you very much", ""), ("Xin lỗi, tôi đến muộn", "Sorry, I am late", ""),
    ("Bạn có thể giúp tôi không?", "Can you help me?", ""), ("Tôi không hiểu", "I do not understand", ""), ("Bạn có thể nói chậm hơn không?", "Can you speak more slowly?", ""),
    ("Cái này giá bao nhiêu?", "How much is this?", ""), ("Tôi muốn một ly nước", "I would like a glass of water", ""), ("Nhà vệ sinh ở đâu?", "Where is the bathroom?", ""),
    ("Rất vui được gặp bạn", "Nice to meet you", ""), ("Hẹn gặp lại bạn", "See you later", ""), ("Chúc một ngày tốt lành", "Have a nice day", ""),
    ("Tôi đang học tiếng Anh", "I am learning English", ""), ("Bạn tên là gì?", "What is your name?", ""), ("Tôi đến từ Việt Nam", "I am from Vietnam", ""),
    ("Bạn làm nghề gì?", "What do you do?", ""), ("Tôi đói rồi", "I am hungry", ""), ("Làm ơn cho tôi hoá đơn", "Could I have the bill, please?", ""),
    ("Chúc mừng sinh nhật", "Happy birthday", ""), ("Chúc may mắn", "Good luck", ""), ("Đừng lo lắng", "Do not worry", ""),
    ("Tôi nghĩ vậy", "I think so", ""), ("Tôi đồng ý", "I agree", ""), ("Không sao đâu", "It is okay", ""),
    ("Bạn đang ở đâu?", "Where are you?", ""), ("Mấy giờ rồi?", "What time is it?", ""), ("Tôi bị lạc đường", "I am lost", ""),
    ("Chúc ngủ ngon", "Sleep well", ""), ("Hôm nay trời đẹp quá", "The weather is lovely today", ""),
]


def quyluat(seed):
    """Dãy số theo quy luật, tự sinh và tự tính đáp án: (dãy hiển thị, đáp án, mô tả quy luật, mức khó)."""
    r = random.Random(seed); k = seed % 5
    if k == 0:
        a, d = r.randint(2, 9), r.randint(2, 7); s = [a + d * i for i in range(5)]; return s[:4], s[4], f'cộng thêm {d} mỗi lần', 1
    if k == 1:
        a, q = r.randint(1, 4), r.choice([2, 3]); s = [a * q ** i for i in range(5)]; return s[:4], s[4], f'nhân với {q} mỗi lần', 2
    if k == 2:
        a = r.randint(1, 4); s = [(a + i) ** 2 for i in range(5)]; return s[:4], s[4], 'các số chính phương liên tiếp', 3
    if k == 3:
        x, y = r.randint(1, 4), r.randint(2, 6); s = [x, y]
        while len(s) < 6: s.append(s[-1] + s[-2])
        return s[:5], s[5], 'mỗi số bằng tổng hai số đứng trước', 4
    a, d1, d2 = r.randint(3, 9), r.randint(2, 5), r.randint(1, 3); s = [a]
    for i in range(5): s.append(s[-1] + (d1 if i % 2 == 0 else -d2))
    return s[:5], s[5], f'lần lượt cộng {d1}, trừ {d2}', 5


def _single(th, out, title, emoji, ask_text, qmain, qsub, amain, asub, a_vi, a_en, think, caption, cid, afg='#0B6B3A', header='ĐÁP ÁN · ANSWER', top=None, bot_slow=False):
    tr = Track()
    ask = say(ask_text, CAT_VOICES, 'ask', '+4%', '+22Hz')
    a1 = say(a_vi, CAT_VOICES, 'a1', '+6%', '+22Hz')
    a2 = say(a_en, BOT_VOICES, 'a2', '-12%' if bot_slow else '+0%', '-6Hz', robot=not bot_slow)
    lg = get_laugh(C, 2.4)
    tr.put(sfx_pop(), 0.0); e = tr.put(ask, 0.25, 'cat')
    t_cd = e + 0.15; tr.put(M.synth_ticks(think), t_cd)
    t_rv = t_cd + think; tr.put(sfx_ting(), t_rv); tr.put(sfx_win(), t_rv + 0.05)
    e = tr.put(a1, t_rv + 0.1, 'cat'); e = tr.put(a2, e + 0.1, 'bot')
    t_end = e + 0.1; tr.put(lg * 0.9, t_end, 'cat'); total = t_end + 2.5
    audio, env = tr.mix(total)
    st = Stage(th, f'{title} · TẬP {C + 1}', emoji, total, env, tr.speak)
    q_card = card(qmain, qsub, th[0], th[1], th[4], th[5], th[6], tail='left')
    a_card = card(amain, asub, th[0], th[1], '#FFFFFF', afg, '#1971C2', header=header, accent='#2BAE66', top=top, maxh=600, max_size=110)
    end_p = pill('Bạn đoán đúng không?', 44, th[6], '#FFFFFF', '⏱️')
    end_e = pill(f'Tiếp theo {teaser()[0]} · {teaser()[1]}', 32, '#FFFFFF', th[5], '⏰')
    cdl = pill('Gõ đáp án vào bình luận!', 32, '#FFFFFF', th[5]); CY = 660

    def draw(t):
        im = st.base(t)
        if t < t_rv: paste_c(im, q_card, W / 2, CY, 0.93 + 0.07 * ease_back(t / 0.32))
        else:
            u = t - t_rv; paste_c(im, a_card, W / 2, CY, 0.5 + 0.5 * ease_back(u / 0.32)); confetti(im, u, C + 3)
        if t_cd <= t < t_rv:
            u = t - t_cd; frac = u - int(u)
            paste_c(im, ring(1 - u / think, max(1, int(math.ceil(think - u))), st.th[6], '#FFFFFF'), W / 2, 1330, 1 + 0.16 * max(0, 1 - frac / 0.22))
            paste_c(im, cdl, W / 2, 1150)
        if t >= t_end:
            u = t - t_end; paste_c(im, end_p, W / 2, 1050, ease_back(u / 0.3)); paste_c(im, end_e, W / 2, 1135, ease_back((u - 0.15) / 0.3))
        cat = '😺' if t < t_cd else '😼' if t < t_rv else '😸' if t < t_end else '😹'
        st.char(im, 'cat', cat, t, boost=1.5 if t >= t_end else 1.0)
        st.char(im, 'bot', '🤖', t, over='🤔' if t_cd <= t < t_rv else '👏' if t >= t_rv else None)
        return im

    encode(draw, total, audio, out, shots=(0.15, t_cd + 2.0, t_rv + 0.6, t_end + 1.2))
    return caption, cid


def _vn_days():
    return int((time.time() + 7 * 3600) // 86400) - int(time.mktime(time.strptime('2026-11-18', '%Y-%m-%d')) // 86400)


def make_dungsai(th, out, D):
    i = int(os.environ.get('RID') or (_vn_days() // 3 if os.environ.get('ROT') else KC)) % len(DUNGSAI)
    vi, en, ok, ev, ee = DUNGSAI[i]
    ans = 'ĐÚNG' if ok else 'SAI'; ae = 'TRUE' if ok else 'FALSE'
    cap = (f"🤔 Đúng hay Sai? {vi}\n🤔 True or False? {en}\n\n⏱️ Bạn đoán mấy giây? Gõ ĐÚNG hoặc SAI trong bình luận!\n\n"
           "#SongVuiMoiNgay #DungHaySai #TrueOrFalse #KienThucVui #HocTiengAnh")
    return _single(th, out, 'ĐÚNG HAY SAI?', '🤔', 'Đúng hay sai? ' + vi, vi, en, ans, f'{ae} · {ev}', f'Đáp án là: {ans}. {ev}', f'{ae}! {ee}', min(THINK, 6.0), cap, f'ds-{i}',
                   afg='#0B6B3A' if ok else '#C92A2A', header='ĐÁP ÁN · ANSWER')


def make_quyluat(th, out, D):
    seq, ans, rule, lv = quyluat(int(os.environ.get('RID') or (_vn_days() // 3 if os.environ.get('ROT') else KC)) + 11)
    shown = ',  '.join(str(x) for x in seq) + ',  ?'
    spoken = ', '.join(str(x) for x in seq)
    cap = (f"🔢 Quy luật nào đây? Mức {lv}/5\n{shown}\n\n⏱️ Số tiếp theo là gì? Gõ đáp án trong bình luận!\n\n"
           "#SongVuiMoiNgay #QuyLuat #IQ #BrainTeaser #DoVui")
    return _single(th, out, 'QUY LUẬT NÀO ĐÂY?', '🔢', f'Quy luật nào đây? Mức {lv} trên 5. Dãy số: {spoken}. Số tiếp theo là gì?', shown, f'Level {lv}/5 · What comes next?', str(ans), f'Quy luật: {rule}', f'Số tiếp theo là {ans}. Quy luật: {rule}.',
                   f'The next number is {ans}!', min(THINK + 2, 10.0), cap, f'ql-{seq[0]}-{ans}', afg='#0B6B3A', header='ĐÁP ÁN · QUY LUẬT', top='Số tiếp theo?')


def make_tienganh(th, out, D):
    i = int(os.environ.get('RID') or (_vn_days() // 3 if os.environ.get('ROT') else KC)) % len(ANH10)
    vi, en, _ = ANH10[i]
    cap = (f"🗣️ 10 giây tiếng Anh: \"{vi}\" nói thế nào?\n\nĐáp án trong video, nói theo Robot Tây nhé! Bạn nhớ được câu này không?\n\n"
           "#SongVuiMoiNgay #TiengAnhMoiNgay #HocTiengAnh #EnglishInUse #Shorts")
    return _single(th, out, '10 GIÂY TIẾNG ANH', '💬', f'Nói câu này bằng tiếng Anh: {vi}', vi, 'Say it in English!', en, vi, f'Tiếng Anh là: {en}. Nói theo Robot nhé!', f'{en}. Repeat after me: {en}.', 5.0, cap, f'en-{i}', afg='#0B6B3A',
                   header='TIẾNG ANH · ENGLISH', top=vi, bot_slow=True)


def make_thu(th, out, D):
    """Khung giờ thử nghiệm: xoay vòng 3 loạt mới theo ngày."""
    os.environ['ROT'] = '1'
    return [make_dungsai, make_quyluat, make_tienganh][_vn_days() % 3](th, out, D)


# ------------------------------------------------------------------ Loạt 3: Đuổi hình bắt chữ bằng emoji
def make_emoji(th, out, D):
    if D.get('emoji'):
        q = dict(id=D.get('id', 'sheet'), emoji=str(D['emoji']), kind=str(D.get('kind', 'VH')), vi=str(D.get('vi', '')).strip(), en=str(D.get('en', '')).strip(),
                 mean=str(D.get('mean', '')).strip(), g_en=str(D.get('g_en', '')).strip(), g_vi=str(D.get('g_vi', '')).strip())
    else:
        data = load_v2()['emoji']; eid = os.environ.get('EID')
        q = next((x for x in data if x['id'] == eid), None) or M.pick(data, C, 41)
    kc = q['kind'].strip(); kc = kc if kc in KINDS else KIND_BY_NAME.get(kc.lower(), 'VH')
    kv, ke, ask_line = KINDS[kc]
    ems = [e for e in q['emoji'].split() if M.emoji_img(e, 64) is not None][:5]
    words = q['vi'].split()
    g_en, g_vi = (q['g_en'], q.get('g_vi', '')) if q.get('g_en') else GUESS_DEFAULT
    tr = Track()
    ask = say('Đuổi hình bắt chữ! ' + ask_line, CAT_VOICES, 'ask', '+8%', '+22Hz')
    gs = say(g_en, BOT_VOICES, 'guess', '+0%', '-6Hz', robot=True)
    a1 = say(q['vi'] + '!', CAT_VOICES, 'a1', '+0%', '+22Hz')
    a2 = say('. '.join(x for x in (q['en'].rstrip('.'), q['mean'].rstrip('.')) if x) + '.', BOT_VOICES, 'a2', '+6%', '-6Hz', robot=True)
    for i in range(len(ems)): tr.put(sfx_pop(), 0.05 + i * 0.3)
    e = tr.put(ask, 0.2, 'cat'); t_cd = e + 0.1; tr.put(M.synth_ticks(THINK), t_cd)
    t_gs = t_cd + 0.5; tr.put(gs, t_gs, 'bot'); t_hint = t_cd + THINK * 0.62; tr.put(sfx_pop(), t_hint)
    t_rv = t_cd + THINK; tr.put(sfx_ting(), t_rv); tr.put(sfx_win(), t_rv + 0.05)
    e = tr.put(a1, t_rv + 0.25, 'cat'); e = tr.put(a2, e + 0.15, 'bot')
    t_end = e; tr.put(get_laugh(C, 1.8) * 0.8, t_end, 'cat'); total = t_end + 1.9
    audio, env = tr.mix(total)
    st = Stage(th, f'ĐUỔI HÌNH BẮT CHỮ · TẬP {C + 1}', '🧩', total, env, tr.speak)
    chip = pill(f"{kv} · {len(words)} tiếng  ·  {ke}", 30, '#FFFFFF', th[5])
    PH = 290
    panel = Image.new('RGBA', (940, PH), (0, 0, 0, 0)); ImageDraw.Draw(panel).rounded_rectangle((0, 0, 939, PH - 1), 54, fill=(255, 255, 255, 225))
    n = max(1, len(ems)); gap = 940 / n; ES = int(min(200, gap * 0.86))
    # ô chữ: tự xuống dòng (tối đa 2 dòng), tự thu nhỏ
    for fs in (58, 50, 44, 38):
        fw = M.font(th[0], fs, th[1]); bh = int(fs * 1.85); padx = int(fs * 0.48); sp = 16
        bw = [max(int(fs * 1.7), int(fw.getlength(w)) + 2 * padx) for w in words]
        lines, cur, cw = [], [], 0
        for i, w_ in enumerate(bw):
            if cur and cw + sp + w_ > 920: lines.append(cur); cur, cw = [], 0
            cw += (sp if cur else 0) + w_; cur.append(i)
        lines.append(cur)
        if len(lines) <= 2: break
    BH = len(lines) * bh + (len(lines) - 1) * 14 + 26
    hint_n = max(1, len(words) // 4)

    def boxes(reveal):  # reveal: số tiếng đã mở
        im = Image.new('RGBA', (960, BH), (0, 0, 0, 0)); d = ImageDraw.Draw(im); y = 8
        for ln in lines:
            lw = sum(bw[i] for i in ln) + sp * (len(ln) - 1); x = (960 - lw) / 2
            for i in ln:
                on = i < reveal
                d.rounded_rectangle((x, y + 7, x + bw[i], y + bh + 7), 26, fill=(0, 0, 0, 50))
                d.rounded_rectangle((x, y, x + bw[i], y + bh), 26, fill='#2BAE66' if on else '#FFFFFF', outline=th[6], width=5)
                if on:
                    a, ds = fw.getmetrics(); d.text((x + bw[i] / 2 - fw.getlength(words[i]) / 2, y + (bh - a - ds) / 2), words[i], font=fw, fill='#FFFFFF')
                else:
                    d.rounded_rectangle((x + 24, y + bh - 30, x + bw[i] - 24, y + bh - 23), 4, fill=th[6])
                x += bw[i] + sp
            y += bh + 14
        return im
    B0, B1, BA = boxes(0), boxes(hint_n), boxes(len(words))
    BY = 712 + BH / 2; top = 712 + BH + 4
    g_card = card(g_en, g_vi, BOT_FONT, None, BOT_FILL, BOT_FG, BOT_SUB, w=600, maxh=250, tail='right', max_size=48, sub_ratio=0.74)
    m_card = card(q['en'], q['mean'], M.TAGFONT, None, '#FFFFFF', '#0B6B3A', '#1971C2', maxh=max(170, 1196 - top), max_size=46, sub_ratio=0.8)
    MY = top + (m_card.height - 192) / 2; GY2 = min(1090, top + 16 + (g_card.height - 192) / 2)
    end_p = pill('Theo dõi để không lỡ!', 29, th[6], '#FFFFFF', '🔔')

    def draw(t):
        im = st.base(t)
        paste_c(im, chip, W / 2, 335)
        im.alpha_composite(panel, (70, 400))
        for i, ch in enumerate(ems):
            p = (t + 1.5 - i * 0.3) / 0.25  # hiện sẵn ngay khung đầu
            if p > 0: M.paste_emoji(im, ch, 70 + gap * i + gap / 2, 400 + PH / 2 + 8 * math.sin(t * 3 + i), max(4, int(ES * ease_back(p))))
        bx = BA if t >= t_rv else B1 if t >= t_hint else B0
        k = 1 + 0.10 * max(0, 1 - (t - t_rv) / 0.25) if t >= t_rv else 1 + 0.06 * max(0, 1 - (t - t_hint) / 0.2) if t >= t_hint else 1
        paste_c(im, bx, W / 2, BY, k)
        if t_cd <= t < t_rv:
            u = t - t_cd; frac = u - int(u)
            paste_c(im, ring(1 - u / THINK, max(1, int(math.ceil(THINK - u))), st.th[6], '#FFFFFF'), W / 2, 1330, 1 + 0.16 * max(0, 1 - frac / 0.22))
            if t_gs <= t < t_gs + len(gs) / SR + 0.9:
                paste_c(im, g_card, 640, GY2, 0.5 + 0.5 * ease_back((t - t_gs) / 0.25))
        if t >= t_rv:
            u = t - t_rv
            paste_c(im, m_card, W / 2, MY, 0.5 + 0.5 * ease_back((u - 0.2) / 0.3)); confetti(im, u, C + 9)
        if t >= t_end:
            paste_c(im, end_p, W / 2, 1330, ease_back((t - t_end) / 0.3))
        cat = '😺' if t < t_cd else '😼' if t < t_rv else '😸' if t < t_end else '😹'
        st.char(im, 'cat', cat, t, boost=1.5 if t >= t_end else 1); st.char(im, 'bot', '🤖', t, over='🤔' if t_cd <= t < t_rv else '👏' if t >= t_rv else None)
        return im

    encode(draw, total, audio, out, shots=(0.3, 1.5, t_gs + 1.0, t_hint + 0.5, t_rv + 0.6, t_rv + 2.5, t_end + 1.0))
    return (f"🧩 Đuổi hình bắt chữ: {' '.join(ems)}\n{ask_line} ({len(words)} tiếng)\nCan you guess it from the emojis? ({ke})\n\n"
            f"👇 Bạn đoán ra không?\n\n#SongVuiMoiNgay #DuoiHinhBatChu #EmojiQuiz #TiengViet #HocTiengAnh"), q['id']


def build(kind, c, D):
    """Dựng video cho một loạt. Trả về (đường dẫn video, chú thích, mã nội dung)."""
    global C, THINK, KC
    C = int(c); D = D or {}
    try: KC = int(D.get('kcount'))
    except Exception: KC = C
    try: THINK = float(min(12, max(4, float(D.get('think') or THINK))))
    except Exception: pass
    os.makedirs(WORK, exist_ok=True); M.ensure_fonts()
    th = list(M.THEMES[(C * 5) % len(M.THEMES)])
    if th[0] in ('Pacifico.ttf', 'DancingScript.ttf', 'Lobster.ttf', 'Pattaya.ttf'): th[0], th[1] = 'Baloo2.ttf', 700  # chữ đố cần dễ đọc
    out = f'{WORK}/final.mp4'
    cap, cid = {'meo': make_meo, 'odd': make_odd, 'emoji': make_emoji, 'tuan': make_tuan, 'dungsai': make_dungsai, 'quyluat': make_quyluat, 'tienganh': make_tienganh, 'thu': make_thu}[kind](th, out, D)
    if D.get('q_vi'):  # câu nói vui của ngày đưa vào chú thích
        qs = f"😹 Mèo Vui: “{str(D['q_vi']).strip()}”" + (f"\n🤖 Robot Tây: “{str(D['q_en']).strip()}”" if D.get('q_en') else '')
        head, tags = cap.rsplit('\n\n#', 1); cap = f"{head}\n\n{qs}\n\n#{tags}"
    return out, cap, cid


def main():
    out, cap, cid = build(KIND, C, {})
    if os.path.exists(out): os.replace(out, f'{WORK}/{KIND}.mp4')
    open(f'{WORK}/{KIND}_caption.txt', 'w', encoding='utf8').write(cap)
    print(cid); print(cap)


if __name__ == '__main__':
    main()
