---
name: sdlc-intake
description: Phase 1–2 của Agentic SDLC khi đã có BRD — dựng tài liệu Intake (intent, glossary, stakeholders, sources) từ BRD và kiểm tra BRD có đủ chất lượng IEEE 29148 để phân tích tiếp. Được /sdlc giao cho sdlc-author; cũng gọi riêng được bằng /sdlc-intake <đường dẫn BRD>.
argument-hint: "<đường dẫn BRD>"
---

# Phase 1–2 — Intake & BRD readiness

Đầu vào: BRD ở **$ARGUMENTS** (mặc định `docs/02-requirements/BRD.md`).

## Tham chiếu
- Quy trình: `docs/agentic-sdlc-process.md` §2–3, `docs/AI_SDLC-SOP.md` §5.2.
- Prompt: `docs/prompts/BRD_Prompt_IEEE_standard.md` (cấu trúc BRD chuẩn), `docs/prompts/BRD_Elicitation_Prompt_IEEE_standard.md` (bộ câu hỏi khám phá — dùng để **tìm lỗ hổng**, không phỏng vấn người dùng).
- Checklist: `docs/checklists/BRD_IEEE_29148_Checklist.xlsx`.

## Đầu ra

| File | Nội dung |
|---|---|
| `docs/01-intake/intent.md` | 7 mục: Problem, Proposed outcome, Affected users, Constraints, Success measures, Out of scope, Open questions; thêm risk tier (Low/Medium/High) có lý do |
| `docs/01-intake/glossary.md` | Thuật ngữ nghiệp vụ và kỹ thuật lấy từ BRD, định nghĩa một nghĩa |
| `docs/01-intake/stakeholders.md` | Ai · vai trò · concern · quyền duyệt ở cổng nào (G1–G6) |
| `docs/01-intake/sources.md` | Nguồn dữ liệu/hệ thống/tài liệu tham chiếu, phân loại dữ liệu (công khai/nội bộ/nhạy cảm) |
| `docs/02-requirements/BRD.md` | **Chỉ sửa khi BRD không có ID** cho BR/BO/ràng buộc: thêm ID, không đổi nghĩa, ghi lịch sử phiên bản. Mọi thay đổi khác là đề xuất trong `BRD_gap_report.md` |
| `docs/02-requirements/BRD_gap_report.md` | Đối chiếu BRD với các mục của BRD prompt và bộ câu hỏi elicitation: mục thiếu, mơ hồ, mâu thuẫn, yêu cầu không kiểm chứng được. Mỗi gap: ID `GAP-xx`, mức độ, câu hỏi cho PO, giả định `ASM-xx` đề xuất |

## Các bước
1. Đọc BRD toàn bộ. Liệt kê BO (mục tiêu kinh doanh), BR (yêu cầu nghiệp vụ), ràng buộc, KPI; đếm số lượng.
2. Đi qua từng nhóm câu hỏi của elicitation prompt; nhóm nào BRD không trả lời được → `GAP-xx`.
3. Viết 4 tài liệu intake; mọi câu chữ truy về mục BRD (ghi `BRD §x`).
4. Gán risk tier theo dữ liệu nhạy cảm, tích hợp ngoài, tác động người dùng. Risk tier quyết định độ sâu L3 ở Verify.
5. Audit (do orchestrator giao `artifact-auditor`): BRD theo `BRD_IEEE_29148_Checklist.xlsx` → `docs/02-requirements/audits/`.

## Tiêu chí qua cổng G1
- Không có GAP mức Critical chưa có giả định hoặc câu trả lời.
- Mọi BR có ID; intent.md đủ 7 mục; risk tier có lý do.
- Câu hỏi cho PO tối đa 4 câu quan trọng nhất được đưa lên cổng; số còn lại nằm trong gap report.
