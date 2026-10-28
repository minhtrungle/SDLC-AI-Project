# Đặc tả Use Case — Chat với tài liệu (MVP)

> Bổ sung theo finding DF-08. Sơ đồ: [diagrams/use_case_diagram.drawio](diagrams/use_case_diagram.drawio). Checklist: [UseCase_Document_UML2.0_Checklist.xlsx](../checklists/UseCase_Document_UML2.0_Checklist.xlsx).
> Tiền điều kiện chung (trừ UC-01): người dùng đã đăng nhập, phiên còn hạn; mọi bước lỗi 401 đưa về SCR-06 và giữ câu hỏi đang soạn.

## UC-01 Đăng nhập / đăng xuất
| Mục | Nội dung |
|---|---|
| Actor | ACT-01 (chính), ACT-02 |
| Story / FR | US-101 · FR-001, FR-002, FR-019, NFR-010 |
| Trigger | Mở ứng dụng khi chưa có phiên |
| Tiền điều kiện | Tài khoản do quản trị tạo (UC-11) |
| Hậu điều kiện thành công | Có phiên trong `sessions` (token băm), cookie `HttpOnly; SameSite=Strict`, bản ghi `auth.login_success` |
| Luồng chính | 1. Hệ thống hiển thị SCR-01. 2. Người dùng nhập tên + mật khẩu. 3. Hệ thống kiểm tra khóa tạm. 4. Xác minh mật khẩu. 5. Tạo phiên, trả CSRF token. 6. Hiển thị SCR-02. |
| Luồng thay thế | 6a. Người dùng bấm "Đăng xuất" → xóa phiên, ghi `auth.logout`, về SCR-01. |
| Ngoại lệ | 3a. ≥ 5 lần sai trong 5 phút → 429, thông báo thử lại sau. 4a. Sai thông tin → 401, thông báo chung (không lộ tài khoản tồn tại), ghi `auth.login_failed`. |
| Quy tắc | BR-019; phiên hết hạn sau 8 giờ không hoạt động |
| NFR | NFR-010 |

## UC-02 Tải lên PDF
| Mục | Nội dung |
|---|---|
| Actor | ACT-01 |
| Story / FR | US-201, US-202 · FR-004, FR-005 |
| Trigger | Bấm "+ Tải lên PDF" hoặc kéo-thả file |
| Hậu điều kiện | Mỗi file hợp lệ có bản ghi `processing`, file trên đĩa, bản ghi `document.upload`; tác vụ nền được đăng ký |
| Luồng chính | 1. Người dùng chọn n file. 2. UI tải từng file, hiện tiến độ. 3. Với mỗi file, hệ thống kiểm tra: còn chỗ trong workspace → chữ ký `%PDF-` → dung lượng. 4. Lưu và trả kết quả từng file. 5. UI hiện tài liệu với trạng thái "Đang xử lý" (tiếp UC-03). |
| Ngoại lệ | 3a. Hết chỗ → `docs.limit_reached` cho file đó. 3b. Sai định dạng → `file.wrong_type`. 3c. Quá dung lượng → `file.too_large` kèm giới hạn. Các file khác trong lô không bị ảnh hưởng. 2a. Mất mạng → file đó báo lỗi, có thể tải lại. |
| Quy tắc | BRU-001, BRU-002 |

## UC-03 Xem danh sách và trạng thái
| Mục | Nội dung |
|---|---|
| Story / FR | US-203, US-204 · FR-006, FR-007 |
| Luồng chính | 1. UI tải danh sách. 2. Còn tài liệu `processing` → hỏi lại mỗi 2 giây. 3. Tác vụ nền đặt `ready` / `no_text` / `failed`. 4. UI cập nhật trạng thái (biểu tượng + chữ) không tải lại trang. |
| Ngoại lệ | 3a. PDF hỏng/mật khẩu → `failed` + lý do. 3b. Không có văn bản → `no_text`. 3c. Máy chủ khởi động lại khi đang xử lý → xử lý lại khi khởi động (ADR-008). |

## UC-04 Xóa tài liệu
| Mục | Nội dung |
|---|---|
| Story / FR | US-205 · FR-008, FR-019 |
| Luồng chính | 1. Bấm 🗑. 2. SCR-04 hỏi xác nhận. 3. Xác nhận. 4. Hệ thống xóa bản ghi, chunk, chỉ mục, file; ghi `document.delete`. 5. UI cập nhật danh sách và phạm vi. |
| Thay thế | 3a. Hủy / Esc → không làm gì. |
| Hậu điều kiện | Câu hỏi mới không dùng tài liệu này (BRU-004); lượt cũ hiển thị trích dẫn "tài liệu đã bị xóa" |

## UC-05 Đặt câu hỏi (include UC-12; extend UC-07, UC-13)
| Mục | Nội dung |
|---|---|
| Story / FR | US-301..304, US-306 · FR-009..FR-013 |
| Tiền điều kiện | ≥ 1 tài liệu `ready` trong phạm vi |
| Luồng chính | 1. Người dùng nhập câu hỏi, Enter. 2. UI tạo hội thoại nếu chưa có, gửi câu hỏi, hiện "Đang trả lời…". 3. Hệ thống kiểm tra câu hỏi và phạm vi. 4. UC-12 truy xuất chunk. 5. Sinh câu trả lời có `[n]`. 6. Kiểm tra trích dẫn với CSDL. 7. Lưu lượt, trả kết quả. 8. UI hiển thị câu trả lời + nguồn + nút đánh giá. |
| Thay thế | 4a. Không chunk nào đạt ngưỡng → `not_found`, không gọi bộ sinh. 6a. Không còn trích dẫn hợp lệ → `not_found`. 7a. Còn tài liệu đang xử lý trong phạm vi → kèm `warning = docs_processing`. |
| Ngoại lệ | 3a. Câu hỏi rỗng/quá 2000 ký tự → 422. 3b. Không có tài liệu sẵn sàng → 409. 5a. Bộ sinh ngoài lỗi/timeout/từ chối → 503, không lưu lượt; UI giữ câu hỏi và hiện "Gửi lại". |
| Quy tắc | BR-009, BR-010, BR-011, BRU-003 |
| NFR | NFR-001 (P90), NFR-002 (độ chính xác), NFR-003 |

## UC-06 Xem trích dẫn
| Story / FR | US-305 · FR-013 |
|---|---|
| Luồng chính | 1. Bấm `[n]` hoặc dòng nguồn. 2. Panel SCR-03 mở, tải đoạn gốc qua `getChunk`. 3. Hiển thị tên tài liệu, trang, đoạn văn. 4. Esc / "Đóng" → focus trở lại nút đã bấm. |
| Ngoại lệ | 2a. Tài liệu đã xóa → hiển thị "Tài liệu đã bị xóa" và đoạn trích đã lưu. |

## UC-09 Đánh giá câu trả lời
| Story / FR | US-501 · FR-017 |
|---|---|
| Luồng chính | 1. Bấm 👍 hoặc 👎. 2. (👎) nhập lý do tùy chọn ≤ 500 ký tự. 3. Hệ thống lưu/ghi đè đánh giá. 4. Nút hiển thị trạng thái `aria-pressed`. |
| Ngoại lệ | 3a. Lý do quá dài → 422 `feedback.invalid`. |

## UC-10 Xem số liệu sử dụng
| Actor | ACT-02 (vai trò `manager`) · US-502 · FR-018 |
|---|---|
| Luồng chính | 1. Bấm "Số liệu sử dụng". 2. Hệ thống tính theo tuần ISO (định nghĩa: blueprint §3.9.4). 3. SCR-05 hiển thị bảng 8 tuần. |
| Ngoại lệ | 2a. Không phải `manager` → 403; nút không hiển thị với người dùng thường. |

## UC-11 Quản trị qua CLI
| Actor | ACT-03 · US-103 · NFR-006, NFR-007 |
|---|---|
| Luồng | `create-user`, `seed-demo`, `backup <dir>`, `restore <dir>`, `prune-audit --days ≥ 90`. Đọc nhật ký kiểm toán: `sqlite3 data/cwd.db "SELECT * FROM audit_log ORDER BY id DESC LIMIT 100"`. |

## UC-12 Truy xuất và kiểm tra trích dẫn · UC-13 Sinh bằng LLM ngoài
Xem SAD §6.1 và blueprint §3.9 (thuật toán). UC-13 chỉ khả dụng khi `CWD_ALLOW_EXTERNAL_AI=true` + có API key (ADR-003); không có UC riêng cho US-102 vì đó là ràng buộc cấu hình, được kiểm chứng ở AC-102.1/102.2.
