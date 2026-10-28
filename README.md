# SDLC-AI-Project
Software Development Life Cycle with AI

Dự án thực hành [Agentic SDLC](docs/agentic-sdlc-process.md): sản phẩm **"Chat với tài liệu"** (MVP) được đi qua đủ 11 phase, từ intake đến decommission. Mỗi phase để lại artifact và commit riêng, nên chuỗi commit chính là audit trail.

**Sản phẩm:** ứng dụng web để tải lên PDF và hỏi đáp bằng tiếng Việt. Câu trả lời chỉ lấy từ tài liệu và kèm trích dẫn tên tài liệu + số trang. Mặc định xử lý hoàn toàn cục bộ, không gửi dữ liệu ra ngoài.

## Chạy nhanh
```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements-dev.txt    # Linux/macOS: .venv/bin/python
.venv/Scripts/python -m app.cli seed-demo                      # in ra mật khẩu của linh (user) và hung (manager)
.venv/Scripts/python -m uvicorn app.main:app                   # mở http://127.0.0.1:8000
.venv/Scripts/python tools/ci_local.py                         # cổng chất lượng L0, giống CI
```
Yêu cầu Python ≥ 3.12. Không cần Docker, cơ sở dữ liệu ngoài hay API key.

## Artifact theo phase
| Phase | Artifact |
|---|---|
| 1 Intake | [intent](docs/01-intake/intent.md) · [glossary](docs/01-intake/glossary.md) · [stakeholders](docs/01-intake/stakeholders.md) · [sources](docs/01-intake/sources.md) |
| 2 Requirements | [BRD v0.2](docs/02-requirements/BRD.md) · [audit IEEE 29148](docs/02-requirements/BRD_checklist_audit.md) · [interviews/](docs/02-requirements/interviews/) |
| 3 Analysis | [PRD v0.2 (FR/NFR)](docs/03-analysis/PRD.md) · [USER_STORIES](docs/03-analysis/USER_STORIES.md) · [traceability](docs/03-analysis/traceability.md) |
| 4 Design | [SAD v0.3](docs/04-design/SAD.md) · [ADR-001..008](docs/04-design/adr/) · [blueprint](docs/04-design/blueprint.md) · [openapi.yaml](docs/04-design/openapi.yaml) · [data model](docs/04-design/data/model.md) · [use cases](docs/04-design/use_cases.md) · [diagrams](docs/04-design/diagrams/) · [UI/UX](docs/04-design/UI_UX_design/README.md) · [audits](docs/04-design/design_checklist_audit.md) · [refine log](docs/04-design/design-refine-log.md) |
| 5 Planning | [PLAN](docs/05-implement/PLAN.md) · [tasks/](docs/05-implement/tasks/) |
| 6 Build | [AGENTS.md](AGENTS.md) · [app/](app/) · [tests/](tests/) |
| 7–8 Verify & Review | [test plan](docs/07-verification/test-plan.md) · [test report](docs/07-verification/test-report.md) · [L1 review](docs/07-verification/code-review-L1.md) · [review record](docs/07-verification/review-record.md) |
| 9–11 Release / Operate / Retire | [release plan](docs/09-release/release-plan.md) · [runbook](docs/10-operations/runbook.md) · [decommission plan](docs/11-decommissioning/decommission-plan.md) |

## Công cụ của quy trình
| Lệnh | Việc |
|---|---|
| `python tools/ci_local.py --log docs/07-verification/ci-log.txt` | Chạy cổng L0: format, lint, compile, quét secret, quét lỗ hổng phụ thuộc, cross-view audit, truy vết, test + coverage |
| `python tools/cross_view_audit.py --write` | Kiểm tra nhất quán giữa các view thiết kế và code |
| `python tools/trace_matrix.py` | Sinh lại ma trận truy vết BR → FR → US → AC → CMP → code → test |
| `python tools/gen_diagrams.py` | Sinh lại 6 sơ đồ draw.io từ `elements.yaml` |
| `python tools/checklist_fill.py <xlsx> <audit.md> <out.xlsx>` | Ghi kết quả audit markdown vào checklist Excel |

## Phê duyệt
Agent sinh nội dung nhưng không tự phê duyệt, merge hay deploy. Mọi bảng phê duyệt trong tài liệu đang chờ người có trách nhiệm ký.
