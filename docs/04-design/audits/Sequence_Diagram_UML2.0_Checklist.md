# Audit — Sequence Diagram theo checklist UML 2

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | docs/04-design/diagrams/sequence_diagram.drawio (trang "Hỏi đáp", "Đăng nhập"); đối chiếu SAD §5.3, §6.1, §6.4, openapi.yaml, design-refine-log.md |
| Checklist | docs/checklists/Sequence_Diagram_UML2.0_Checklist.xlsx |
| Reviewer | Vòng 1: Independent reviewer agent · Vòng 2: artifact-auditor (agent) |
| Ngày | Vòng 1: 2026-10-28 · Vòng 2: 2026-11-02 |
| Vòng | 2 — Audit lại 2026-11-02 sau REFINE (e1c8a1d) |
| Ghi chú vòng 2 | Đã áp dụng DF-07: khung lỗi trả về Web UI (401/403/404/409/422), nhánh 503 chat.ai_unavailable, trang Đăng nhập có alt bị khóa / sai / đúng với LoginLimiter.fail/reset. DF-20 (activation) vẫn Partial, hoãn. 35 thông điệp, 4 khung alt. |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Diagram Name | Done | Tên trang "Hỏi đáp" (US-301..305, SAD §6.1) và "Đăng nhập" (US-101, SAD §6.4). Không có khung "sd <tên>" (Minor). |
| 3 | Time Axis | Done | Thông điệp đi từ trên xuống: Hỏi đáp 1..16 (kèm 6a/6b, 11a/11b, 12x/12y), Đăng nhập 1..8 (kèm 3a, 6a–6c, 7a–7d); dy 44 px (Hỏi đáp) và 30 px (alt Đăng nhập). |
| 4 | Lifeline Notation | Done | shape=umlLifeline (đầu chữ nhật + đường đứt) cho 7 lifeline Hỏi đáp và 5 lifeline Đăng nhập. |
| 5 | Naming Convention | Pending | Lifeline vẫn đặt "CMP-08 Chat Service", "CMP-06 Retriever"…, không theo "tên : Lớp" (vd. "chat : ChatService", "retriever : FtsRetriever"). Không được xử lý trong REFINE. |
| 6 | Actor vs. System | Pending | "ACT-01 Người dùng" vẫn là umlLifeline chữ nhật như đối tượng hệ thống, không dùng hình người. |
| 7 | Synchronous Messages | Done | Nét liền, mũi tên đặc (endArrow=block;endFill=1) cho lời gọi, gồm thông điệp mới 6a LoginLimiter.fail, 7b INSERT sessions. |
| 8 | Asynchronous Messages | N/A | Hai luồng đều đồng bộ; luồng nền BackgroundTasks nằm ở activity_diagram.drawio. |
| 9 | Return/Reply Messages | Done | Nét đứt mũi tên mở cho reply: 4, 6, 6a, 6b, 9, 10, 12, 12x, 12y, 15, 16 (Hỏi đáp); 3a, 6c, 7d, 8 (Đăng nhập). Còn Minor: "4: SELECT users WHERE username" (Đăng nhập) vẫn không có reply. |
| 10 | Self Messages | In Progress | 11a, 13 (Hỏi đáp) và 3, 5, 6a, 7a (Đăng nhập) vẫn vẽ bằng mũi tên chéo ngắn (x → x+60, y → y+16), không phải vòng chữ U quay về lifeline. |
| 11 | Creation & Destruction | N/A | Không tạo/hủy đối tượng trong luồng (INSERT turns/sessions là thao tác dữ liệu). |
| 12 | Message Signatures | In Progress | Cải thiện: "7: retrieve(question, history, phạm vi, tài liệu trích dẫn trước)" nay có cited_documents; "11b: generate(question, chunks)", "6a: LoginLimiter.fail(username)". Còn trộn văn xuôi: "5: hội thoại thuộc user? tài liệu ready trong phạm vi? 3 lượt trước"; bước 7 thiếu conn, user_id so với SAD §5.3. |
| 13 | Activation Boxes | Pending | Không có activation bar trên lifeline nào. DF-20 Partial: activation hoãn, owner Architect. |
| 14 | Overlapping Activations | Pending | Không có activation (xem row 13), nên không có activation chồng cho self-call 13, 3, 5. |
| 15 | Frame Notation | In Progress | 4 khung alt vẫn là chữ nhật thường (S_BOUNDARY) với chữ "alt [..]" căn giữa ở đỉnh, không có ô ngũ giác toán tử ở góc trái trên. Khung "alt [không có chunk] / [có chunk] / [bộ sinh lỗi]" bắt đầu x=640 nên không bao lifeline Web UI dù 12y trả về Web UI. |
| 16 | Alternative (alt) | In Progress | Nội dung đã đủ (DF-07): Đăng nhập có "alt [bị khóa]" (3a 429) và "alt [sai thông tin] / [đúng]" (6a fail, 6b login_failed, 6c 401 / 7a reset, 7b INSERT sessions, 7c login_success, 7d 200); Hỏi đáp có nhánh not_found, generate, 503. Ký hiệu chưa đạt: guard dồn vào tiêu đề, các operand không ngăn bằng đường đứt; "alt [lỗi kiểm tra]" và "alt [bị khóa]" chỉ có một operand. |
| 17 | Optional (opt) | In Progress | Vòng 1 N/A; sau DF-07 có logic chỉ chạy khi điều kiện đúng (lỗi kiểm tra 6a/6b, bị khóa 3a — trả về sớm) nhưng vẽ bằng alt một operand thay vì opt (hoặc alt có [else]); warning docs_processing chỉ nằm trong nhãn 15. |
| 18 | Loop (loop) | N/A | Không có vòng lặp ở mức tương tác này (vòng lặp chunk nằm trong CMP-06). |
| 19 | Parallel (par) | N/A | Không có xử lý song song trong hai luồng. |
| 20 | Reference (ref) | N/A | Không bắt buộc; bước 3 xác thực có thể ref sang trang Đăng nhập. |
| 21 | No Dangling Messages | In Progress | DF-07 đã thêm phản hồi lỗi về Web UI (6a 401/403, 6b 404/422/409, 12y 503). Vẫn còn: cả 35 cạnh là free edge chỉ có sourcePoint/targetPoint, không có source/target gắn lifeline (grep source= trả 0); lỗi 6a/6b/12y không được chuyển tiếp tới ACT-01. |
| 22 | Readability & Spacing | Done | Hỏi đáp dy 44 px, Đăng nhập dy 30 px trong alt; 7 lifeline cách 190 px, nhãn không chồng nhau theo tọa độ. |
| 23 | State Invariants | Pending | Bất biến (chỉ document.status = ready được truy xuất — AC-203.4; rel ≥ 0.6) chỉ xuất hiện trong nhãn thông điệp 8, 10, không đặt trên lifeline bằng ký hiệu state invariant. |

## Kiểm tra lại vòng trước

| Vấn đề vòng 1 | Trạng thái vòng 2 | Bằng chứng |
|---|---|---|
| Thiếu lỗi trả về Web UI, thiếu 422 và 503 (row 21) | Đã sửa (DF-07) | Thông điệp 6a, 6b, 12x, 12y |
| Đăng nhập không có alt thành công/thất bại, thiếu LoginLimiter.fail (row 16) | Đã sửa (DF-07) | Khung "alt [sai thông tin] / [đúng]", 6a fail, 7a reset |
| Chữ ký retrieve lệch SAD (row 12) | Một phần | Nhãn 7 có history, phạm vi, tài liệu trích dẫn trước; thiếu conn, user_id |
| Alt hai khung riêng thay vì operand ngăn đường đứt (row 15, 16) | Chưa sửa ký hiệu | S_BOUNDARY, không có dashed separator |
| Thiếu activation, actor hình người, "tên : Lớp", self-message chữ U (row 5, 6, 10, 13, 14) | Chưa sửa — DF-20 Partial | tools/gen_diagrams.py sequence() |
| Thiếu reply cho "4: SELECT users" | Chưa sửa | Trang Đăng nhập |

## Phát hiện

| ID | Mức | Vị trí | Mô tả | Khuyến nghị |
|---|---|---|---|---|
| AUD-SEQ-01 | Major | Cả hai trang (row 13, 14) | Không có activation bar (DF-20 hoãn) | Thêm activation cho CMP-08, CMP-06, CMP-07, CMP-03 trong gen_diagrams.py |
| AUD-SEQ-02 | Minor | Lifeline (row 5, 6) | Tên không theo "tên : Lớp"; actor không phải hình người | Đổi nhãn và dùng shape=umlActor cho ACT-01 |
| AUD-SEQ-03 | Minor | 4 khung alt (row 15, 16, 17) | Không có pentagon, không có đường đứt ngăn operand, alt một operand nên là opt/break; khung thứ hai không bao Web UI | Vẽ lại fragment với separator và nhãn góc trái |
| AUD-SEQ-04 | Minor | Toàn bộ cạnh (row 21) | Cạnh không gắn source/target vào lifeline | Gắn source/target hoặc dùng điểm neo trên lifeline |
| AUD-SEQ-05 | Minor | Đăng nhập bước 4 | Thiếu reply cho SELECT users | Thêm reply "user hoặc không có" |
| AUD-SEQ-06 | Minor | Self-message (row 10) | Mũi tên chéo thay vì vòng chữ U | Dùng edge có waypoint quay về lifeline |

## Tóm tắt

- Status: Done 6 · In Progress 6 · Pending 5 · N/A 5 (tổng 22 dòng).
- Phát hiện: Critical 0 · Major 1 · Minor 5.
- Nhận định: **Cần sửa** — nội dung luồng (lỗi, 503, đăng nhập thất bại) đã đầy đủ sau DF-07; ký hiệu UML (activation, actor, tên lifeline, fragment) còn thiếu theo DF-20 hoãn.

## Lịch sử audit

| Vòng | Ngày | Thay đổi Status | Lý do |
|---|---|---|---|
| 1 | 2026-10-28 | Bản đầu: Done 6 · In Progress 5 · Pending 5 · N/A 6 | Audit độc lập trước REFINE |
| 2 | 2026-11-02 | Row 17 N/A → In Progress | Sau DF-07 xuất hiện logic chỉ chạy khi điều kiện đúng (lỗi kiểm tra, bị khóa) nhưng vẽ bằng alt một operand thay vì opt, nên mục này áp dụng và chưa đạt |
| 2 | 2026-11-02 | Các dòng khác giữ nguyên Status | Row 16, 21 đã sửa nội dung (DF-07) nhưng vẫn In Progress vì ký hiệu operand và cạnh không gắn lifeline; row 12 cải thiện một phần; row 5, 6, 13, 14, 23 không được xử lý (DF-20 hoãn) |
