# 05 — Hướng dẫn quản trị (IT / quản trị viên)

## Yêu cầu hệ thống
- Python ≥ 3.12, Node.js ≥ 22.12 (chỉ để build giao diện).
- Không cần Docker, CSDL ngoài hay API key. Dữ liệu lưu trong SQLite và thư mục file trên đĩa.

## Cài đặt và khởi động
Từ thư mục gốc mã nguồn:

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r app/backend/requirements-dev.txt     # Linux/macOS: .venv/bin/python
npm ci --prefix app/frontend && npm run build --prefix app/frontend        # build giao diện

cd app/backend
../../.venv/Scripts/python -m uvicorn cwd.main:app                          # http://127.0.0.1:8000
```

Khi triển khai cho nhiều người dùng, đặt ứng dụng sau reverse proxy có **HTTPS** và bật `CWD_COOKIE_SECURE=true`.

## Quản lý tài khoản
Chạy trong `app/backend`:

| Việc | Lệnh |
|---|---|
| Tạo người dùng thường | `../../.venv/Scripts/python -m cwd.cli create-user --username linh` (mật khẩu được hỏi ẩn) |
| Tạo tài khoản quản lý | `… create-user --username hung --role manager` |
| Tạo tài khoản demo | `… seed-demo` — tạo `linh` (user) và `hung` (manager), **in mật khẩu ngẫu nhiên ra màn hình một lần** |

- Mật khẩu tối thiểu 8 ký tự; lưu dạng băm, quản trị viên không xem lại được.
- Tên đăng nhập đã tồn tại → lệnh báo lỗi, không ghi đè.
- Không truyền `--password` trên dòng lệnh ở môi trường thật (sẽ nằm trong lịch sử shell); để trống để nhập ẩn.

## Sao lưu và khôi phục

| Việc | Lệnh | Ghi chú |
|---|---|---|
| Sao lưu | `… backup <thư mục>` | Chạy được khi ứng dụng **đang chạy**; chép CSDL và toàn bộ file PDF |
| Khôi phục | `… restore <thư mục>` | Phải **dừng dịch vụ** trước. Bản sao lưu được kiểm tra toàn vẹn trước; nếu hỏng, dữ liệu hiện tại **không bị thay đổi** |

Khuyến nghị: sao lưu hằng ngày ra **đĩa khác** với thư mục dữ liệu, và thử khôi phục định kỳ.

## Nhật ký kiểm toán
Hệ thống ghi các sự kiện đăng nhập thành công/thất bại, tải lên, xóa tài liệu (người dùng, thời điểm, mã tài liệu) — **không** ghi nội dung câu hỏi hay tài liệu.

Dọn nhật ký cũ: `… prune-audit --days 180`. Hệ thống bắt buộc giữ tối thiểu **90 ngày**; giá trị nhỏ hơn bị từ chối.

## Cấu hình (biến môi trường)

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `CWD_DATA_DIR` | `data` | Thư mục chứa `cwd.db` và `files/` |
| `CWD_MAX_FILE_MB` | `20` | Dung lượng tối đa mỗi PDF |
| `CWD_MAX_DOCS` | `50` | Số tài liệu tối đa mỗi người dùng |
| `CWD_MAX_QUESTION_CHARS` | `2000` | Độ dài tối đa câu hỏi |
| `CWD_SESSION_IDLE_HOURS` | `8` | Số giờ không hoạt động trước khi phiên hết hạn |
| `CWD_COOKIE_SECURE` | `false` | Đặt `true` khi chạy sau HTTPS |
| `CWD_ALLOW_EXTERNAL_AI` | `false` | Cho phép gọi dịch vụ AI bên ngoài |
| `ANTHROPIC_API_KEY` | — | Chỉ có tác dụng khi `CWD_ALLOW_EXTERNAL_AI=true` |
| `CWD_ANTHROPIC_MODEL` | `claude-opus-5-5` | Model dùng ở chế độ AI bên ngoài |
| `CWD_ANSWER_TIMEOUT_S` | `15` | Thời gian chờ tối đa khi gọi AI bên ngoài |
| `CWD_MIN_RELEVANCE`, `CWD_TOP_K`, `CWD_PER_DOC_LIMIT` | `0.6`, `6`, `2` | Tinh chỉnh truy hồi — chỉ đổi khi có bộ đánh giá đi kèm |

### Chế độ AI bên ngoài
Mặc định ứng dụng chạy **hoàn toàn cục bộ** (huy hiệu **🔒 Xử lý cục bộ**). Chỉ khi đặt **cả** `CWD_ALLOW_EXTERNAL_AI=true` **và** `ANTHROPIC_API_KEY`, đoạn trích tài liệu liên quan mới được gửi tới dịch vụ AI bên ngoài; huy hiệu đổi thành **☁ Dùng dịch vụ AI bên ngoài**. Chỉ bật khi bộ phận Bảo mật/Pháp chế đã phê duyệt. Có API key nhưng không bật cờ thì vẫn chạy cục bộ.

## Kiểm tra sức khỏe nhanh
- Mở trang chủ thấy màn hình đăng nhập.
- Đăng nhập bằng tài khoản thử, tải một PDF nhỏ, chờ **✓ Sẵn sàng**, hỏi một câu có trong tài liệu và thấy trích dẫn.
