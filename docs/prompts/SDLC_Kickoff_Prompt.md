# SDLC Kickoff — một prompt cho toàn bộ vòng đời

> **Mục đích:** từ một BRD có sẵn, Claude Code tự chạy Analysis → Design → Planning → Build → Verify. Người dùng chỉ **phê duyệt** hoặc **yêu cầu sửa** ở các cổng.
> **Quy trình gốc:** `docs/agentic-sdlc-process.md`, `docs/AI_SDLC-SOP.md`.

## 1. Prompt duy nhất (dán vào đầu phiên Claude Code)

```text
/sdlc docs/02-requirements/BRD.md
Stack: <ví dụ: Python 3.12 FastAPI + SQLite, Vue 3 + TypeScript>.
Ràng buộc: <ví dụ: chạy on-prem, không gửi dữ liệu ra ngoài, tiếng Việt>.
Phạm vi: chỉ P0/P1 cho MVP. Dừng ở mỗi cổng để tôi duyệt.
```

Phiên bị ngắt hoặc muốn làm tiếp hôm sau: `/sdlc resume`. Muốn mở lại một phase: `/sdlc from design`.

Khuyến nghị bật chế độ **auto/accept edits** để agent ghi file không phải hỏi, và thêm vào `.claude/settings.json` một danh sách `permissions.allow` cho các lệnh test/lint/commit (`.venv/Scripts/python`, `npm run`, `npm test`, `git add`, `git commit`…) cùng `permissions.deny` cho `git push`, `git merge`, `git reset --hard`, `Edit(docs/checklists/**)`, `Edit(docs/prompts/**)`.

## 2. Kiến trúc workflow

```
                    ┌──────────────── /sdlc (orchestrator, phiên chính) ────────────────┐
 BRD ─► G1 Intake ─► G2 Analysis ─► G3a Architecture ─► G3b Detailed design ─► G4 Plan ─► G5 Build ─► G6 Verify ─► L2 người
         │              │                 │                    │                  │           │            │
   sdlc-intake    sdlc-analysis     sdlc-design A        sdlc-design B       sdlc-plan   sdlc-build   sdlc-verify
         └──────── sdlc-author soạn ──► tools/*.py kiểm deterministic ──► artifact-auditor chấm checklist ───┘
                                       (Build: ci_local.py · Verify: code-reviewer + security-auditor + test-plan)
```

| Thành phần | Loại | Vai trò |
|---|---|---|
| `.claude/skills/sdlc` | Skill (phiên chính) | Điều phối, giữ state, chạy cổng bằng `AskUserQuestion` |
| `.claude/skills/sdlc-intake`, `-analysis`, `-design`, `-plan`, `-build`, `-verify` | Skill theo phase | "Làm gì": đầu vào, prompt, đầu ra, checklist, tiêu chí cổng |
| `.claude/skills/test-plan` | Skill có sẵn | Master Test Plan IEEE 829 |
| `.claude/agents/sdlc-author` | Agent | Người soạn tài liệu/mã |
| `.claude/agents/artifact-auditor` | Agent | Audit độc lập theo checklist xlsx (người tạo ≠ người duyệt) |
| `.claude/agents/code-reviewer`, `security-auditor` | Agent có sẵn | Review L1 IEEE 1028, kiểm toán bảo mật |
| `tools/*.py` | Script | Kiểm tra deterministic: `checklist_fill`, `cross_view_audit`, `gen_diagrams`, `trace_matrix`, `ci_local`, `secret_scan`, `e2e_report` |

## 3. Vòng lặp mỗi phase

`ENTRY → SPECIFY → GENERATE (author) → VERIFY (tools) → AUDIT (auditor) → REFINE (≤ 2 vòng) → HANDOFF → GATE`

- **Approve** → tài liệu chuyển `Baseline`, ghi lịch sử phiên bản, commit `docs(<phase>): …`.
- **Yêu cầu sửa** → feedback nguyên văn quay lại GENERATE, tăng phiên bản, audit lại, cổng lại.
- **Quay lại phase trước** → mở lại phase đó và các phase phụ thuộc (change control).
- Trạng thái và handoff record: `docs/00-workflow/`.

## 4. Ánh xạ prompt và checklist

| Phase | Prompt (`docs/prompts/`) | Checklist (`docs/checklists/`) |
|---|---|---|
| 1–2 Intake | BRD_Prompt, BRD_Elicitation_Prompt | BRD_IEEE_29148 |
| 3 Analysis | PRD_Prompt | PRD_IEEE_29148 |
| 4a Architecture | SAD_Prompt | SAD_IEEE_1016 |
| 4b Detailed design | bluePrint_design, apiDesign, databaseDesign_SQL, UI-UX-Design, useCase, classDiagram, sequenceDiagram, activityDiagram, componentDiagram, deploymentDiagram | BluePrint_Design, API_Design, Database_Design, UI_UX_Design, UseCase_Document, Class/Sequence/Activity/Component/Deployment_Diagram |
| 5 Planning | — (rubric trong skill) | — |
| 6 Build | — (`AGENTS.md`, TDD) | cổng L0 `tools/ci_local.py` |
| 7 Verify | testPlan_prompt | Test_Plan_IEEE_829, Code_Review_IEEE_1028 |

## 5. Người làm gì

| Cổng | Người duyệt | Xem gì |
|---|---|---|
| G1 | PO | intent, gap report BRD, trả lời câu hỏi mở |
| G2 | PO + Tech Lead | PRD, user stories, AC, truy vết |
| G3a | Architect | SAD, ADR, stack |
| G3b | Architect + Tech Lead | blueprint, OpenAPI, DB, UI/UX, sơ đồ, cross-view audit |
| G4 | PO + Tech Lead | PLAN, thứ tự, rủi ro |
| G5 | Human owner | L0 xanh, truy vết code↔test, lệch thiết kế |
| G6 | Reviewer ≠ author | test report, L1 review, security audit, review record → L2, merge, release do người làm |

Agent không approve, merge, push, deploy (SOP §3.6).
