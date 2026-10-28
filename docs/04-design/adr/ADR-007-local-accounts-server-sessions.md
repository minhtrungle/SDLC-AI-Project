# ADR-007 — Tài khoản cục bộ, phiên phía máy chủ, workspace riêng

- **Trạng thái:** Proposed — **High risk, cần review L3** · **Ngày:** 2026-10-28 · **Tác giả:** Agent (Claude)
- **Liên quan:** BR-019, BR-028, FR-001, FR-002, NFR-004, NFR-010; OQ-007

## Bối cảnh
- Chưa biết có SSO nội bộ không (câu hỏi cho IT, buổi 3).
- Mặc định OQ-007: workspace riêng từng người.

## Quyết định
1. Tài khoản do quản trị tạo bằng CLI (`python -m app.cli create-user`); không có tự đăng ký.
2. Mật khẩu: PBKDF2-HMAC-SHA256, 210 000 vòng, salt 16 byte ngẫu nhiên (thư viện chuẩn `hashlib`); so sánh hằng thời gian.
3. Phiên: token 32 byte ngẫu nhiên (`secrets`), chỉ lưu **băm SHA-256** trong bảng `sessions`; cookie `cwd_session` `HttpOnly; SameSite=Strict; Path=/` (+ `Secure` khi `CWD_COOKIE_SECURE=true`). Hết hạn sau 8 giờ không hoạt động.
4. CSRF: token riêng mỗi phiên, trả về khi đăng nhập và tại `GET /api/auth/me`; mọi `POST/PUT/DELETE` (trừ login) phải gửi header `X-CSRF-Token` khớp.
5. Giới hạn đăng nhập sai: 5 lần / 5 phút theo tên đăng nhập (bộ nhớ tiến trình).
6. Cô lập workspace: **mọi** truy vấn tài nguyên có điều kiện `user_id = :current_user`; không tìm thấy hoặc không thuộc người dùng đều trả 404.
7. Vai trò: `user`, `manager` (xem dashboard số liệu).

## Phương án đã cân nhắc
| Phương án | Lý do không chọn |
|---|---|
| JWT trong localStorage | Dễ bị XSS đánh cắp; khó thu hồi |
| SSO (OIDC) | Chưa có thông tin IdP; thêm sau bằng cách thay `app/auth.py` |

## Hệ quả
- (+) Thu hồi phiên tức thì (xóa dòng); không lộ token khi CSDL bị đọc.
- (−) Giới hạn đăng nhập sai mất khi khởi động lại; chấp nhận cho MVP một tiến trình.
- **Khó đảo ngược:** Trung bình — chuyển SSO cần đổi luồng đăng nhập, không đổi phân quyền.
