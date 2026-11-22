import json, re, sys, os
sys.path.insert(0, 'tools'); sys.path.insert(0, 'reel')
from extra_emoji import EMOJI_NEW
from extra_quiz import DUNGSAI_NEW, ANH10_NEW, RIDDLES_NEW
import make as M
p = 'data/content_v2.json'
d = json.load(open(p))
ex = {e['vi'].lower() for e in d['emoji']}
nums = [int(e['id'][1:]) for e in d['emoji'] if re.fullmatch(r'E\d+', e['id'])]
n = max(nums); added = 0
for k, em, vi, en, mean, ge, gv in EMOJI_NEW:
    if vi.lower() in ex: continue
    toks = em.split()
    bad = [t for t in toks[:5] if M.emoji_img(t, 64) is None]
    if bad: print('BỎ (emoji không vẽ được):', vi, bad); continue
    n += 1; added += 1; ex.add(vi.lower())
    d['emoji'].append(dict(id='E%03d' % n, emoji=em, kind=k, vi=vi, en=en, mean=mean, g_en=ge, g_vi=gv, season=''))
rq = {r['vi_q'].lower() for r in d['riddles']}; ra = 0
for i, q, a, eq, ea, ge, gv, vo in RIDDLES_NEW:
    if q.lower() in rq: continue
    ra += 1
    d['riddles'].append(dict(id=i, vi_q=q, vi_a=a, en_q=eq, en_a=ea, g_en=ge, g_vi=gv, vi_only=vo, season=''))
json.dump(d, open(p, 'w'), ensure_ascii=False, indent=1)
print('emoji +%d, riddles +%d' % (added, ra))
s = open('reel/show.py', encoding='utf-8').read()
def ins(s, name, items, fmt):
    i = s.index(name + ' = ['); j = s.index('\n]\n', i)
    old = s[i:j]
    new = [x for x in items if x[0] not in old]
    return s[:j] + '\n' + '\n'.join('    ' + fmt(x) + ',' for x in new) + s[j:], len(new)
s, a = ins(s, 'DUNGSAI', DUNGSAI_NEW, lambda x: repr(tuple(x)))
s, b = ins(s, 'ANH10', ANH10_NEW, lambda x: repr(tuple(x)))
open('reel/show.py', 'w', encoding='utf-8').write(s)
print('dungsai +%d, anh10 +%d' % (a, b))
