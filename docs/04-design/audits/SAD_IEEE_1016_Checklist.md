# Audit — SAD theo checklist IEEE 1016

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | docs/04-design/SAD.md (v0.4), kèm adr/ADR-001..009, diagrams/*.drawio, blueprint.md, data/model.md, openapi.yaml/openapi.md |
| Checklist | docs/checklists/SAD_IEEE_1016_Checklist.xlsx |
| Reviewer | artifact-auditor (agent) — vòng 1: Independent reviewer agent |
| Ngày | 2026-11-02 (vòng 1: 2026-10-28) |
| Vòng | 2 — Audit lại 2026-11-02 sau REFINE (e1c8a1d), đối chiếu design-refine-log.md DF-01..DF-27 và code app/ hiện tại |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Scope & Boundary | Done | SAD §3.1 (C4 mức 1) tách hệ thống với ACT-01..04; §3.2 liệt kê kênh trình duyệt, đĩa, Anthropic. Không đổi sau REFINE. |
| 3 | Context View | Done | §3.1 + §3.2 nêu dịch vụ cung cấp (hỏi đáp, số liệu, CLI) và dịch vụ cần từ môi trường (đĩa, Anthropic tùy chọn, reverse proxy TLS và kho sao lưu ngoài máy ở §7, §7.2). |
| 4 | Architectural Drivers | Done | §1.2 Q1..Q5 có thước đo + nguồn; §10 QS-01..QS-09, đã bổ sung QS-08 Availability (NFR-005) và QS-09 Accessibility (NFR-009) theo DF-24. |
| 5 | System Constraints | Done | §2 TC-01..TC-04, OC-01 có nguồn. TC-02 và §7 đã nói rõ Python 3.15 là máy dev, ≥ 3.12 là tối thiểu, CI chạy 3.12 (DF-24). |
| 6 | Composition View | Done | §5.1 container, §5.2 CMP-01..CMP-13 có module app/backend/cwd/*, trách nhiệm, phụ thuộc, yêu cầu; khớp elements.yaml (cross-view-audit 36 PASS). |
| 7 | Logical View | Done | Bảng đầu SAD (dòng View chi tiết) nay liên kết data/model.md (ERD, ENT-01..08), blueprint.md §3.3 (lớp chính) và §5.2 trỏ class_diagram.drawio. Mô hình miền được định nghĩa ở các view liên kết thay vì lặp trong SAD. |
| 8 | Dependency View | In Progress | §5.2 đã sửa (DF-13): CMP-02 phụ thuộc CMP-03..CMP-10, CMP-13 (bỏ CMP-12); CMP-09→CMP-03; CMP-06→CMP-13; CMP-05 dùng textnorm là module tiện ích. Nhưng component_diagram.drawio vẫn còn cạnh CMP-05→CMP-06 nhãn "textnorm.fold()" mâu thuẫn §5.2; cần xóa cạnh này (tools/gen_diagrams.py). |
| 9 | Interaction View | Done | §6.1..6.4 + sequence_diagram.drawio (Hỏi đáp có khung alt lỗi 401/403/404/409/422/503, Đăng nhập có alt khóa/sai/đúng — DF-07); luồng xóa, đánh giá, số liệu ở use_cases.md UC-xx (DF-08). |
| 10 | State Dynamics View | Done | SAD liên kết blueprint.md; blueprint §3.7 có máy trạng thái tài liệu (processing/ready/no_text/failed, recover_pending) và trạng thái ô hỏi chuẩn; SAD §6.2 nêu chuyển trạng thái. `ingest.interrupted` đã định nghĩa (model.md §3, DF-15). Minor: nhãn chuyển processing→failed ở blueprint §3.7 chưa ghi `ingest.interrupted` (AUD-SAD-02). |
| 11 | Information View | Done | §3.2, §8.1 (dữ liệu, nơi lưu, có rời máy chủ không), ADR-002, §6.2 luồng ingestion, liên kết data/model.md. |
| 12 | Interface View | Done | Bảng đầu SAD liên kết openapi.yaml/openapi.md; §5.3 chữ ký Retriever thống nhất với app/backend/cwd/retrieval.py (thêm conn, cited_documents — DF-14); hợp đồng Anthropic: ADR-003 bước 4 (timeout CWD_ANSWER_TIMEOUT_S → chat.ai_unavailable 503), §8.1 (tối đa 6 chunk trong thẻ document). |
| 13 | Resource View | Done | §7.1 Resource view (DF-10): đĩa PDF ≈ 4,5 GB (trần 30 GB), cwd.db 1–2 GB, RAM ~300 MB + ~100 MB/PDF đang xử lý, 2 vCPU (1 request, 1 ingestion), uvicorn 1 worker + threadpool 40 luồng; cấu hình tối thiểu 2 vCPU/4 GB/50 GB SSD. |
| 14 | Physical/Execution Mapping | Done | §7 + deployment_diagram.drawio; đã có node Kho sao lưu ngoài máy chủ và lịch 01:00 (DF-11), bỏ nhãn CMP-11 khỏi thư mục dữ liệu (DF-21). Minor: nhãn trong sơ đồ còn ghi `python -m app.cli` thay vì `python -m cwd.cli` (AUD-SAD-03). |
| 15 | Architectural Decisions | Done | §9 + ADR-001..009 có Bối cảnh/Quyết định/Hệ quả; ADR-006 Superseded bởi ADR-009. Tất cả vẫn Proposed, chờ người duyệt (DF-26, không thuộc phạm vi agent). |
| 16 | Rejected Alternatives | Done | Mỗi ADR có bảng Phương án đã cân nhắc kèm lý do (vd. ADR-002 PostgreSQL/Chroma/JSON). |
| 17 | Traceability | Done | ADR ghi FR/BR liên quan; §5.2 cột Yêu cầu (NFR-006, NFR-007 tại CMP-11/CMP-12); §10 QS-08 → NFR-005, QS-09 → NFR-009; §1.2 nguồn. |

## Kiểm tra lại vòng trước
| Row | Vấn đề vòng 1 | Kết quả vòng 2 |
|---|---|---|
| 4 | Thiếu kịch bản NFR-005, NFR-009 | Đã sửa: QS-08, QS-09 (§10) |
| 5 | Mâu thuẫn Python 3.15 / ≥ 3.12 | Đã sửa: TC-02, §7 |
| 7 | Không liên kết data/model.md, blueprint.md | Đã sửa: bảng đầu SAD dòng View chi tiết |
| 8 | Cột phụ thuộc §5.2 lệch | §5.2 đã sửa; component diagram còn cạnh CMP-05→CMP-06 |
| 10 | Không có/không tham chiếu state view; `ingest.interrupted` chưa có chuyển trạng thái | Liên kết blueprint §3.7; mã đã định nghĩa; còn thiếu nhãn (Minor) |
| 12 | Không liên kết openapi; chữ ký Retriever lệch | Đã sửa (DF-14, DF-24) |
| 13 | Không có resource view | Đã sửa: §7.1 (DF-10) |
| 14 | backups/ cùng đĩa | Đã sửa: §7.2 + node sao lưu ngoài máy (DF-11) |

## Phát hiện
| ID | Mức | Vị trí | Mô tả | Khuyến nghị |
|---|---|---|---|---|
| AUD-SAD-01 | Minor | diagrams/component_diagram.drawio | Còn cạnh CMP-05 Ingestion → CMP-06 Retriever nhãn "textnorm.fold()", trái SAD §5.2 (textnorm là module tiện ích) và DF-13 ghi Fixed | Xóa cạnh trong tools/gen_diagrams.py, sinh lại sơ đồ |
| AUD-SAD-02 | Minor | blueprint.md §3.7 (được SAD tham chiếu) | Chuyển processing→failed chỉ ghi pdf.corrupt / pdf.encrypted, thiếu `ingest.interrupted` | Bổ sung nhãn |
| AUD-SAD-03 | Minor | diagrams/deployment_diagram.drawio; SAD §8.3 | Còn đường dẫn cũ `python -m app.cli`, `app/textnorm.fold()` sau khi tái cấu trúc sang package `cwd` (v0.4) | Đổi thành `cwd.cli`, `app/backend/cwd/textnorm.py` |
| AUD-SAD-04 | Minor | SAD §8.2 | Ghi "log có request_id" nhưng middleware trong app/backend/cwd/main.py chỉ log method, path, status, latency_ms (DF-17 hoãn X-Request-ID) | Sửa câu cho đúng hiện trạng hoặc hiện thực request_id |
| AUD-SAD-05 | Minor | SAD Lịch sử phiên bản | Dòng 0.4 đứng trước 0.3 | Sắp xếp lại theo thứ tự phiên bản |

## Tóm tắt
- Status: Done 15 · In Progress 1 · Pending 0 · N/A 0 (tổng 16).
- Phát hiện: Critical 0 · Major 0 · Minor 5.
- Nhận định: Sẵn sàng qua cổng về nội dung kiến trúc, với điều kiện sửa AUD-SAD-01 (một cạnh sơ đồ) để đóng Row 8; ADR vẫn cần người duyệt chuyển Accepted (DF-26).

## Lịch sử audit
| Ngày | Vòng | Row | Status cũ → mới | Lý do |
|---|---|---|---|---|
| 2026-10-28 | 1 | — | — | Audit ban đầu trên SAD v0.2: Done 11, In Progress 4, Pending 1 |
| 2026-11-02 | 2 | 7 | In Progress → Done | SAD v0.4 liên kết data/model.md, blueprint §3.3, class diagram (DF-24) |
| 2026-11-02 | 2 | 8 | In Progress → In Progress | §5.2 đã sửa (DF-13) nhưng component diagram còn cạnh CMP-05→CMP-06 |
| 2026-11-02 | 2 | 10 | In Progress → Done | State view qua blueprint §3.7 được liên kết; `ingest.interrupted` định nghĩa ở model.md §3 (DF-15) |
| 2026-11-02 | 2 | 12 | In Progress → Done | Liên kết openapi; chữ ký Retriever khớp code (DF-14); hợp đồng Anthropic ở ADR-003, §8.1 |
| 2026-11-02 | 2 | 13 | Pending → Done | Thêm §7.1 Resource view (DF-10) |
| 2026-11-02 | 2 | 4, 5, 14, 17 | Done → Done | Cập nhật Notes: QS-08/09, Python 3.12/3.15, node sao lưu ngoài máy |
