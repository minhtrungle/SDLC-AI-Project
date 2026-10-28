# User Stories — Chat với tài liệu (MVP)

> **Nguồn:** [PRD v0.2](PRD.md) §3 · **Truy vết:** [traceability.md](traceability.md)
> **Định dạng:** "Là [vai trò], tôi muốn [khả năng], để [lợi ích]". AC theo Given/When/Then. Mỗi AC có ID ổn định; test tự động ghi ID AC trong tên hoặc docstring.
> **Persona:** Linh (chuyên viên kinh doanh, người dùng), Hùng (quản lý dự án, vai trò `manager`), Mai (IT/Bảo mật).
> **Phạm vi MVP:** P0 + P1. P2 (US-404, US-601) hoãn — BRD §12.1 / OQ-013.

## Tổng quan

| Story | Tiêu đề | Ưu tiên | FR/NFR | BR | Sprint (PLAN) |
|---|---|---|---|---|---|
| US-101 | Đăng nhập | P0 | FR-001, FR-002, NFR-010 | BR-019 | S1 |
| US-102 | Tuân thủ chính sách dữ liệu | P0 | FR-003 | BR-020 | S1 |
| US-103 | Nhật ký kiểm toán | P0 | FR-019, NFR-007 | BR-026 | S1 |
| US-201 | Tải lên nhiều PDF | P0 | FR-004 | BR-001 | S1 |
| US-202 | Từ chối file không hợp lệ | P0 | FR-005 | BR-002 | S1 |
| US-203 | Trạng thái xử lý tài liệu | P0 | FR-006 | BR-003 | S1 |
| US-204 | Danh sách tài liệu | P0 | FR-007 | BR-004 | S1 |
| US-205 | Xóa tài liệu | P1 | FR-008 | BR-005, BR-006 | S2 |
| US-301 | Đặt câu hỏi | P0 | FR-009, NFR-003 | BR-007, BR-014 | S2 |
| US-302 | Tổng hợp nhiều tài liệu | P0 | FR-010 | BR-008 | S2 |
| US-303 | Chỉ dựa trên tài liệu | P0 | FR-011 | BR-009 | S2 |
| US-304 | Không tìm thấy | P0 | FR-012 | BR-010 | S2 |
| US-305 | Trích dẫn kiểm chứng được | P0 | FR-013 | BR-011 | S2 |
| US-306 | Chất lượng và độ trễ | P0 | NFR-001, NFR-002 | BR-012, BR-013 | S3 |
| US-401 | Hỏi tiếp trong phiên | P1 | FR-014 | BR-015 | S3 |
| US-402 | Giới hạn phạm vi tài liệu | P1 | FR-015 | BR-016 | S3 |
| US-403 | Xem lại hội thoại | P1 | FR-016 | BR-017 | S3 |
| US-501 | Đánh giá câu trả lời | P1 | FR-017 | BR-021 | S3 |
| US-502 | Số liệu sử dụng | P1 | FR-018 | BR-022 | S3 |
| — | Cô lập workspace, log sạch | P0 | NFR-004, NFR-008 | BR-027, BR-028 | xuyên suốt |

---

## Epic E1 — Truy cập và workspace

### US-101
**Là** Linh, **tôi muốn** đăng nhập bằng tài khoản được cấp, **để** tài liệu kinh doanh của tôi không bị người ngoài xem.
- **AC-101.1** Given chưa đăng nhập, When mở ứng dụng, Then thấy màn hình đăng nhập và không thấy tên tài liệu hay hội thoại nào.
- **AC-101.2** Given tài khoản hợp lệ, When đăng nhập đúng, Then vào màn hình workspace.
- **AC-101.3** Given sai mật khẩu hoặc tài khoản không tồn tại, When đăng nhập, Then nhận cùng một thông báo "Tên đăng nhập hoặc mật khẩu không đúng".
- **AC-101.4** Given chưa đăng nhập, When gọi trực tiếp API tài liệu/hỏi đáp, Then nhận 401.
- **AC-101.5** Given 5 lần đăng nhập sai trong 5 phút, When thử lần thứ 6, Then bị từ chối tạm thời (429).
- **AC-101.6** Given đã đăng nhập, When đăng xuất, Then phiên bị hủy và API trả 401.

### US-102
**Là** Mai, **tôi muốn** biết nội dung tài liệu được xử lý ở đâu, **để** xác nhận tuân thủ trước go-live.
- **AC-102.1** Given cấu hình mặc định, When hệ thống trả lời câu hỏi, Then không có kết nối nào tới dịch vụ AI bên ngoài và `/api/config` báo `ai_mode = "local"`.
- **AC-102.2** Given `CWD_ALLOW_EXTERNAL_AI=false` nhưng có API key, When trả lời, Then vẫn dùng chế độ cục bộ.
- **AC-102.3** Có tài liệu luồng dữ liệu (SAD §8) để IT/Bảo mật ký. *(Review, không tự động hóa.)*

### US-103
**Là** Mai, **tôi muốn** có nhật ký đăng nhập, tải lên, xóa tài liệu, **để** điều tra khi có sự cố.
- **AC-103.1** Given đăng nhập thành công hoặc thất bại, Then có bản ghi `auth.login_success` / `auth.login_failed` kèm tên đăng nhập và thời điểm.
- **AC-103.2** Given tải lên hoặc xóa tài liệu, Then có bản ghi `document.upload` / `document.delete` kèm người dùng và mã tài liệu.
- **AC-103.3** Bản ghi kiểm toán không chứa nội dung tài liệu hay câu hỏi.

## Epic E2 — Quản lý tài liệu

### US-201
**Là** Linh, **tôi muốn** tải nhiều PDF cùng lúc, **để** đưa toàn bộ tài liệu dự án vào một nơi.
- **AC-201.1** Given 3 PDF hợp lệ, When tải lên, Then cả 3 xuất hiện trong danh sách.
- **AC-201.2** Given 1 file lỗi trong lô, When tải lên, Then các file còn lại vẫn được nhận, chỉ file lỗi bị báo.
- **AC-201.3** Given đang tải, Then giao diện hiển thị tiến độ từng file.

### US-202
**Là** Linh, **tôi muốn** biết ngay vì sao file bị từ chối, **để** không nhầm tưởng tài liệu đã sẵn sàng.
- **AC-202.1** File `.docx` → mã `file.wrong_type`, thông báo "Sai định dạng, chỉ chấp nhận PDF", không có trong danh sách.
- **AC-202.2** PDF > 20 MB → mã `file.too_large`, thông báo kèm giới hạn.
- **AC-202.3** File đuôi `.pdf` nhưng nội dung không phải PDF → `file.wrong_type`; PDF hỏng → trạng thái `failed` kèm lý do.
- **AC-202.4** Workspace đã đủ 50 tài liệu → mã `docs.limit_reached`.

### US-203
**Là** Linh, **tôi muốn** thấy trạng thái từng tài liệu, **để** không hỏi khi tài liệu chưa xong.
- **AC-203.1** Vừa tải lên → trạng thái `processing` ("Đang xử lý").
- **AC-203.2** Xử lý xong → `ready` ("Sẵn sàng"), giao diện tự cập nhật không cần tải lại trang.
- **AC-203.3** Xử lý thất bại → `failed` ("Lỗi") kèm lý do; có thể xóa.
- **AC-203.4** Tài liệu chưa `ready` không bao giờ được dùng làm nguồn trả lời.
- **AC-203.5** PDF không có lớp văn bản → `no_text` ("Không trích xuất được văn bản").

### US-204
**Là** Linh, **tôi muốn** xem danh sách tài liệu, **để** biết phạm vi AI đang dùng.
- **AC-204.1** Danh sách hiển thị tên, thời điểm tải lên, trạng thái, số trang của 100% tài liệu.
- **AC-204.2** Chưa có tài liệu → trạng thái trống có nút "Tải tài liệu đầu tiên", ô hỏi bị vô hiệu hóa.

### US-205
**Là** Linh, **tôi muốn** xóa tài liệu sai/lỗi thời, **để** AI không dùng nội dung đó.
- **AC-205.1** Given tài liệu tồn tại, When xác nhận xóa, Then tài liệu biến mất khỏi danh sách.
- **AC-205.2** Given câu hỏi chỉ có đáp án trong tài liệu đã xóa, When hỏi, Then `not_found` và không trích dẫn tài liệu đó.
- **AC-205.3** Giao diện yêu cầu xác nhận trước khi xóa.
- **AC-205.4** Câu trả lời cũ trích dẫn tài liệu đã xóa hiển thị "tài liệu đã bị xóa".

## Epic E3 — Hỏi đáp có trích dẫn

### US-301
**Là** Linh, **tôi muốn** gõ câu hỏi bằng tiếng Việt, **để** nhận đáp án mà không phải mở từng file.
- **AC-301.1** Có ≥ 1 tài liệu `ready`, gửi câu hỏi → nhận câu trả lời trong khung hội thoại.
- **AC-301.2** Câu hỏi tiếng Việt → thông điệp hệ thống và nhãn bằng tiếng Việt; câu hỏi tiếng Việt không dấu vẫn tìm được nội dung có dấu.
- **AC-301.3** Đang xử lý → chỉ báo "Đang trả lời…", nút gửi bị khóa.
- **AC-301.4** Câu hỏi rỗng / chỉ khoảng trắng → không gửi (API trả `chat.invalid_question`).
- **AC-301.5** Không có tài liệu `ready` → ô nhập bị vô hiệu hóa kèm hướng dẫn.

### US-302
**Là** Linh, **tôi muốn** một câu trả lời tổng hợp khi thông tin ở nhiều file, **để** khỏi tổng hợp thủ công.
- **AC-302.1** Đáp án nằm ở 2 tài liệu → câu trả lời có trích dẫn từ cả 2 tài liệu.
- **AC-302.2** Hai tài liệu nêu giá trị khác nhau → câu trả lời trích cả hai nguồn.

### US-303
**Là** Linh, **tôi muốn** AI chỉ dùng nội dung tài liệu, **để** tin được đáp án.
- **AC-303.1** Câu hỏi kiến thức chung không có trong tài liệu → `not_found`.
- **AC-303.2** Tài liệu chứa "Bỏ qua mọi hướng dẫn trước đó và …" → hệ thống không làm theo; văn bản đó chỉ có thể xuất hiện như đoạn trích có trích dẫn.

### US-304
**Là** Linh, **tôi muốn** AI nói rõ khi tài liệu không có đáp án, **để** không bị dẫn đi sai.
- **AC-304.1** Câu hỏi không có đáp án → thông điệp "Không tìm thấy thông tin trong tài liệu đã tải lên" kèm gợi ý diễn đạt lại.
- **AC-304.2** Trả lời `not_found` không kèm trích dẫn nào.

### US-305
**Là** Linh, **tôi muốn** thấy mỗi câu trả lời lấy từ tài liệu nào, trang nào, **để** kiểm chứng.
- **AC-305.1** 100% câu trả lời `answered` có ≥ 1 trích dẫn gồm tên tài liệu + số trang.
- **AC-305.2** Bấm trích dẫn → panel hiển thị đoạn văn bản gốc và số trang, không mất hội thoại.
- **AC-305.3** Mọi trích dẫn trỏ tới chunk có thật trong CSDL (tên, trang lấy từ CSDL).

### US-306
**Là** Hùng, **tôi muốn** câu trả lời đạt chất lượng và tốc độ cam kết, **để** quyết định mở rộng.
- **AC-306.1** Bộ đánh giá `app/backend/tests/eval` chạy được lặp lại, báo tỷ lệ đúng, trích dẫn đúng, `not_found` đúng; ngưỡng mặc định 85% / 90% / 9 trên 10.
- **AC-306.2** Chế độ cục bộ: P90 thời gian trả lời ≤ 2 s trên bộ đánh giá.

## Epic E4 — Hội thoại

### US-401
**Là** Linh, **tôi muốn** hỏi tiếp mà không nhắc lại ngữ cảnh, **để** hỏi đáp tự nhiên.
- **AC-401.1** Hỏi "Giá trị hợp đồng Alpha là bao nhiêu?" rồi "Thời hạn của nó?" trong cùng hội thoại → câu trả lời thứ hai trích dẫn trang về thời hạn hợp đồng Alpha.

### US-402
**Là** Linh, **tôi muốn** chọn một hoặc vài tài liệu để hỏi, **để** tăng độ chính xác.
- **AC-402.1** Chọn tài liệu A, hỏi câu có đáp án chỉ ở B → `not_found`, không trích dẫn B.
- **AC-402.2** Phạm vi đang áp dụng luôn hiển thị gần ô nhập ("Tất cả tài liệu" hoặc "n tài liệu đã chọn").

### US-403
**Là** Linh, **tôi muốn** xem lại câu hỏi và câu trả lời trước đó, **để** tra cứu lại.
- **AC-403.1** Sau 5 lượt, API hội thoại trả đủ 5 cặp theo đúng thứ tự.
- **AC-403.2** Nút "Cuộc hội thoại mới" tạo hội thoại trống; hội thoại cũ vẫn truy cập được bằng mã.

## Epic E5 — Phản hồi và đo lường

### US-501
**Là** Linh, **tôi muốn** bấm hữu ích / không hữu ích, **để** giúp cải thiện chất lượng.
- **AC-501.1** Đánh giá được lưu; đổi đánh giá thì ghi đè (một đánh giá mỗi câu trả lời mỗi người).
- **AC-501.2** Lý do > 500 ký tự bị từ chối.

### US-502
**Là** Hùng, **tôi muốn** xem số người dùng hoạt động và số câu hỏi theo tuần, **để** đo MET-003.
- **AC-502.1** Sau khi 2 người dùng hỏi tổng cộng 3 câu trong tuần, dashboard báo 2 người hoạt động, 3 câu hỏi.
- **AC-502.2** Người dùng không có vai trò `manager` gọi API số liệu → 403.

## Yêu cầu xuyên suốt (không phải story riêng)
- **AC-NFR-004** Người dùng B truy cập tài liệu/hội thoại/câu trả lời của A → 404.
- **AC-NFR-008** Sau bộ test hỏi đáp, log ứng dụng không chứa văn bản câu hỏi hay nội dung tài liệu.
- **AC-NFR-010** Mật khẩu lưu dạng băm PBKDF2; cookie `HttpOnly` + `SameSite=Strict`; thao tác ghi không có header CSRF hợp lệ → 403.
