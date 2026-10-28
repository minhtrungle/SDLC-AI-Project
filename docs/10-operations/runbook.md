# Runbook vận hành — Chat với tài liệu

> Đối tượng: IT vận hành (ACT-03). Agent **không** thay đổi production (Process §10).

## 1. Cài đặt và khởi động
```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt     # Linux: .venv/bin/python
set CWD_DATA_DIR=D:\cwd-data                                # Linux: export CWD_DATA_DIR=/srv/cwd-data
set CWD_COOKIE_SECURE=true
.venv/Scripts/python -m app.cli create-user --username <tên> --role user      # nhập mật khẩu ẩn
.venv/Scripts/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000     # sau reverse proxy TLS
```
Chạy như dịch vụ: Windows dùng NSSM hoặc Task Scheduler "At startup"; Linux dùng systemd (`Restart=on-failure`). **Một worker duy nhất** (ADR-008).

## 2. Cấu hình
Xem SAD §8.5. Thay đổi cấu hình cần khởi động lại. **Không** đặt `CWD_ALLOW_EXTERNAL_AI=true` khi chưa có văn bản phê duyệt của IT/Bảo mật.

## 3. Giám sát
| Tín hiệu | Cách lấy | Ngưỡng cảnh báo |
|---|---|---|
| Sức khỏe | `GET /api/health` mỗi phút | 2 lần liên tiếp không phải 200 |
| Lỗi máy chủ | Log stdout, logger `cwd.error`, dòng `cwd.access` có `"status": 5xx` | > 5 lỗi / 10 phút |
| Độ trễ hỏi đáp | `turns.latency_ms`: `SELECT max(latency_ms) FROM turns WHERE created_at > datetime('now','-1 hour')` | P90 > 2 000 ms (local) / 15 000 ms (external) |
| Tài liệu kẹt | `SELECT count(*) FROM documents WHERE status='processing' AND created_at < datetime('now','-10 minutes')` | > 0 |
| Đĩa | Dung lượng còn trống của `CWD_DATA_DIR` | < 20% |
| Sử dụng | Dashboard "Số liệu sử dụng" (vai trò manager) | `not_found_rate` > 40% trong tuần |

Log không chứa nội dung tài liệu/câu hỏi (NFR-008) — có thể chuyển sang hệ thống log tập trung.

## 4. Đọc nhật ký kiểm toán (US-103)
```bash
sqlite3 %CWD_DATA_DIR%\cwd.db "SELECT created_at, username, action, target FROM audit_log ORDER BY id DESC LIMIT 100;"
```
Dọn bản ghi cũ (giữ tối thiểu 90 ngày — NFR-007): `python -m app.cli prune-audit --days 90` (đặt lịch hằng tháng).

## 5. Sao lưu và khôi phục (NFR-006, RPO 24 h, RTO 4 h)
- **Hằng ngày 01:00:** `python -m app.cli backup \\nas\cwd-backup\%DATE%` — giữ 30 bản, xóa bản cũ hơn.
- **Khôi phục:**
  1. Dừng dịch vụ.
  2. `python -m app.cli restore \\nas\cwd-backup\<ngày>` (ghi đè `cwd.db` và `files/`).
  3. Khởi động dịch vụ; kiểm tra `/api/health`, đăng nhập, mở danh sách tài liệu, hỏi 1 câu.
  4. Ghi biên bản (thời điểm sự cố, bản sao lưu dùng, dữ liệu mất ước tính).
- **Diễn tập:** mỗi quý, khôi phục vào máy thử, đo thời gian (QS-07).

## 6. Xử lý sự cố
| Triệu chứng | Chẩn đoán | Xử lý |
|---|---|---|
| Không đăng nhập được, báo "nhập sai quá nhiều lần" | Khóa tạm 5 phút theo tên đăng nhập | Chờ 5 phút hoặc khởi động lại dịch vụ (xóa bộ đếm trong bộ nhớ) |
| Tài liệu "Đang xử lý" mãi | Tiến trình chết giữa chừng | Khởi động lại — tài liệu được xử lý lại tự động (ADR-008); nếu file gốc mất → `failed` + `ingest.interrupted` |
| "Dịch vụ trả lời đang gặp sự cố" (503) | Chỉ ở chế độ external: timeout/lỗi Anthropic API | Kiểm tra kết nối ra ngoài, API key; tạm tắt `CWD_ALLOW_EXTERNAL_AI` để về chế độ cục bộ |
| `database is locked` trong log | Ghi đồng thời quá lâu | Kiểm tra không chạy 2 worker; sao lưu không giữ khóa lâu |
| Nghi rò rỉ dữ liệu / truy cập trái phép | — | **Sev1**: dừng dịch vụ, giữ nguyên `cwd.db` + log, báo IT/Bảo mật, tạo incident record |

Mức độ: **Sev1** bảo mật hoặc mất dữ liệu · **Sev2** không ai dùng được · **Sev3** một chức năng lỗi · **Sev4** khó chịu nhỏ.
Sau mỗi sự cố Sev1/Sev2: post-incident review trong 5 ngày làm việc, dùng [incident-record-template.md](incident-record-template.md); bài học đưa vào test, tài liệu, runbook; nếu cần thay đổi sản phẩm → tạo `intent.md` mới (Process §10).

## 7. Quản lý tài khoản
- Tạo: `python -m app.cli create-user --username <tên> [--role manager]`.
- Vô hiệu hóa (MVP chưa có lệnh riêng): `sqlite3 cwd.db "DELETE FROM sessions WHERE user_id=(SELECT id FROM users WHERE username='<tên>'); UPDATE users SET password_hash='disabled' WHERE username='<tên>';"` — đăng nhập sẽ luôn thất bại; dữ liệu được giữ.
