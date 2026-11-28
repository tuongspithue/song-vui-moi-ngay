import json, re, sys, unicodedata
sys.path.insert(0, 'tools'); sys.path.insert(0, 'reel')
from kid_emoji import KID_NEW
import make as M
CLS = {'con', 'qua', 'cai', 'chiec', 'cu', 'chum', 'cay', 'ban', 'bo', 'doi', 'mau', 'quyen', 'chu', 'bong', 'bac', 'dang', 'tro', 'mieng', 'thanh', 'hop', 'bang'}
def nz(s):
    s = unicodedata.normalize('NFD', s.lower()); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn').replace('đ', 'd')
    w = re.sub(r'[^a-z0-9 ]', ' ', s).split()
    while len(w) > 1 and w[0] in CLS: w = w[1:]
    return ' '.join(w)
p = 'data/content_v2.json'
d = json.load(open(p, encoding='utf8'))
seen = {nz(e['vi']): e['id'] for e in d['emoji']}
seen_em = {e['emoji'].strip() for e in d['emoji']}
seen_ans = {nz(r['vi_a']) for r in d['riddles']}
nums = [int(e['id'][1:]) for e in d['emoji'] if re.fullmatch(r'E\d+', e['id'])]; n = max(nums); add = 0
for k, em, vi, en, mean, ge, gv in KID_NEW:
    key = nz(vi)
    if key in seen: print('TRÙNG đáp án, bỏ:', vi, '~', seen[key]); continue
    if em in seen_em: print('TRÙNG emoji, bỏ:', em, vi); continue
    if key in seen_ans: print('TRÙNG đáp án câu đố, bỏ:', vi); continue
    bad = [t for t in em.split()[:5] if M.emoji_img(t, 64) is None]
    if bad: print('KHÔNG VẼ ĐƯỢC, bỏ:', vi, bad); continue
    n += 1; add += 1; seen[key] = 'E%03d' % n; seen_em.add(em)
    d['emoji'].append(dict(id='E%03d' % n, emoji=em, kind=k, vi=vi, en=en, mean=mean, g_en=ge, g_vi=gv, season=''))
json.dump(d, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('thêm', add, '| tổng emoji', len(d['emoji']))
