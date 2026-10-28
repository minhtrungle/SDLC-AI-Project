# Audit BRD v0.2 theo checklist IEEE 29148

- **Tài liệu được audit:** [BRD.md](BRD.md) v0.2
- **Checklist:** [BRD_IEEE_29148_Checklist.xlsx](../checklists/BRD_IEEE_29148_Checklist.xlsx) → bản đã điền: `BRD_IEEE_29148_Checklist_v0.2.xlsx`
- **Người audit:** Agent (Claude). Agent sinh BRD v0.2 nên **không thể là người review độc lập**. Kết quả này là tự kiểm tra; PO/BA phải review lại.
- **Ngày:** 2026-10-28

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Business Purpose & Drivers | Done | §3 nêu vấn đề, nguyên nhân gốc, chi phí nếu không làm |
| 3 | Business Objectives & Success Metrics | In Progress | BO-001..003 và MET-001..003 có định nghĩa và công thức. Target mới là đề xuất (§12.1, OQ-005); baseline MET-001 vẫn chờ OQ-003 |
| 4 | Scope & Boundaries | Done | §5 có trong phạm vi, ngoài phạm vi, hoãn, ranh giới |
| 5 | Vision Statement | Done | Thêm §2.1 ở v0.2 |
| 6 | Stakeholder Identification | Done | STK-001..006, thêm QA ở v0.2; RACI ở 01-intake/stakeholders.md |
| 7 | User Personas & Profile Characteristics | Done | Tham chiếu persona Linh/Hùng/Mai tại PRD §2.1 |
| 8 | Business Constraints | In Progress | CON-001..005 đủ loại; ngân sách và deadline (CON-005) vẫn chờ OQ-008/009 |
| 9 | Current State ('As-Is') Workflow | Done | §3.1 có sơ đồ; chi tiết còn [Unverified] chờ phỏng vấn (OQ-002) |
| 10 | Target State ('To-Be') Workflow | Done | §3.2 |
| 11 | Operational Scenario & Use Cases | Done | Kịch bản trong AC-015, To-Be, và use case diagram ở Phase 4 |
| 12 | Singularity & Clarity | Done | Mỗi BR một nghĩa vụ, dùng phải/nên/có thể |
| 13 | Completeness & Implementation-Free | Done | Không có ngôn ngữ giải pháp trong BR; các [TBD] định lượng đã có giá trị mặc định tham số hóa (§12.1) |
| 14 | Traceability & Rationale | Done | Mỗi BR có lý do, nguồn, AC; §11 truy vết tới NFR/PRD |
| 15 | Feasibility & Realism | Done | Phạm vi MoSCoW; prototype chạy được trong môi trường hiện có (ADR-001/002) |
| 16 | Compliance & Regulatory Standards | In Progress | BR-020, BR-026, BR-027 có; quy định pháp lý cụ thể của tổ chức chờ IT/Bảo mật (OQ-006) |
| 17 | Business Continuity & Availability | Done | BR-024 (99% giờ làm việc), BR-025 (RTO 4h, RPO 24h) |
| 18 | Security & Business Policy Constraints | Done | BR-019, BR-020, BR-026..BR-028; BRU-003..005 |
| 19 | Business Assumptions | Done | ASM-001..004 |
| 20 | Dependencies & Constraints | Done | DEP-001..003 |
| 21 | Business Risks & Mitigation | Done | RSK-001..006 có owner, giảm thiểu, hạn |

## Tổng hợp

| Done | In Progress | Pending |
|---|---|---|
| 17 | 4 | 0 |

## Các mục còn mở và người chịu trách nhiệm
| Mục | Việc cần làm | Owner |
|---|---|---|
| Row 3 | Đo baseline MET-001, chốt target | Quản lý dự án |
| Row 8 | Chốt ngân sách và deadline | Sponsor |
| Row 16 | Cung cấp chính sách phân loại dữ liệu | IT / Bảo mật |

## Kết luận
BRD v0.2 **đủ điều kiện baseline có điều kiện**: PO ký và chấp nhận các giá trị mặc định ở §12.1 (hoặc thay bằng giá trị khác). Các mục In Progress không chặn thiết kế vì đều là tham số cấu hình.
