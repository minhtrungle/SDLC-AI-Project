# Review record (IEEE 1028) — Phase 8 Review

| Mục | Giá trị |
|---|---|
| Đối tượng review | Nhánh `feat/chat-with-docs-sdlc` (working tree 2026-10-28, gồm thay đổi chưa commit) |
| Checklist | [Code_Review_IEEE_1028_Checklist.xlsx](../../checklists/Code_Review_IEEE_1028_Checklist.xlsx) |
| Tác giả | Agent (Claude) |
| Trạng thái | **L1 hoàn tất · L2 (người) chưa thực hiện · L3 chưa thực hiện** → **chưa được merge** |

> Luật bất biến của process: người/agent tạo nội dung ≠ người phê duyệt. Agent **không** approve, merge hay deploy. Tài liệu này chuẩn bị đầy đủ để reviewer con người ra quyết định.

## 1. Tháp đảm bảo chất lượng
| Tầng | Ai | Kết quả | Bằng chứng |
|---|---|---|---|
| L0 — máy | `tools/ci_local.py` (= CI) | **16/16 PASS** | [ci-log.txt](../ci/ci-log.txt) |
| L1 — agent review vòng 1 | Reviewer agent độc lập | 9/14 — chưa đạt; 15 finding | [code-review-L1.md](code-review-L1.md) |
| L1 — agent review vòng 2 | Reviewer agent độc lập khác | 10/14 — đạt ngưỡng, khuyến nghị sửa 3 Major trước merge; 12 finding mới | [code-review-L1-round2.md](code-review-L1-round2.md) |
| L1 — xác minh sửa vòng 2 | Tác giả + test hồi quy chứng minh thất bại khi bỏ bản sửa | Xem §3 | §3 |
| L2 — người | Reviewer ≠ tác giả | ☐ Chưa thực hiện | §5 |
| L3 — inspection rủi ro cao | IT/Bảo mật | ☐ Chưa thực hiện | §6 |
| L4 — demo với stakeholder | Đội kinh doanh | ☐ Chưa thực hiện | Report Playwright có thể dùng làm kịch bản demo |

## 2. Tóm tắt L1 vòng 1 → vòng 2
- Vòng 1: 15 finding (5 Major). Tất cả được sửa kèm test hồi quy, riêng CR-12 chuyển cho L3. Reviewer vòng 2 xác minh lại: 13 **Verified**, CR-03 Verified nhưng test yếu (đã sửa test ở NR-08), CR-12 hoãn có ghi nhận.
- Vòng 2 (sau tái cấu trúc Vue 3 + TypeScript): 12 finding mới, gồm 3 Major (NR-01, NR-02, NR-03).

## 3. Phản hồi của tác giả cho finding vòng 2 và các lỗi phát hiện thêm
Mỗi bản sửa Major có test hồi quy được **kiểm chứng là thất bại khi tạm gỡ bản sửa**.

| ID | Mức | Xử lý | Test hồi quy (thất bại khi gỡ bản sửa?) |
|---|---|---|---|
| NR-01 | Major | Upload lấy khóa ghi `BEGIN IMMEDIATE` trước khi đếm → song song không vượt `CWD_MAX_DOCS` | `test_nr01_parallel_uploads_respect_document_limit` (6 luồng, giới hạn 3) — **có** |
| NR-02 | Major | `PRAGMA user_version` + `migrate()` dựng lại FTS có cột `owner` cho CSDL/backup cũ | `test_nr02_old_schema_is_migrated` — **có** |
| NR-03 | Major | `reset()` cho `useDocuments`/`useChat`, gọi khi đăng xuất và hết phiên; bản nháp lưu kèm username | `review-fixes.spec.ts` › NR-03 (2 test) |
| NR-04 | Minor | Cờ `polling`: phản hồi đến muộn sau unmount/logout không khởi động lại polling; không poll tiếp khi 401 | `review-fixes.spec.ts` › NR-04 |
| NR-05 | Minor | Mỗi lô upload có id; timer chỉ xóa dòng thành công của lô đó | `review-fixes.spec.ts` › NR-05 |
| NR-06 | Minor | Đánh số request danh sách; bỏ phản hồi cũ → tài liệu đã xóa không hiện lại | `review-fixes.spec.ts` › NR-06 |
| NR-07 | Minor | Đồng bộ `maxLength`: question 4000 (code = hợp đồng); reason hợp đồng 5000, nghiệp vụ 500 → `feedback.invalid` (mô tả trong hợp đồng). **Còn lại:** client dùng path dạng chuỗi thay vì kiểu `paths` sinh tự động: chấp nhận cho MVP, vì cross-view audit (route = hợp đồng) và Playwright E2E phủ phần path | — |
| NR-08 | Minor | Test CR-03 viết lại: xóa **sau** bước kiểm tra (trong `chunk_page`), kiểm log không có ERROR | `test_cr03_…` — **có** (đã thử gỡ nhánh `IntegrityError`) |
| NR-09 | Nit | Đã thêm test cho reset, upload nối tiếp, poll xen delete (NR-03..06) | — |
| NR-10 | Nit | `restore` từ chối khi CSDL đang bị khóa (app đang chạy) | `test_nr10_restore_refuses_while_database_is_in_use` |
| NR-11 | Nit | `commit()` đưa vào trong `try`, lỗi commit vẫn dọn PDF | (phủ bởi `test_cr15_…`) |
| NR-12 | Nit | Đăng xuất lỗi mạng: báo lỗi và giữ đăng nhập (không giả vờ đã đăng xuất) | `review-fixes.spec.ts` › NR-12 |
| **E2E-1** | Major | Phát hiện khi chạy UI thật: connection SQLite dùng qua thread → 500 khi upload song song | `test_connection_usable_across_threads` |
| **E2E-2** | **Blocker** | Phát hiện bởi **Playwright**: FastAPI đóng dependency (commit) **sau** khi gửi response → request ngay sau đăng nhập không thấy phiên → 401 → người dùng bị đẩy về màn hình đăng nhập. Sửa: `DB = Depends(get_conn, scope="function")` (commit trước khi trả response) | Playwright: 0/3 → 5/5 đăng nhập thành công; gỡ bản sửa → lại 3/3 lần 401. Test uvicorn-trong-thread **không** tái hiện được nên đã bỏ (không giữ test không thể fail) |

## 4. Rubric 7 tiêu chí (đề xuất của L1 cho người review L2)
| Tiêu chí | Vòng 1 | Vòng 2 | Sau sửa (tự đánh giá của tác giả, **cần L2 xác nhận**) | Lý do |
|---|---|---|---|---|
| Đúng AC | 2 | 1 | 2 | NR-01, NR-05 đã sửa; 23/23 hàng truy vết có test; 20 kịch bản E2E theo AC |
| Test | 1 | 1 | 2 | 138 backend + 49 frontend + 20 Playwright; test hồi quy được chứng minh thất bại khi gỡ bản sửa |
| Thiết kế | 1 | 1 | 2 | Migration có version (NR-02), state reset (NR-03), hợp đồng API là nguồn sinh type |
| An toàn | 1 | 1 | 1 | Còn CR-12/DF-18 chờ L3 — giữ 1 cho tới khi L3 ký |
| Hiệu năng | 0 | 2 | 2 | Truy xuất 0,23–0,47 s ở 450 000 chunk; không còn khóa ghi khi sinh câu trả lời |
| Dễ đọc | 2 | 2 | 2 | ruff/ESLint/vue-tsc sạch |
| Truy vết | 2 | 2 | 2 | Module ↔ CMP; test ↔ AC (BE, FE, E2E) sinh tự động |
| **Tổng** | 9/14 | 10/14 | **13/14 (chưa xác nhận)** | Ngưỡng merge: ≥ 10/14 do người review L2 chấm |

## 5. Hướng dẫn cho reviewer L2 (con người)
**Kích thước:** process giới hạn PR ≤ 400 dòng. Thay đổi hiện tại khoảng 7 400 dòng viết tay (chưa kể lockfile, `schema.d.ts` sinh tự động), nên **không thể review như một PR**. Đề xuất chuỗi PR theo task, mỗi PR đọc diff trực tiếp:

| PR | Nội dung | Ước lượng (dòng, không gồm file sinh) |
|---|---|---|
| 1 | T-01 khung backend + cổng L0 + AGENTS.md | ~350 |
| 2 | T-02 auth/phiên/CSRF/audit + CLI | ~400 |
| 3 | T-03 tài liệu + ingestion | ~350 |
| 4 | T-04 truy xuất + bộ sinh + hỏi đáp | ~400 |
| 5 | T-05/T-06 xóa, hội thoại, đánh giá, số liệu | ~350 |
| 6 | T-07 LLM ngoài (High risk → L3) | ~200 |
| 7 | T-08/T-09 eval, test bảo mật, backup/restore | ~400 |
| 8 | Sửa review L1 vòng 1 (CR-01..15) | ~400 |
| 9 | T-10a tái cấu trúc thư mục + hợp đồng API | ~300 (chủ yếu di chuyển file) |
| 10–12 | T-10b frontend Vue: api/composables · components · tests | 3 × ~400 |
| 13 | Sửa review vòng 2 + E2E-1/E2E-2 | ~350 |
| 14 | Playwright E2E | ~300 |
| 15+ | Tài liệu Phase 1–8 (review riêng bởi PO/Architect) | — |

**Trình tự đề xuất cho người review:** đọc diff, không đọc tóm tắt. Chạy `python tools/ci_local.py`. Mở report Playwright (`npm run report` trong `app/e2e`). Chấm rubric §4.

## 6. Checklist inspection L3 (auth, dữ liệu kinh doanh, PII) — cho IT/Bảo mật
| # | Hạng mục | File | Câu hỏi kiểm tra |
|---|---|---|---|
| 1 | Băm mật khẩu | `cwd/security.py` | PBKDF2-SHA256 210 000 vòng, salt 16 byte, so sánh hằng thời gian: đạt chuẩn nội bộ? |
| 2 | Phiên | `cwd/auth.py` | Token 32 byte, lưu băm; cookie HttpOnly + SameSite=Strict (+Secure ở prod); hết hạn 8 h không hoạt động. Có cần thời hạn tuyệt đối? |
| 3 | Khóa đăng nhập | `cwd/security.py`, ADR-007 | **CR-12/DF-18:** khóa theo username → có thể bị lợi dụng; có cần khóa theo IP? |
| 4 | CSRF | `cwd/auth.py`, `src/api/client.ts` | Header token cho mọi POST/PUT/DELETE; so sánh bytes |
| 5 | Cô lập workspace | mọi router; `test_isolation.py`, E2E `access.spec.ts` | Mọi truy vấn lọc `user_id`; 404 cho tài nguyên người khác |
| 6 | Dữ liệu rời máy chủ | `cwd/generation_external.py`, ADR-003, SAD §8.1 | Mặc định không gửi gì ra ngoài; bật chỉ khi có văn bản cho phép (AC-102.3) |
| 7 | Prompt injection | `generation_external.py` | Chunk và tên file được escape; mô hình không có công cụ; trích dẫn kiểm tra với CSDL |
| 8 | Log | `cwd/main.py`, `test_logs_never_contain_content` | Không có nội dung tài liệu, câu hỏi, mật khẩu, token |
| 9 | Giới hạn tài nguyên | `BodyLimitMiddleware`, `MAX_FILES_PER_REQUEST` | 413 cho body quá lớn; cần đặt thêm giới hạn ở reverse proxy |
| 10 | Phụ thuộc | `requirements.txt`, `package-lock.json` | pip-audit, npm audit = 0; phiên bản pin, phát hành ≥ 14 ngày |

## 7. Pull request và phê duyệt
PR chưa được tạo vì thay đổi chưa được commit. Khi chủ dự án cho phép commit/push, tạo chuỗi PR theo §5. Mỗi PR mô tả: task, story/FR, AC, test, link report Playwright.

| Vai trò | Quyết định | Rubric | Ngày |
|---|---|---|---|
| Reviewer L2 (≠ tác giả) | ☐ Approve ☐ Request changes | __/14 | |
| IT/Bảo mật (L3, mục 1–10 §6) | ☐ Approve ☐ Reject | — | |
| Tech Lead | ☐ Approve ☐ Reject | — | |
