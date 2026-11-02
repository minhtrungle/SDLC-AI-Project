# Audit — Activity Diagram theo checklist UML 2.0

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | docs/04-design/diagrams/activity_diagram.drawio (trang "Tải lên và xử lý tài liệu", sinh bởi tools/gen_diagrams.py; sửa ở e1c8a1d, không đổi sau đó); đối chiếu SAD §6.2, ADR-008, FR-004..006, use_cases.md UC-02/UC-03, app/backend/cwd/documents.py |
| Checklist | docs/checklists/Activity_Diagram_UML2.0_Checklist.xlsx |
| Reviewer | artifact-auditor (agent) — vòng 1: Independent reviewer agent (2026-10-28) |
| Ngày | 2026-11-02 |
| Vòng | 2 — Audit lại 2026-11-02 sau REFINE (e1c8a1d) |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Activity Name | In Progress | Chỉ có tên trang "Tải lên và xử lý tài liệu"; vẫn không có khung activity bo góc bao toàn sơ đồ. |
| 3 | Activity Parameters | Pending | Không có Activity Parameter Node cho đầu vào (files[] multipart) và đầu ra (results[]). |
| 4 | Pre/Post-conditions | Pending | Không ghi «precondition» (phiên hợp lệ + CSRF) hay «postcondition» trên sơ đồ; hậu điều kiện chỉ có ở use_cases.md UC-02, không trên activity. |
| 5 | Action Nodes | Done | Hành động là hình chữ nhật bo góc (rounded=1, arcSize=40), c5, c7, c9, c11..c13, c15, c18, c19, c21, c23..c26. |
| 6 | Action Naming | In Progress | Còn node không phải cụm động từ: c7 "Kết quả file: docs.limit_reached", c9 "Kết quả: file.wrong_type", c11 "Kết quả: file.too_large", c21 "status = failed", c23 "status = no_text", c26 "status = ready, page_count". |
| 7 | Control Flows | In Progress | Toàn bộ cạnh c28..c57 vẫn dùng mũi tên đặc (endArrow=block, endFill=1) thay vì mũi tên mở; DF-20 không xử lý mục này. |
| 8 | Pins | Pending | Không có pin cho dữ liệu vào/ra hành động. |
| 9 | Object Nodes | Pending | Không có object node (File PDF, Document, Chunk[]). |
| 10 | Object Flows | Pending | Không có object flow. |
| 11 | Data Stores (<<datastore>>) | Pending | cwd.db và files/ không được mô hình bằng «datastore» (chỉ nêu trong nhãn c12, c25). |
| 12 | Central Buffers | N/A | Hàng đợi BackgroundTasks nằm trong tiến trình; không bắt buộc mô hình. |
| 13 | Decision Nodes | Done | 7 hình thoi (c6, c8, c10, c14, c17, c20, c22). Lỗi logic vòng 1 đã sửa (DF-02): c6 "[với mỗi file] Còn chỗ? (đã có + đã nhận < CWD_MAX_DOCS)" nằm trong vòng, c40 "[còn file]" quay về c6, c42 docs.limit_reached → c14 nên kết quả theo từng file; khớp documents.py và test_document_limit. |
| 14 | Guard Conditions | Done | DF-20: mọi guard trong ngoặc vuông ([có]/[không] c30..c35, c45..c51; [còn file]/[hết file] c40, c41). Minor: c20 "Mã hóa / hỏng?" gộp hai điều kiện, nhưng hành động c21 ghi rõ mã pdf.encrypted hoặc pdf.corrupt. |
| 15 | Merge Nodes | In Progress | Vẫn không có merge node: c37, c38, c39, c42 đổ thẳng vào decision c14; c54..c57 đổ thẳng vào final c27. |
| 16 | Fork Nodes | Pending | c13 "Audit document.upload; đăng ký tác vụ nền" vẫn có hai luồng ra (c37 tới c14, c44 sang làn nền) — fork ngầm, không có thanh fork. |
| 17 | Join Nodes | N/A | Không cần đồng bộ hai luồng (tác vụ nền độc lập với phản hồi request). |
| 18 | Send Signal Actions | Pending | Việc đăng ký tác vụ nền bất đồng bộ (c44 "BackgroundTasks") chưa dùng send signal "Bắt đầu ingest(document_id)". |
| 19 | Accept Event Actions | Pending | Làn CMP-05 không có accept event; thiếu điểm vào recover_pending khi khởi động (ADR-008, blueprint §3.7 processing → processing). |
| 20 | Time Events | N/A | Không có chờ thời gian trong luồng này (polling 2 s ở UI). |
| 21 | Expansion Regions | Pending | Xử lý từng file vẫn bằng vòng decision c6/c14 (nhãn "[với mỗi file]"); chưa dùng expansion region «iterative» trên files[]. |
| 22 | Interruptible Activity Regions | Pending | Xóa tài liệu khi đang xử lý chỉ kiểm tra ở đầu (c17 "Tài liệu còn tồn tại?"); không có vùng ngắt cho xóa giữa chừng (ADR-008 "bỏ kết quả"). |
| 23 | Interrupting Edges | Pending | Không có (xem row 22). |
| 24 | Exception Handlers | Pending | Lỗi pypdf vẫn mô hình bằng decision c20; không có exception handler; lỗi I/O khi lưu file và ingest.interrupted (DF-15, file gốc mất khi xử lý) chưa có nhánh. |
| 25 | Activity Partitions | Done | Hai swimlane: c2 CMP-04 Document Service (trong request), c3 CMP-05 Ingestion Pipeline (tác vụ nền, ADR-008); khớp elements.yaml. |
| 26 | Multidimensional Partitions | N/A | Không cần. |
| 27 | External Partitions | N/A | Không có hệ thống ngoài trong luồng này. |
| 28 | Flow Final Node | In Progress | Vẫn có hai activity final (c16, c27 đều shape=endState); activity final ở làn request sẽ kết thúc cả tác vụ nền theo ngữ nghĩa UML — một trong hai phải là flow final (⊗). |
| 29 | Activity Final Node | Done | Có node kết thúc (shape=endState) c16, c27. Xem row 28 về ngữ nghĩa. |

## Kiểm tra lại vòng trước
- Lỗi logic giới hạn tài liệu ngoài vòng lặp (row 13): đã sửa (DF-02), xác minh qua c6, c40, c42.
- Guard không trong ngoặc vuông (row 14): đã sửa (DF-20 phần guard).
- Các mục ký hiệu nâng cao (object flow, datastore, fork, signal, flow final, interruptible region, merge, mũi tên mở): chưa sửa; DF-20 ghi phần còn lại là cải tiến ký hiệu, owner Architect.

## Phát hiện
| ID | Mức | Vị trí | Mô tả | Khuyến nghị |
|---|---|---|---|---|
| AUD-ACT-01 | Major | c16, c27 | Hai activity final; final ở làn request về ngữ nghĩa kết thúc cả tác vụ nền. | Đổi c16 thành flow final hoặc tách tác vụ nền thành activity riêng nhận tín hiệu. |
| AUD-ACT-02 | Minor | c13, c44 | Fork ngầm, không có send signal/accept event cho tác vụ nền và recover_pending. | Thêm fork bar hoặc send signal + accept event ở làn CMP-05. |
| AUD-ACT-03 | Minor | c14, c27 | Không có merge node trước decision và final. | Thêm merge node. |
| AUD-ACT-04 | Minor | c28..c57 | Mũi tên đặc thay vì mũi tên mở. | Sửa style edge trong tools/gen_diagrams.py. |
| AUD-ACT-05 | Minor | Toàn sơ đồ | Thiếu activity frame, parameter node, object node/flow, «datastore», pre/post-condition, exception handler. | Bổ sung khi làm phần còn lại của DF-20. |

## Tóm tắt
- Status: Done 5 · In Progress 5 · Pending 13 · N/A 5 (tổng 28 dòng).
- Phát hiện: Critical 0 · Major 1 · Minor 4.
- Nhận định: Cần sửa — nội dung nghiệp vụ đã đúng sau DF-02 (kiểm tra giới hạn theo từng file), nhưng ký hiệu UML nâng cao vẫn vắng mặt và ngữ nghĩa hai activity final chưa sửa.

## Lịch sử audit
| Vòng | Ngày | Dòng | Thay đổi | Lý do |
|---|---|---|---|---|
| 1 | 2026-10-28 | — | Audit ban đầu: Done 4 · In Progress 6 · Pending 13 · N/A 5 | Trước REFINE e1c8a1d |
| 2 | 2026-11-02 | 14 Guard Conditions | In Progress → Done | DF-20: guard đặt trong [ ] |
| 2 | 2026-11-02 | 13 Decision Nodes | Giữ Done, cập nhật Notes | Lỗi logic giới hạn tài liệu đã sửa (DF-02) |
| 2 | 2026-11-02 | 2, 6, 7, 15, 28 và các dòng Pending | Giữ nguyên | Sơ đồ không có thay đổi tương ứng sau e1c8a1d |
