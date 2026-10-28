# Audit PRD v0.2 theo checklist IEEE 29148

- **Tài liệu:** [PRD.md](PRD.md) v0.2 + [USER_STORIES.md](USER_STORIES.md)
- **Checklist:** [PRD_IEEE_29148_Checklist.xlsx](../checklists/PRD_IEEE_29148_Checklist.xlsx) → bản đã điền `PRD_IEEE_29148_Checklist_v0.2.xlsx`
- **Người audit:** Agent (Claude), tự kiểm tra. PO và Tech Lead phải review độc lập.
- **Ngày:** 2026-10-28

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Purpose & Scope | Done | PRD §1 tầm nhìn, §1.3 non-goals; ranh giới hệ thống ở §3.9.4 |
| 3 | Business Context | Done | §0.1 nền tảng từ BRD; OKR §1.2 truy về BO-001..003 |
| 4 | User Characteristics | Done | Persona Linh, Hùng, Mai ở §2.1 |
| 5 | Operating Environment | Done | §3.9.4 (máy chủ, trình duyệt, độ rộng) |
| 6 | Singular & Complete | Done | FR-001..FR-019 mỗi dòng một nghĩa vụ |
| 7 | Implementation-Free | In Progress | FR nêu "cái gì"; một số FR nhắc cơ chế cụ thể (chữ ký %PDF-, PBKDF2 ở NFR-010) để kiểm thử được — chấp nhận, ghi nhận để Tech Lead xác nhận |
| 8 | Verifiable | Done | Mỗi FR/NFR có phương pháp kiểm chứng; mỗi AC dạng Given/When/Then |
| 9 | Performance & Capacity | Done | NFR-001, quy mô thiết kế §3.9.4 |
| 10 | Security & Privacy | Done | FR-001..003, FR-019, NFR-004, NFR-007, NFR-008, NFR-010 |
| 11 | Reliability & Availability | Done | NFR-005 (99%), NFR-006 (RTO 4h / RPO 24h) |
| 12 | Scalability | Done | §3.9.4 quy mô và đường mở rộng sang pgvector |
| 13 | User Interfaces (UI) | Done | §4 bố cục, UX-001..011, EC-01..17 |
| 14 | Hardware Interfaces | Done | Không áp dụng, đã ghi rõ |
| 15 | Software Interfaces | Done | REST/OpenAPI, Anthropic API tùy chọn |
| 16 | Communication Interfaces | Done | HTTPS, multipart, cookie |
| 17 | Design Constraints | Done | CON-001..005, ADR-001..003 về môi trường |
| 18 | Dependencies | Done | DEP-001..003, §6 |
| 19 | Unambiguous Language | Done | Không còn "nhanh/dễ"; ngưỡng đều có số |
| 20 | Traceable & Numbered | Done | BR → FR → US → AC trong traceability.md |
| 21 | Consistent | Done | Đã rà: FR-008 (P1) khớp US-205 P1; FR-018 giới hạn `manager` khớp persona Hùng; không có mâu thuẫn |

## Tổng hợp
| Done | In Progress | Pending |
|---|---|---|
| 19 | 1 | 0 |

## Mâu thuẫn đã phát hiện và xử lý
| # | Mâu thuẫn | Xử lý |
|---|---|---|
| 1 | PRD v0.1 để ngỏ "workspace chung hay riêng" (A-1) trong khi BR-028 mới yêu cầu cô lập | Áp dụng mặc định workspace riêng (BRD §12.1) |
| 2 | US-205 có thể nâng P0 nếu workspace chung | Workspace riêng → giữ P1 nhưng vẫn làm trong MVP |
| 3 | UX-005 đề xuất streaming; NFR-001 chế độ cục bộ ≤ 2 s | Streaming không cần cho MVP chế độ cục bộ; ghi vào ADR-006 |
