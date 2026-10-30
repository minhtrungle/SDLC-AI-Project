# 06 — FAQ & xử lý sự cố

### Gõ `/sdlc` không thấy skill
Mở Claude Code **tại gốc repo** (nơi có thư mục `.claude/`). Kiểm tra file `.claude/skills/sdlc/SKILL.md` tồn tại. Khởi động lại phiên sau khi thêm skill mới.

### Agent hỏi quyền liên tục
Thêm `permissions.allow` vào `.claude/settings.json` (mẫu ở [01-quick-start.md](01-quick-start.md)) và bật chế độ accept edits.

### Phiên bị ngắt giữa chừng
`/sdlc resume`. Trạng thái nằm ở `docs/00-workflow/sdlc-state.md`; phase đang dở sẽ chạy tiếp từ bước gần nhất có file đầu ra.

### Muốn sửa lại một tài liệu đã duyệt
`/sdlc from <phase>` hoặc chọn **Quay lại phase trước** ở cổng. Tài liệu đã `Baseline` sẽ được tăng phiên bản và có dòng lịch sử (change control) — không sửa âm thầm.

### Audit báo `In Progress` mãi không hết
Sau 2 vòng tự sửa, phần tồn đọng được đưa lên cổng là "gap mở". Bạn có thể:
- **Yêu cầu sửa** cụ thể từng mục, hoặc
- **Phê duyệt** kèm chấp nhận gap (ghi rõ lý do trong ghi chú — được lưu vào state).

### Checklist xlsx điền sai hoặc trống
`tools/checklist_fill.py` đọc **bảng đầu tiên có cả cột `Status` và `Notes`** trong file .md. Nếu tài liệu có bảng khác phía trên dùng hai tiêu đề này, đổi tên cột đó (ví dụ "Trạng thái", "Ghi chú"). Giá trị Status phải đúng bộ trong template.

### `cross_view_audit.py` fail
Thường do một ID (CMP, endpoint, entity, screen) có trong một view mà không có trong `elements.yaml`, hoặc ngược lại. Sửa `elements.yaml` trước rồi đến view; nếu đổi API thì sửa `openapi.yaml` rồi chạy `npm run gen:api`.

### `trace_matrix.py` exit 1
Có dòng FR/AC trong phạm vi chưa có test mang ID AC. Ở Analysis/Design là bình thường; từ Build trở đi phải xử lý hoặc liệt kê rõ ở test report.

### Agent nói "test đã pass" — có tin được không?
Không tin báo cáo, tin output lệnh. Orchestrator tự chạy lại lệnh; bạn tự kiểm bằng `tools/ci_local.py` nếu cần. Lệnh nào không chạy được phải được ghi lý do, không được làm tròn thành "Đạt".

### Agent có tự merge hoặc push không?
Không. Skill và agent đều cấm; nên thêm `deny` cho `git push`/`git merge` trong settings để chắc chắn. Merge và release là việc của reviewer L2 và release owner.

### Dùng cho dự án khác không phải "Chat với tài liệu"?
Được. Các skill `sdlc-*` và `artifact-auditor` viết theo phase, không gắn sản phẩm. Lưu ý:
- `code-reviewer`, `security-auditor`, `test-plan` có quy tắc riêng của dự án này (NFR-004, ADR-005…) — cần chỉnh lại cho dự án mới.
- `tools/trace_matrix.py`, `cross_view_audit.py`, `gen_diagrams.py` đọc cấu trúc của dự án này; task `T-00` ở Planning sẽ dựng hoặc chỉnh lại các công cụ này.

### Tốn nhiều token quá
- Duyệt kỹ ở G2/G3a để tránh làm lại thiết kế chi tiết.
- Chạy thủ công từng artifact ở phase 4b (`/sdlc-design B api`…) thay vì cả nhóm.
- Ghi đủ stack, ràng buộc, phạm vi trong prompt khởi động để giảm vòng hỏi lại.

### Khi nào phải dừng agent ngay
Agent yêu cầu secret/dữ liệu cá nhân, thay đổi rộng không giải thích, thêm dependency lạ, hoặc bạn không còn hiểu được kết quả (SOP §7). Chọn **Dừng** ở cổng hoặc nhấn Esc, rồi báo Tech Lead.
