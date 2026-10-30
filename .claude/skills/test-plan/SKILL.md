---
name: test-plan
description: Lập hoặc cập nhật Master Test Plan (MTP) theo IEEE 829-2008 cho dự án "Chat với tài liệu", bám prompt docs/prompts/testPlan_prompt.md. Phân tích PRD/SAD/UI-UX/OpenAPI/USER_STORIES/PLAN, dựng chiến lược và test case truy vết tới FR/NFR/AC và tới test có thật trong repo, chạy test để lấy số liệu thật, tự audit theo docs/checklists/Test_Plan_IEEE_829_Checklist.xlsx và xuất bản sao checklist đã điền Status. Dùng khi người dùng muốn "lập test plan", "cập nhật test plan", "làm kế hoạch kiểm thử", hoặc gọi /test-plan.
argument-hint: "[ghi chú phạm vi, ví dụ: cập nhật sau sprint S3 | chỉ audit]"
---

# Test Plan theo IEEE 829 (testPlan_prompt)

Bạn thực hiện vai trò trong `docs/prompts/testPlan_prompt.md`: **Senior QA Architect / Test Documentation Expert**. Ngôn ngữ tài liệu: tiếng Việt; giữ nguyên thuật ngữ và tên mục IEEE bằng tiếng Anh như MTP hiện có.

Ghi chú phạm vi từ người dùng (có thể trống): **$ARGUMENTS**

## Đầu vào và đầu ra

| Loại | Đường dẫn |
|---|---|
| Prompt (khung nội dung) | `docs/prompts/testPlan_prompt.md` |
| SRS/PRD | `docs/03-analysis/PRD.md` §3.9 (FR, NFR, UX, EC, launch gate), `docs/02-requirements/BRD.md` |
| User stories + AC | `docs/03-analysis/USER_STORIES.md` |
| SAD / Blueprint (IEEE 1016) | `docs/04-design/SAD.md`, `docs/04-design/blueprint.md`, `docs/04-design/adr/`, `docs/04-design/elements.yaml` |
| UI/UX | `docs/04-design/UI_UX_design/` |
| API | `app/api-contract/openapi.yaml`, `docs/04-design/openapi.md` |
| Data model | `docs/04-design/data/model.md` |
| Development plan | `docs/05-implement/PLAN.md`, `docs/05-implement/tasks/` |
| Truy vết | `docs/03-analysis/traceability.md` (sinh bởi `tools/trace_matrix.py`) |
| Test có thật | `app/backend/tests/`, `app/frontend/src/**/*.spec.ts`, `app/e2e/tests/`, `app/backend/tests/eval/` |
| Checklist (template, chỉ đọc) | `docs/checklists/Test_Plan_IEEE_829_Checklist.xlsx` |
| **Đầu ra 1: MTP** | `docs/07-verification/testing/test-plan.md` |
| **Đầu ra 2: checklist đã điền** | `docs/07-verification/testing/Test_Plan_IEEE_829_Checklist_v<phiên bản MTP>.xlsx` |

Thiếu file đầu vào nào thì ghi vào A.1 là "không có" và nêu rủi ro ở 15.0. Không được bịa nội dung cho phần thiếu.

## Quy trình

### 1. Chuẩn bị
1. Đọc **toàn bộ** `docs/prompts/testPlan_prompt.md`. Lưu ý: bản prompt hiện tại chỉ chi tiết đến §6.1.10 và để trống §6.2. Các mục 6.2 → 16.0 phải được viết theo bảng mục IEEE 829 ở prompt §3.1 (clause 5.6–5.16).
2. Đọc `AGENTS.md` (quy ước ID AC trong test, lệnh chạy test, điều cấm).
3. Nếu `docs/07-verification/testing/test-plan.md` đã có, đây là **chế độ cập nhật**:
   - Đọc bản hiện có, giữ cấu trúc Phần A / Phần B / Phụ lục và các ID đã cấp (F-xx, RISK-xx, INT-API-xxx, E2E-xxx…). Không đánh số lại; ID mới được cấp tiếp nối.
   - Tăng phiên bản: thay đổi nội dung là tăng minor (2.0 → 2.1), viết lại cấu trúc là tăng major.
   - Thêm hoặc cập nhật mục **Lịch sử phiên bản** (phiên bản · ngày · thay đổi · người soạn), vì `AGENTS.md` cấm sửa tài liệu đã baseline mà không ghi lịch sử.
   - Chỉ sửa những gì đã thay đổi so với thực tế (yêu cầu, test, số liệu). Liệt kê các thay đổi đó trong lịch sử phiên bản.
4. Nếu người dùng ghi "chỉ audit", bỏ qua bước 2–3 dưới đây, chỉ làm bước 4–5.

### 2. Phân tích đầu vào (Phần A, tương ứng prompt §2)
Viết A.1 → A.7 đúng các bảng của prompt §2.1–2.7:
- **A.1** danh mục tài liệu, ghi phiên bản thật (đọc từ header của từng tài liệu).
- **A.2** yêu cầu kiểm thử được: mọi FR và NFR **trong phạm vi** của PRD §3.9, kèm ưu tiên và story. Không bỏ sót mục nào: so số lượng với PRD.
- **A.3** thành phần thiết kế theo các view IEEE 1016 (Composition CMP-xx, Interaction, Information, Interface, State Dynamics từ blueprint §3.7).
- **A.4** màn hình SCR-xx và các trạng thái UI; **A.5** mọi endpoint trong `openapi.yaml` (method, schema, mã lỗi problem+json, có cần auth không). Đối chiếu số endpoint thực tế với file.
- **A.6** story và AC (có thể trỏ tới USER_STORIES.md thay vì chép lại toàn bộ).
- **A.7** rủi ro: điểm = khả năng × ảnh hưởng (1–5). Rủi ro cao định hướng mức đầu tư test ở 4.1.

### 3. Viết MTP (Phần B, IEEE 829 mục 1.0 → 16.0)
Theo đúng thứ tự và tên mục ở prompt §3.1. Nội dung từng mục như prompt §4 (4.1 → 4.6), áp dụng vào dự án này:
- **6.1 Test levels/types**: Unit (pytest, Vitest), Integration/API (TestClient, contract `check:api`), System/E2E (Playwright, `app/e2e`), Acceptance (UAT theo AC), Regression (cổng L0 `tools/ci_local.py`), Performance (theo NFR có ngưỡng), Security (NFR-004/008/010, SAD §8.1; tham chiếu agent `security-auditor` nếu đã có biên bản), Accessibility (WCAG 2.1 AA), UI/UX, API, và Eval AI (`tests/eval`). Mỗi loại có công cụ, entry/exit criteria, test case.
- **Test case phải truy vết hai chiều**: mỗi test case ghi FR/NFR/AC mà nó kiểm tra, **và** trỏ tới test tự động có thật (`file::tên_test`, hoặc `test("AC-…")` E2E) tìm được bằng `Grep` theo ID AC. Không tìm thấy test thì ghi rõ "Thủ công" hoặc "**Chưa có test**". Mọi trường hợp "chưa có test" phải được liệt kê ở 15.0 hoặc trong mục khoảng trống.
- Không viết ví dụ chung chung từ template (thanh toán, JWT, OAuth, Kubernetes…) nếu dự án không có. Thay bằng chức năng thật của dự án hoặc ghi N/A kèm lý do.
- **6.2 Test execution strategy**: thứ tự chạy (L0 → E2E → UAT), tần suất, quản lý lỗi, tiêu chí smoke.
- **7.0–8.0**: ngưỡng đo được (coverage backend ≥ 70% theo AGENTS.md, 0 lỗi Critical mở, AC pass…), điều kiện tạm dừng và điều kiện tiếp tục.
- **12.0 / 16.0**: agent không phê duyệt. Bảng Approvals để trống chữ ký; trạng thái tài liệu là `Draft` hoặc `Review`, không bao giờ `Approved`.

### 4. Lấy số liệu thật (Phụ lục A) và kiểm tra truy vết
Chạy từ gốc repo và ghi kết quả thật vào Phụ lục A (số test, pass/fail, coverage, ngày chạy):
```bash
cd app/backend && ../../.venv/Scripts/python -m pytest -q          # backend + coverage
cd app/frontend && npm test                                         # Vitest + coverage
.venv/Scripts/python tools/trace_matrix.py                          # exit 1 nếu có dòng trong phạm vi chưa có test
```
- E2E (`cd app/e2e && npm test`) cần bản build frontend và mất nhiều thời gian. Chỉ chạy khi người dùng yêu cầu hoặc bản build đã có sẵn. Nếu không chạy, ghi lại kết quả gần nhất từ `test_reports/report.md` hoặc `docs/07-verification/testing/test-report.md`, có ghi chú nguồn và ngày.
- Lệnh nào fail hoặc không chạy được: ghi đúng output tóm tắt. Không làm tròn thành "Đạt".
- `trace_matrix.py` có ghi lại `docs/03-analysis/traceability.md`. Đây là file sinh tự động nên được phép cập nhật; báo cho người dùng nếu file thay đổi.
- Đếm số AC trong USER_STORIES.md (phạm vi P0/P1) và số AC có ít nhất một test, rồi ghi tỉ lệ bao phủ AC vào 2.3 (Objectives) và Phụ lục A.

### 5. Tự audit theo checklist (Phụ lục B) và xuất xlsx
1. Đọc template để lấy danh sách mục và **bộ giá trị Status hợp lệ từ data validation** (hiện là `Pending, In Progress, Done, N/A`; không dùng giá trị ngoài danh sách này):
   ```bash
   .venv/Scripts/python -c "import openpyxl; ws=openpyxl.load_workbook('docs/checklists/Test_Plan_IEEE_829_Checklist.xlsx').worksheets[0]; print([d.formula1 for d in ws.data_validations.dataValidation]); [print(r[0].row,'|',r[1].value,'|',r[2].value) for r in ws.iter_rows(min_row=2) if r[1].value]"
   ```
2. Viết Phụ lục B trong `test-plan.md` dưới dạng bảng `| Row | Item | Status | Notes |`, trong đó `Row` là số dòng trong sheet. Mọi dòng phải có Status và Notes; Notes trỏ tới mục MTP làm bằng chứng và không chứa `|` hay xuống dòng. Mục nào chưa đủ (ví dụ lịch UAT chưa có ngày) thì đánh `In Progress` kèm lý do, không đánh `Done`. Ghi rõ đây là tự kiểm tra của người soạn; QA Lead phải review độc lập.
3. **Ràng buộc với parser:** `tools/checklist_fill.py` đọc **bảng đầu tiên trong file có cả hai cột `Status` và `Notes`**. Vì vậy không bảng nào phía trên Phụ lục B được có đồng thời hai tiêu đề cột này (dùng "Trạng thái", "Ghi chú" hoặc "Kết quả" thay thế).
4. Xuất bản sao (template không bị sửa):
   ```bash
   .venv/Scripts/python tools/checklist_fill.py docs/checklists/Test_Plan_IEEE_829_Checklist.xlsx docs/07-verification/testing/test-plan.md docs/07-verification/testing/Test_Plan_IEEE_829_Checklist_v<phiên bản>.xlsx
   ```
5. Kiểm tra: số dòng được điền bằng số mục của template, không có ô Status trống hay sai giá trị, và `git status docs/checklists` sạch.

## Điều cấm
- Không sửa code ứng dụng hay test. Skill này chỉ viết tài liệu. Test còn thiếu thì ghi thành khoảng trống hoặc việc cần làm, không tự viết test.
- Không sửa template checklist và prompt.
- Không bịa số liệu, phiên bản, ngày, tên người phê duyệt; không đánh dấu tài liệu là `Approved`.
- Không ghi dữ liệu nhạy cảm (mật khẩu demo, token, nội dung tài liệu người dùng) vào MTP.
- Không commit trừ khi người dùng yêu cầu. Nếu được yêu cầu commit: dùng `docs(test): …` và thêm dòng `Refs:` theo AGENTS.md.

## Kết thúc
Báo lại cho người dùng ngắn gọn:
- Đường dẫn MTP và file xlsx; phiên bản cũ → mới; các thay đổi chính.
- Số FR/NFR/AC trong phạm vi, tỉ lệ AC có test tự động, danh sách AC "chưa có test".
- Kết quả các lệnh test (số thật) và lệnh nào không chạy được.
- Bảng đếm Status của checklist và các mục chưa `Done`.
