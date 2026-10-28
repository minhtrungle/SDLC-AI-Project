# Test Plan (IEEE 829) — Chat với tài liệu (MVP)

> **Prompt:** [testPlan_prompt.md](../prompts/testPlan_prompt.md) · **Checklist:** [Test_Plan_IEEE_829_Checklist.xlsx](../verification/Test_Plan_IEEE_829_Checklist.xlsx) → [test-plan-checklist-audit.md](test-plan-checklist-audit.md)
> Phiên bản 1.0 · 2026-10-28 · Tác giả: Agent (Claude) · Người duyệt: QA (STK-006) — chưa duyệt

## 1. Test plan identifier
TP-CWD-001 v1.0, áp dụng cho nhánh `feat/chat-with-docs-sdlc` (commit range `main...HEAD`).

## 2. Introduction
Kiểm chứng MVP đáp ứng FR-001..FR-019 và NFR-001..NFR-010 (PRD §3.9), mọi AC trong [USER_STORIES.md](../03-analysis/USER_STORIES.md), và launch gate PRD §5.1. Tài liệu tham chiếu: BRD v0.2, PRD v0.2, SAD v0.3, openapi.yaml, traceability.md.

## 3. Test items
| Item | Phiên bản | Nguồn |
|---|---|---|
| Backend `app/*.py` (CMP-02..CMP-13) | HEAD của nhánh | git |
| Web UI `app/web/*` (CMP-01) | HEAD | git |
| Schema `app/schema.sql` | HEAD | git |
| Bộ đánh giá `tests/eval` | HEAD | git |

## 4. Features to be tested
Mọi story trong phạm vi: US-101..103, US-201..205, US-301..306, US-401..403, US-501..502; NFR-001..008, NFR-010. Ánh xạ test ↔ AC: [traceability.md](../03-analysis/traceability.md) (sinh tự động).

## 5. Features not to be tested
| Hạng mục | Lý do |
|---|---|
| US-404, US-601 | Hoãn (P2) |
| AnthropicGenerator với API thật | Không có API key; chặn bởi OQ-006. Kiểm thử bằng client giả (hợp đồng gọi, xử lý lỗi, chống injection) |
| Độ chính xác trên dữ liệu thật | Chờ DEP-002; hiện dùng bộ tổng hợp (PD-04) |
| Tải đồng thời, khả dụng 99% (NFR-005), RTO thực tế | Cần môi trường prod (DEP-003) |
| Trình duyệt ngoài Chrome | Chỉ có Chrome/Edge trên máy kiểm thử |

## 6. Approach
| Mức | Kỹ thuật | Công cụ | Tự động |
|---|---|---|---|
| Unit | Hàm thuần: `textnorm`, `chunk_page`, `security`, bộ sinh | pytest | Có |
| Integration / API | `TestClient` qua toàn bộ stack + SQLite tạm + PDF sinh bằng fpdf2 | pytest | Có |
| Contract | Route FastAPI = `elements.yaml` = `openapi.yaml`; enum mã lỗi = `app/errors.py` | `tools/cross_view_audit.py` | Có |
| Security | 401 cho mọi endpoint bảo vệ (sinh từ registry), CSRF, cô lập workspace, injection, log sạch | pytest | Có |
| Quality (AI) | Bộ câu hỏi chuẩn: độ đúng, trích dẫn đúng, not_found đúng, P90; tập diễn đạt khác (không chặn) | `tests/eval` | Có |
| UI E2E | Chrome headless qua DevTools Protocol: đăng nhập → tải lên → hỏi → mở trích dẫn → Esc | script trong test-report §4 | Bán tự động |
| Static | ruff format/lint, compileall, quét secret, pip-audit | `tools/ci_local.py` | Có |
| Review | L1 agent review (IEEE 1028), L2 người, L3 inspection auth/data | review-record.md | Không |

TDD: test của mỗi AC viết trước code trong từng task T-01..T-09 (lịch sử commit).

## 7. Item pass/fail criteria
- Mỗi test case: pass khi mọi assertion đạt.
- Bản build đạt khi: 100% test pass; coverage ≥ 70%; lint/format sạch; 0 secret; 0 lỗ hổng phụ thuộc đã biết; cross-view audit 0 FAIL; mọi hàng truy vết có test; eval đạt ngưỡng 85% / 90% / 9 trên 10 / P90 ≤ 2 s.

## 8. Suspension criteria and resumption requirements
Tạm dừng khi cổng L0 không chạy được (lỗi môi trường) hoặc có Blocker bảo mật; tiếp tục sau khi sửa và chạy lại toàn bộ cổng.

## 9. Test deliverables
[test-report.md](test-report.md) · `ci-log.txt` · `coverage.xml` · `junit.xml` · `eval-report.json` · [code-review-L1.md](code-review-L1.md) · [review-record.md](review-record.md).

## 10. Testing tasks
| Task | Phụ thuộc |
|---|---|
| Viết test theo AC (TDD) | USER_STORIES |
| Chạy cổng L0 | Code |
| Chạy eval | Bộ tài liệu |
| UI E2E | Server chạy cục bộ |
| L1 review, sửa finding | Cổng L0 xanh |
| Lập test report | Tất cả trên |

## 11. Environmental needs
Windows 10, Python 3.15.2 (dev) / 3.12 (CI), font Unicode (Arial hoặc DejaVu) cho PDF test, Chrome cho UI E2E. Không cần mạng ngoài khi chạy test.

## 12. Responsibilities
| Vai trò | Trách nhiệm |
|---|---|
| Agent | Viết và chạy test tự động, L1 review, lập báo cáo |
| QA (STK-006) | Duyệt test plan, chạy UAT, ký test report |
| Đội kinh doanh | Cung cấp bộ câu hỏi chuẩn thật (DEP-002) |
| IT/Bảo mật | Inspection L3, ký AC-102.3 |

## 13. Staffing and training needs
QA cần biết chạy `python tools/ci_local.py` và đọc `eval-report.json` (README).

## 14. Schedule
Theo PLAN.md S1–S3; test chạy trong mỗi task, báo cáo cuối Phase 7.

## 15. Risks and contingencies
| Rủi ro | Giảm thiểu |
|---|---|
| Bộ câu hỏi tổng hợp thiên lệch (cùng tác giả với tài liệu) | Báo cáo riêng tập diễn đạt khác; bắt buộc chạy lại với DEP-002 trước go-live |
| Không kiểm thử được LLM thật | Client giả + cờ tắt mặc định |
| Không có CI server | `tools/ci_local.py` chạy cùng bước với workflow |

## 16. Approvals
| Vai trò | Quyết định | Ngày |
|---|---|---|
| QA | ☐ Approve ☐ Reject | |
| Tech Lead | ☐ Approve ☐ Reject | |
