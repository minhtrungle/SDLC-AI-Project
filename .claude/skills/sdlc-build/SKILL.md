---
name: sdlc-build
description: Phase 6 (Implementation) của Agentic SDLC — thực hiện từng task trong docs/05-implement/tasks/ theo vòng TDD SPECIFY → GENERATE → VERIFY → REFINE, giữ code khớp hợp đồng OpenAPI và thiết kế, chạy cổng L0 sau mỗi task và commit nhỏ theo Conventional Commits. Được /sdlc giao cho sdlc-author (một task mỗi lần); gọi riêng bằng /sdlc-build T-xx.
argument-hint: "<T-xx | next | all>"
---

# Phase 6 — Build

Task: **$ARGUMENTS** (`next` = task chưa xong đầu tiên mà mọi phụ thuộc đã xong).

## Tham chiếu
`AGENTS.md` (bắt buộc đọc trước), `docs/agentic-sdlc-process.md` §7, `docs/AI_SDLC-SOP.md` §5.6, `docs/05-implement/PLAN.md`, file task, và các thiết kế mà task trỏ tới (SAD, elements.yaml, ADR, openapi.yaml, data model, UI/UX).

## Cách orchestrator điều phối
- Chạy tuần tự theo đồ thị phụ thuộc trong PLAN.md, **một `sdlc-author` mỗi task** (ngữ cảnh sạch, diff nhỏ). Hai task không chung file và không phụ thuộc nhau có thể chạy song song với `isolation: "worktree"`, rồi orchestrator merge lần lượt và chạy lại L0.
- Sau mỗi task orchestrator tự chạy L0 và cập nhật cột trạng thái task trong PLAN.md. Task fail L0 sau 2 vòng sửa → đánh `Blocked`, ghi lý do, chuyển task khác không phụ thuộc; đưa lên cổng G5.
- Không có cổng cho từng task; cổng G5 ở cuối phase. Nếu PLAN có milestone, orchestrator có thể dừng ở cổng phụ sau mỗi milestone khi người dùng yêu cầu trong Kickoff.

## Vòng cho một task (author làm)
1. **SPECIFY** — đọc task + AC; viết test **trước**, mỗi test mang ID AC (backend: docstring `"""AC-xxx.n …"""`; frontend: trong `describe`/`it`; E2E: `test("AC-xxx …")`). Chạy để thấy test đỏ.
2. **GENERATE** — code theo vertical slice DB → API → UI. Đổi API ⇒ sửa `app/api-contract/openapi.yaml` và `elements.yaml` trước, rồi sinh type (`npm run gen:api`). Module đặt đúng đường dẫn của `CMP-xx`.
3. **VERIFY** — chạy lệnh trong task và cổng L0:
   ```bash
   .venv/Scripts/python tools/ci_local.py            # hoặc lệnh tương đương trong AGENTS.md
   .venv/Scripts/python tools/cross_view_audit.py   # code vẫn khớp thiết kế
   ```
   Task `risk: high` (auth, upload, transaction) chạy thêm E2E Playwright.
4. **REFINE** — sửa nhỏ nhất đến khi xanh. Không xóa hay nới test để qua; không hạ ngưỡng coverage.
5. **Commit** — một hoặc vài commit nhỏ: `feat(<scope>): …` / `test(<scope>): …`, thân có `Refs: US-xxx, FR-xxx` và dòng attribution theo hướng dẫn phiên. Không push.
6. Cập nhật truy vết: `.venv/Scripts/python tools/trace_matrix.py` (nếu có).

Phát hiện thiết kế sai trong lúc code: không tự lệch khỏi thiết kế. Ghi `DEV-xx` (vấn đề, đề xuất, ảnh hưởng) vào file task; nếu là quyết định khó đảo ngược thì soạn ADR mới trạng thái `Proposed` và đưa lên cổng G5.

## Tiêu chí qua cổng G5
- Mọi task `Done` hoặc `Blocked` có lý do; L0 xanh trên HEAD (dán số thật: số test, coverage).
- `trace_matrix.py` không còn dòng P0/P1 thiếu test (hoặc liệt kê rõ).
- `cross_view_audit.py` pass; không còn `DEV-xx`/ADR `Proposed` chưa được người dùng quyết.
