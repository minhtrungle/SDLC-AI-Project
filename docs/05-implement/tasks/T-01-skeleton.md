# T-01 — Khung ứng dụng, cấu hình, CSDL, lỗi, health, CI

| Mục | Giá trị |
|---|---|
| Story / FR | NFR-005, FR-003 (một phần) |
| Phụ thuộc | — |
| Risk tier | Low |
| Owner | Agent (sinh) · Dev owner (review, merge) |
| Trạng thái | Planned |

## Tiêu chí hoàn thành (AC đích)
- [ ] `create_app(settings)` trả FastAPI; `GET /api/health` → `{status: ok}`
- [ ] `GET /api/config` → `ai_mode=local` mặc định (AC-102.1 một phần)
- [ ] `init_schema()` tạo đủ 8 bảng + FTS + trigger; `foreign_keys=ON`, WAL
- [ ] Lỗi `ProblemError` → problem+json, lỗi bất ngờ → 500 không lộ stack trace
- [ ] Header bảo mật SAD §8.1
- [ ] Log request JSON không chứa body (NFR-008)
- [ ] CI: `.github/workflows/ci.yml` + `tools/ci_local.py`; `AGENTS.md`

## Test (viết trước)
- `app/backend/tests/test_app_basics.py`

## File chạm
- `app/backend/cwd/main.py`
- `app/backend/cwd/config.py`
- `app/backend/cwd/db.py`
- `app/backend/cwd/errors.py`
- `AGENTS.md`
- `pyproject.toml`
- `.github/workflows/ci.yml`
- `tools/ci_local.py`

## Definition of Done
Theo [PLAN.md §3](../PLAN.md#3-definition-of-done-mọi-task).
