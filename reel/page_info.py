"""Đọc / cập nhật phần giới thiệu Trang (about, description) từ data/page_about.json."""
import json, os, sys, requests
G = 'https://graph.facebook.com/v23.0'; T = os.environ['FB_PAGE_TOKEN_SVMN']; P = os.environ['FB_PAGE_ID']
def show(tag):
    r = requests.get(f'{G}/{P}', params={'fields': 'name,about,description,category,followers_count', 'access_token': T}, timeout=30)
    print(tag, r.status_code, json.dumps(r.json(), ensure_ascii=False)[:900])
r = requests.get(f'{G}/me/permissions', params={'access_token': T}, timeout=30); print('PERMS', r.status_code, r.text[:600])
show('TRUOC')
if os.environ.get('MODE') == 'write':
    d = json.load(open('data/page_about.json', encoding='utf8'))
    for k in ('about', 'description'):
        w = requests.post(f'{G}/{P}', data={k: d[k], 'access_token': T}, timeout=30)
        print('GHI', k, len(d[k]), w.status_code, w.text[:300])
    show('SAU')
