# Requirements Traceability Matrix (RTM) — Chat với tài liệu (MVP)

| Mục | Giá trị |
|---|---|
| Mã | RTM-CWD-001 v1.0 · thuộc [Test Plan TP-CWD-001](TEST_PLAN.md) · case: [TEST_CASES.md](TEST_CASES.md) |
| Lần chạy | `RUN-20261102-25eb89f` — bằng chứng: [../evidence/RUN-20261102-25eb89f/](../evidence/RUN-20261102-25eb89f/) và [test_reports/](../../../test_reports/report.md) |
| Sinh bởi | `python tools/rtm.py RUN-20261102-25eb89f` — không sửa tay |

## 1. Tóm tắt
| Chỉ số | Giá trị |
|---|---|
| Tổng AC | 58 |
| AC có test case tự động | 57 |
| AC PASS (mọi test liên kết đạt) | 57 |
| AC chờ review thủ công | 1 (AC-102.3) |
| GAP (AC không có case) | 0 |
| Test liên kết không đạt / chưa chạy | 0 |
| Test đã chạy trong lần này (BE: test có tham số tính là 1) | BE 126/126 pass · FE 49/49 pass · E2E 20/20 pass |

## 2. Chiều xuôi: BR → FR/NFR → US → AC → TC → kết quả → bằng chứng
| BR | FR/NFR | Story | AC | TC | Ưu tiên | Số test | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|---|---|
| BR-019 | FR-001, FR-002, NFR-010 | US-101 | AC-101.1 | TC-101.1 | P0 | BE 1 · E2E 1 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [E2E](../../../test_reports/dang-nhap-04-ac-101-1-chua-dang-nhap-chi-thay-man-hinh-dang-nhap/report.md) |
| BR-019 | FR-001, FR-002, NFR-010 | US-101 | AC-101.2 | TC-101.2 | P0 | BE 1 · E2E 1 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [E2E](../../../test_reports/dang-nhap-06-ac-101-2-ac-101-6-dang-nhap-vao-workspace-dang-xuat-ve/report.md) |
| BR-019 | FR-001, FR-002, NFR-010 | US-101 | AC-101.3 | TC-101.3 | P0 | BE 1 · FE 1 · E2E 1 | **PASS** (3/3) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [FE](../evidence/RUN-20261102-25eb89f/frontend-junit.xml) [E2E](../../../test_reports/dang-nhap-05-ac-101-3-sai-mat-khau-hien-thi-thong-bao-chung/report.md) |
| BR-019 | FR-001, FR-002, NFR-010 | US-101 | AC-101.4 | TC-101.4 | P0 | BE 2 · E2E 1 | **PASS** (3/3) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [E2E](../../../test_reports/dang-nhap-07-ac-101-4-goi-api-truc-tiep-khi-chua-dang-nhap-bi-tu-cho/report.md) |
| BR-019 | FR-001, FR-002, NFR-010 | US-101 | AC-101.5 | TC-101.5 | P0 | BE 1 | **PASS** (1/1) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-019 | FR-001, FR-002, NFR-010 | US-101 | AC-101.6 | TC-101.6 | P0 | BE 1 · E2E 1 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [E2E](../../../test_reports/dang-nhap-06-ac-101-2-ac-101-6-dang-nhap-vao-workspace-dang-xuat-ve/report.md) |
| BR-020 | FR-003 | US-102 | AC-102.1 | TC-102.1 | P0 | BE 3 | **PASS** (3/3) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-020 | FR-003 | US-102 | AC-102.2 | TC-102.2 | P0 | BE 1 | **PASS** (1/1) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-020 | FR-003 | US-102 | AC-102.3 | TC-102.3 | P0 | — | **PENDING REVIEW** | Review: IT/Bảo mật ký luồng dữ liệu SAD §8; owner IT/Bảo mật (STK-005) |
| BR-026 | FR-019, NFR-007 | US-103 | AC-103.1 | TC-103.1 | P0 | BE 1 | **PASS** (1/1) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-026 | FR-019, NFR-007 | US-103 | AC-103.2 | TC-103.2 | P0 | BE 2 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-026 | FR-019, NFR-007 | US-103 | AC-103.3 | TC-103.3 | P0 | BE 1 | **PASS** (1/1) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-001 | FR-004 | US-201 | AC-201.1 | TC-201.1 | P0 | BE 1 · E2E 1 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [E2E](../../../test_reports/tai-lieu-19-ac-201-1-ac-201-2-ac-202-1-tai-song-song-nhieu-file-fil/report.md) |
| BR-001 | FR-004 | US-201 | AC-201.2 | TC-201.2 | P0 | BE 1 · FE 1 · E2E 1 | **PASS** (3/3) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [FE](../evidence/RUN-20261102-25eb89f/frontend-junit.xml) [E2E](../../../test_reports/tai-lieu-19-ac-201-1-ac-201-2-ac-202-1-tai-song-song-nhieu-file-fil/report.md) |
| BR-001 | FR-004 | US-201 | AC-201.3 | TC-201.3 | P0 | FE 2 | **PASS** (2/2) | [FE](../evidence/RUN-20261102-25eb89f/frontend-junit.xml) |
| BR-002 | FR-005 | US-202 | AC-202.1 | TC-202.1 | P0 | BE 1 · E2E 1 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [E2E](../../../test_reports/tai-lieu-19-ac-201-1-ac-201-2-ac-202-1-tai-song-song-nhieu-file-fil/report.md) |
| BR-002 | FR-005 | US-202 | AC-202.2 | TC-202.2 | P0 | BE 1 | **PASS** (1/1) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-002 | FR-005 | US-202 | AC-202.3 | TC-202.3 | P0 | BE 2 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-002 | FR-005 | US-202 | AC-202.4 | TC-202.4 | P0 | BE 2 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-003 | FR-006 | US-203 | AC-203.1 | TC-203.1 | P0 | BE 1 | **PASS** (1/1) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-003 | FR-006 | US-203 | AC-203.2 | TC-203.2 | P0 | BE 1 · FE 1 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [FE](../evidence/RUN-20261102-25eb89f/frontend-junit.xml) |
| BR-003 | FR-006 | US-203 | AC-203.3 | TC-203.3 | P0 | BE 2 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-003 | FR-006 | US-203 | AC-203.4 | TC-203.4 | P0 | BE 1 | **PASS** (1/1) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-003 | FR-006 | US-203 | AC-203.5 | TC-203.5 | P0 | BE 1 | **PASS** (1/1) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-004 | FR-007 | US-204 | AC-204.1 | TC-204.1 | P0 | BE 1 | **PASS** (1/1) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-004 | FR-007 | US-204 | AC-204.2 | TC-204.2 | P0 | BE 1 · FE 2 · E2E 1 | **PASS** (4/4) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [FE](../evidence/RUN-20261102-25eb89f/frontend-junit.xml) [E2E](../../../test_reports/tai-lieu-18-ac-204-2-workspace-trong-huong-dan-tai-tai-lieu-va-khoa/report.md) |
| BR-005, BR-006 | FR-008 | US-205 | AC-205.1 | TC-205.1 | P1 | BE 1 · E2E 1 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [E2E](../../../test_reports/tai-lieu-20-ac-205-1-ac-205-3-xoa-tai-lieu-phai-xac-nhan-huy-giu-ng/report.md) |
| BR-005, BR-006 | FR-008 | US-205 | AC-205.2 | TC-205.2 | P1 | BE 1 | **PASS** (1/1) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-005, BR-006 | FR-008 | US-205 | AC-205.3 | TC-205.3 | P1 | FE 1 · E2E 1 | **PASS** (2/2) | [FE](../evidence/RUN-20261102-25eb89f/frontend-junit.xml) [E2E](../../../test_reports/tai-lieu-20-ac-205-1-ac-205-3-xoa-tai-lieu-phai-xac-nhan-huy-giu-ng/report.md) |
| BR-005, BR-006 | FR-008 | US-205 | AC-205.4 | TC-205.4 | P1 | BE 1 · FE 1 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [FE](../evidence/RUN-20261102-25eb89f/frontend-junit.xml) |
| BR-007, BR-014 | FR-009, NFR-003 | US-301 | AC-301.1 | TC-301.1 | P0 | BE 1 · E2E 1 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [E2E](../../../test_reports/hoi-dap-09-ac-301-1-ac-305-1-cau-tra-loi-kem-trich-dan-ten-tai-lie/report.md) |
| BR-007, BR-014 | FR-009, NFR-003 | US-301 | AC-301.2 | TC-301.2 | P0 | BE 3 · E2E 1 | **PASS** (4/4) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [E2E](../../../test_reports/hoi-dap-11-ac-301-2-cau-hoi-khong-dau-van-tim-duoc-noi-dung-co-dau/report.md) |
| BR-007, BR-014 | FR-009, NFR-003 | US-301 | AC-301.3 | TC-301.3 | P0 | FE 1 | **PASS** (1/1) | [FE](../evidence/RUN-20261102-25eb89f/frontend-junit.xml) |
| BR-007, BR-014 | FR-009, NFR-003 | US-301 | AC-301.4 | TC-301.4 | P0 | BE 1 · FE 1 · E2E 1 | **PASS** (3/3) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [FE](../evidence/RUN-20261102-25eb89f/frontend-junit.xml) [E2E](../../../test_reports/hoi-dap-17-ac-301-4-cau-hoi-rong-khong-duoc-gui/report.md) |
| BR-007, BR-014 | FR-009, NFR-003 | US-301 | AC-301.5 | TC-301.5 | P0 | BE 1 · FE 2 | **PASS** (3/3) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [FE](../evidence/RUN-20261102-25eb89f/frontend-junit.xml) |
| BR-008 | FR-010 | US-302 | AC-302.1 | TC-302.1 | P0 | BE 1 | **PASS** (1/1) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-008 | FR-010 | US-302 | AC-302.2 | TC-302.2 | P0 | BE 1 | **PASS** (1/1) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-009 | FR-011 | US-303 | AC-303.1 | TC-303.1 | P0 | BE 1 · E2E 1 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [E2E](../../../test_reports/hoi-dap-12-ac-304-1-ac-303-1-cau-hoi-ngoai-tai-lieu-duoc-bao-khong/report.md) |
| BR-009 | FR-011 | US-303 | AC-303.2 | TC-303.2 | P0 | BE 2 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-010 | FR-012 | US-304 | AC-304.1 | TC-304.1 | P0 | BE 1 · E2E 1 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [E2E](../../../test_reports/hoi-dap-12-ac-304-1-ac-303-1-cau-hoi-ngoai-tai-lieu-duoc-bao-khong/report.md) |
| BR-010 | FR-012 | US-304 | AC-304.2 | TC-304.2 | P0 | BE 1 | **PASS** (1/1) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-011 | FR-013 | US-305 | AC-305.1 | TC-305.1 | P0 | BE 1 · FE 2 · E2E 1 | **PASS** (4/4) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [FE](../evidence/RUN-20261102-25eb89f/frontend-junit.xml) [E2E](../../../test_reports/hoi-dap-09-ac-301-1-ac-305-1-cau-tra-loi-kem-trich-dan-ten-tai-lie/report.md) |
| BR-011 | FR-013 | US-305 | AC-305.2 | TC-305.2 | P0 | BE 1 · FE 2 · E2E 1 | **PASS** (4/4) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [FE](../evidence/RUN-20261102-25eb89f/frontend-junit.xml) [E2E](../../../test_reports/hoi-dap-10-ac-305-2-bam-trich-dan-mo-doan-goc-esc-dong-va-tra-focu/report.md) |
| BR-011 | FR-013 | US-305 | AC-305.3 | TC-305.3 | P0 | BE 1 | **PASS** (1/1) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-012, BR-013 | NFR-001, NFR-002 | US-306 | AC-306.1 | TC-306.1 | P0 | BE 1 | **PASS** (1/1) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-012, BR-013 | NFR-001, NFR-002 | US-306 | AC-306.2 | TC-306.2 | P0 | BE 1 | **PASS** (1/1) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-015 | FR-014 | US-401 | AC-401.1 | TC-401.1 | P1 | BE 1 · E2E 1 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [E2E](../../../test_reports/hoi-dap-13-ac-401-1-hoi-tiep-hieu-ngu-canh-luot-truoc/report.md) |
| BR-016 | FR-015 | US-402 | AC-402.1 | TC-402.1 | P1 | BE 1 · E2E 1 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [E2E](../../../test_reports/hoi-dap-14-ac-402-1-ac-402-2-gioi-han-pham-vi-vao-mot-tai-lieu/report.md) |
| BR-016 | FR-015 | US-402 | AC-402.2 | TC-402.2 | P1 | E2E 1 | **PASS** (1/1) | [E2E](../../../test_reports/hoi-dap-14-ac-402-1-ac-402-2-gioi-han-pham-vi-vao-mot-tai-lieu/report.md) |
| BR-017 | FR-016 | US-403 | AC-403.1 | TC-403.1 | P1 | BE 1 · E2E 1 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [E2E](../../../test_reports/hoi-dap-15-ac-403-1-ac-403-2-hoi-thoai-giu-thu-tu-cuoc-hoi-thoai-m/report.md) |
| BR-017 | FR-016 | US-403 | AC-403.2 | TC-403.2 | P1 | BE 1 · FE 1 · E2E 1 | **PASS** (3/3) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [FE](../evidence/RUN-20261102-25eb89f/frontend-junit.xml) [E2E](../../../test_reports/hoi-dap-15-ac-403-1-ac-403-2-hoi-thoai-giu-thu-tu-cuoc-hoi-thoai-m/report.md) |
| BR-021 | FR-017 | US-501 | AC-501.1 | TC-501.1 | P1 | BE 1 · E2E 1 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [E2E](../../../test_reports/hoi-dap-16-ac-501-1-danh-gia-cau-tra-loi-duoc-ghi-nhan/report.md) |
| BR-021 | FR-017 | US-501 | AC-501.2 | TC-501.2 | P1 | BE 1 | **PASS** (1/1) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-022 | FR-018 | US-502 | AC-502.1 | TC-502.1 | P1 | BE 1 · E2E 1 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [E2E](../../../test_reports/phan-quyen-03-ac-502-1-quan-ly-xem-so-lieu-theo-tuan/report.md) |
| BR-022 | FR-018 | US-502 | AC-502.2 | TC-502.2 | P1 | BE 1 · FE 1 · E2E 1 | **PASS** (3/3) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [FE](../evidence/RUN-20261102-25eb89f/frontend-junit.xml) [E2E](../../../test_reports/phan-quyen-02-ac-502-2-nguoi-dung-thuong-khong-co-muc-so-lieu-su-dung/report.md) |
| BR-028 | NFR-004 | — | AC-NFR-004 | TC-NFR-004 | P0 | BE 1 · E2E 1 | **PASS** (2/2) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [E2E](../../../test_reports/phan-quyen-01-ac-nfr-004-nguoi-dung-khac-khong-thay-va-khong-hoi-duoc/report.md) |
| BR-027 | NFR-008 | — | AC-NFR-008 | TC-NFR-008 | P0 | BE 1 | **PASS** (1/1) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| BR-019 | NFR-010 | — | AC-NFR-010 | TC-NFR-010 | P0 | BE 3 · FE 1 | **PASS** (4/4) | [BE](../evidence/RUN-20261102-25eb89f/backend-junit.xml) [FE](../evidence/RUN-20261102-25eb89f/frontend-junit.xml) |

## 3. Chiều ngược: test → AC
90/195 test tự động có ID AC và đã gắn vào ít nhất một dòng ở §2. Test không mang ID AC (105) là test hồi quy kỹ thuật (lỗi CR/NR/E2E, migration, đồng thời, tiện ích) và không chứng minh AC nào:

- `app/backend/tests/test_app_basics.py::test_health`
- `app/backend/tests/test_app_basics.py::test_schema_created`
- `app/backend/tests/test_app_basics.py::test_security_headers`
- `app/backend/tests/test_app_basics.py::test_unknown_api_route_is_problem_json`
- `app/backend/tests/test_app_basics.py::test_unexpected_error_hides_stack_trace`
- `app/backend/tests/test_app_basics.py::test_index_served`
- `app/backend/tests/test_app_basics.py::test_access_log_has_no_body`
- `app/backend/tests/test_app_basics.py::test_settings_from_env`
- `app/backend/tests/test_app_basics.py::test_wal_mode`
- `app/backend/tests/test_app_basics.py::test_serves_built_frontend`
- `app/backend/tests/test_app_basics.py::test_connection_usable_across_threads`
- `app/backend/tests/test_auth.py::test_login_is_case_insensitive_on_username`
- `app/backend/tests/test_auth.py::test_session_token_is_stored_hashed`
- `app/backend/tests/test_auth.py::test_idle_session_expires`
- `app/backend/tests/test_auth.py::test_password_not_stored_in_plaintext`
- `app/backend/tests/test_auth.py::test_login_validation_error`
- `app/backend/tests/test_auth.py::test_cookie_secure_flag_when_configured`
- `app/backend/tests/test_chat.py::test_unknown_conversation_404`
- `app/backend/tests/test_chat.py::test_turn_is_persisted`
- `app/backend/tests/test_chat.py::test_upload_then_ask_end_to_end`
- `app/backend/tests/test_chat.py::test_ai_failure_returns_503`
- `app/backend/tests/test_chat.py::test_invalid_citation_markers_are_dropped`
- `app/backend/tests/test_cli.py::test_create_user_and_duplicate`
- `app/backend/tests/test_cli.py::test_create_user_rejects_short_password`
- `app/backend/tests/test_cli.py::test_seed_demo_is_idempotent`
- `app/backend/tests/test_cli.py::test_backup_and_restore_roundtrip`
- `app/backend/tests/test_cli.py::test_restore_missing_backup`
- `app/backend/tests/test_cli.py::test_prune_audit_keeps_minimum_retention`
- `app/backend/tests/test_conversation.py::test_chunk_ids_not_reused_after_delete`
- `app/backend/tests/test_conversation.py::test_delete_requires_csrf`
- `app/backend/tests/test_conversation.py::test_scope_with_no_ready_document`
- `app/backend/tests/test_documents.py::test_encrypted_pdf_fails`
- `app/backend/tests/test_documents.py::test_filename_path_is_stripped`
- `app/backend/tests/test_documents.py::test_get_unknown_document_404`
- `app/backend/tests/test_documents.py::test_upload_requires_csrf`
- `app/backend/tests/test_generation.py::test_local_generator_picks_best_sentence_and_cites`
- `app/backend/tests/test_generation.py::test_local_generator_one_sentence_per_chunk_up_to_four`
- `app/backend/tests/test_generation.py::test_local_generator_never_follows_embedded_instructions`
- `app/backend/tests/test_generation.py::test_external_sends_only_retrieved_chunks_as_data`
- `app/backend/tests/test_generation.py::test_external_not_found_token`
- `app/backend/tests/test_generation.py::test_external_failure_raises_unavailable`
- `app/backend/tests/test_ingestion.py::test_chunk_page_respects_size_and_overlap`
- `app/backend/tests/test_ingestion.py::test_chunk_page_splits_very_long_sentence`
- `app/backend/tests/test_ingestion.py::test_chunk_page_blank`
- `app/backend/tests/test_ingestion.py::test_chunks_are_indexed_folded`
- `app/backend/tests/test_ingestion.py::test_recover_pending_on_startup`
- `app/backend/tests/test_ingestion.py::test_missing_file_marks_failed`
- `app/backend/tests/test_ingestion.py::test_ingest_skips_deleted_document`
- `app/backend/tests/test_metrics.py::test_feedback_on_someone_elses_turn_404`
- `app/backend/tests/test_metrics.py::test_metrics_counts_old_turns_in_their_week`
- `app/backend/tests/test_metrics.py::test_iso_week_format`
- `app/backend/tests/test_retrieval.py::test_finds_relevant_chunk_with_page`
- `app/backend/tests/test_retrieval.py::test_unrelated_question_returns_nothing`
- `app/backend/tests/test_retrieval.py::test_scope_limits_documents`
- `app/backend/tests/test_retrieval.py::test_per_document_limit_keeps_sources_diverse`
- `app/backend/tests/test_retrieval.py::test_history_breaks_ties_but_does_not_create_matches`
- `app/backend/tests/test_retrieval.py::test_other_users_documents_are_invisible`
- `app/backend/tests/test_review_fixes.py::test_cr01_slow_answer_does_not_block_other_users`
- `app/backend/tests/test_review_fixes.py::test_cr03_delete_during_ingestion_is_discarded`
- `app/backend/tests/test_review_fixes.py::test_nr02_old_schema_is_migrated`
- `app/backend/tests/test_review_fixes.py::test_nr10_restore_refuses_while_database_is_in_use`
- `app/backend/tests/test_review_fixes.py::test_cr04_oversized_body_rejected_with_413`
- `app/backend/tests/test_review_fixes.py::test_cr05_non_ascii_csrf_header_is_403`
- `app/backend/tests/test_review_fixes.py::test_cr06_unhandled_error_keeps_security_headers`
- `app/backend/tests/test_review_fixes.py::test_cr07_file_name_cannot_forge_document_tag`
- `app/backend/tests/test_review_fixes.py::test_cr09_retrieval_ignores_other_workspaces_at_scale`
- `app/backend/tests/test_review_fixes.py::test_cr10_bad_backup_leaves_live_data_untouched`
- `app/backend/tests/test_review_fixes.py::test_cr13_question_limit_message_uses_configuration`
- `app/backend/tests/test_review_fixes.py::test_cr14_expired_sessions_are_cleaned_up_on_login`
- `app/backend/tests/test_review_fixes.py::test_cr15_failed_batch_leaves_no_orphan_files`
- `app/backend/tests/test_review_fixes.py::test_generated_answer_type_unchanged`
- `app/backend/tests/test_textnorm.py::test_tokens_split_on_non_alphanumerics`
- `app/backend/tests/test_textnorm.py::test_content_terms_drop_stopwords_and_duplicates`
- `app/frontend/src/api/client.spec.ts::raises ApiError with the problem code and Vietnamese title`
- `app/frontend/src/api/client.spec.ts::calls the unauthorized handler on 401 auth.required (EC-15)`
- `app/frontend/src/api/client.spec.ts::maps network failures to a readable error (EC-04)`
- `app/frontend/src/api/client.spec.ts::handles 204 and sends scope only when given (FR-015)`
- `app/frontend/src/components/components.spec.ts::shows the login screen when not signed in, then the workspace after login`
- `app/frontend/src/components/components.spec.ts::lists name, status label and pages; only ready documents can be scoped`
- `app/frontend/src/components/components.spec.ts::renders [n] as a button that opens the citation`
- `app/frontend/src/components/components.spec.ts::marks not-found answers, deleted sources and processing warnings`
- `app/frontend/src/components/components.spec.ts::records feedback and reflects it with aria-pressed`
- `app/frontend/src/components/components.spec.ts::sends with Enter, scoped to selected documents, and shows the answer`
- `app/frontend/src/components/components.spec.ts::keeps the question and offers retry when sending fails (EC-04)`
- `app/frontend/src/components/components.spec.ts::renders weekly metrics`
- `app/frontend/src/composables/composables.spec.ts::drops a selection when the document is no longer ready`
- `app/frontend/src/composables/composables.spec.ts::reports load errors`
- `app/frontend/src/composables/composables.spec.ts::removes a document and its selection`
- `app/frontend/src/composables/composables.spec.ts::keeps the draft question when the session expires (EC-15)`
- `app/frontend/src/composables/composables.spec.ts::logs out, forgets the conversation and falls back to default config`
- `app/frontend/src/composables/composables.spec.ts::drops a conversation id the server no longer knows`
- `app/frontend/src/composables/composables.spec.ts::shows the dashboard link only to managers (US-502)`
- `app/frontend/src/composables/composables.spec.ts::cancel keeps the document`
- `app/frontend/src/composables/review-fixes.spec.ts::logout clears documents, selection and conversation`
- `app/frontend/src/composables/review-fixes.spec.ts::session expiry clears data too, and the saved draft is offered only to the same user`
- `app/frontend/src/composables/review-fixes.spec.ts::stays signed in and tells the user when the server cannot end the session`
- `app/frontend/src/composables/review-fixes.spec.ts::does not start polling again after stopPolling (unmount) while a request is in flight`
- `app/frontend/src/composables/review-fixes.spec.ts::ignores a stale poll response that arrives after a newer load (deleted document stays gone)`
- `app/frontend/src/composables/review-fixes.spec.ts::clearing a finished batch never removes rows of a newer batch`
- `app/frontend/src/utils/utils.spec.ts::explains documents still processing (EC-02)`
- `app/frontend/src/utils/utils.spec.ts::is disabled when only failed documents exist`
- `app/frontend/src/utils/utils.spec.ts::labels every status with icon and text (UX-002)`
- `app/frontend/src/utils/utils.spec.ts::formats percentages and dates`
- `app/frontend/src/utils/utils.spec.ts::sessionStore survives storage errors`
- `app/e2e/tests/auth.spec.ts::EC-15 phiên hết hạn giữ lại câu hỏi đang soạn`
