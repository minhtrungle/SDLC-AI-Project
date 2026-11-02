# Test Summary Report (IEEE 829) — Chat với tài liệu (MVP)

| Mục | Giá trị |
|---|---|
| Mã | TSR-CWD-001 v1.2 · tham chiếu [Test Plan CWD-MTP-v2.0](TEST_PLAN.md) · [TEST_CASES.md](TEST_CASES.md) · [RTM.md](RTM.md) |
| Phạm vi | Nhánh `feat/chat-with-docs-sdlc`, commit `25eb89f`. Lần chạy bằng chứng [RUN-20261102-25eb89f](../evidence/RUN-20261102-25eb89f/README.md), 2026-11-02 |
| Tác giả | Agent (Claude) |
| Người duyệt | QA (STK-006): **chưa duyệt** |

## 1. Tóm tắt
| Hạng mục | Kết quả | Bằng chứng |
|---|---|---|
| Cổng L0 (`tools/ci_local.py`) | **16/17 PASS** (427 s). FAIL `py-dependency-audit`: DEF-001 | [ci-log.txt](../evidence/RUN-20261102-25eb89f/ci-log.txt) |
| Test backend (pytest) | **138/138** · coverage **97,73%** (ngưỡng 70%) | [backend-junit.xml](../evidence/RUN-20261102-25eb89f/backend-junit.xml) |
| Test frontend (Vitest) | **49/49** · statements 91,3% · branches 81,8% · functions 79,5% · lines 91,8% | [frontend-junit.xml](../evidence/RUN-20261102-25eb89f/frontend-junit.xml) |
| **E2E Playwright** | **20/20 · 0 flaky · 0 bỏ qua** (~60 s, Chrome) · 20 ảnh chụp + 20 video mp4 | [test_reports/](../../../test_reports/report.md) |
| Truy vết | 23/23 hàng có test. RTM: **58 AC — 57 PASS, 1 chờ review (AC-102.3), 0 GAP** | [RTM.md](RTM.md) · [traceability.md](../../03-analysis/traceability.md) |
| Hợp đồng API | Route = registry = `openapi.yaml`; type frontend khớp (`check:api`) | cross-view-audit |
| Eval chất lượng (bộ tổng hợp) | Đúng 100% · trích dẫn đúng 100% · not_found 100% · P90 35,6 ms / 50 tài liệu | [eval-report.json](../evidence/RUN-20261102-25eb89f/eval-report.json) |
| Eval từ đồng nghĩa (không chặn) | **12,5%**: hạn chế R-01 (§6) | eval-report.json |
| Phụ thuộc | **pip-audit: 3 CVE `pypdf 6.21.3`** (DEF-001, bản sửa 6.21.4) · npm audit 0 (frontend, e2e) | ci-log |

**Kết luận của QA agent:** mọi test chức năng đạt, nhưng cổng L0 **chưa xanh** vì DEF-001. Khuyến nghị: **NO-GO** cho tới khi nâng `pypdf` và chạy lại L0. Ngoài ra còn thiếu eval trên bộ câu hỏi thật (DEP-002) và review L2/L3 của con người ([review-record.md](../code-review/review-record.md)).

## 2. Variances (khác biệt so với kế hoạch)
| # | Khác biệt | Lý do |
|---|---|---|
| V-1 | Frontend Vue 3 + TypeScript; cấu trúc `app/{backend,frontend,api-contract,e2e}` (T-10, ADR-009) | Yêu cầu chủ dự án |
| V-2 | UI E2E chuyển từ script DevTools viết tay sang **bộ Playwright** chạy trong cổng L0 và CI | Yêu cầu chủ dự án |
| V-3 | Phạm vi dừng ở Phase 8 | Yêu cầu chủ dự án (PD-07) |

## 3. Comprehensiveness assessment
| Mức | Đã làm | Chưa làm (lý do) |
|---|---|---|
| Unit + API backend | 138 test, SQLite tạm, PDF sinh bằng fpdf2 | — |
| Component frontend | 49 test: hàm thuần, API client, component, composable, các race (NR-03..06) | — |
| **E2E (Playwright)** | 20 kịch bản qua trình duyệt thật + backend thật: đăng nhập/đăng xuất/phiên hết hạn, tải song song + từ chối file, xóa có xác nhận, hỏi đáp có trích dẫn, panel nguồn + Esc, không dấu, không tìm thấy, hỏi tiếp, phạm vi, lịch sử, đánh giá, cô lập workspace, phân quyền dashboard | Trình duyệt khác Chrome; E2E chế độ LLM ngoài |
| Bảo mật | 401 mọi endpoint (sinh từ registry); CSRF; cô lập (API + E2E); log sạch; injection; 413; khóa đăng nhập | Pentest, inspection L3 (người) |
| Đồng thời | Khóa ghi (CR-01), connection qua thread (E2E-1), upload song song vượt giới hạn (NR-01), commit sau response (E2E-2) | Test tải nhiều người dùng |
| Hiệu năng | P90 47 ms / 50 tài liệu; truy xuất 0,23–0,47 s ở 450 000 chunk | Khả dụng 99% (cần prod) |
| AI | Bộ tổng hợp 32 câu + 8 câu diễn đạt khác | Bộ câu hỏi thật DEP-002; LLM ngoài thật |
| Phục hồi | Backup/restore; backup hỏng; restore khi app chạy; migration schema cũ | Diễn tập trên máy thật |

## 4. Summary of results
### 4.1 Theo story
Mọi story US-101…US-502 trong phạm vi: **PASS** ở cả mức API (pytest) và mức người dùng (Playwright). Ngoại lệ: AC-102.3 chờ IT ký luồng dữ liệu; US-306 mới đo trên bộ tổng hợp. Chi tiết từng AC ↔ test (BE/FE/E2E): [traceability.md](../../03-analysis/traceability.md).

### 4.2 Playwright E2E
Bằng chứng từng kịch bản (ảnh chụp màn hình cuối test, video mp4 toàn bộ test, JSON) ở [test_reports/report.md](../../../test_reports/report.md).

| Spec | Kịch bản | Kết quả |
|---|---|---|
| `auth.spec.ts` | AC-101.1, AC-101.3, AC-101.2/101.6 (+AC-102.1 chế độ cục bộ hiển thị), AC-101.4 (API), EC-15 phiên hết hạn giữ câu hỏi | 5/5 |
| `documents.spec.ts` | AC-204.2 trạng thái trống, AC-201.1/201.2/202.1 tải song song + từ chối .docx, AC-205.1/205.3 xóa có xác nhận | 3/3 |
| `chat.spec.ts` | AC-301.1/305.1, AC-305.2 panel nguồn + Esc + trả focus, AC-301.2, AC-304.1/303.1, AC-401.1, AC-402.1/402.2, AC-403.1/403.2, AC-501.1, AC-301.4 | 9/9 |
| `access.spec.ts` | AC-NFR-004 cô lập workspace, AC-502.2, AC-502.1 | 3/3 |

## 5. Defects phát hiện trong quá trình kiểm chứng
| ID | Nguồn | Mức | Mô tả | Trạng thái |
|---|---|---|---|---|
| DF-01 | Audit thiết kế độc lập | Blocker | `chunks.id` tái sử dụng → trích dẫn cũ trỏ sai tài liệu | Đã sửa + test |
| T05-1 | TDD (AC-401.1) | Major | Hỏi tiếp chọn sai hợp đồng | Đã sửa + test |
| CR-01..15 | L1 vòng 1 | 5 Major | Khóa ghi, ingestion kẹt, body không giới hạn, truy xuất chậm, restore phá dữ liệu… | 14 đã sửa; CR-12 → L3 |
| NR-01..12 | L1 vòng 2 | 3 Major | Vượt giới hạn tài liệu khi song song, thiếu migration, rò dữ liệu giữa user cùng tab… | Đã sửa + test (NR-07 phần typed path chấp nhận) |
| E2E-1 | UI E2E (upload song song) | Major | Connection SQLite dùng qua thread → 500 | Đã sửa + test |
| DEF-001 | pip-audit (RUN-20261102) | Major | 3 CVE mới cho `pypdf 6.21.3`, bản sửa 6.21.4 | **Open**: Tech Lead duyệt nâng phiên bản |
| DEF-002 | Kiểm chứng bằng chứng | Minor | Test eval ghi `docs/07-verification/eval-report.json`, còn tài liệu trỏ `eval/eval-report.json` (bản cũ) | **Open**: Tech Lead |
| **E2E-2** | **Playwright** | **Blocker** | Commit phiên chạy **sau** khi gửi response → ngay sau đăng nhập bị 401 và bị đẩy về màn hình đăng nhập | Đã sửa (`scope="function"`); Playwright 0/3 → 5/5, gỡ bản sửa → 3/3 lỗi |

**Bài học:** 4 lỗi đồng thời/thứ tự (CR-01, NR-01, E2E-1, E2E-2) đều không bị test API tuần tự (`TestClient`) phát hiện. E2E-2, lỗi nặng nhất, làm hỏng toàn bộ luồng đăng nhập trên trình duyệt thật nhưng 138 test backend vẫn xanh. Playwright trong cổng L0 là lớp bắt được loại lỗi này.

## 6. Hạn chế và rủi ro còn mở
| ID | Nội dung | Đề xuất | Owner |
|---|---|---|---|
| R-01 | Truy xuất từ khóa bỏ sót từ đồng nghĩa (12,5%) | Embedding/LLM khi OQ-006 cho phép; hướng dẫn dùng đúng thuật ngữ | PO + IT |
| R-EV | Bộ eval do agent soạn, có thể lạc quan | Chạy lại với DEP-002 | QA + đội kinh doanh |
| R-LLM | AnthropicGenerator chưa chạy với API thật | Đo khi được phép | Tech Lead |
| R-L3 | CR-12/DF-18 khóa đăng nhập theo username | Inspection L3 (review-record §6) | IT/Bảo mật |

## 7. Evaluation
Còn 1 defect Major đang mở là DEF-001 (phụ thuộc có CVE). Không còn defect chức năng Blocker/Major nào. Mức sẵn sàng còn phụ thuộc review của con người: L2 chấm rubric, L3 inspection.

## 8. Summary of activities
| Hoạt động | Thời lượng chạy |
|---|---|
| Cổng L0 đầy đủ (17 bước, RUN-20261102) | 427 s |
| Backend pytest | ~80 s |
| Frontend Vitest | ~35 s |
| Playwright E2E | ~60–80 s |
| Benchmark truy xuất 450 000 chunk | 90 s |

## 9. Approvals
| Vai trò | Quyết định | Ngày |
|---|---|---|
| QA | ☐ Approve ☐ Reject | |
| Tech Lead | ☐ Approve ☐ Reject | |

## Lịch sử phiên bản
| Phiên bản | Ngày | Thay đổi |
|---|---|---|
| 1.1 | 2026-10-28 | Thêm kết quả Playwright E2E |
| 1.2 | 2026-11-02 | Chạy lại toàn bộ trên RUN-20261102-25eb89f; liên kết TEST_CASES, RTM và thư mục evidence; thêm DEF-001 (CVE pypdf), DEF-002; đổi khuyến nghị sang NO-GO; đổi tên file thành TEST_REPORT.md |
