# Audit — Deployment Diagram theo checklist UML 2

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | docs/04-design/diagrams/deployment_diagram.drawio (trang "Deployment"); đối chiếu SAD §7, NFR-006, ADR-002/007 |
| Checklist | docs/checklists/Deployment_Diagram_UML2.0_Checklist.xlsx |
| Reviewer | Independent reviewer agent |
| Ngày | 2026-10-28 |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Diagram Name | In Progress | Tên trang "Deployment" chung chung; không nêu kịch bản (vd. "prod — máy chủ nội bộ DEP-003"). |
| 3 | Scope & Topology | In Progress | SAD §7 nói on-premises (máy chủ nội bộ), nhưng sơ đồ không ghi; không phân biệt dev/test/prod. |
| 4 | Device Nodes (<<device>>) | Done | shape=cube «device»: Máy trạm, Reverse proxy, Máy chủ ứng dụng, Console quản trị. |
| 5 | Execution Environments (<<executionEnvironment>>) | In Progress | «execution env» Trình duyệt và Python/uvicorn vẽ bằng chữ nhật thường lồng trong node, không phải cube; stereotype viết tắt. |
| 6 | Node Specifications | Pending | Không có CPU/RAM/đĩa/OS version cho máy chủ (cần cho 30 GB PDF tối đa, pypdf 300 trang). |
| 7 | Artifacts (<<artifact>>) | In Progress | Dùng shape=note (biểu tượng tài liệu) cho app/, app/frontend/, cli.py, cwd.db, files/, backups/ nhưng không có stereotype «artifact». |
| 8 | Deployment Relationships | N/A | Dùng lồng (row 10) thay cho «deploy». |
| 9 | Manifestations | In Progress | Artifact ghi CMP-xx trong nhãn (ngầm manifest) nhưng không có quan hệ «manifest». «storage» CWD_DATA_DIR gán CMP-11 Persistence — sai: CMP-11 là code db.py chạy trong tiến trình, không phải thư mục dữ liệu. |
| 10 | Nesting (Alternative) | Done | Artifact lồng trong execution env/node. |
| 11 | Node Connections | Done | Đường liền giữa node (endArrow=none). |
| 12 | Protocols & Networks | In Progress | Nhãn "HTTPS", "HTTP 127.0.0.1:8000", "SSH / RDP" không viết dạng stereotype «HTTPS». Mâu thuẫn: proxy → app dùng 127.0.0.1 (cùng máy) nhưng proxy vẽ là «device» riêng. |
| 13 | Multiplicity | Pending | Không có multiplicity (máy trạm người dùng 1..30, uvicorn 1 worker chỉ ghi trong nhãn). |
| 14 | Disaster Recovery (DR) | Pending | Không có node DR/ lưu trữ sao lưu ngoài máy. backups/ nằm trong cùng «storage» CWD_DATA_DIR trên máy chủ ứng dụng — hỏng đĩa mất cả dữ liệu và bản sao, không đạt RPO ≤ 24 h/RTO ≤ 4 h (NFR-006) trong kịch bản mất máy. |
| 15 | Databases & Storage | In Progress | SQLite nhúng nên lưu trữ nằm trong node ứng dụng (đúng với ADR-002), nhưng chưa tách lưu trữ sao lưu (row 14). |
| 16 | Scalability & Constraints | In Progress | Ghi "1 worker" (ràng buộc LoginLimiter trong bộ nhớ + SQLite một writer) nhưng không chú thích nút thắt hay trigger mở rộng ADR-002 trên sơ đồ. |
| 17 | Clarity | Done | 5 node chính, 4 đường kết nối, không cắt chéo. |

## Tóm tắt
Sơ đồ đơn giản, dễ đọc, phản ánh đúng SAD §7. Thiếu thông số node, stereotype chuẩn, multiplicity và đặc biệt là DR: backup cùng đĩa với dữ liệu.
