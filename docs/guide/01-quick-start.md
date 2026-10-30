# 01 — Quick start

## 1. Chuẩn bị (một lần)

| Việc | Lệnh / cách làm |
|---|---|
| Cài Claude Code (CLI hoặc extension VS Code) | Theo hướng dẫn chính thức |
| Môi trường Python cho công cụ `tools/*.py` | `python -m venv .venv && .venv/Scripts/python -m pip install -r app/backend/requirements-dev.txt` (cần ít nhất `openpyxl`, `ruamel.yaml`) |
| Node ≥ 22.12 (cho Build/Verify frontend, E2E) | `cd app/frontend && npm ci` |
| Có BRD | Đặt ở `docs/02-requirements/BRD.md` |
| Làm trên nhánh riêng | `git switch -c feat/sdlc-<tên>` (workflow sẽ tự tạo nếu bạn đang ở `main`) |

Kiểm tra skill và agent đã được nhận: mở Claude Code tại gốc repo, gõ `/` — danh sách phải có `sdlc`, `sdlc-intake`, … `test-plan`. Gõ `/agents` để thấy `sdlc-author`, `artifact-auditor`, `code-reviewer`, `security-auditor`.

### (Tùy chọn) Giảm số lần bị hỏi quyền
Tạo `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(.venv/Scripts/python:*)", "Bash(../../.venv/Scripts/python:*)",
      "Bash(npm ci:*)", "Bash(npm run:*)", "Bash(npm test:*)",
      "Bash(git status:*)", "Bash(git diff:*)", "Bash(git log:*)",
      "Bash(git add:*)", "Bash(git commit:*)", "Bash(git switch -c:*)"
    ],
    "deny": [
      "Bash(git push:*)", "Bash(git merge:*)", "Bash(git reset --hard:*)",
      "Edit(docs/checklists/**)", "Edit(docs/prompts/**)"
    ]
  }
}
```

`deny` bảo vệ template checklist/prompt và ngăn agent push/merge. Bật thêm chế độ *accept edits* nếu muốn agent ghi file không cần hỏi.

## 2. Chạy

Mở phiên Claude Code mới tại gốc repo và gửi **một** prompt:

```text
/sdlc docs/02-requirements/BRD.md
Stack: Python 3.12 FastAPI + SQLite, Vue 3 + TypeScript.
Ràng buộc: chạy on-prem, không gửi dữ liệu ra ngoài, giao diện tiếng Việt.
Phạm vi: chỉ P0/P1 cho MVP. Dừng ở mỗi cổng để tôi duyệt.
```

Mẹo viết dòng ghi chú: càng rõ stack, ràng buộc và phạm vi, càng ít giả định `ASM-xx` agent phải hỏi lại ở cổng.

## 3. Trong lúc chạy
- Agent báo tiến độ ngắn gọn ("P4b: 6/10 artifact xong…").
- Đến cổng, bạn nhận **bản tóm tắt + hộp chọn**: Phê duyệt / Yêu cầu sửa / Quay lại phase trước / Dừng. Xem chi tiết ở [02-workflow-tu-dong.md](02-workflow-tu-dong.md).
- Muốn nghỉ: chọn **Dừng**. Lần sau: `/sdlc resume`.

## 4. Kết quả nằm ở đâu

| Phase | Thư mục |
|---|---|
| Trạng thái lượt chạy, handoff record | `docs/00-workflow/` |
| Intake | `docs/01-intake/` |
| BRD + gap report + audit | `docs/02-requirements/` |
| PRD, User Stories, truy vết | `docs/03-analysis/` |
| SAD, ADR, blueprint, sơ đồ, UI/UX, audit | `docs/04-design/` |
| PLAN, tasks | `docs/05-implement/` |
| Mã nguồn, test | `app/`, `tools/` |
| Test plan, test report, review, CI log | `docs/07-verification/` |
