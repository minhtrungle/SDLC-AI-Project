# Audit — Activity Diagram theo checklist UML 2.0

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | docs/04-design/diagrams/activity_diagram.drawio (trang "Tải lên và xử lý tài liệu"); đối chiếu SAD §6.2, ADR-008, FR-004..006 |
| Checklist | docs/design/Activity_Diagram_UML2.0_Checklist.xlsx |
| Reviewer | Independent reviewer agent |
| Ngày | 2026-10-28 |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Activity Name | In Progress | Chỉ có tên trang; không có khung activity bo góc bao toàn sơ đồ. |
| 3 | Activity Parameters | Pending | Không có Activity Parameter Node cho đầu vào (files[] multipart) và đầu ra (results[]). |
| 4 | Pre/Post-conditions | Pending | Không ghi «precondition» (phiên hợp lệ + CSRF) hay «postcondition» (mỗi file có kết quả; tài liệu hợp lệ ở processing rồi ready/no_text/failed). |
| 5 | Action Nodes | Done | Hành động là hình chữ nhật bo góc (rounded=1, arcSize=40). |
| 6 | Action Naming | In Progress | Nhiều node không phải cụm động từ: "Kết quả: docs.limit_reached", "status = ready, page_count", "status = no_text". |
| 7 | Control Flows | In Progress | Dùng mũi tên đặc (endArrow=block, endFill=1) thay vì mũi tên mở. |
| 8 | Pins | Pending | Không có pin cho dữ liệu vào/ra hành động. |
| 9 | Object Nodes | Pending | Không có object node (File PDF, Document, Chunk[]). |
| 10 | Object Flows | Pending | Không có object flow. |
| 11 | Data Stores (<<datastore>>) | Pending | cwd.db và files/ không được mô hình bằng «datastore». |
| 12 | Central Buffers | N/A | Hàng đợi BackgroundTasks nằm trong tiến trình; không bắt buộc mô hình. |
| 13 | Decision Nodes | Done | 7 hình thoi cho quyết định. Lỗi logic: "Workspace còn chỗ?" chỉ kiểm tra MỘT lần trước vòng lặp; vòng "Còn file?" quay về "%PDF-?" nên workspace có 49 tài liệu vẫn nhận cả 3 file (vượt CWD_MAX_DOCS), và nhánh "không" trả docs.limit_reached cho cả lô thay vì từng file (trái FR-004). |
| 14 | Guard Conditions | In Progress | Nhãn "có"/"không" không nằm trong ngoặc vuông; "Mã hóa / hỏng?" gộp hai điều kiện vào một nhánh failed nên không phân biệt pdf.encrypted với pdf.corrupt. |
| 15 | Merge Nodes | In Progress | Không có merge node: nhiều luồng đổ thẳng vào decision "Còn file?" và vào "Trả 200 results[]" và vào final node. |
| 16 | Fork Nodes | Pending | "Audit document.upload; đăng ký tác vụ nền" có hai luồng ra (tới "Còn file?" và sang làn nền) — fork ngầm, không có thanh fork. |
| 17 | Join Nodes | N/A | Không cần đồng bộ hai luồng. |
| 18 | Send Signal Actions | Pending | Việc đăng ký tác vụ nền là bất đồng bộ — nên dùng send signal "Bắt đầu ingest(document_id)". |
| 19 | Accept Event Actions | Pending | Làn CMP-05 không có accept event để nhận tín hiệu; cũng thiếu điểm vào recover_pending khi khởi động (ADR-008). |
| 20 | Time Events | N/A | Không có chờ thời gian trong luồng này (polling 2 s ở UI). |
| 21 | Expansion Regions | Pending | Xử lý từng file được mô hình bằng vòng decision; nên dùng expansion region «iterative» trên files[]. |
| 22 | Interruptible Activity Regions | Pending | Xóa tài liệu trong lúc xử lý chỉ kiểm tra ở đầu ("Tài liệu còn tồn tại?"); không có vùng ngắt cho trường hợp xóa giữa chừng (ADR-008 nói "bỏ kết quả"). |
| 23 | Interrupting Edges | Pending | Không có (xem row 22). |
| 24 | Exception Handlers | Pending | Lỗi pypdf mô hình bằng decision; không có exception handler; lỗi I/O khi lưu file chưa có nhánh. |
| 25 | Activity Partitions | Done | Hai swimlane: CMP-04 Document Service (trong request), CMP-05 Ingestion Pipeline (tác vụ nền). |
| 26 | Multidimensional Partitions | N/A | Không cần. |
| 27 | External Partitions | N/A | Không có hệ thống ngoài trong luồng này. |
| 28 | Flow Final Node | In Progress | Cả hai làn đều kết thúc bằng activity final (bullseye). Theo UML, activity final ở làn request sẽ kết thúc toàn bộ activity kể cả tác vụ nền — một trong hai phải là flow final (⊗). |
| 29 | Activity Final Node | Done | Có node kết thúc (shape=endState). Xem row 28 về ngữ nghĩa. |

## Tóm tắt
Sơ đồ truyền đạt được luồng chính và hai làn trách nhiệm, nhưng có lỗi logic (kiểm tra giới hạn tài liệu ngoài vòng lặp) và ký hiệu UML nâng cao gần như vắng mặt (object flow, datastore, fork, signal, flow final, interruptible region).
