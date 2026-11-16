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
CAT_VOICES = ['vi-VN-HoaiMyNeural', 'vi-VN-NamMinhNeural']
BOT_VOICES = ['en-US-GuyNeural', 'en-US-AndrewNeural', 'en-GB-SoniaNeural']
BOT_FONT = 'ChakraPetch-Bold.ttf'
BOT_FILL, BOT_FG, BOT_SUB = '#10243E', '#E6FBFF', '#7FE9FF'

# dữ liệu mẫu cho bản xem thử (sau khi duyệt sẽ chuyển vào Google Sheet)
GUESS = {  # câu Robot đoán sai cho từng câu đố
    'default': ('Hmm... is it a banana?', 'Hừm… là quả chuối hả?'),
    'R122': ('Is it... my nose?', 'Là… cái mũi của tôi hả?'),
    'R072': ('Is it... a fish?', 'Là… con cá hả?'),
    'R050': ('Is it... a ghost?', 'Là… con ma hả?'),
}
EMOJI_QUIZ = [
    {'emoji': ['🐸', '🪑', '🕳️'], 'kind_vi': 'Thành ngữ · 4 tiếng', 'kind_en': 'Vietnamese idiom', 'vi': 'Ếch ngồi đáy giếng',
     'en': 'A frog sitting in a well', 'mean': 'someone who sees only a tiny part of the world',
     'guess_en': 'Frog... chair... hole?', 'guess_vi': 'Ếch… ghế… lỗ?'},
    {'emoji': ['🐘', '🕳️', '🪡'], 'kind_vi': 'Thành ngữ · 4 tiếng', 'kind_en': 'Vietnamese idiom', 'vi': 'Voi chui lỗ kim',
     'en': 'An elephant through the eye of a needle', 'mean': 'something impossible',
     'guess_en': 'Elephant... hole... needle?', 'guess_vi': 'Voi… lỗ… kim?'},
]
ODD_PAIRS = [[('🍎', '🍅'), ('🌕', '🌝'), ('🍊', '🍑')], [('😄', '😁'), ('🙂', '🙃'), ('🐵', '🙈')], [('😮', '😯'), ('😀', '😃'), ('🕐', '🕑')]]


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
        e = M.emoji_img(ch, size)
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
def make_meo(th, out):
    data = json.load(open(os.path.join(M.ROOT, 'data', 'content.json'), encoding='utf8'))['riddles']
    rid = os.environ.get('RID'); r = next((x for x in data if x['id'] == rid), None) or M.pick(data, C, 29)
    g_en, g_vi = GUESS.get(r['id'], GUESS['default'])
    if os.environ.get('GUESS_EN'): g_en, g_vi = os.environ['GUESS_EN'], os.environ.get('GUESS_VI', '')
    ans_vi, ans_en = r['vi_a'].rstrip('.'), r['en_a'].rstrip('.')
    tr = Track()
    ask = say(r['vi_q'], CAT_VOICES, 'ask', '+6%', '+22Hz')
    gs = say(g_en, BOT_VOICES, 'guess', '+0%', '-6Hz', robot=True)
    a1 = say('Sai rồi! Đáp án là: ' + ans_vi + '.', CAT_VOICES, 'a1', '+6%', '+22Hz')
    a2 = say('Oh! ' + ans_en + '!', BOT_VOICES, 'a2', '+0%', '-6Hz', robot=True)
    lg = get_laugh(C, 2.4)
    t_ask = 0.25; tr.put(sfx_pop(), 0.0); e = tr.put(ask, t_ask, 'cat')
    t_cd = e + 0.15; tr.put(M.synth_ticks(5.0), t_cd)
    t_g = t_cd + 5.0; tr.put(sfx_whoosh(), t_g - 0.05); e = tr.put(gs, t_g + 0.15, 'bot')
    t_bz = e + 0.05; tr.put(sfx_buzz(), t_bz)
    t_rv = t_bz + 0.5; tr.put(sfx_ting(), t_rv); tr.put(sfx_win(), t_rv + 0.05)
    e = tr.put(a1, t_rv - 0.35, 'cat'); e = tr.put(a2, max(e, t_rv + 0.6) + 0.1, 'bot')
    t_end = e + 0.1; tr.put(lg * 0.9, t_end, 'cat'); total = t_end + 2.5
    audio, env = tr.mix(total)
    st = Stage(th, 'MÈO ĐỐ · 5 GIÂY', '😺', total, env, tr.speak)
    q_card = card(r['vi_q'], r['en_q'], th[0], th[1], th[4], th[5], th[6], tail='left')
    g_card = card(g_en, g_vi, BOT_FONT, None, BOT_FILL, BOT_FG, BOT_SUB, tail='right', maxh=480)
    a_card = card(ans_vi, ans_en, th[0], th[1], '#FFFFFF', '#0B6B3A', '#1971C2', header='ĐÁP ÁN · ANSWER', accent='#2BAE66', top=r['vi_q'], maxh=600, max_size=110)
    end_p = pill('Bạn đoán mất mấy giây?', 44, th[6], '#FFFFFF', '⏱️')
    end_e = pill('How fast were you?', 32, '#FFFFFF', th[5])
    cdl = pill('Đoán nhanh!  Quick, guess!', 30, '#FFFFFF', th[5])
    CY = 660

    def draw(t):
        im = st.base(t)
        if t < t_g:
            paste_c(im, q_card, W / 2, CY, 0.55 + 0.45 * ease_back((t) / 0.32))
        elif t < t_rv:
            u = t - t_g; sh = 16 * math.sin((t - t_bz) * 55) * max(0, 1 - (t - t_bz) / 0.4) if t >= t_bz else 0
            paste_c(im, g_card, W / 2 + sh, CY, 0.55 + 0.45 * ease_back(u / 0.28))
            if t >= t_bz: M.paste_emoji(im, '❌', W / 2 + 350, CY - 120, int(210 * (1.6 - 0.6 * ease((t - t_bz) / 0.18))), rot=-10)
        else:
            u = t - t_rv
            paste_c(im, a_card, W / 2, CY, 0.5 + 0.5 * ease_back(u / 0.32))
            confetti(im, u, C + 3)
        if t_cd <= t < t_g:
            u = t - t_cd; n = 5 - int(u); frac = u - int(u)
            rg = ring(1 - u / 5.0, n, st.th[6], '#FFFFFF')
            paste_c(im, rg, W / 2, 1330, 1 + 0.16 * max(0, 1 - frac / 0.22))
            paste_c(im, cdl, W / 2, 1165)
        if t >= t_end:
            u = t - t_end
            paste_c(im, end_p, W / 2, 1050, ease_back(u / 0.3)); paste_c(im, end_e, W / 2, 1135, ease_back((u - 0.15) / 0.3))
        cat = '😺' if t < t_cd else '😼' if t < t_g else '🙀' if t < t_bz else '😸' if t < t_end else '😹'
        over = '🤔' if t_cd <= t < t_g else '💡' if t_g <= t < t_bz else '💦' if t_bz <= t < t_rv else '👏' if t >= t_rv else None
        st.char(im, 'cat', cat, t, boost=1.5 if t >= t_end else 1.0); st.char(im, 'bot', '🤖', t, over=over)
        return im

    encode(draw, total, audio, out, shots=(0.15, t_ask + 1.0, t_cd + 2.4, t_g + 0.8, t_bz + 0.25, t_rv + 0.5, t_end + 1.2))
    return (f"😺 Mèo Vui đố, 🤖 Robot Tây đoán sai mất rồi. Còn bạn thì sao?\n\n🧩 {r['vi_q']}\n🧩 {r['en_q']}\n\n"
            f"⏱️ Bạn đoán mất mấy giây? / How fast were you?\n\n#SongVuiMoiNgay #MeoDo #CauDoVui #Riddle #HocTiengAnh")


# ------------------------------------------------------------------ Loạt 2: Tìm emoji khác biệt
def make_odd(th, out):
    rng = random.Random(C * 31 + 5)
    levels = []
    for li, (n, dur) in enumerate(((5, 3.6), (6, 4.0), (8, 4.6))):
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
    st = Stage(th, 'TÌM EMOJI KHÁC BIỆT', '🔍', total, env, tr.speak, char_y=1460, char_size=190)
    sub = pill('Spot the odd one out', 30, '#FFFFFF', th[5])
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

    def draw(t):
        im = st.base(t)
        paste_c(im, sub, W / 2, 322)
        if t < t_end:
            li = max(i for i, lv in enumerate(levels) if t >= lv['t0']); lv = levels[li]; u = t - lv['t0']
            im.alpha_composite(panel, (GX - 30, GY - 30))
            n, cs, sz = lv['n'], lv['cs'], lv['sz']; ox, oy = lv['pos']
            if u < 0.34:  # ô bật ra theo làn sóng
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
        rev = any(lv['t1'] <= t < lv['t1'] + 1.3 for lv in levels)
        st.char(im, 'cat', '😹' if t >= t_end + 2 else '😸' if rev else '😺', t, x=200); st.char(im, 'bot', '🤖', t, over='👏' if rev else '🤔', x=880)
        return im

    L = levels
    encode(draw, total, audio, out, shots=(0.2, L[0]['t0'] + 2, L[0]['t1'] + 0.6, L[1]['t0'] + 2, L[2]['t0'] + 2, L[2]['t1'] + 0.6, t_end + 1.5))
    return ("🔍 Tìm emoji khác biệt trong vài giây! 3 màn khó dần, bạn qua được mấy màn?\n"
            "Spot the odd emoji! 3 levels, how many can you find?\n\n#SongVuiMoiNgay #TimDiemKhacBiet #OddOneOut #EmojiChallenge #BrainTeaser")


# ------------------------------------------------------------------ Loạt 3: Đuổi hình bắt chữ bằng emoji
def make_emoji(th, out):
    q = EMOJI_QUIZ[C % len(EMOJI_QUIZ)]
    words = q['vi'].split()
    tr = Track()
    ask = say('Đuổi hình bắt chữ! Đây là thành ngữ gì?', CAT_VOICES, 'ask', '+8%', '+22Hz')
    gs = say(q['guess_en'], BOT_VOICES, 'guess', '-5%', '-6Hz', robot=True)
    a1 = say(q['vi'] + '!', CAT_VOICES, 'a1', '+0%', '+22Hz')
    a2 = say(q['en'] + '. It means ' + q['mean'] + '.', BOT_VOICES, 'a2', '+6%', '-6Hz', robot=True)
    for i in range(len(q['emoji'])): tr.put(sfx_pop(), 0.05 + i * 0.3)
    e = tr.put(ask, 0.2, 'cat'); t_cd = e + 0.1; tr.put(M.synth_ticks(5.0), t_cd)
    t_gs = t_cd + 0.6; tr.put(gs, t_gs, 'bot'); t_hint = t_cd + 3.0; tr.put(sfx_pop(), t_hint)
    t_rv = t_cd + 5.0; tr.put(sfx_ting(), t_rv); tr.put(sfx_win(), t_rv + 0.05)
    e = tr.put(a1, t_rv + 0.25, 'cat'); e = tr.put(a2, e + 0.15, 'bot')
    t_end = e; tr.put(get_laugh(C, 1.8) * 0.8, t_end, 'cat'); total = t_end + 1.9
    audio, env = tr.mix(total)
    st = Stage(th, 'ĐUỔI HÌNH BẮT CHỮ', '🧩', total, env, tr.speak)
    chip = pill(q['kind_vi'] + '  ·  ' + q['kind_en'], 30, '#FFFFFF', th[5])
    panel = Image.new('RGBA', (940, 330), (0, 0, 0, 0)); ImageDraw.Draw(panel).rounded_rectangle((0, 0, 939, 329), 54, fill=(255, 255, 255, 225))
    n = len(q['emoji']); ES = 220; gap = 940 / n
    fw = M.font(th[0], 64, th[1]); bh = 124
    bw = [max(120, int(fw.getlength(w)) + 56) for w in words]; tw = sum(bw) + 22 * (len(bw) - 1)
    sc = min(1.0, 940 / tw)
    g_card = card(q['guess_en'], q['guess_vi'], BOT_FONT, None, BOT_FILL, BOT_FG, BOT_SUB, w=560, maxh=260, tail='right', max_size=50, sub_ratio=0.74)
    m_card = card(q['en'], '= ' + q['mean'], M.TAGFONT, None, '#FFFFFF', '#0B6B3A', '#1971C2', maxh=285, max_size=46, sub_ratio=0.8)
    end_p = pill('Bạn đoán ra không?', 29, th[6], '#FFFFFF')

    def boxes(reveal):  # reveal: số tiếng đã mở
        im = Image.new('RGBA', (tw + 20, bh + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = 10
        for i, w in enumerate(words):
            on = i < reveal
            d.rounded_rectangle((x, 10 + 8, x + bw[i], 10 + bh + 8), 30, fill=(0, 0, 0, 50))
            d.rounded_rectangle((x, 10, x + bw[i], 10 + bh), 30, fill='#2BAE66' if on else '#FFFFFF', outline=th[6], width=5)
            if on:
                a, ds = fw.getmetrics(); d.text((x + bw[i] / 2 - fw.getlength(w) / 2, 10 + (bh - a - ds) / 2), w, font=fw, fill='#FFFFFF')
            else:
                d.rounded_rectangle((x + 28, 10 + bh - 34, x + bw[i] - 28, 10 + bh - 26), 4, fill=th[6])
            x += bw[i] + 22
        return im
    B0, B1, BA = boxes(0), boxes(1), boxes(len(words))

    def draw(t):
        im = st.base(t)
        paste_c(im, chip, W / 2, 335)
        im.alpha_composite(panel, (70, 400))
        for i, ch in enumerate(q['emoji']):
            p = (t - 0.05 - i * 0.3) / 0.25
            if p > 0: M.paste_emoji(im, ch, 70 + gap * i + gap / 2, 565 + 8 * math.sin(t * 3 + i), max(4, int(ES * ease_back(p))))
        bx = BA if t >= t_rv else B1 if t >= t_hint else B0
        k = 1 + 0.12 * max(0, 1 - (t - t_rv) / 0.25) if t >= t_rv else 1 + 0.08 * max(0, 1 - (t - t_hint) / 0.2) if t >= t_hint else 1
        paste_c(im, bx, W / 2, 825, sc * k)
        if t_cd <= t < t_rv:
            u = t - t_cd; frac = u - int(u)
            paste_c(im, ring(1 - u / 5.0, 5 - int(u), st.th[6], '#FFFFFF'), W / 2, 1330, 1 + 0.16 * max(0, 1 - frac / 0.22))
            if t_gs <= t < t_gs + len(gs) / SR + 0.9:
                paste_c(im, g_card, 660, 1045, 0.5 + 0.5 * ease_back((t - t_gs) / 0.25))
        if t >= t_rv:
            u = t - t_rv
            paste_c(im, m_card, W / 2, 1025, 0.5 + 0.5 * ease_back((u - 0.2) / 0.3)); confetti(im, u, C + 9)
        if t >= t_end: paste_c(im, end_p, W / 2, 1330, ease_back((t - t_end) / 0.3))
        cat = '😺' if t < t_cd else '😼' if t < t_rv else '😸' if t < t_end else '😹'
        st.char(im, 'cat', cat, t, boost=1.5 if t >= t_end else 1); st.char(im, 'bot', '🤖', t, over='🤔' if t_cd <= t < t_rv else '👏' if t >= t_rv else None)
        return im

    encode(draw, total, audio, out, shots=(0.3, 1.5, t_gs + 1.0, t_hint + 0.5, t_rv + 0.6, t_rv + 2.5, t_end + 1.0))
    return (f"🧩 Đuổi hình bắt chữ: {' '.join(q['emoji'])} là {q['kind_vi'].split(' · ')[0].lower()} gì?\nGuess the Vietnamese idiom from the emojis!\n\n"
            f"👇 Bạn đoán ra không?\n\n#SongVuiMoiNgay #DuoiHinhBatChu #EmojiQuiz #ThanhNgu #HocTiengAnh")


def main():
    os.makedirs(WORK, exist_ok=True); M.ensure_fonts()
    th = list(M.THEMES[(C * 5) % len(M.THEMES)])
    if th[0] in ('Pacifico.ttf', 'DancingScript.ttf', 'Lobster.ttf', 'Pattaya.ttf'): th[0], th[1] = 'Baloo2.ttf', 700  # chữ đố cần dễ đọc
    out = f'{WORK}/{KIND}.mp4'
    cap = {'meo': make_meo, 'odd': make_odd, 'emoji': make_emoji}[KIND](th, out)
    open(f'{WORK}/{KIND}_caption.txt', 'w', encoding='utf8').write(cap)


if __name__ == '__main__':
    main()
