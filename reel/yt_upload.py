"""Đăng video lên YouTube Shorts (chế độ riêng tư) bằng YouTube Data API v3.
Cần 3 secret: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN. Thiếu thì bỏ qua, không làm hỏng bước đăng Facebook."""
import json, os, sys, requests

WORK = os.environ.get('WORK_DIR', '/tmp/svmn')


def main():
    cid, sec, rt = (os.environ.get(k) for k in ('YT_CLIENT_ID', 'YT_CLIENT_SECRET', 'YT_REFRESH_TOKEN'))
    if not (cid and sec and rt): print('YouTube: chưa có khóa, bỏ qua'); return 0
    vid, meta = f'{WORK}/final.mp4', f'{WORK}/youtube.txt'
    if not (os.path.exists(vid) and os.path.exists(meta)): print('YouTube: chưa có video/tiêu đề, bỏ qua'); return 0
    txt = open(meta, encoding='utf8').read()
    title = txt.split('TIÊU ĐỀ:\n', 1)[1].split('\n\nMÔ TẢ:', 1)[0].strip()[:100]
    desc = txt.split('MÔ TẢ:\n', 1)[1].strip()[:4900]
    tok = requests.post('https://oauth2.googleapis.com/token', data=dict(client_id=cid, client_secret=sec, refresh_token=rt, grant_type='refresh_token'), timeout=60)
    if tok.status_code != 200: print('YouTube: lỗi đổi token', tok.status_code, tok.text[:300]); return 1
    h = {'Authorization': 'Bearer ' + tok.json()['access_token']}
    body = {'snippet': {'title': title, 'description': desc, 'categoryId': '24', 'defaultLanguage': 'vi'},
            'status': {'privacyStatus': os.environ.get('YT_PRIVACY', 'private'), 'selfDeclaredMadeForKids': False}}
    data = open(vid, 'rb').read()
    r = requests.post('https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status',
                      headers=dict(h, **{'Content-Type': 'application/json; charset=UTF-8', 'X-Upload-Content-Type': 'video/mp4', 'X-Upload-Content-Length': str(len(data))}), data=json.dumps(body), timeout=60)
    if r.status_code != 200: print('YouTube: lỗi khởi tạo', r.status_code, r.text[:300]); return 1
    u = requests.put(r.headers['Location'], headers={'Content-Type': 'video/mp4'}, data=data, timeout=600)
    if u.status_code not in (200, 201): print('YouTube: lỗi tải lên', u.status_code, u.text[:300]); return 1
    print('YouTube: đã đăng', u.json().get('id'), body['status']['privacyStatus']); return 0


if __name__ == '__main__':
    sys.exit(main())
