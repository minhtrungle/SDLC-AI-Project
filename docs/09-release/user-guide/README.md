# Hướng dẫn sử dụng — Chat với tài liệu (MVP)

**Chat với tài liệu** là ứng dụng web cho phép bạn tải lên các file PDF rồi đặt câu hỏi bằng tiếng Việt. Câu trả lời **chỉ dựa trên nội dung tài liệu bạn đã tải lên** và luôn kèm **trích dẫn tên tài liệu + số trang** để bạn kiểm chứng. Mặc định mọi xử lý diễn ra trên máy chủ nội bộ, không gửi dữ liệu ra ngoài.

![Câu trả lời kèm trích dẫn](images/tra-loi-trich-dan.png)

## Mục lục

| Bạn là… | Đọc |
|---|---|
| Người dùng mới | [01 — Bắt đầu: đăng nhập và làm quen giao diện](01-bat-dau.md) |
| Người dùng | [02 — Quản lý tài liệu](02-quan-ly-tai-lieu.md) |
| Người dùng | [03 — Hỏi đáp với tài liệu](03-hoi-dap.md) |
| Quản lý (vai trò `manager`) | [04 — Xem số liệu sử dụng](04-so-lieu-su-dung.md) |
| Quản trị viên / IT | [05 — Cài đặt, tài khoản, sao lưu, cấu hình](05-quan-tri.md) |
| Mọi người | [06 — Thông báo lỗi và cách xử lý](06-loi-thuong-gap.md) |

## Bắt đầu nhanh trong 3 bước

1. **Đăng nhập** bằng tài khoản quản trị viên cấp cho bạn.
2. **Tải lên PDF** — bấm **+ Tải lên PDF** hoặc kéo thả file vào ô bên trái; chờ trạng thái chuyển sang **✓ Sẵn sàng**.
3. **Đặt câu hỏi** ở ô dưới cùng, nhấn **Enter**. Bấm vào **[1]**, **[2]**… để xem đoạn văn gốc.

## Giới hạn của phiên bản MVP

| Hạng mục | Giới hạn mặc định |
|---|---|
| Định dạng tài liệu | Chỉ PDF có lớp văn bản (PDF scan dạng ảnh không đọc được) |
| Dung lượng mỗi file | 20 MB |
| Số tài liệu mỗi người dùng | 50 |
| Độ dài câu hỏi | 2.000 ký tự |
| Phiên đăng nhập | Tự hết hạn sau 8 giờ không hoạt động |

Quản trị viên có thể thay đổi các giới hạn này (xem [05-quan-tri.md](05-quan-tri.md)).

## Quyền riêng tư
- Mỗi người dùng chỉ thấy tài liệu và hội thoại **của chính mình**.
- Hệ thống không ghi nội dung câu hỏi, câu trả lời hay văn bản tài liệu vào nhật ký.
- Huy hiệu **🔒 Xử lý cục bộ** ở góc trên cho biết nội dung không được gửi tới dịch vụ AI bên ngoài.
