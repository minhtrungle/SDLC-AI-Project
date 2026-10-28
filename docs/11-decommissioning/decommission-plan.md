# Decommission plan — Chat với tài liệu

> Chuẩn bị sẵn theo Process §11. Thực hiện khi sản phẩm được thay thế hoặc ngừng. Owner phải ký trước khi bắt đầu bước 4.

## 1. Inventory
| Hạng mục | Vị trí | Ghi chú |
|---|---|---|
| Mã nguồn | Repo git, nhánh `main` | Lưu trữ (archive), không xóa |
| Dữ liệu ứng dụng | `CWD_DATA_DIR/cwd.db` | Tài liệu (chunk), câu hỏi/câu trả lời, phản hồi, nhật ký kiểm toán |
| File PDF | `CWD_DATA_DIR/files/` | Bản sao tài liệu kinh doanh |
| Bản sao lưu | Thư mục chia sẻ của IT (30 bản) | |
| Tài khoản & secret | Bảng `users`, biến môi trường (`ANTHROPIC_API_KEY` nếu có) | |
| Phụ thuộc bên ngoài | Anthropic API (chỉ khi đã bật), reverse proxy, lịch sao lưu, giám sát | |
| Người dùng phụ thuộc | Đội phát triển kinh doanh | Thông báo trước ≥ 2 tuần |

## 2. Lưu giữ và xóa dữ liệu
| Dữ liệu | Quyết định mặc định | Người quyết định |
|---|---|---|
| Nhật ký kiểm toán | Xuất CSV, lưu theo chính sách lưu trữ của tổ chức (≥ 90 ngày kể từ bản ghi cuối) | IT/Bảo mật |
| Số liệu sử dụng tổng hợp | Xuất dashboard 8 tuần cuối làm báo cáo đóng dự án | PO |
| PDF, chunk, hội thoại | **Xóa** (bản gốc đã có ở kho tài liệu của đội); không chuyển đi nơi khác | PO + IT |
| Bản sao lưu | Xóa sau khi hết hạn lưu giữ nhật ký | IT |

## 3. Các bước
1. Thông báo người dùng, đặt ngày ngừng.
2. Chuyển sang chỉ đọc: đặt `CWD_MAX_DOCS=0` (không tải lên được); khởi động lại.
3. Xuất nhật ký kiểm toán + số liệu sử dụng.
4. **(Cần owner ký)** Dừng dịch vụ, gỡ dịch vụ khỏi Task Scheduler/systemd, gỡ cấu hình reverse proxy, tắt giám sát và lịch sao lưu.
5. Thu hồi: xóa `ANTHROPIC_API_KEY` khỏi máy chủ và vô hiệu hóa key trên Anthropic Console; xóa tài khoản dịch vụ.
6. Xóa an toàn `CWD_DATA_DIR` (ghi đè/xóa theo chuẩn IT) và các bản sao lưu đến hạn.
7. Cập nhật tài liệu: đánh dấu SAD, runbook "Retired"; cập nhật deployment diagram.
8. Ghi decommission record bên dưới.

## 4. Decommission record
| Mục | Giá trị |
|---|---|
| Ngày ngừng | |
| Dữ liệu đã xuất (vị trí) | |
| Dữ liệu đã xóa (bằng chứng) | |
| Secret đã thu hồi | |
| Owner ký | |
