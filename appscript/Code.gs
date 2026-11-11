/** Sống vui mỗi ngày - Apps Script: lấy nội dung từ Google Sheet, đặt lịch 4 tin/ngày, gọi GitHub Actions dựng và đăng Reel.
 *  Script Properties: GH_TOKEN (thầy tự nhập), PAGE_ID, SHEET_ID (tự tạo bởi SETUP_SHEET).
 *  Google Sheet: tab CAU_NOI (câu nói vui) và CAU_DO (câu đố). Thêm/sửa/xoá dòng thoải mái;
 *  cột "Dùng" bỏ tích = tạm không đăng; bot luôn chọn dòng có "Số lần đã đăng" thấp nhất (ngẫu nhiên khi bằng nhau). */
var CFG = {
  GH_REPO: 'tuongspithue/song-vui-moi-ngay',
  TIMES: [[7, 30], [11, 45], [17, 0], [20, 30]],
  EVENT: 'dang_tin'
};
var SH_Q = 'CAU_NOI', SH_R = 'CAU_DO';

function _props() { return PropertiesService.getScriptProperties(); }
function _log(msg) {
  var p = _props(), arr = [];
  try { arr = JSON.parse(p.getProperty('LOG') || '[]'); } catch (e) {}
  arr.push(Utilities.formatDate(new Date(), 'Asia/Ho_Chi_Minh', 'yyyy-MM-dd HH:mm') + ' ' + msg);
  p.setProperty('LOG', JSON.stringify(arr.slice(-40)));
  Logger.log(msg);
}
function _ss() {
  var id = _props().getProperty('SHEET_ID');
  if (!id) throw new Error('Chưa có SHEET_ID: hãy chạy SETUP_SHEET một lần');
  return SpreadsheetApp.openById(id);
}

/** Chạy 1 lần: tạo Google Sheet dữ liệu và nạp sẵn nội dung từ kho GitHub. */
function SETUP_SHEET() {
  var p = _props();
  if (p.getProperty('SHEET_ID')) { Logger.log('Đã có Sheet: ' + SpreadsheetApp.openById(p.getProperty('SHEET_ID')).getUrl()); return; }
  var d = JSON.parse(UrlFetchApp.fetch('https://raw.githubusercontent.com/' + CFG.GH_REPO + '/main/data/content.json').getContentText());
  var ss = SpreadsheetApp.create('Sống vui mỗi ngày - Dữ liệu');
  var a = ss.getSheets()[0]; a.setName(SH_Q);
  var qa = [['Mã', 'Câu nói (Tiếng Việt)', 'Quote (English)', 'Dùng', 'Số lần đã đăng']];
  d.quotes.forEach(function (x) { qa.push([x.id, x.vi, x.en, true, 0]); });
  a.getRange(1, 1, qa.length, 5).setValues(qa);
  var b = ss.insertSheet(SH_R);
  var ra = [['Mã', 'Câu đố (Tiếng Việt)', 'Đáp án (Tiếng Việt)', 'Riddle (English)', 'Answer (English)', 'Dùng', 'Số lần đã đăng']];
  d.riddles.forEach(function (x) { ra.push([x.id, x.vi_q, x.vi_a, x.en_q, x.en_a, true, 0]); });
  b.getRange(1, 1, ra.length, 7).setValues(ra);
  a.getRange(2, 4, qa.length - 1, 1).insertCheckboxes();
  b.getRange(2, 6, ra.length - 1, 1).insertCheckboxes();
  [a, b].forEach(function (s) {
    s.setFrozenRows(1); s.getRange(1, 1, 1, s.getLastColumn()).setFontWeight('bold').setBackground('#FFE08A');
    s.getRange(2, 2, s.getLastRow(), 4).setWrap(true);
  });
  a.setColumnWidth(2, 420); a.setColumnWidth(3, 420); b.setColumnWidth(2, 340); b.setColumnWidth(3, 220); b.setColumnWidth(4, 340); b.setColumnWidth(5, 220);
  p.setProperty('SHEET_ID', ss.getId());
  _log('Đã tạo Sheet ' + ss.getUrl());
  Logger.log(ss.getUrl());
}

/** Chọn dòng đang bật có số lần đăng thấp nhất (ngẫu nhiên khi bằng nhau). */
function _pick(name, useCol, cntCol) {
  var sh = _ss().getSheetByName(name), n = sh.getLastRow() - 1;
  if (n < 1) throw new Error('Tab ' + name + ' chưa có dữ liệu');
  var v = sh.getRange(2, 1, n, sh.getLastColumn()).getValues(), best = [], bc = 1e9;
  for (var i = 0; i < v.length; i++) {
    var on = v[i][useCol - 1];
    if (!(on === true || String(on).toUpperCase() === 'TRUE')) continue;
    if (!String(v[i][1]).trim()) continue;
    var c = Number(v[i][cntCol - 1]) || 0;
    if (c < bc) { bc = c; best = [i]; } else if (c === bc) best.push(i);
  }
  if (!best.length) throw new Error('Tab ' + name + ' không còn dòng nào được bật');
  var k = best[Math.floor(Math.random() * best.length)];
  return { sheet: sh, row: k + 2, cntCol: cntCol, d: v[k].map(String) };
}
function _mark(x) { var r = x.sheet.getRange(x.row, x.cntCol); r.setValue((Number(r.getValue()) || 0) + 1); }

function _dispatch(payload) {
  var token = _props().getProperty('GH_TOKEN');
  if (!token) throw new Error('Thiếu Script Property GH_TOKEN');
  var r = UrlFetchApp.fetch('https://api.github.com/repos/' + CFG.GH_REPO + '/dispatches', {
    method: 'post', contentType: 'application/json', muteHttpExceptions: true,
    headers: { Authorization: 'Bearer ' + token, Accept: 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28' },
    payload: JSON.stringify({ event_type: CFG.EVENT, client_payload: payload })
  });
  var code = r.getResponseCode();
  _log('dispatch ' + (payload.ids || '') + ' preview=' + payload.preview + ' -> HTTP ' + code + (code === 204 ? '' : ' ' + r.getContentText().slice(0, 200)));
  return code;
}

function _send(preview, force) {
  var pid = _props().getProperty('PAGE_ID');
  if (!pid && !preview) throw new Error('Thiếu Script Property PAGE_ID');
  var q = _pick(SH_Q, 4, 5), r = _pick(SH_R, 6, 7);
  var code = _dispatch({
    page_id: pid || '', preview: String(preview), force: String(force),
    ids: q.d[0] + '/' + r.d[0], quote_vi: q.d[1], quote_en: q.d[2],
    r_vq: r.d[1], r_va: r.d[2], r_eq: r.d[3], r_ea: r.d[4]
  });
  if (code === 204 && !preview) { _mark(q); _mark(r); }
  return code;
}

/** Được đặt lịch gọi 4 lần/ngày. */
function POST_NOW() { return _send(false, false); }
/** Dựng video xem thử, KHÔNG đăng (xem video ở mục Artifacts của lần chạy trên GitHub). */
function PREVIEW_NOW() { return _send(true, false); }
/** Ép đăng ngay một tin (bỏ qua giới hạn 40 phút). */
function POST_FORCE() { return _send(false, true); }

/** Cài 4 lịch đăng mỗi ngày (chạy 1 lần). */
function SETUP_TRIGGERS() {
  ScriptApp.getProjectTriggers().forEach(function (t) { ScriptApp.deleteTrigger(t); });
  CFG.TIMES.forEach(function (hm) {
    ScriptApp.newTrigger('POST_NOW').timeBased().atHour(hm[0]).nearMinute(hm[1]).everyDays(1).inTimezone('Asia/Ho_Chi_Minh').create();
  });
  _log('Đã cài ' + CFG.TIMES.length + ' lịch đăng mỗi ngày');
}
function SHOW_LOG() { Logger.log(_props().getProperty('LOG')); }
