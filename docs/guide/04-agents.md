# 04 — Tra cứu Agent

Agent (subagent) chạy **trong ngữ cảnh riêng**, làm xong thì trả về một bản tóm tắt ngắn; kết quả chính nằm trong file. Định nghĩa ở `.claude/agents/<tên>.md`. Xem danh sách bằng lệnh `/agents`.

## Cách gọi
Agent không có lệnh `/`. Yêu cầu bằng lời, nêu tên agent và đủ ba thứ: **đối tượng**, **tiêu chuẩn/checklist**, **phạm vi**.

```text
Dùng agent <tên> để <việc> cho <file/phạm vi> theo <checklist/tiêu chuẩn>.
```

Muốn chạy song song: yêu cầu trong cùng một câu, ví dụ "chạy song song code-reviewer và security-auditor trên diff so với main".

---

## `sdlc-author` — Người soạn
| | |
|---|---|
| Khi dùng | Soạn hoặc sửa artifact của một phase; sửa theo biên bản audit |
| Đọc | Skill phase (`.claude/skills/sdlc-*/SKILL.md`), `AGENTS.md`, prompt trong `docs/prompts/`, checklist liên quan |
| Ghi | Chỉ các đầu ra của phase đó (tài liệu hoặc code); commit chỉ ở phase Build |
| Không làm | Tự chấm đạt, sửa checklist/prompt, push/merge |
| Trả về | File đã tạo/sửa + phiên bản, lệnh đã chạy + kết quả, giả định `ASM-xx`, câu hỏi mở |

Prompt mẫu:
```text
Dùng agent sdlc-author: đọc .claude/skills/sdlc-analysis/SKILL.md và thực hiện Phase 3 từ docs/02-requirements/BRD.md. Phạm vi P0/P1.
```
```text
Dùng agent sdlc-author: sửa docs/03-analysis/PRD.md theo các phát hiện Major trong docs/03-analysis/audits/PRD_IEEE_29148_Checklist.md. Ghi mỗi phát hiện đã sửa ở mục nào.
```

## `artifact-auditor` — Auditor tài liệu
| | |
|---|---|
| Khi dùng | Sau khi tài liệu được soạn hoặc sửa; trước mỗi cổng |
| Đầu vào | Một artifact + một checklist `docs/checklists/*.xlsx` (+ biên bản vòng trước nếu có) |
| Ghi | `audits/<Checklist>.md` (bảng Row/Item/Status/Notes) và `audits/<Checklist>_v<phiên bản>.xlsx` |
| Status | `Done` · `In Progress` · `Pending` · `N/A` (lấy từ data validation của template) |
| Không làm | Sửa artifact, sửa template, commit |
| Trả về | Bảng đếm Status, phát hiện Critical/Major, nhận định "Sẵn sàng qua cổng" / "Cần sửa" |

Prompt mẫu:
```text
Dùng agent artifact-auditor audit docs/04-design/SAD.md (v0.3) theo docs/checklists/SAD_IEEE_1016_Checklist.xlsx, đối chiếu PRD.md và elements.yaml. Có biên bản vòng trước ở docs/04-design/audits/SAD_IEEE_1016_Checklist.md.
```

Bảng ghép artifact ↔ checklist: xem [03-skills.md](03-skills.md) mục `/sdlc-design`.

## `code-reviewer` — Review mã L1 (IEEE 1028)
| | |
|---|---|
| Khi dùng | Sau Build, trước khi mở PR; sau mỗi vòng sửa lỗi |
| Phạm vi mặc định | `git diff main...HEAD` + thay đổi chưa commit |
| Chạy | pytest + coverage, ruff, lint/type-check/test frontend, `check:api` |
| Ghi | `docs/07-verification/code-review/code-review-L1-round<N>.md` + `Code_Review_IEEE_1028_Checklist_round<N>.xlsx` |
| Status | `Pass` · `Fail` · `N/A` · `Pending` |
| Phát hiện | ID `CR-xx`, mức Critical/Major/Minor/Nit, `file:dòng` |

Prompt mẫu:
```text
Dùng agent code-reviewer review nhánh hiện tại so với main. Verify lại các phát hiện của round 3.
```

## `security-auditor` — Kiểm toán bảo mật
| | |
|---|---|
| Khi dùng | Thay đổi chạm auth, upload, ingestion, gọi AI, transaction, header/CSP, dependency; trước review L3 |
| Đối chiếu | NFR/BR bảo mật của dự án, SAD §8.1, ADR, OWASP Top 10 (2021), STRIDE |
| Ghi | Biên bản markdown + checklist đã điền Status |

Prompt mẫu:
```text
Dùng agent security-auditor kiểm toán module upload và auth trên diff so với main, tập trung NFR-004 (lọc user_id) và NFR-008 (không log dữ liệu nhạy cảm).
```

## Ghép agent theo phase

| Phase | Soạn | Audit |
|---|---|---|
| 1–2 Intake | `sdlc-author` | `artifact-auditor` (BRD) |
| 3 Analysis | `sdlc-author` | `artifact-auditor` (PRD) |
| 4 Design | `sdlc-author` (nhiều, song song) | `artifact-auditor` ×11 |
| 5 Plan | `sdlc-author` | `artifact-auditor` (rubric) |
| 6 Build | `sdlc-author` mỗi task | cổng L0 tự động |
| 7 Verify | `sdlc-author` (report, sửa lỗi) + `/test-plan` | `code-reviewer` ∥ `security-auditor` |

Quy tắc: **không** dùng cùng một agent vừa soạn vừa audit cùng một artifact.
