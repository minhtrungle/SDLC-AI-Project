---
name: sdlc-plan
description: Phase 5 (Planning) của Agentic SDLC — phân rã SAD + USER_STORIES thành vertical slice nhỏ (PLAN.md + tasks/T-xx.md) có thứ tự, phụ thuộc, file chạm, AC cần xanh, rủi ro; đồng thời chuẩn bị AGENTS.md và cổng L0 (CI) cho phase Build. Được /sdlc giao cho sdlc-author; gọi riêng bằng /sdlc-plan.
argument-hint: "[ghi chú: số sprint, ưu tiên]"
---

# Phase 5 — Planning

## Tham chiếu
- Quy trình: `docs/agentic-sdlc-process.md` §6, `docs/AI_SDLC-SOP.md` §5.5.
- Đầu vào (Baseline): PRD, USER_STORIES, traceability, SAD, ADR, elements.yaml, blueprint, openapi.yaml, data model, UI/UX.

## Đầu ra

| File | Nội dung |
|---|---|
| `docs/05-implement/PLAN.md` | Mục tiêu, milestone/sprint, bảng task (ID · tiêu đề · US/FR · CMP · phụ thuộc · ước lượng · rủi ro), thứ tự thực hiện, Definition of Done, quyết định kèm lý do, rủi ro/unknown có owner |
| `docs/05-implement/tasks/T-xx-<slug>.md` | Mỗi task: mục tiêu · US/AC phải xanh · file/module chạm (theo CMP) · endpoint/entity/screen · test cần viết trước (tên test mang ID AC) · lệnh verify · tiêu chí xong · rủi ro |
| `AGENTS.md` (gốc repo) | Tạo nếu chưa có, cập nhật nếu đã có: sản phẩm, cấu trúc thư mục, lệnh build/test/lint, quy ước (Conventional Commits + `Refs:`, TDD, ID AC trong test, đổi API thì sửa hợp đồng trước), điều cấm (log dữ liệu nhạy cảm, secret, gọi AI ngoài…) lấy từ NFR/ADR |

## Quy tắc phân rã
1. **T-00 Tooling & skeleton** luôn đứng đầu: khung dự án theo ADR, cấu hình lint/format/type-check, test runner + coverage, `tools/ci_local.py` (cổng L0: format, lint, type, unit test, coverage ≥ 70%, secret scan, build), `tools/checklist_fill.py`, `tools/trace_matrix.py` nếu repo chưa có.
2. Các task tiếp theo là **vertical slice**: DB → API → UI → test của một story, chạy được độc lập; ưu tiên P0 trước, phụ thuộc trước.
3. Mỗi task đủ nhỏ cho một subagent hoàn thành trong một lượt (gợi ý: ≤ 400 dòng diff, ≤ 1 story chính).
4. Task chạm auth, upload, transaction, dữ liệu nhạy cảm đánh dấu `risk: high` → bắt buộc E2E và được `security-auditor` xem ở Verify.
5. Task cuối: E2E toàn luồng, seed demo, tài liệu chạy.

## Kiểm tra
- Deterministic: mọi US P0/P1 xuất hiện trong ít nhất một task; mọi CMP trong elements.yaml được ít nhất một task chạm; đồ thị phụ thuộc không có vòng (kiểm bằng script nhỏ trong scratchpad, ghi kết quả vào PLAN.md).
- Audit: `artifact-auditor` chấm PLAN.md theo rubric (không có checklist xlsx): đủ trường mỗi task · truy vết US/AC · thứ tự hợp lý · vertical slice · rủi ro có owner · DoD đo được. Biên bản `docs/05-implement/audits/plan-audit.md` (không cần xlsx).

## Tiêu chí qua cổng G4
- 100% AC P0/P1 được gán cho task; không có vòng phụ thuộc; T-00 có cổng L0 rõ ràng; AGENTS.md có lệnh chạy thật.
