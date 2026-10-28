# Cross-view audit — Phase 4 Design

> Sinh tự động bởi `python tools/cross_view_audit.py --write`. Không sửa tay.
> Nguồn sự thật: [elements.yaml](elements.yaml).

| View | Quy tắc | Kết quả | Chi tiết |
|---|---|---|---|
| SAD | mọi CMP có trong SAD §5.2 | PASS | — |
| Blueprint | mọi CMP có trong composition view | PASS | — |
| Component diagram | mọi CMP có trong sơ đồ | PASS | — |
| openapi.yaml | endpoint trong registry ⊆ openapi | PASS | — |
| openapi.yaml | không có endpoint ngoài registry | PASS | — |
| openapi.md | mọi operationId được mô tả | PASS | — |
| Registry | endpoint gán cho CMP tồn tại | PASS | — |
| schema.sql | bảng trong registry = bảng trong DDL | PASS | thiếu [], thừa [] |
| data/model.md | ENT-01 `users` được mô tả | PASS | — |
| Class diagram | ENT-01 User có trong sơ đồ | PASS | — |
| data/model.md | ENT-02 `sessions` được mô tả | PASS | — |
| Class diagram | ENT-02 Session có trong sơ đồ | PASS | — |
| data/model.md | ENT-03 `documents` được mô tả | PASS | — |
| Class diagram | ENT-03 Document có trong sơ đồ | PASS | — |
| data/model.md | ENT-04 `chunks` được mô tả | PASS | — |
| Class diagram | ENT-04 Chunk có trong sơ đồ | PASS | — |
| data/model.md | ENT-05 `conversations` được mô tả | PASS | — |
| Class diagram | ENT-05 Conversation có trong sơ đồ | PASS | — |
| data/model.md | ENT-06 `turns` được mô tả | PASS | — |
| Class diagram | ENT-06 Turn có trong sơ đồ | PASS | — |
| data/model.md | ENT-07 `feedback` được mô tả | PASS | — |
| Class diagram | ENT-07 Feedback có trong sơ đồ | PASS | — |
| data/model.md | ENT-08 `audit_log` được mô tả | PASS | — |
| Class diagram | ENT-08 AuditEvent có trong sơ đồ | PASS | — |
| Use case diagram | mọi actor có trong sơ đồ | PASS | — |
| Sequence diagram | CMP-03 tham gia luồng hỏi đáp | PASS | — |
| Sequence diagram | CMP-06 tham gia luồng hỏi đáp | PASS | — |
| Sequence diagram | CMP-07 tham gia luồng hỏi đáp | PASS | — |
| Sequence diagram | CMP-08 tham gia luồng hỏi đáp | PASS | — |
| Sequence diagram | CMP-11 tham gia luồng hỏi đáp | PASS | — |
| Deployment diagram | CMP-01, CMP-11, CMP-12 và ACT-04 được triển khai | PASS | — |
| PRD → Design | 19 FR đều có CMP/endpoint | PASS | — |
| ADR | 9 ADR (≥ 3) đều được SAD §9 tham chiếu | PASS | — |
| UI/UX | mọi màn hình có prototype | PASS | — |
| Code | mọi module của CMP tồn tại | PASS | — |
| Code ↔ openapi.yaml | enum Problem.code = mã lỗi trong cwd/errors.py | PASS | chỉ ở openapi [], chỉ ở code [] |
| Code | route FastAPI = endpoint registry | PASS | thiếu [], thừa [] |

**Tổng:** 37 PASS · 0 FAIL · 0 SKIP
