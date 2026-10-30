# 03 — Tra cứu Skill

Skill là bộ hướng dẫn chạy **ngay trong phiên hiện tại**. Gọi bằng `/tên-skill [đối số]`. Định nghĩa đầy đủ ở `.claude/skills/<tên>/SKILL.md`.

---

## `/sdlc` — Điều phối toàn bộ
| | |
|---|---|
| Đối số | `<BRD> <ghi chú>` · `resume` · `from <phase>` |
| Làm gì | Gọi lần lượt các skill phase qua agent `sdlc-author`, chạy công cụ kiểm tra, gọi agent audit, dừng ở 7 cổng |
| Đầu ra | `docs/00-workflow/sdlc-state.md`, `handoff-<phase>.md` + artifact của mọi phase |
| Ví dụ | `/sdlc docs/02-requirements/BRD.md Stack: FastAPI + Vue 3. Phạm vi: P0/P1.` |

Xem chi tiết ở [02-workflow-tu-dong.md](02-workflow-tu-dong.md).

---

## `/sdlc-intake` — Phase 1–2
| | |
|---|---|
| Đối số | đường dẫn BRD (mặc định `docs/02-requirements/BRD.md`) |
| Prompt dùng | `BRD_Prompt_IEEE_standard.md`, `BRD_Elicitation_Prompt_IEEE_standard.md` |
| Đầu ra | `docs/01-intake/{intent,glossary,stakeholders,sources}.md`, `docs/02-requirements/BRD_gap_report.md` |
| Audit tiếp theo | `artifact-auditor` + `BRD_IEEE_29148_Checklist.xlsx` |
| Ví dụ | `/sdlc-intake docs/02-requirements/BRD.md` |

## `/sdlc-analysis` — Phase 3
| | |
|---|---|
| Đối số | ghi chú phạm vi (tùy chọn) |
| Prompt dùng | `PRD_Prompt_IEEE_standard.md` |
| Đầu ra | `docs/03-analysis/PRD.md`, `USER_STORIES.md`, `traceability.md` |
| Kiểm tra | `tools/trace_matrix.py` (nếu có) |
| Audit tiếp theo | `artifact-auditor` + `PRD_IEEE_29148_Checklist.xlsx` |
| Ví dụ | `/sdlc-analysis chỉ P0 cho sprint đầu` |

## `/sdlc-design` — Phase 4
| | |
|---|---|
| Đối số | `A` (kiến trúc) · `B` (toàn bộ chi tiết) · `B <artifact>` với artifact ∈ `blueprint, api, database, uiux, usecase, class, sequence, activity, component, deployment` |
| Kiểm tra | `tools/gen_diagrams.py`, `tools/cross_view_audit.py --write` |
| Ví dụ | `/sdlc-design A` · `/sdlc-design B api` |

| Đối số | Đầu ra | Prompt | Checklist để audit |
|---|---|---|---|
| `A` | `SAD.md`, `adr/ADR-*.md`, `elements.yaml` | `SAD_Prompt_IEEE_standard.md` | `SAD_IEEE_1016_Checklist.xlsx` |
| `B blueprint` | `blueprint.md` | `bluePrint_design_prompt.md` | `BluePrint_Design_IEEE_1016_2009_Checklist.xlsx` |
| `B api` | `app/api-contract/openapi.yaml`, `openapi.md` | `apiDesign_prompt.md` | `API_Design_IEEE-1016-2009Checklist.xlsx` |
| `B database` | `data/model.md`, `schema.sql` | `databaseDesign_SQL_prompt.md` | `Database_Design_Checklist.xlsx` |
| `B uiux` | `UI_UX_design/` | `UI-UX-Design_prompt.md` | `UI_UX_Design_IEEE-1016-2009_Checklist.xlsx` |
| `B usecase` | `use_cases.md`, `diagrams/use_case_diagram.drawio` | `useCase_prompt.md` | `UseCase_Document_UML2.0_Checklist.xlsx` |
| `B class` | `diagrams/class_diagram.drawio` | `classDiagram_prompt.md` | `Class_Diagram_UML2.0_Checklist.xlsx` |
| `B sequence` | `diagrams/sequence_diagram.drawio` | `sequenceDiagram_prompt.md` | `Sequence_Diagram_UML2.0_Checklist.xlsx` |
| `B activity` | `diagrams/activity_diagram.drawio` | `activityDiagram_prompt.md` | `Activity_Diagram_UML2.0_Checklist.xlsx` |
| `B component` | `diagrams/component_diagram.drawio` | `componentDiagram_prompt.md` | `Component_Diagram_UML2.0_Checklist.xlsx` |
| `B deployment` | `diagrams/deployment_diagram.drawio` | `deploymentDiagram_prompt.md` | `Deployment_Diagram_UML2.0_Checklist.xlsx` |

Thứ tự khuyên dùng cho `B`: `api` → `database` → `blueprint` → `uiux` → các sơ đồ.

## `/sdlc-plan` — Phase 5
| | |
|---|---|
| Đối số | ghi chú (số sprint, ưu tiên) |
| Đầu ra | `docs/05-implement/PLAN.md`, `tasks/T-xx-*.md`, `AGENTS.md` |
| Audit tiếp theo | `artifact-auditor` theo rubric trong skill → `docs/05-implement/audits/plan-audit.md` |
| Ví dụ | `/sdlc-plan 3 sprint, mỗi sprint 1 tuần` |

## `/sdlc-build` — Phase 6
| | |
|---|---|
| Đối số | `T-xx` · `next` · `all` |
| Làm gì | Test trước (mang ID AC) → code DB→API→UI → L0 → sửa → commit `feat/test(...)` + `Refs:` |
| Kiểm tra | `tools/ci_local.py`, `tools/cross_view_audit.py`, `tools/trace_matrix.py`; E2E cho task `risk: high` |
| Ví dụ | `/sdlc-build T-00` rồi `/sdlc-build next` lặp lại |

## `/sdlc-verify` — Phase 7
| | |
|---|---|
| Đối số | `full` · `review-only` · `retest` |
| Làm gì | Test plan → chạy test thật → test report → `code-reviewer` ∥ `security-auditor` → sửa → review record |
| Đầu ra | `docs/07-verification/{testing,code-review,ci,eval}/` |
| Ví dụ | `/sdlc-verify full` |

## `/test-plan` — Master Test Plan IEEE 829 (có sẵn)
| | |
|---|---|
| Đối số | ghi chú phạm vi, ví dụ `cập nhật sau sprint S3` hoặc `chỉ audit` |
| Đầu ra | `docs/07-verification/testing/test-plan.md` + `Test_Plan_IEEE_829_Checklist_v<x>.xlsx` |
| Ví dụ | `/test-plan` · `/test-plan chỉ audit` |
