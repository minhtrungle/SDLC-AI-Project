# Ma trận truy vết — BR → FR/NFR → US → AC → Thiết kế → Code → Test

> Sinh tự động bởi `python tools/trace_matrix.py` (Phase 6 ↻). Không sửa tay.
> Test được gắn với AC qua ID trong docstring. Thiết kế lấy từ `elements.yaml` + SAD §5.2.

| BR | FR/NFR | Story | AC | Thiết kế (CMP) | Code | Test |
|---|---|---|---|---|---|---|
| BR-019 | FR-001, FR-002, NFR-010 | US-101 | AC-101.1, AC-101.2, AC-101.3, AC-101.4, AC-101.5, AC-101.6, AC-NFR-010 | CMP-03 | `app/auth.py`<br>`app/security.py` | `test_unauthenticated_api_is_rejected`<br>`test_login_success_returns_user_and_sets_secure_cookie`<br>`test_wrong_password_and_unknown_user_get_same_message`<br>`test_lockout_after_five_failures`<br>`test_logout_invalidates_session`<br>`test_write_without_csrf_is_forbidden`<br>`test_password_hashing`<br>`test_every_protected_endpoint_requires_login` |
| BR-020 | FR-003 | US-102 | AC-102.1, AC-102.2 | CMP-02, CMP-07, CMP-13 | `app/config.py`<br>`app/generation.py`<br>`app/main.py` | `test_config_defaults_to_local_ai`<br>`test_build_generator_defaults_to_local`<br>`test_build_generator_needs_flag_and_key` |
| BR-026 | FR-019, NFR-007 | US-103 | AC-103.1, AC-103.2, AC-103.3 | CMP-03, CMP-04, CMP-10, CMP-12 | `app/audit.py`<br>`app/auth.py`<br>`app/cli.py`<br>`app/documents.py` | `test_audit_log_for_login_events`<br>`test_delete_is_audited`<br>`test_upload_is_audited` |
| BR-001 | FR-004 | US-201 | AC-201.1, AC-201.2 | CMP-04 | `app/documents.py` | `test_upload_three_pdfs`<br>`test_one_bad_file_does_not_block_others` |
| BR-002 | FR-005 | US-202 | AC-202.1, AC-202.2, AC-202.3, AC-202.4 | CMP-02, CMP-04 | `app/documents.py`<br>`app/main.py` | `test_one_bad_file_does_not_block_others`<br>`test_pdf_extension_with_non_pdf_content_is_rejected`<br>`test_too_large_file_rejected_with_limit`<br>`test_document_limit`<br>`test_corrupt_pdf_fails_with_reason` |
| BR-003 | FR-006 | US-203 | AC-203.1, AC-203.2, AC-203.3, AC-203.4, AC-203.5 | CMP-04, CMP-05, CMP-11, CMP-12 | `app/cli.py`<br>`app/db.py`<br>`app/documents.py`<br>`app/ingestion.py` | `test_processing_document_is_never_a_source`<br>`test_status_lifecycle_processing_then_ready`<br>`test_corrupt_pdf_fails_with_reason`<br>`test_scanned_pdf_without_text_is_flagged` |
| BR-004 | FR-007 | US-204 | AC-204.1, AC-204.2 | CMP-04, CMP-12 | `app/cli.py`<br>`app/documents.py` | `test_list_shows_name_time_status_pages`<br>`test_empty_list` |
| BR-005, BR-006 | FR-008 | US-205 | AC-006, AC-205.1, AC-205.2, AC-205.4 | CMP-04 | `app/documents.py` | `test_delete_removes_document`<br>`test_deleted_document_is_never_used_again`<br>`test_old_citation_marked_deleted` |
| BR-007, BR-014 | FR-009, NFR-003 | US-301 | AC-301.1, AC-301.2, AC-301.4, AC-301.5 | CMP-01, CMP-08 | `app/chat.py`<br>`app/textnorm.py`<br>`app/web` | `test_answer_with_citation`<br>`test_answers_are_in_vietnamese_for_unaccented_question`<br>`test_empty_question_rejected`<br>`test_no_ready_documents`<br>`test_unaccented_query_matches_accented_text`<br>`test_fold_removes_vietnamese_diacritics` |
| BR-008 | FR-010 | US-302 | AC-302.1, AC-302.2 | CMP-03, CMP-06, CMP-08 | `app/auth.py`<br>`app/chat.py`<br>`app/retrieval.py` | `test_multi_document_answer_cites_both`<br>`test_conflicting_documents_both_cited` |
| BR-009 | FR-011 | US-303 | AC-303.1, AC-303.2 | CMP-07, CMP-08 | `app/chat.py`<br>`app/generation.py` | `test_general_knowledge_question_not_found`<br>`test_prompt_injection_text_is_not_obeyed`<br>`test_document_text_cannot_forge_tags` |
| BR-010 | FR-012 | US-304 | AC-304.1, AC-304.2 | CMP-06, CMP-08 | `app/chat.py`<br>`app/retrieval.py` | `test_general_knowledge_question_not_found` |
| BR-011 | FR-013 | US-305 | AC-305.1, AC-305.2, AC-305.3 | CMP-08 | `app/chat.py` | `test_answer_with_citation`<br>`test_citation_chunk_text` |
| BR-012, BR-013 | NFR-001, NFR-002 | US-306 | AC-306.1, AC-306.2 | — | `app/generation.py`<br>`app/retrieval.py` | `test_quality_and_latency` |
| BR-015 | FR-014 | US-401 | AC-401.1 | CMP-06, CMP-08 | `app/chat.py`<br>`app/retrieval.py` | `test_follow_up_question_uses_previous_context` |
| BR-016 | FR-015 | US-402 | AC-402.1 | CMP-06, CMP-08 | `app/chat.py`<br>`app/retrieval.py` | `test_scope_excludes_other_documents` |
| BR-017 | FR-016 | US-403 | AC-403.1, AC-403.2 | CMP-08 | `app/chat.py` | `test_new_conversation_has_no_history`<br>`test_five_turns_in_order` |
| BR-021 | FR-017 | US-501 | AC-501.1, AC-501.2 | CMP-09 | `app/metrics.py` | `test_feedback_is_saved_and_can_change`<br>`test_feedback_validation` |
| BR-022 | FR-018 | US-502 | AC-502.1, AC-502.2 | CMP-09 | `app/metrics.py` | `test_weekly_metrics`<br>`test_metrics_forbidden_for_regular_user` |
| BR-024 | NFR-005 | — | — | CMP-02 | `app/main.py` | `test_health` |
| BR-025 | NFR-006 | — | AC-025 | CMP-11, CMP-12 | `app/cli.py`<br>`app/db.py` | `test_backup_and_restore_roundtrip` |
| BR-027 | NFR-008 | — | AC-NFR-008 | — | `app/main.py` | `test_access_log_has_no_body`<br>`test_logs_never_contain_content` |
| BR-028 | NFR-004 | — | AC-NFR-004 | CMP-04 | `app/auth.py`<br>`app/documents.py` | `test_workspace_isolation_on_every_resource`<br>`test_other_users_documents_are_invisible` |
| BR-018 | — | US-404 | — | Hoãn (P2, BRD §12.1) | — | — |
| BR-023 | — | US-601 | — | Hoãn (P2, BRD §12.1) | — | — |

## Độ phủ
- Hàng trong phạm vi: 23; thiếu test: không có.
- Tổng số test function: 108; có ID AC/NFR trong docstring: 56.
- AC chỉ kiểm chứng bằng review (không tự động hóa): AC-102.3 (IT ký luồng dữ liệu), AC-201.3 / AC-204.2 / AC-305.2 / AC-402.2 phần giao diện (kiểm chứng bằng UI E2E thủ công, xem test-report §4), NFR-009 (inspection WCAG).
