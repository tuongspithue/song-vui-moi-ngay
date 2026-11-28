import json, re, sys, unicodedata, difflib
sys.path.insert(0, 'tools'); sys.path.insert(0, 'reel')
from extra2_emoji import EMOJI2
from extra2_quiz import RIDDLES2, DUNGSAI2, ANH10_2
import make as M
CLS = {'con', 'qua', 'cai', 'chiec', 'cu', 'chum', 'cay', 'ban', 'bo', 'doi', 'mau', 'quyen', 'chu', 'bong', 'bac', 'dang', 'tro', 'mieng', 'thanh', 'hop', 'bang', 'cuc'}
def nz(s, strip=True):
    s = unicodedata.normalize('NFD', s.lower()); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn').replace('đ', 'd')
    w = re.sub(r'[^a-z0-9 ]', ' ', s).split()
    while strip and len(w) > 1 and w[0] in CLS: w = w[1:]
    return ' '.join(w)
p = 'data/content_v2.json'; d = json.load(open(p, encoding='utf8'))
# ---- emoji
seen = {nz(e['vi']): e['id'] for e in d['emoji']}; seen_em = {e['emoji'].strip() for e in d['emoji']}
seen_ans = {nz(r['vi_a']) for r in d['riddles']}
n = max(int(e['id'][1:]) for e in d['emoji'] if re.fullmatch(r'E\d+', e['id'])); add = 0
for k, em, vi, en, mean, ge, gv in EMOJI2:
    key = nz(vi)
    if key in seen: print('emoji TRÙNG:', vi, '~', seen[key]); continue
    if em in seen_em: print('emoji TRÙNG hình:', em, vi); continue
    if key in seen_ans: print('emoji TRÙNG đáp án câu đố:', vi); continue
    bad = [t for t in em.split()[:5] if M.emoji_img(t, 64) is None]
    if bad: print('emoji KHÔNG VẼ ĐƯỢC:', vi, bad); continue
    n += 1; add += 1; seen[key] = 'E%03d' % n; seen_em.add(em)
    d['emoji'].append(dict(id='E%03d' % n, emoji=em, kind=k, vi=vi, en=en, mean=mean, g_en=ge, g_vi=gv, season=''))
print('emoji +%d (tổng %d)' % (add, len(d['emoji'])))
# ---- câu đố
qs = [nz(r['vi_q'], False) for r in d['riddles']]; ra = 0
for i, q, a, eq, ea, ge, gv, vo in RIDDLES2:
    if any(r['id'] == i for r in d['riddles']): print('câu đố trùng mã', i); continue
    if nz(a) in seen_ans: print('câu đố TRÙNG đáp án:', a); continue
    if any(difflib.SequenceMatcher(None, nz(q, False), x).ratio() > 0.8 for x in qs): print('câu đố TRÙNG câu hỏi:', q); continue
    seen_ans.add(nz(a)); ra += 1
    d['riddles'].append(dict(id=i, vi_q=q, vi_a=a, en_q=eq, en_a=ea, g_en=ge, g_vi=gv, vi_only=vo, season=''))
print('câu đố +%d (tổng %d)' % (ra, len(d['riddles'])))
json.dump(d, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
# ---- Đúng/Sai & Tiếng Anh vào reel/show.py
import ast
s = open('reel/show.py', encoding='utf-8').read()
t = ast.parse(s); L = {x.targets[0].id: ast.literal_eval(x.value) for x in t.body if isinstance(x, ast.Assign) and getattr(x.targets[0], 'id', '') in ('DUNGSAI', 'ANH10')}
def ins(s, name, items, old):
    seen = [nz(x[0], False) for x in old]; out = []
    for x in items:
        k = nz(x[0], False)
        if any(difflib.SequenceMatcher(None, k, y).ratio() > 0.85 for y in seen): print(name, 'TRÙNG:', x[0]); continue
        seen.append(k); out.append(x)
    i = s.index(name + ' = ['); j = s.index('\n]\n', i)
    return s[:j] + '\n' + '\n'.join('    ' + repr(tuple(x)) + ',' for x in out) + s[j:], len(out)
s, a = ins(s, 'DUNGSAI', DUNGSAI2, L['DUNGSAI']); s, b = ins(s, 'ANH10', ANH10_2, L['ANH10'])
open('reel/show.py', 'w', encoding='utf-8').write(s)
print('đúng/sai +%d, tiếng Anh +%d' % (a, b))
