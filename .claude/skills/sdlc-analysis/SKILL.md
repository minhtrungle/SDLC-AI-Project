---
name: sdlc-analysis
description: Phase 3 (Analysis) của Agentic SDLC — từ BRD đã baseline sinh PRD/SRS theo IEEE 29148 (FR/NFR có ID, đo được), USER_STORIES với Acceptance Criteria Given-When-Then và ma trận truy vết BR→FR/NFR→US→AC. Được /sdlc giao cho sdlc-author; gọi riêng bằng /sdlc-analysis.
argument-hint: "[ghi chú phạm vi]"
---

# Phase 3 — Analysis

## Tham chiếu
- Quy trình: `docs/agentic-sdlc-process.md` §4, `docs/AI_SDLC-SOP.md` §5.3.
- Prompt: `docs/prompts/PRD_Prompt_IEEE_standard.md`.
- Checklist: `docs/checklists/PRD_IEEE_29148_Checklist.xlsx`.
- Đầu vào: `docs/02-requirements/BRD.md` (Baseline), `docs/01-intake/*`, gap report và giả định `ASM-xx` đã được xác nhận ở G1.

## Đầu ra (`docs/03-analysis/`)

| File | Nội dung bắt buộc |
|---|---|
| `PRD.md` | Đủ các mục của PRD prompt (1 Executive Summary & OKR · 2 Personas & Journey · 3 FR & Stories · 4 UX & Edge cases · 5 Launch gate & Analytics) **cộng** một mục đặc tả hợp nhất (ví dụ §3.9): bảng FR-xxx và NFR-xxx — mô tả · nguồn BR · ưu tiên P0/P1/P2 · tiêu chí kiểm chứng đo được · trong/ngoài phạm vi MVP. NFR theo ISO 25010 (hiệu năng, bảo mật, khả dụng, khả năng tiếp cận, bảo trì) và có ngưỡng số. Có mục Out of scope và Assumptions |
| `USER_STORIES.md` | Story `US-xxx`: "Là [persona], tôi muốn …, để …", gắn FR-ID, ưu tiên; AC `AC-xxx.n` dạng Given-When-Then cho mọi P0/P1, gồm cả luồng lỗi và biên. Mỗi AC kiểm thử tự động được hoặc ghi rõ "UAT thủ công" |
| `traceability.md` | Ma trận BR → FR/NFR → US → AC. Cột design/code/test để trống, điền ở phase sau. Nếu repo có `tools/trace_matrix.py` thì cập nhật bảng `ROWS` của nó và sinh file bằng công cụ |

## Các bước
1. Tách mỗi BR thành FR/NFR; mỗi FR một hành vi, không dùng từ mơ hồ ("nhanh", "thân thiện", "v.v.").
2. Kiểm tra hai chiều: mọi BR trong phạm vi có ≥ 1 FR/NFR; mọi FR/NFR có nguồn BR (hoặc ghi "phái sinh" kèm lý do).
3. Viết story + AC; mọi FR P0 có ≥ 1 story và AC.
4. Kiểm tra mâu thuẫn giữa FR, NFR và ràng buộc BRD; ghi vào mục Open issues.
5. Deterministic: đếm BR/FR/NFR/US/AC và xác nhận không có ID trùng hay mồ côi (dùng `Grep`, hoặc `tools/trace_matrix.py` nếu có — exit 1 ở phase này được chấp nhận vì chưa có test, nhưng không được có dòng thiếu US/AC).
6. Audit: PRD (kèm USER_STORIES) theo PRD checklist → `docs/03-analysis/audits/`.

## Tiêu chí qua cổng G2
- 100% BR trong phạm vi được phủ; 100% FR P0 có AC Given-When-Then.
- NFR có ngưỡng đo được; checklist PRD không còn mục `Pending`.
