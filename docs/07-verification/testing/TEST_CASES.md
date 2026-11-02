# Test Cases (IEEE 829) — Chat với tài liệu (MVP)

| Mục | Giá trị |
|---|---|
| Mã | TCS-CWD-001 v1.0 · thuộc [Test Plan TP-CWD-001](TEST_PLAN.md) |
| Nguồn | Acceptance Criteria trong [USER_STORIES.md](../../03-analysis/USER_STORIES.md) |
| Sinh bởi | `python tools/rtm.py RUN-20261102-25eb89f` — không sửa tay |

Mỗi AC có một test case `TC-<AC>`: **Tiền điều kiện** = mệnh đề Given, **Bước** = When, **Kết quả mong đợi** = Then. Dữ liệu cụ thể (PDF sinh bằng fpdf2, tài khoản, câu hỏi) nằm trong fixture của test tự động ở cột *Chứng minh bởi*. BE = pytest, FE = Vitest, E2E = Playwright.

## US-101 — Đăng nhập (P0)

| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |
|---|---|---|---|---|---|---|
| TC-101.1 | AC-101.1 | chưa đăng nhập | mở ứng dụng | thấy màn hình đăng nhập và không thấy tên tài liệu hay hội thoại nào. | BE/E2E | `test_unauthenticated_api_is_rejected` (BE)<br>`AC-101.1 chưa đăng nhập chỉ thấy màn hình đăng nhập` (E2E) |
| TC-101.2 | AC-101.2 | tài khoản hợp lệ | đăng nhập đúng | vào màn hình workspace. | BE/E2E | `test_login_success_returns_user_and_sets_secure_cookie` (BE)<br>`AC-101.2 / AC-101.6 đăng nhập vào workspace, đăng xuất về màn hình đăng nhập` (E2E) |
| TC-101.3 | AC-101.3 | sai mật khẩu hoặc tài khoản không tồn tại | đăng nhập | nhận cùng một thông báo "Tên đăng nhập hoặc mật khẩu không đúng". | BE/FE/E2E | `test_wrong_password_and_unknown_user_get_same_message` (BE)<br>`shows the server message on wrong credentials (AC-101.3)` (FE)<br>`AC-101.3 sai mật khẩu hiển thị thông báo chung` (E2E) |
| TC-101.4 | AC-101.4 | chưa đăng nhập | gọi trực tiếp API tài liệu/hỏi đáp | nhận 401. | BE/E2E | `test_unauthenticated_api_is_rejected` (BE)<br>`test_every_protected_endpoint_requires_login` (BE)<br>`AC-101.4 gọi API trực tiếp khi chưa đăng nhập bị từ chối` (E2E) |
| TC-101.5 | AC-101.5 | 5 lần đăng nhập sai trong 5 phút | thử lần thứ 6 | bị từ chối tạm thời (429). | BE | `test_lockout_after_five_failures` (BE) |
| TC-101.6 | AC-101.6 | đã đăng nhập | đăng xuất | phiên bị hủy và API trả 401. | BE/E2E | `test_logout_invalidates_session` (BE)<br>`AC-101.2 / AC-101.6 đăng nhập vào workspace, đăng xuất về màn hình đăng nhập` (E2E) |

## US-102 — Tuân thủ chính sách dữ liệu (P0)

| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |
|---|---|---|---|---|---|---|
| TC-102.1 | AC-102.1 | cấu hình mặc định | hệ thống trả lời câu hỏi | không có kết nối nào tới dịch vụ AI bên ngoài và `/api/config` báo `ai_mode = "local"`. | BE | `test_config_defaults_to_local_ai` (BE)<br>`test_build_generator_defaults_to_local` (BE)<br>`test_build_generator_needs_flag_and_key` (BE) |
| TC-102.2 | AC-102.2 | `CWD_ALLOW_EXTERNAL_AI=false` nhưng có API key | trả lời | vẫn dùng chế độ cục bộ. | BE | `test_build_generator_needs_flag_and_key` (BE) |
| TC-102.3 | AC-102.3 | — | — | Có tài liệu luồng dữ liệu (SAD §8) để IT/Bảo mật ký. *(Review, không tự động hóa.)* | Review | Review: IT/Bảo mật ký luồng dữ liệu SAD §8 |

## US-103 — Nhật ký kiểm toán (P0)

| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |
|---|---|---|---|---|---|---|
| TC-103.1 | AC-103.1 | đăng nhập thành công hoặc thất bại | — | có bản ghi `auth.login_success` / `auth.login_failed` kèm tên đăng nhập và thời điểm. | BE | `test_audit_log_for_login_events` (BE) |
| TC-103.2 | AC-103.2 | tải lên hoặc xóa tài liệu | — | có bản ghi `document.upload` / `document.delete` kèm người dùng và mã tài liệu. | BE | `test_delete_is_audited` (BE)<br>`test_upload_is_audited` (BE) |
| TC-103.3 | AC-103.3 | — | — | Bản ghi kiểm toán không chứa nội dung tài liệu hay câu hỏi. | BE | `test_audit_log_for_login_events` (BE) |

## US-201 — Tải lên nhiều PDF (P0)

| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |
|---|---|---|---|---|---|---|
| TC-201.1 | AC-201.1 | 3 PDF hợp lệ | tải lên | cả 3 xuất hiện trong danh sách. | BE/E2E | `test_upload_three_pdfs` (BE)<br>`AC-201.1 / AC-201.2 / AC-202.1 tải song song nhiều file, file sai định dạng bị từ chối riêng` (E2E) |
| TC-201.2 | AC-201.2 | 1 file lỗi trong lô | tải lên | các file còn lại vẫn được nhận, chỉ file lỗi bị báo. | BE/FE/E2E | `test_one_bad_file_does_not_block_others` (BE)<br>`tracks per-file upload results, one bad file never blocks others (AC-201.2)` (FE)<br>`AC-201.1 / AC-201.2 / AC-202.1 tải song song nhiều file, file sai định dạng bị từ chối riêng` (E2E) |
| TC-201.3 | AC-201.3 | đang tải | — | giao diện hiển thị tiến độ từng file. | FE | `reports progress and resolves with the file result` (FE)<br>`rejects on HTTP errors and network failures` (FE) |

## US-202 — Từ chối file không hợp lệ (P0)

| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |
|---|---|---|---|---|---|---|
| TC-202.1 | AC-202.1 | — | File `.docx` | mã `file.wrong_type`, thông báo "Sai định dạng, chỉ chấp nhận PDF", không có trong danh sách. | BE/E2E | `test_one_bad_file_does_not_block_others` (BE)<br>`AC-201.1 / AC-201.2 / AC-202.1 tải song song nhiều file, file sai định dạng bị từ chối riêng` (E2E) |
| TC-202.2 | AC-202.2 | — | PDF > 20 MB | mã `file.too_large`, thông báo kèm giới hạn. | BE | `test_too_large_file_rejected_with_limit` (BE) |
| TC-202.3 | AC-202.3 | — | File đuôi `.pdf` nhưng nội dung không phải PDF | `file.wrong_type`; PDF hỏng → trạng thái `failed` kèm lý do. | BE | `test_pdf_extension_with_non_pdf_content_is_rejected` (BE)<br>`test_corrupt_pdf_fails_with_reason` (BE) |
| TC-202.4 | AC-202.4 | — | Workspace đã đủ 50 tài liệu | mã `docs.limit_reached`. | BE | `test_document_limit` (BE)<br>`test_nr01_parallel_uploads_respect_document_limit` (BE) |

## US-203 — Trạng thái xử lý tài liệu (P0)

| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |
|---|---|---|---|---|---|---|
| TC-203.1 | AC-203.1 | — | Vừa tải lên | trạng thái `processing` ("Đang xử lý"). | BE | `test_status_lifecycle_processing_then_ready` (BE) |
| TC-203.2 | AC-203.2 | — | Xử lý xong | `ready` ("Sẵn sàng"), giao diện tự cập nhật không cần tải lại trang. | BE/FE | `test_status_lifecycle_processing_then_ready` (BE)<br>`polls while a document is processing, then stops (AC-203.2)` (FE) |
| TC-203.3 | AC-203.3 | — | Xử lý thất bại | `failed` ("Lỗi") kèm lý do; có thể xóa. | BE | `test_corrupt_pdf_fails_with_reason` (BE)<br>`test_cr02_unexpected_ingestion_error_marks_failed` (BE) |
| TC-203.4 | AC-203.4 | — | — | Tài liệu chưa `ready` không bao giờ được dùng làm nguồn trả lời. | BE | `test_processing_document_is_never_a_source` (BE) |
| TC-203.5 | AC-203.5 | — | PDF không có lớp văn bản | `no_text` ("Không trích xuất được văn bản"). | BE | `test_scanned_pdf_without_text_is_flagged` (BE) |

## US-204 — Danh sách tài liệu (P0)

| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |
|---|---|---|---|---|---|---|
| TC-204.1 | AC-204.1 | — | — | Danh sách hiển thị tên, thời điểm tải lên, trạng thái, số trang của 100% tài liệu. | BE | `test_list_shows_name_time_status_pages` (BE) |
| TC-204.2 | AC-204.2 | — | Chưa có tài liệu | trạng thái trống có nút "Tải tài liệu đầu tiên", ô hỏi bị vô hiệu hóa. | BE/FE/E2E | `test_empty_list` (BE)<br>`renders the empty state (AC-204.2)` (FE)<br>`is disabled without documents (AC-204.2, AC-301.5)` (FE)<br>`AC-204.2 workspace trống hướng dẫn tải tài liệu và khóa ô hỏi` (E2E) |

## US-205 — Xóa tài liệu (P1)

| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |
|---|---|---|---|---|---|---|
| TC-205.1 | AC-205.1 | tài liệu tồn tại | xác nhận xóa | tài liệu biến mất khỏi danh sách. | BE/E2E | `test_delete_removes_document` (BE)<br>`AC-205.1 / AC-205.3 xóa tài liệu phải xác nhận; Hủy giữ nguyên` (E2E) |
| TC-205.2 | AC-205.2 | câu hỏi chỉ có đáp án trong tài liệu đã xóa | hỏi | `not_found` và không trích dẫn tài liệu đó. | BE | `test_deleted_document_is_never_used_again` (BE) |
| TC-205.3 | AC-205.3 | — | — | Giao diện yêu cầu xác nhận trước khi xóa. | FE/E2E | `asks for confirmation before deleting (AC-205.3)` (FE)<br>`AC-205.1 / AC-205.3 xóa tài liệu phải xác nhận; Hủy giữ nguyên` (E2E) |
| TC-205.4 | AC-205.4 | — | — | Câu trả lời cũ trích dẫn tài liệu đã xóa hiển thị "tài liệu đã bị xóa". | BE/FE | `test_old_citation_marked_deleted` (BE)<br>`falls back to the stored snippet for deleted documents (AC-205.4)` (FE) |

## US-301 — Đặt câu hỏi (P0)

| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |
|---|---|---|---|---|---|---|
| TC-301.1 | AC-301.1 | — | Có ≥ 1 tài liệu `ready`, gửi câu hỏi | nhận câu trả lời trong khung hội thoại. | BE/E2E | `test_answer_with_citation` (BE)<br>`AC-301.1 / AC-305.1 câu trả lời kèm trích dẫn tên tài liệu và trang` (E2E) |
| TC-301.2 | AC-301.2 | — | Câu hỏi tiếng Việt | thông điệp hệ thống và nhãn bằng tiếng Việt; câu hỏi tiếng Việt không dấu vẫn tìm được nội dung có dấu. | BE/E2E | `test_answers_are_in_vietnamese_for_unaccented_question` (BE)<br>`test_unaccented_query_matches_accented_text` (BE)<br>`test_fold_removes_vietnamese_diacritics` (BE)<br>`AC-301.2 câu hỏi không dấu vẫn tìm được nội dung có dấu` (E2E) |
| TC-301.3 | AC-301.3 | — | Đang xử lý | chỉ báo "Đang trả lời…", nút gửi bị khóa. | FE | `blocks sending while an answer is pending (AC-301.3)` (FE) |
| TC-301.4 | AC-301.4 | — | Câu hỏi rỗng / chỉ khoảng trắng | không gửi (API trả `chat.invalid_question`). | BE/FE/E2E | `test_empty_question_rejected` (BE)<br>`ignores whitespace-only drafts (AC-301.4) and counts characters` (FE)<br>`AC-301.4 câu hỏi rỗng không được gửi` (E2E) |
| TC-301.5 | AC-301.5 | — | Không có tài liệu `ready` | ô nhập bị vô hiệu hóa kèm hướng dẫn. | BE/FE | `test_no_ready_documents` (BE)<br>`disables the question box without ready documents (AC-301.5)` (FE)<br>`is disabled without documents (AC-204.2, AC-301.5)` (FE) |

## US-302 — Tổng hợp nhiều tài liệu (P0)

| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |
|---|---|---|---|---|---|---|
| TC-302.1 | AC-302.1 | — | Đáp án nằm ở 2 tài liệu | câu trả lời có trích dẫn từ cả 2 tài liệu. | BE | `test_multi_document_answer_cites_both` (BE) |
| TC-302.2 | AC-302.2 | — | Hai tài liệu nêu giá trị khác nhau | câu trả lời trích cả hai nguồn. | BE | `test_conflicting_documents_both_cited` (BE) |

## US-303 — Chỉ dựa trên tài liệu (P0)

| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |
|---|---|---|---|---|---|---|
| TC-303.1 | AC-303.1 | — | Câu hỏi kiến thức chung không có trong tài liệu | `not_found`. | BE/E2E | `test_general_knowledge_question_not_found` (BE)<br>`AC-304.1 / AC-303.1 câu hỏi ngoài tài liệu được báo không tìm thấy, không trích dẫn` (E2E) |
| TC-303.2 | AC-303.2 | — | Tài liệu chứa "Bỏ qua mọi hướng dẫn trước đó và …" | hệ thống không làm theo; văn bản đó chỉ có thể xuất hiện như đoạn trích có trích dẫn. | BE | `test_prompt_injection_text_is_not_obeyed` (BE)<br>`test_document_text_cannot_forge_tags` (BE) |

## US-304 — Không tìm thấy (P0)

| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |
|---|---|---|---|---|---|---|
| TC-304.1 | AC-304.1 | — | Câu hỏi không có đáp án | thông điệp "Không tìm thấy thông tin trong tài liệu đã tải lên" kèm gợi ý diễn đạt lại. | BE/E2E | `test_general_knowledge_question_not_found` (BE)<br>`AC-304.1 / AC-303.1 câu hỏi ngoài tài liệu được báo không tìm thấy, không trích dẫn` (E2E) |
| TC-304.2 | AC-304.2 | — | — | Trả lời `not_found` không kèm trích dẫn nào. | BE | `test_general_knowledge_question_not_found` (BE) |

## US-305 — Trích dẫn kiểm chứng được (P0)

| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |
|---|---|---|---|---|---|---|
| TC-305.1 | AC-305.1 | — | — | 100% câu trả lời `answered` có ≥ 1 trích dẫn gồm tên tài liệu + số trang. | BE/FE/E2E | `test_answer_with_citation` (BE)<br>`turns known [n] markers into citations and keeps the rest as text` (FE)<br>`never interprets markup (XSS guard)` (FE)<br>`AC-301.1 / AC-305.1 câu trả lời kèm trích dẫn tên tài liệu và trang` (E2E) |
| TC-305.2 | AC-305.2 | — | Bấm trích dẫn | panel hiển thị đoạn văn bản gốc và số trang, không mất hội thoại. | BE/FE/E2E | `test_citation_chunk_text` (BE)<br>`loads the original passage and closes with Escape` (FE)<br>`falls back to the stored snippet for deleted documents (AC-205.4)` (FE)<br>`AC-305.2 bấm trích dẫn mở đoạn gốc; Esc đóng và trả focus` (E2E) |
| TC-305.3 | AC-305.3 | — | — | Mọi trích dẫn trỏ tới chunk có thật trong CSDL (tên, trang lấy từ CSDL). | BE | `test_answer_with_citation` (BE) |

## US-306 — Chất lượng và độ trễ (P0)

| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |
|---|---|---|---|---|---|---|
| TC-306.1 | AC-306.1 | — | — | Bộ đánh giá `app/backend/tests/eval` chạy được lặp lại, báo tỷ lệ đúng, trích dẫn đúng, `not_found` đúng; ngưỡng mặc định 85% / 90% / 9 trên 10. | BE | `test_quality_and_latency` (BE) |
| TC-306.2 | AC-306.2 | — | — | Chế độ cục bộ: P90 thời gian trả lời ≤ 2 s trên bộ đánh giá. | BE | `test_quality_and_latency` (BE) |

## US-401 — Hỏi tiếp trong phiên (P1)

| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |
|---|---|---|---|---|---|---|
| TC-401.1 | AC-401.1 | — | Hỏi "Giá trị hợp đồng Alpha là bao nhiêu?" rồi "Thời hạn của nó?" trong cùng hội thoại | câu trả lời thứ hai trích dẫn trang về thời hạn hợp đồng Alpha. | BE/E2E | `test_follow_up_question_uses_previous_context` (BE)<br>`AC-401.1 hỏi tiếp hiểu ngữ cảnh lượt trước` (E2E) |

## US-402 — Giới hạn phạm vi tài liệu (P1)

| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |
|---|---|---|---|---|---|---|
| TC-402.1 | AC-402.1 | — | Chọn tài liệu A, hỏi câu có đáp án chỉ ở B | `not_found`, không trích dẫn B. | BE/E2E | `test_scope_excludes_other_documents` (BE)<br>`AC-402.1 / AC-402.2 giới hạn phạm vi vào một tài liệu` (E2E) |
| TC-402.2 | AC-402.2 | — | — | Phạm vi đang áp dụng luôn hiển thị gần ô nhập ("Tất cả tài liệu" hoặc "n tài liệu đã chọn"). | E2E | `AC-402.1 / AC-402.2 giới hạn phạm vi vào một tài liệu` (E2E) |

## US-403 — Xem lại hội thoại (P1)

| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |
|---|---|---|---|---|---|---|
| TC-403.1 | AC-403.1 | — | — | Sau 5 lượt, API hội thoại trả đủ 5 cặp theo đúng thứ tự. | BE/E2E | `test_five_turns_in_order` (BE)<br>`AC-403.1 / AC-403.2 hội thoại giữ thứ tự; cuộc hội thoại mới trống` (E2E) |
| TC-403.2 | AC-403.2 | — | — | Nút "Cuộc hội thoại mới" tạo hội thoại trống; hội thoại cũ vẫn truy cập được bằng mã. | BE/FE/E2E | `test_new_conversation_has_no_history` (BE)<br>`starts a new, empty conversation (AC-403.2)` (FE)<br>`AC-403.1 / AC-403.2 hội thoại giữ thứ tự; cuộc hội thoại mới trống` (E2E) |

## US-501 — Đánh giá câu trả lời (P1)

| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |
|---|---|---|---|---|---|---|
| TC-501.1 | AC-501.1 | — | — | Đánh giá được lưu; đổi đánh giá thì ghi đè (một đánh giá mỗi câu trả lời mỗi người). | BE/E2E | `test_feedback_is_saved_and_can_change` (BE)<br>`AC-501.1 đánh giá câu trả lời được ghi nhận` (E2E) |
| TC-501.2 | AC-501.2 | — | — | Lý do > 500 ký tự bị từ chối. | BE | `test_feedback_validation` (BE) |

## US-502 — Số liệu sử dụng (P1)

| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |
|---|---|---|---|---|---|---|
| TC-502.1 | AC-502.1 | — | — | Sau khi 2 người dùng hỏi tổng cộng 3 câu trong tuần, dashboard báo 2 người hoạt động, 3 câu hỏi. | BE/E2E | `test_weekly_metrics` (BE)<br>`AC-502.1 quản lý xem số liệu theo tuần` (E2E) |
| TC-502.2 | AC-502.2 | — | Người dùng không có vai trò `manager` gọi API số liệu | 403. | BE/FE/E2E | `test_metrics_forbidden_for_regular_user` (BE)<br>`shows the error for non-managers (AC-502.2)` (FE)<br>`AC-502.2 người dùng thường không có mục Số liệu sử dụng` (E2E) |

## Yêu cầu xuyên suốt (NFR) (P0)

| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |
|---|---|---|---|---|---|---|
| TC-NFR-004 | AC-NFR-004 | — | Người dùng B truy cập tài liệu/hội thoại/câu trả lời của A | 404. | BE/E2E | `test_workspace_isolation_on_every_resource` (BE)<br>`AC-NFR-004 người dùng khác không thấy và không hỏi được tài liệu của mình` (E2E) |
| TC-NFR-008 | AC-NFR-008 | — | — | Sau bộ test hỏi đáp, log ứng dụng không chứa văn bản câu hỏi hay nội dung tài liệu. | BE | `test_logs_never_contain_content` (BE) |
| TC-NFR-010 | AC-NFR-010 | — | Mật khẩu lưu dạng băm PBKDF2; cookie `HttpOnly` + `SameSite=Strict`; thao tác ghi không có header CSRF hợp lệ | 403. | BE/FE | `test_login_success_returns_user_and_sets_secure_cookie` (BE)<br>`test_write_without_csrf_is_forbidden` (BE)<br>`test_password_hashing` (BE)<br>`sends the CSRF header on writes only (AC-NFR-010)` (FE) |
