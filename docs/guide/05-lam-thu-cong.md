# 05 — Làm thủ công từng phase

Dùng khi bạn muốn kiểm soát từng bước, chỉ làm lại một phần, hoặc học quy trình. Mỗi phase lặp cùng một vòng:

```
Soạn (/sdlc-<phase>) → Kiểm tra (tools/*.py) → Audit (agent) → Sửa nếu cần → Bạn duyệt → Commit baseline
```

Các khối dưới đây copy được nguyên vào ô chat Claude Code. Lệnh công cụ chạy từ gốc repo.

---

## Phase 1–2 — Intake
```text
/sdlc-intake docs/02-requirements/BRD.md
```
```text
Dùng agent artifact-auditor audit docs/02-requirements/BRD.md theo docs/checklists/BRD_IEEE_29148_Checklist.xlsx, đầu ra ở docs/02-requirements/audits/.
```
✅ Duyệt khi: intent.md đủ 7 mục, mọi BR có ID, không còn GAP Critical chưa trả lời.

## Phase 3 — Analysis
```text
/sdlc-analysis
```
```bash
.venv/Scripts/python tools/trace_matrix.py   # ở phase này exit 1 vì chưa có test là bình thường
```
```text
Dùng agent artifact-auditor audit docs/03-analysis/PRD.md và USER_STORIES.md theo docs/checklists/PRD_IEEE_29148_Checklist.xlsx.
```
✅ Duyệt khi: 100% BR được phủ, mọi FR P0 có AC Given-When-Then, NFR có ngưỡng số.

## Phase 4a — Kiến trúc
```text
/sdlc-design A
```
```text
Dùng agent artifact-auditor audit docs/04-design/SAD.md và docs/04-design/adr/ theo docs/checklists/SAD_IEEE_1016_Checklist.xlsx.
```
✅ Duyệt khi: ≥ 3 ADR, mọi NFR có kịch bản chất lượng QS, mọi CMP có trong elements.yaml.

## Phase 4b — Thiết kế chi tiết
```text
/sdlc-design B api
/sdlc-design B database
/sdlc-design B blueprint
/sdlc-design B uiux
/sdlc-design B usecase
/sdlc-design B class
/sdlc-design B sequence
/sdlc-design B activity
/sdlc-design B component
/sdlc-design B deployment
```
(gửi từng dòng một, đợi xong rồi gửi dòng tiếp)

```bash
.venv/Scripts/python tools/gen_diagrams.py              # nếu muốn sinh sơ đồ từ elements.yaml
.venv/Scripts/python tools/cross_view_audit.py --write  # phải pass
```
```text
Chạy song song agent artifact-auditor cho từng cặp: blueprint.md–BluePrint_Design, openapi–API_Design, data/model.md–Database_Design, UI_UX_design–UI_UX_Design, use_cases–UseCase_Document, và 5 sơ đồ .drawio với checklist UML tương ứng. Tổng hợp vào docs/04-design/design_checklist_audit.md.
```
✅ Duyệt khi: cross_view_audit pass, không checklist nào còn `Pending`.

## Phase 5 — Planning
```text
/sdlc-plan
```
```text
Dùng agent artifact-auditor chấm docs/05-implement/PLAN.md theo rubric trong .claude/skills/sdlc-plan/SKILL.md, ghi docs/05-implement/audits/plan-audit.md.
```
✅ Duyệt khi: mọi AC P0/P1 được gán task, không có vòng phụ thuộc, T-00 dựng xong cổng L0.

## Phase 6 — Build
```text
/sdlc-build T-00
/sdlc-build next
```
(lặp `next` đến khi hết task; mỗi task kết thúc bằng commit)

```bash
.venv/Scripts/python tools/ci_local.py
.venv/Scripts/python tools/trace_matrix.py
.venv/Scripts/python tools/cross_view_audit.py
```
✅ Duyệt khi: L0 xanh trên HEAD, không còn AC P0/P1 thiếu test (hoặc đã liệt kê), không còn DEV-xx chưa quyết.

## Phase 7 — Verify
```text
/test-plan
```
```bash
.venv/Scripts/python tools/ci_local.py --log docs/07-verification/ci/ci-log.txt
cd app/e2e && npm test && cd ../.. && .venv/Scripts/python tools/e2e_report.py
```
```text
Chạy song song agent code-reviewer và agent security-auditor trên diff so với main.
```
```text
/sdlc-verify review-only
```
(lập test report, sửa Critical/Major, review record; chạy lại code-reviewer cho round tiếp theo nếu có sửa)

✅ Bàn giao L2 khi: không còn Critical, Major còn lại đã được bạn quyết, checklist IEEE 829 và IEEE 1028 đã xuất xlsx.

---

## Sau mỗi lần duyệt
```text
Đánh dấu các tài liệu Phase <X> là Baseline v<x.y>, thêm dòng lịch sử phiên bản "Approved by <tên>", rồi commit docs(<phase>): baseline … với dòng Refs.
```

## Làm lại một phần
| Tình huống | Làm |
|---|---|
| Chỉ sửa API | `/sdlc-design B api` → audit API → `tools/cross_view_audit.py` → kiểm tra các task Build bị ảnh hưởng |
| BRD đổi | `/sdlc from intake` (tự động) hoặc chạy lại từ `/sdlc-intake`; mọi tài liệu đã baseline phải tăng phiên bản |
| Chỉ review lại code | `Dùng agent code-reviewer review nhánh hiện tại so với main` |
