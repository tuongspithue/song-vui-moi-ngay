"""Đọc số liệu các Reel đã đăng (chỉ đọc). Chạy trong GitHub Actions."""
import json, os, requests
G = 'https://graph.facebook.com/v23.0'
T = os.environ['FB_PAGE_TOKEN_SVMN']; P = os.environ['FB_PAGE_ID']
def get(path, **kw):
    kw['access_token'] = T
    try:
        r = requests.get(f'{G}/{path}', params=kw, timeout=30); return r.status_code, r.json()
    except Exception as e:
        return 0, {'error': str(e)}
print('PAGE', get(P, fields='name,followers_count,fan_count'))
st = json.load(open('state.json'))
rows = []
for h in st.get('history', []):
    v = h['video']; row = {'n': h['n'], 'kind': h.get('kind', 'cu'), 'id': h.get('id') or h.get('r'), 't': h['t']}
    c, d = get(v, fields='length,likes.summary(true).limit(0),comments.summary(true).limit(0)')
    if c == 200:
        row['len'] = round(d.get('length', 0), 1)
        row['likes'] = d.get('likes', {}).get('summary', {}).get('total_count')
        row['cmts'] = d.get('comments', {}).get('summary', {}).get('total_count')
    else:
        row['err_v'] = str(d)[:150]
    c, d = get(f'{v}/video_insights')
    if c == 200:
        for m in d.get('data', []):
            val = m['values'][0]['value'] if m.get('values') else None
            if m['name'] == 'post_video_retention_graph' and isinstance(val, dict):
                ks = sorted(val, key=lambda x: int(x)); n = len(ks)
                val = [round(float(val[ks[i]]), 2) for i in sorted(set([0, n//10, n//5, n//3, n//2, 2*n//3, n-1]))] if n else None
            row[m['name']] = val
    else:
        row['err_i'] = str(d)[:150]
    rows.append(row); print(json.dumps(row, ensure_ascii=False))
