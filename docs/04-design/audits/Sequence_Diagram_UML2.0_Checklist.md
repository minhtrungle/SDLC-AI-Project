# Audit — Sequence Diagram theo checklist UML 2

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | docs/04-design/diagrams/sequence_diagram.drawio (trang "Hỏi đáp", "Đăng nhập"); đối chiếu SAD §6.1, §6.4, openapi.yaml |
| Checklist | docs/design/Sequence_Diagram_UML2.0_Checklist.xlsx |
| Reviewer | Independent reviewer agent |
| Ngày | 2026-10-28 |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Diagram Name | Done | Tên trang "Hỏi đáp" và "Đăng nhập" ứng với US-301..305 và US-101. Không có khung "sd <tên>". |
| 3 | Time Axis | Done | Thông điệp đánh số 1..16 từ trên xuống, cách đều 44 px. |
| 4 | Lifeline Notation | Done | shape=umlLifeline (đầu chữ nhật + đường đứt). |
| 5 | Naming Convention | Pending | Lifeline đặt "CMP-08 Chat Service", không theo "tên : Lớp" (vd. "chat : ChatService", "retriever : FtsRetriever"). |
| 6 | Actor vs. System | Pending | ACT-01 Người dùng vẽ bằng lifeline chữ nhật giống đối tượng hệ thống, không dùng hình người. |
| 7 | Synchronous Messages | Done | Nét liền, mũi tên đặc (endArrow=block, endFill=1). |
| 8 | Asynchronous Messages | N/A | Hai luồng này đồng bộ; luồng nền (BackgroundTasks) không nằm trong sequence. |
| 9 | Return/Reply Messages | Done | Nét đứt mũi tên mở (4, 6, 9, 10, 12, 15, 16). Trang Đăng nhập thiếu reply cho "4: SELECT users". |
| 10 | Self Messages | In Progress | 11a, 13 (Hỏi đáp) và 3, 5 (Đăng nhập) vẽ bằng mũi tên chéo ngắn (vd. 690,590 → 750,606), không phải vòng chữ U quay về lifeline. |
| 11 | Creation & Destruction | N/A | Không tạo/hủy đối tượng trong luồng (INSERT là thao tác dữ liệu). |
| 12 | Message Signatures | In Progress | Trộn chữ ký và văn xuôi: "5: kiểm tra hội thoại thuộc user, có tài liệu ready" gửi tới Persistence; "7: retrieve(question, 3 câu trước, phạm vi)" không khớp chữ ký retrieve(conn, user_id, question, history, document_ids). |
| 13 | Activation Boxes | Pending | Không có activation bar trên lifeline nào. |
| 14 | Overlapping Activations | Pending | Không có activation (xem row 13). |
| 15 | Frame Notation | In Progress | Khung alt là hình chữ nhật thường với chữ "alt [..]" ở đỉnh, không có ô ngũ giác toán tử. |
| 16 | Alternative (alt) | In Progress | Vẽ hai khung "alt" riêng biệt thay vì một khung alt có hai operand ngăn bằng đường đứt. Trang Đăng nhập không có alt thành công/thất bại: bước 7 INSERT sessions xuất hiện vô điều kiện sau "record(login_success hoặc login_failed)"; thiếu LoginLimiter.fail. |
| 17 | Optional (opt) | N/A | Có thể dùng cho warning docs_processing nhưng không bắt buộc. |
| 18 | Loop (loop) | N/A | Không có vòng lặp ở mức này. |
| 19 | Parallel (par) | N/A | Không có xử lý song song. |
| 20 | Reference (ref) | N/A | Không bắt buộc; bước 3 xác thực có thể ref sang trang Đăng nhập. |
| 21 | No Dangling Messages | In Progress | Cạnh dùng sourcePoint/targetPoint tự do, không gắn source/target vào lifeline (di chuyển lifeline sẽ làm rời thông điệp). Phản hồi lỗi 401/403/404/409 chỉ trả về ChatService, không có thông điệp lỗi trả về Web UI; thiếu nhánh 422 chat.invalid_question và 503 chat.ai_unavailable (ADR-003 bước 4). |
| 22 | Readability & Spacing | Done | Khoảng cách 44 px đều, 7 lifeline cách 190 px. |
| 23 | State Invariants | Pending | Bất biến quan trọng (chỉ document.status = ready được truy xuất — AC-203.4; rel ≥ 0.6) không được đặt trên lifeline. |

## Tóm tắt
Hai sơ đồ thể hiện đúng thứ tự và bên tham gia, nhưng ký hiệu UML chưa đạt: thiếu activation, alt sai cấu trúc, self-message không đúng dạng, actor không phân biệt, luồng ngoại lệ (422, 503, login thất bại) thiếu.
