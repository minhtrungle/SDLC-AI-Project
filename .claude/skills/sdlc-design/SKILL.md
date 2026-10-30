---
name: sdlc-design
description: Phase 4 (Design) của Agentic SDLC, chia hai cổng — Phần A kiến trúc (SAD arc42/IEEE 1016, ADR, elements.yaml) và Phần B thiết kế chi tiết (Blueprint IEEE 1016, OpenAPI, Database, UI/UX, 6 sơ đồ UML 4+1 dạng draw.io, cross-view audit). Mỗi artifact có prompt trong docs/prompts/ và checklist trong docs/checklists/. Được /sdlc giao cho sdlc-author; gọi riêng bằng /sdlc-design A hoặc /sdlc-design B <artifact>.
argument-hint: "A | B [blueprint|api|database|uiux|usecase|class|sequence|activity|component|deployment]"
---

# Phase 4 — Design

Phạm vi lần chạy: **$ARGUMENTS** (A = kiến trúc; B = toàn bộ thiết kế chi tiết hoặc một artifact).

Đầu vào chung: `docs/03-analysis/PRD.md`, `USER_STORIES.md`, `traceability.md` (Baseline ở G2), `docs/01-intake/*`, ghi chú Kickoff về stack. Quy trình: `docs/agentic-sdlc-process.md` §5, `docs/AI_SDLC-SOP.md` §5.4.

## Phần A — Kiến trúc (cổng G3a)

| Đầu ra | Prompt | Checklist |
|---|---|---|
| `docs/04-design/SAD.md` | `SAD_Prompt_IEEE_standard.md` | `SAD_IEEE_1016_Checklist.xlsx` |
| `docs/04-design/adr/ADR-0xx-*.md` | — (Nygard: Bối cảnh · Quyết định · Phương án đã cân nhắc · Hệ quả · Khó đảo ngược?) | chấm cùng SAD (dòng Architectural Decisions / Rejected Alternatives) |
| `docs/04-design/elements.yaml` | — | kiểm bằng `tools/cross_view_audit.py` ở phần B |

Yêu cầu:
- SAD theo khung arc42 12 mục và đủ các view mà checklist SAD hỏi: Context, Composition, Logical, Dependency, Interaction, State dynamics, Information, Interface, Resource, Physical mapping. Thiếu view nào phải ghi lý do.
- Thành phần `CMP-xx` có module/đường dẫn dự kiến, trách nhiệm, phụ thuộc, FR/NFR đáp ứng. Kịch bản chất lượng `QS-xx` cho **mọi** NFR.
- ≥ 3 ADR cho các quyết định khó đảo ngược (ngôn ngữ/framework, lưu trữ, xác thực, tích hợp AI/ngoài…), mỗi ADR có bảng phương án bị loại.
- `elements.yaml` là **nguồn ID duy nhất** cho actor, CMP, endpoint, entity, screen; mọi view phần B phải dùng đúng ID này.
- Chọn stack theo ghi chú Kickoff; nếu không có thì đề xuất và đưa lên cổng như giả định `ASM-xx`.

## Phần B — Thiết kế chi tiết (cổng G3b)

Orchestrator chạy các nhóm độc lập **song song**, mỗi nhóm một `sdlc-author`:

| Nhóm | Đầu ra | Prompt | Checklist |
|---|---|---|---|
| B1 Blueprint | `docs/04-design/blueprint.md` | `bluePrint_design_prompt.md` | `BluePrint_Design_IEEE_1016_2009_Checklist.xlsx` |
| B2 API | `app/api-contract/openapi.yaml` + `docs/04-design/openapi.md` | `apiDesign_prompt.md` | `API_Design_IEEE-1016-2009Checklist.xlsx` |
| B3 Database | `docs/04-design/data/model.md` + `schema.sql` | `databaseDesign_SQL_prompt.md` | `Database_Design_Checklist.xlsx` |
| B4 UI/UX | `docs/04-design/UI_UX_design/` (README, blueprint UI, `html_design/*.html` prototype tĩnh) | `UI-UX-Design_prompt.md` | `UI_UX_Design_IEEE-1016-2009_Checklist.xlsx` |
| B5 Use case | `docs/04-design/use_cases.md` + `diagrams/use_case_diagram.drawio` | `useCase_prompt.md` | `UseCase_Document_UML2.0_Checklist.xlsx` |
| B6 Logical | `diagrams/class_diagram.drawio` | `classDiagram_prompt.md` | `Class_Diagram_UML2.0_Checklist.xlsx` |
| B7 Process | `diagrams/sequence_diagram.drawio`, `diagrams/activity_diagram.drawio` | `sequenceDiagram_prompt.md`, `activityDiagram_prompt.md` | `Sequence_Diagram_UML2.0_Checklist.xlsx`, `Activity_Diagram_UML2.0_Checklist.xlsx` |
| B8 Development & Physical | `diagrams/component_diagram.drawio`, `diagrams/deployment_diagram.drawio` | `componentDiagram_prompt.md`, `deploymentDiagram_prompt.md` | `Component_Diagram_UML2.0_Checklist.xlsx`, `Deployment_Diagram_UML2.0_Checklist.xlsx` |

Thứ tự phụ thuộc: B2 và B3 trước B1 nếu blueprint trích interface/data; B5–B8 có thể sinh bằng `tools/gen_diagrams.py` từ `elements.yaml` nếu công cụ có, sau đó chỉnh tay phần công cụ không vẽ được.

Yêu cầu chung phần B:
- Mỗi endpoint OpenAPI 3.x có schema request/response, mã lỗi dạng problem+json với enum `code`, yêu cầu xác thực, và FR nguồn (`x-requirements` hoặc mô tả).
- Mỗi bảng/entity `ENT-xx` có khóa, ràng buộc, index, quy tắc lưu giữ/xóa dữ liệu; mỗi màn hình `SCR-xx` có trạng thái rỗng/đang tải/lỗi, WCAG 2.1 AA.
- Sơ đồ draw.io mở được (XML hợp lệ), đúng ký hiệu UML 2.0, tên khớp `elements.yaml`.
- Cập nhật cột design của `docs/03-analysis/traceability.md` (FR → CMP/API/ENT/SCR).

## Deterministic (orchestrator chạy sau phần B)
```bash
.venv/Scripts/python tools/cross_view_audit.py --write     # nhất quán giữa các view; exit 1 nếu lệch
.venv/Scripts/python -c "import xml.dom.minidom,glob; [xml.dom.minidom.parse(f) for f in glob.glob('docs/04-design/diagrams/*.drawio')]; print('drawio XML ok')"
```
Nếu repo chưa có `cross_view_audit.py`, author viết một script tương đương (đọc `elements.yaml`, kiểm mọi ID xuất hiện trong SAD/blueprint/openapi/model/diagrams và ngược lại) vào `tools/`.

Kiểm tra OpenAPI hợp lệ (nếu đã có frontend): `cd app/frontend && npm run gen:api`.

## Audit
Mỗi dòng bảng trên → một `artifact-auditor` với đúng checklist ở cột cuối, đầu ra `docs/04-design/audits/`. Ghi tổng hợp vào `docs/04-design/design_checklist_audit.md` (bảng: checklist · Done · In Progress · Pending · N/A · biên bản) và nhật ký sửa vào `docs/04-design/design-refine-log.md`.

## Tiêu chí qua cổng
- **G3a:** mọi NFR có QS; ≥ 3 ADR; checklist SAD không còn `Pending`; mọi CMP có trong elements.yaml.
- **G3b:** `cross_view_audit` pass; 10 checklist không còn `Pending`; mọi FR P0 trỏ tới ít nhất một CMP và một endpoint/screen.
