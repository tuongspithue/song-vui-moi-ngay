/** Sống vui mỗi ngày - Apps Script (bản 2: gameshow Mèo Vui + Robot Tây).
 *  Lấy nội dung từ Google Sheet, mỗi ngày 4 tin theo giờ, gọi GitHub Actions dựng và đăng Reel.
 *  Script Properties: GH_TOKEN (thầy tự nhập), PAGE_ID. Script gắn trực tiếp trong Google Sheet dữ liệu.
 *  Các tab: CAU_DO (câu đố + câu Robot đoán sai), EMOJI (đuổi hình bắt chữ), CAU_NOI (câu nói vui, đưa vào chú thích).
 *  Thêm/sửa/xoá dòng thoải mái; bỏ tích cột "Dùng" = tạm không đăng; bot luôn chọn dòng có "Số lần đã đăng" thấp nhất.
 *  Cột "Mùa" (dd/MM-dd/MM, ví dụ 19/11-20/11): dòng đó chỉ đăng trong khoảng ngày ấy và được ưu tiên đăng trước.
 *  Lịch: 6:30 Tìm emoji khác biệt · 11:45 Mèo đố · 17:00 Đuổi hình bắt chữ · 19:30 Mèo đố. */
var CFG = {
  GH_REPO: 'tuongspithue/song-vui-moi-ngay',
  TIMES: [[6, 30], [11, 45], [17, 0], [19, 30]],
  KINDS: ['odd', 'meo', 'emoji', 'meo'],   // loạt ứng với từng giờ ở TIMES
  THINK: 8,                               // số giây cho người xem suy nghĩ (4-12)
  EVENT: 'dang_tin'
};
var SH_Q = 'CAU_NOI', SH_R = 'CAU_DO', SH_E = 'EMOJI';
var EMOJI_KINDS = { TN: 'Thành ngữ', TU: 'Tục ngữ', MA: 'Món ăn', DD: 'Địa danh', VH: 'Văn hoá', GC: 'Ghép chữ' };

function _props() { return PropertiesService.getScriptProperties(); }
function _log(msg) {
  var p = _props(), arr = [];
  try { arr = JSON.parse(p.getProperty('LOG') || '[]'); } catch (e) {}
  arr.push(Utilities.formatDate(new Date(), 'Asia/Ho_Chi_Minh', 'yyyy-MM-dd HH:mm') + ' ' + msg);
  p.setProperty('LOG', JSON.stringify(arr.slice(-40)));
  Logger.log(msg);
}
function _ss() {
  var a = SpreadsheetApp.getActiveSpreadsheet();
  if (a) return a;
  var id = _props().getProperty('SHEET_ID');
  if (!id) throw new Error('Script chưa gắn Sheet');
  return SpreadsheetApp.openById(id);
}
function _style(s, wide) {
  s.setFrozenRows(1); s.getRange(1, 1, 1, s.getLastColumn()).setFontWeight('bold').setBackground('#FFE08A');
  s.getRange(2, 2, Math.max(1, s.getLastRow() - 1), s.getLastColumn() - 1).setWrap(true).setVerticalAlignment('top');
  wide.forEach(function (w, i) { if (w) s.setColumnWidth(i + 1, w); });
}

/** Chạy 1 lần nếu Sheet còn trống: nạp câu nói vui gốc, rồi nạp bộ câu hỏi mới. */
function SETUP_SHEET() {
  var ss = _ss(), old = ss.getSheetByName(SH_Q);
  if (!(old && old.getLastRow() > 1)) {
    var d = JSON.parse(UrlFetchApp.fetch('https://raw.githubusercontent.com/' + CFG.GH_REPO + '/main/data/content.json').getContentText());
    var a = old || ss.getSheets()[0]; a.setName(SH_Q); a.clear();
    var qa = [['Mã', 'Câu nói (Tiếng Việt)', 'Quote (English)', 'Dùng', 'Số lần đã đăng']];
    d.quotes.forEach(function (x) { qa.push([x.id, x.vi, x.en, true, 0]); });
    a.getRange(1, 1, qa.length, 5).setValues(qa);
    a.getRange(2, 4, qa.length - 1, 1).insertCheckboxes();
    _style(a, [70, 420, 420]);
  }
  UPDATE_DATA();
}

/** Nạp/cập nhật bộ câu hỏi từ kho GitHub (data/content_v2.json) vào Sheet.
 *  Giữ nguyên cột "Dùng" và "Số lần đã đăng" của các dòng đã có; dòng thầy tự thêm (mã khác) không bị đụng tới. */
function UPDATE_DATA() {
  var ss = _ss();
  var d = JSON.parse(UrlFetchApp.fetch('https://raw.githubusercontent.com/' + CFG.GH_REPO + '/main/data/content_v2.json?t=' + Date.now()).getContentText());
  // ----- CAU_DO
  var sh = ss.getSheetByName(SH_R) || ss.insertSheet(SH_R);
  sh.getRange(1, 1, 1, 11).setValues([['Mã', 'Câu đố (Tiếng Việt)', 'Đáp án (Tiếng Việt)', 'Riddle (English)', 'Answer (English)', 'Dùng', 'Số lần đã đăng',
    'Robot đoán sai (English)', 'Robot đoán sai (Tiếng Việt)', 'Chỉ tiếng Việt', 'Mùa (dd/MM-dd/MM)']]);
  var n = sh.getLastRow() - 1, v = n > 0 ? sh.getRange(2, 1, n, 11).getValues() : [], idx = {}, add = [], upd = 0, off = 0;
  v.forEach(function (row, i) { idx[String(row[0]).trim()] = i; });
  d.riddles.forEach(function (r) {
    var i = idx[r.id];
    if (i === undefined) add.push([r.id, r.vi_q, r.vi_a, r.en_q, r.en_a, true, 0, r.g_en, r.g_vi, !!r.vi_only, r.season || '']);
    else { var row = v[i]; row[1] = r.vi_q; row[2] = r.vi_a; row[3] = r.en_q; row[4] = r.en_a; row[7] = r.g_en; row[8] = r.g_vi; row[9] = !!r.vi_only; if (!String(row[10]).trim()) row[10] = r.season || ''; upd++; }
  });
  (d.riddles_off || []).forEach(function (id) { var i = idx[id]; if (i !== undefined && v[i][5] !== false) { v[i][5] = false; off++; } });
  v.forEach(function (row) { if (row[9] === '') row[9] = false; if (row[5] === '') row[5] = true; });
  sh.getRange(2, 11, Math.max(1, sh.getMaxRows() - 1), 1).setNumberFormat('@');
  if (v.length) sh.getRange(2, 1, v.length, 11).setValues(v);
  if (add.length) sh.getRange(v.length + 2, 1, add.length, 11).setValues(add);
  var tot = v.length + add.length;
  sh.getRange(2, 6, tot, 1).insertCheckboxes(); sh.getRange(2, 10, tot, 1).insertCheckboxes();
  _style(sh, [70, 340, 220, 340, 220, 60, 90, 240, 240, 90, 130]);
  // ----- EMOJI
  var es = ss.getSheetByName(SH_E) || ss.insertSheet(SH_E);
  es.getRange(1, 1, 1, 11).setValues([['Mã', 'Emoji (cách nhau bằng dấu cách)', 'Loại', 'Đáp án (Tiếng Việt)', 'Nghĩa đen (English)', 'Ý nghĩa (English)',
    'Robot đoán sai (English)', 'Robot đoán sai (Tiếng Việt)', 'Dùng', 'Số lần đã đăng', 'Mùa (dd/MM-dd/MM)']]);
  var m = es.getLastRow() - 1, ev = m > 0 ? es.getRange(2, 1, m, 11).getValues() : [], eidx = {}, eadd = [];
  ev.forEach(function (row, i) { eidx[String(row[0]).trim()] = i; });
  d.emoji.forEach(function (e) {
    var kind = EMOJI_KINDS[e.kind] || e.kind, i = eidx[e.id];
    if (i === undefined) eadd.push([e.id, e.emoji, kind, e.vi, e.en, e.mean, e.g_en, e.g_vi, true, 0, e.season || '']);
    else { var row = ev[i]; row[1] = e.emoji; row[2] = kind; row[3] = e.vi; row[4] = e.en; row[5] = e.mean; row[6] = e.g_en; row[7] = e.g_vi; if (!String(row[10]).trim()) row[10] = e.season || ''; }
  });
  es.getRange(2, 11, Math.max(1, es.getMaxRows() - 1), 1).setNumberFormat('@');
  if (ev.length) es.getRange(2, 1, ev.length, 11).setValues(ev);
  if (eadd.length) es.getRange(ev.length + 2, 1, eadd.length, 11).setValues(eadd);
  es.getRange(2, 9, ev.length + eadd.length, 1).insertCheckboxes();
  es.getRange(2, 2, ev.length + eadd.length, 1).setFontSize(16);
  _style(es, [70, 190, 100, 260, 300, 300, 260, 260, 60, 90, 130]);
  _log('UPDATE_DATA: câu đố thêm ' + add.length + ', cập nhật ' + upd + ', tắt ' + off + ' | emoji thêm ' + eadd.length + ', tổng ' + (ev.length + eadd.length));
}

/** Khoảng ngày "dd/MM-dd/MM" có chứa hôm nay không. Trả về null nếu ô trống hoặc sai định dạng. */
function _inSeason(txt) {
  var m = String(txt || '').replace(/\s/g, '').match(/^(\d{1,2})\/(\d{1,2})-(\d{1,2})\/(\d{1,2})$/);
  if (!m) return null;
  var t = Number(Utilities.formatDate(new Date(), 'Asia/Ho_Chi_Minh', 'MMdd'));
  var a = Number(m[2]) * 100 + Number(m[1]), b = Number(m[4]) * 100 + Number(m[3]);
  return a <= b ? (t >= a && t <= b) : (t >= a || t <= b);
}

/** Chọn dòng đang bật có số lần đăng thấp nhất (ngẫu nhiên khi bằng nhau).
 *  Dòng có cột "Mùa": ngoài mùa thì bỏ qua; trong mùa thì được ưu tiên nếu chưa đăng nhiều hơn các dòng thường. */
function _pick(name, useCol, cntCol, seasonCol) {
  var sh = _ss().getSheetByName(name), n = sh ? sh.getLastRow() - 1 : 0;
  if (n < 1) throw new Error('Tab ' + name + ' chưa có dữ liệu (chạy UPDATE_DATA)');
  var v = sh.getRange(2, 1, n, Math.max(sh.getLastColumn(), cntCol, seasonCol || 1)).getValues();
  var best = [], bc = 1e9, sBest = [], sc = 1e9;
  for (var i = 0; i < v.length; i++) {
    var on = v[i][useCol - 1];
    if (!(on === true || String(on).toUpperCase() === 'TRUE')) continue;
    if (!String(v[i][1]).trim()) continue;
    var c = Number(v[i][cntCol - 1]) || 0, ss = seasonCol ? _inSeason(v[i][seasonCol - 1]) : null;
    if (ss === false) continue;
    if (ss === true) { if (c < sc) { sc = c; sBest = [i]; } else if (c === sc) sBest.push(i); }
    else if (c < bc) { bc = c; best = [i]; } else if (c === bc) best.push(i);
  }
  if (sBest.length && (sc <= bc || !best.length)) best = sBest;
  if (!best.length) throw new Error('Tab ' + name + ' không còn dòng nào được bật');
  var k = best[Math.floor(Math.random() * best.length)];
  return { sheet: sh, row: k + 2, cntCol: cntCol, d: v[k].map(function (x) { return x === null || x === undefined ? '' : String(x); }) };
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

/** Loạt ứng với giờ hiện tại (lấy mốc giờ gần nhất trong CFG.TIMES). */
function _kindNow() {
  var now = new Date(), tz = 'Asia/Ho_Chi_Minh';
  var h = Number(Utilities.formatDate(now, tz, 'H')) + Number(Utilities.formatDate(now, tz, 'm')) / 60, best = 0, bd = 99;
  CFG.TIMES.forEach(function (hm, i) { var dd = Math.abs(h - (hm[0] + hm[1] / 60)); if (dd < bd) { bd = dd; best = i; } });
  return CFG.KINDS[best];
}

function _send(preview, force, kind) {
  var pid = _props().getProperty('PAGE_ID');
  if (!pid && !preview) throw new Error('Thiếu Script Property PAGE_ID');
  kind = kind || _kindNow();
  var marks = [], data = { think: CFG.THINK }, ids = kind;
  try { var q = _pick(SH_Q, 4, 5); data.q_vi = q.d[1]; data.q_en = q.d[2]; marks.push(q); } catch (e) { _log('Không lấy được câu nói vui: ' + e); }
  if (kind === 'meo') {
    var r = _pick(SH_R, 6, 7, 11); marks.push(r); ids = 'meo/' + r.d[0];
    data.id = r.d[0]; data.vq = r.d[1]; data.va = r.d[2]; data.eq = r.d[3]; data.ea = r.d[4];
    data.g_en = r.d[7] || ''; data.g_vi = r.d[8] || ''; data.vi_only = r.d[9] || '';
  } else if (kind === 'emoji') {
    var e = _pick(SH_E, 9, 10, 11); marks.push(e); ids = 'emoji/' + e.d[0];
    data.id = e.d[0]; data.emoji = e.d[1]; data.kind = e.d[2]; data.vi = e.d[3]; data.en = e.d[4]; data.mean = e.d[5];
    data.g_en = e.d[6] || ''; data.g_vi = e.d[7] || '';
  }
  if (kind === 'tuan') ids = 'tuan';  // tổng hợp 5 câu đố trong tuần, bot tự lấy từ lịch sử đã đăng
  var code = _dispatch({ page_id: pid || '', preview: String(preview), force: String(force), kind: kind, ids: ids, data: data });
  if (code === 204 && !preview) marks.forEach(_mark);
  return code;
}

/** Được đặt lịch gọi 4 lần/ngày (loạt tự chọn theo giờ). */
function POST_NOW() { return _send(false, false); }
/** Dựng video xem thử, KHÔNG đăng (xem video ở mục Artifacts của lần chạy trên GitHub). */
function PREVIEW_NOW() { return _send(true, false); }
function PREVIEW_MEO() { return _send(true, false, 'meo'); }
function PREVIEW_EMOJI() { return _send(true, false, 'emoji'); }
function PREVIEW_ODD() { return _send(true, false, 'odd'); }
/** Ép đăng ngay một tin (bỏ qua giới hạn 40 phút). */
function POST_FORCE() { return _send(false, true); }
function POST_MEO() { return _send(false, true, 'meo'); }
function POST_EMOJI() { return _send(false, true, 'emoji'); }
function POST_ODD() { return _send(false, true, 'odd'); }
/** Câu đố của tuần (Chủ nhật 20:45): tổng hợp 5 câu Mèo đố đã đăng trong tuần. */
function POST_TUAN() { return _send(false, false, 'tuan'); }
function PREVIEW_TUAN() { return _send(true, false, 'tuan'); }

/** Cài 4 lịch đăng mỗi ngày (chạy 1 lần, hoặc sau khi đổi giờ ở CFG.TIMES). */
function SETUP_TRIGGERS() {
  ScriptApp.getProjectTriggers().forEach(function (t) { ScriptApp.deleteTrigger(t); });
  CFG.TIMES.forEach(function (hm) {
    ScriptApp.newTrigger('POST_NOW').timeBased().atHour(hm[0]).nearMinute(hm[1]).everyDays(1).inTimezone('Asia/Ho_Chi_Minh').create();
  });
  ScriptApp.newTrigger('POST_TUAN').timeBased().onWeekDay(ScriptApp.WeekDay.SUNDAY).atHour(20).nearMinute(45).inTimezone('Asia/Ho_Chi_Minh').create();
  _log('Đã cài ' + CFG.TIMES.length + ' lịch đăng mỗi ngày + Câu đố của tuần Chủ nhật 20:45');
}
function SHOW_LOG() { Logger.log(_props().getProperty('LOG')); }
