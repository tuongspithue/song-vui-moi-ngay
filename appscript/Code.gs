/** Sống vui mỗi ngày - Apps Script đặt lịch 4 tin/ngày, gọi GitHub Actions dựng và đăng Reel.
 *  Cần Script Properties (thầy tự nhập): GH_TOKEN (token GitHub fine-grained chỉ cho kho song-vui-moi-ngay,
 *  quyền Contents: Read and write), PAGE_ID (mã số Trang Facebook). */
var CFG = {
  GH_REPO: 'tuongspithue/song-vui-moi-ngay',
  TIMES: [[7, 30], [11, 45], [17, 0], [20, 30]], // giờ Việt Nam: 4 tin/ngày
  EVENT: 'dang_tin'
};

function _props() { return PropertiesService.getScriptProperties(); }

function _log(msg) {
  var p = _props(), arr = [];
  try { arr = JSON.parse(p.getProperty('LOG') || '[]'); } catch (e) {}
  arr.push(Utilities.formatDate(new Date(), 'Asia/Ho_Chi_Minh', 'yyyy-MM-dd HH:mm') + ' ' + msg);
  p.setProperty('LOG', JSON.stringify(arr.slice(-40)));
  Logger.log(msg);
}

function _dispatch(payload) {
  var token = _props().getProperty('GH_TOKEN');
  if (!token) throw new Error('Thiếu Script Property GH_TOKEN');
  var r = UrlFetchApp.fetch('https://api.github.com/repos/' + CFG.GH_REPO + '/dispatches', {
    method: 'post', contentType: 'application/json', muteHttpExceptions: true,
    headers: { Authorization: 'Bearer ' + token, Accept: 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28' },
    payload: JSON.stringify({ event_type: CFG.EVENT, client_payload: payload })
  });
  var code = r.getResponseCode();
  _log('dispatch ' + JSON.stringify(payload) + ' -> HTTP ' + code + (code === 204 ? '' : ' ' + r.getContentText().slice(0, 200)));
  return code;
}

/** Hàm đặt lịch gọi 4 lần/ngày. */
function POST_NOW() {
  var pid = _props().getProperty('PAGE_ID');
  if (!pid) throw new Error('Thiếu Script Property PAGE_ID');
  return _dispatch({ page_id: pid, preview: 'false', force: 'false' });
}

/** Chạy thử: dựng video xem thử, KHÔNG đăng (tải video ở mục Artifacts của lần chạy). */
function PREVIEW_NOW() { return _dispatch({ preview: 'true' }); }

/** Ép đăng ngay một tin (bỏ qua giới hạn 40 phút). */
function POST_FORCE() {
  var pid = _props().getProperty('PAGE_ID');
  if (!pid) throw new Error('Thiếu Script Property PAGE_ID');
  return _dispatch({ page_id: pid, preview: 'false', force: 'true' });
}

/** Cài 4 lịch đăng mỗi ngày (chạy 1 lần). */
function SETUP_TRIGGERS() {
  ScriptApp.getProjectTriggers().forEach(function (t) { ScriptApp.deleteTrigger(t); });
  CFG.TIMES.forEach(function (hm) {
    ScriptApp.newTrigger('POST_NOW').timeBased().atHour(hm[0]).nearMinute(hm[1]).everyDays(1).inTimezone('Asia/Ho_Chi_Minh').create();
  });
  _log('Đã cài ' + CFG.TIMES.length + ' lịch đăng mỗi ngày');
}

function SHOW_LOG() { Logger.log(_props().getProperty('LOG')); }
