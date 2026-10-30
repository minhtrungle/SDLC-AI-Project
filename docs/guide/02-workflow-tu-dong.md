# 02 — Workflow tự động với `/sdlc`

## Cú pháp

| Lệnh | Tác dụng |
|---|---|
| `/sdlc <đường dẫn BRD> <ghi chú>` | Bắt đầu lượt chạy mới |
| `/sdlc resume` (hoặc `/sdlc` không đối số khi đã có state) | Chạy tiếp từ phase đầu tiên chưa được duyệt |
| `/sdlc from <phase>` | Mở lại một phase và mọi phase sau nó, ví dụ `from design`, `from plan` |

## Bên trong mỗi phase

```
ENTRY ─► SPECIFY ─► GENERATE ─► VERIFY ─► AUDIT ─► REFINE (≤2) ─► HANDOFF ─► GATE (bạn)
```

| Bước | Ai | Việc |
|---|---|---|
| ENTRY | `/sdlc` | Kiểm tra phase đầu vào đã được duyệt |
| SPECIFY | `/sdlc` | Viết "phase brief" cho agent soạn |
| GENERATE | `sdlc-author` | Soạn tài liệu/code theo skill phase và prompt chuẩn |
| VERIFY | `/sdlc` | Chạy `tools/*.py`, test, lint — đọc kết quả thật |
| AUDIT | `artifact-auditor` / `code-reviewer` / `security-auditor` | Chấm theo checklist, ghi biên bản + xlsx |
| REFINE | `sdlc-author` | Sửa theo phát hiện, tối đa 2 vòng tự động |
| HANDOFF | `/sdlc` | Ghi `docs/00-workflow/handoff-<phase>.md` |
| GATE | **Bạn** | Phê duyệt hoặc yêu cầu sửa |

## Các cổng và bạn cần xem gì

| Cổng | Vai trò duyệt | Nên mở các file | Câu hỏi tự kiểm |
|---|---|---|---|
| **G1** Intake | PO | `01-intake/intent.md`, `02-requirements/BRD_gap_report.md` | Vấn đề, phạm vi, risk tier đúng chưa? Giả định ASM có chấp nhận được? |
| **G2** Analysis | PO + Tech Lead | `03-analysis/PRD.md`, `USER_STORIES.md`, `traceability.md` | Mọi BR được phủ? AC đo được? NFR có ngưỡng số? |
| **G3a** Kiến trúc | Architect | `04-design/SAD.md`, `adr/`, `elements.yaml` | Stack/ADR có hợp lý? Có QS cho mọi NFR? |
| **G3b** Thiết kế chi tiết | Architect + Tech Lead | `openapi.yaml`, `data/model.md`, `blueprint.md`, `UI_UX_design/`, `diagrams/`, `cross-view-audit.md` | Các view nhất quán? FR P0 nào chưa có endpoint/màn hình? |
| **G4** Plan | PO + Tech Lead | `05-implement/PLAN.md`, `tasks/` | Thứ tự hợp lý? Task đủ nhỏ? Rủi ro có owner? |
| **G5** Build | Human owner | `ci-log`, `traceability.md`, diff (`git log`, `git diff main...`) | L0 xanh? AC nào chưa có test? Có lệch thiết kế (DEV-xx)? |
| **G6** Verify | Reviewer ≠ author | `07-verification/testing/test-report.md`, `code-review/`, review record | Còn Critical/Major? Đủ bằng chứng để L2 review? |

Mỗi cổng, agent luôn đưa: danh sách artifact + phiên bản, số liệu kiểm tra thật, bảng đếm Status checklist, gap mở, giả định cần xác nhận.

## Trả lời ở cổng

| Lựa chọn | Điều xảy ra |
|---|---|
| **Phê duyệt & baseline** | Tài liệu chuyển `Baseline`, thêm dòng lịch sử phiên bản, commit `docs(<phase>): baseline …`, sang phase sau |
| **Yêu cầu sửa** | Ghi nội dung ở ô *Other*/ghi chú. Agent soạn lại theo đúng góp ý, tăng phiên bản, audit lại, quay về cổng |
| **Quay lại phase trước** | Ghi phase + lý do. Phase đó và các phase sau được mở lại, sửa có ghi lịch sử |
| **Dừng lượt chạy** | Lưu state; chạy tiếp bằng `/sdlc resume` |

Câu hỏi phụ ở cổng (tối đa 3) là giả định agent đã dùng; lựa chọn có "(Recommended)" là giả định hiện tại.

### Viết "Yêu cầu sửa" hiệu quả
Nêu **file/mục**, **vấn đề**, **mong muốn**:

```text
PRD §3.9: NFR-003 "phản hồi nhanh" chưa đo được → đổi thành p95 ≤ 5 giây với 5 người dùng đồng thời.
USER_STORIES US-104: thiếu AC cho trường hợp file PDF có mật khẩu.
```

Tránh góp ý chung chung kiểu "viết lại cho tốt hơn" — agent sẽ không biết dừng ở đâu.

## Theo dõi trạng thái
`docs/00-workflow/sdlc-state.md` cho biết phase nào đang ở trạng thái nào (`In progress`, `Awaiting gate`, `Changes requested`, `Approved`, `Reopened`, `Blocked`), vòng thứ mấy, commit baseline. Feedback của bạn được lưu nguyên văn ở đây.

## Chi phí và thời gian
- Phase thiết kế chi tiết (G3b) tốn nhất: ~8 agent soạn song song + ~10 agent audit.
- Build chạy một agent cho mỗi task, tuần tự theo phụ thuộc.
- Muốn tiết kiệm: duyệt kỹ ở G2 và G3a — sửa sớm rẻ hơn sửa ở thiết kế chi tiết.
