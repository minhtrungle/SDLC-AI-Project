# Hướng dẫn sử dụng Agent & Skill cho Agentic SDLC

Bộ hướng dẫn này giúp bạn dùng Claude Code để đi từ **BRD → Analysis → Design → Planning → Build → Verify**. Có thể chạy tự động bằng một prompt duy nhất hoặc gọi từng bước thủ công.

## Bắt đầu từ đâu?

| Bạn muốn… | Đọc |
|---|---|
| Cài đặt và chạy lần đầu trong 5 phút | [01-quick-start.md](01-quick-start.md) |
| Chạy toàn bộ quy trình bằng một prompt, chỉ phê duyệt ở cổng | [02-workflow-tu-dong.md](02-workflow-tu-dong.md) |
| Tra cứu từng skill (lệnh, đối số, đầu vào, đầu ra) | [03-skills.md](03-skills.md) |
| Tra cứu từng agent (khi nào dùng, cách gọi, đầu ra) | [04-agents.md](04-agents.md) |
| Làm thủ công từng phase, có prompt mẫu để copy | [05-lam-thu-cong.md](05-lam-thu-cong.md) |
| Gặp lỗi hoặc tình huống khó | [06-faq.md](06-faq.md) |

## Toàn cảnh trong một hình

```
                     ┌──────────────── /sdlc (điều phối) ────────────────┐
BRD ─► G1 Intake ─► G2 Analysis ─► G3a Kiến trúc ─► G3b Thiết kế chi tiết ─► G4 Plan ─► G5 Build ─► G6 Verify ─► L2 (người)
          │             │               │                   │                 │           │            │
    /sdlc-intake  /sdlc-analysis  /sdlc-design A     /sdlc-design B      /sdlc-plan  /sdlc-build  /sdlc-verify
          └── sdlc-author soạn ─► tools/*.py kiểm tra ─► artifact-auditor chấm checklist ─► bạn duyệt ──┘
                                 (Verify: /test-plan + code-reviewer + security-auditor)
```

## Danh mục

**Skill** — gọi bằng `/tên` trong ô chat Claude Code:

| Skill | Phase | Một câu |
|---|---|---|
| `/sdlc` | Tất cả | Điều phối toàn bộ, dừng ở cổng cho bạn duyệt |
| `/sdlc-intake` | 1–2 | Dựng intent/glossary/stakeholders/sources, soi lỗ hổng BRD |
| `/sdlc-analysis` | 3 | PRD (FR/NFR), User Stories + AC, truy vết |
| `/sdlc-design` | 4 | A: SAD + ADR + elements.yaml · B: blueprint, API, DB, UI/UX, 6 sơ đồ UML |
| `/sdlc-plan` | 5 | PLAN.md + tasks/T-xx + AGENTS.md |
| `/sdlc-build` | 6 | Code từng task theo TDD, cổng L0, commit nhỏ |
| `/sdlc-verify` | 7 | Test plan, chạy test, review L1, bảo mật, review record |
| `/test-plan` | 7 | Master Test Plan IEEE 829 + checklist |

**Agent** — gọi bằng lời ("Dùng agent … để …"):

| Agent | Vai trò | Có sửa file dự án? |
|---|---|---|
| `sdlc-author` | Người soạn tài liệu / code | Có |
| `artifact-auditor` | Audit tài liệu theo checklist .xlsx | Không — chỉ ghi biên bản |
| `code-reviewer` | Review mã L1 theo IEEE 1028 | Không — chỉ ghi biên bản |
| `security-auditor` | Kiểm toán bảo mật OWASP/STRIDE | Không — chỉ ghi biên bản |

## Ba nguyên tắc cần nhớ

1. **Người tạo ≠ người duyệt.** Agent soạn không tự chấm đạt; agent audit không sửa tài liệu; chỉ **bạn** phê duyệt.
2. **Không có bằng chứng = chưa xong.** Mọi "đạt" phải kèm số liệu thật (test, coverage, checklist).
3. **Agent không approve, merge, push, deploy.** Bước L2 review → merge → release luôn do con người làm.

## Tài liệu gốc
- Quy trình: [../agentic-sdlc-process.md](../agentic-sdlc-process.md), SOP: [../AI_SDLC-SOP.md](../AI_SDLC-SOP.md)
- Prompt chuẩn: [../prompts/](../prompts/) · Checklist: [../checklists/](../checklists/)
- Định nghĩa skill: `.claude/skills/*/SKILL.md` · Định nghĩa agent: `.claude/agents/*.md`
