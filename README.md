# Sống vui mỗi ngày

Bot đăng Reel song ngữ Việt - Anh: một slide gồm câu nói vui (kèm tiếng cười) và một câu đố vui. Đáp án của tin trước được bình luận ngay sau khi tin sau lên sóng.

- `reel/make.py`: chọn nội dung, vẽ slide (17 giao diện đổi phông/màu), đọc giọng Việt + Anh (edge-tts), ghép tiếng cười + tiếng tích tắc, dựng MP4 9:16, đăng Reel, bình luận đáp án tin trước.
- `data/content.json`: 193 câu nói vui + 110 câu đố đã lọc.
- `state.json`: bộ đếm tin, lịch sử, hàng đợi đáp án chờ bình luận (workflow tự cập nhật).
- `.github/workflows/post.yml`: chạy khi Apps Script gửi lệnh `dang_tin`, hoặc chạy tay (mặc định chỉ xem thử).
- `assets/laugh/`: (tuỳ chọn) bỏ tệp tiếng cười thật (.mp3/.wav) vào đây thì bot dùng thay cho tiếng cười tổng hợp.

Secrets cần có: `FB_PAGE_TOKEN_SVMN` (mã truy cập Trang), `FB_PAGE_ID` (mã số Trang).
