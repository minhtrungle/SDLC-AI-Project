---
name: sdlc-verify
description: Phase 7 (Verify & L1 review) của Agentic SDLC — lập Master Test Plan IEEE 829 (skill test-plan), chạy đủ tầng test (unit, integration/API, E2E, eval), lập test report, review mã L1 theo IEEE 1028 (agent code-reviewer), kiểm toán bảo mật (agent security-auditor), vòng sửa lỗi, và review record để bàn giao reviewer L2 là con người. Được /sdlc điều phối; gọi riêng bằng /sdlc-verify.
argument-hint: "[full | review-only | retest]"
---

# Phase 7 — Verify & L1 review

## Tham chiếu
`docs/agentic-sdlc-process.md` §8, `docs/AI_SDLC-SOP.md` §5.7–5.8, `docs/prompts/testPlan_prompt.md`, checklist `Test_Plan_IEEE_829_Checklist.xlsx` và `Code_Review_IEEE_1028_Checklist.xlsx`. Risk tier trong `docs/01-intake/intent.md` quyết định có cần L3 (inspection) hay không.

## Các bước (orchestrator điều phối)

| # | Việc | Ai làm | Đầu ra (`docs/07-verification/`) |
|---|---|---|---|
| 1 | Master Test Plan | skill `test-plan` (orchestrator gọi `Skill`, hoặc giao `sdlc-author` đọc `.claude/skills/test-plan/SKILL.md`) | `testing/test-plan.md` + checklist IEEE 829 đã điền |
| 2 | Chạy test thật: L0 (`tools/ci_local.py --log docs/07-verification/ci/ci-log.txt`), E2E (`cd app/e2e && npm test` rồi `python tools/e2e_report.py`), eval AI nếu có | orchestrator (lệnh deterministic) | `ci/ci-log.txt`, `test_reports/`, `eval/eval-report.json` |
| 3 | Test report | `sdlc-author` | `testing/test-report.md`: số test theo tầng, pass/fail, coverage, AC pass/fail/chưa có test, lỗi mở theo mức độ, so với exit criteria của MTP |
| 4 | L1 code review — **song song với 5** | agent `code-reviewer` | `code-review/code-review-L1-round<N>.md` + xlsx |
| 5 | Security audit — **song song với 4** | agent `security-auditor` | biên bản theo định dạng của agent |
| 6 | Sửa lỗi | `sdlc-author` theo danh sách Critical/Major từ 3–5; mỗi sửa có test hồi quy mang ID AC hoặc ID phát hiện | commit `fix(...)` với `Refs:` |
| 7 | Vòng lại | chạy lại 2 → 4/5 (round N+1) cho đến khi không còn Critical/Major, **tối đa 2 vòng tự động** | |
| 8 | Review record | `sdlc-author` | `code-review/review-record.md`: phạm vi diff, các vòng L1, phát hiện đã đóng/còn mở, kết quả bảo mật, lệnh đã chạy và chưa chạy, rubric 7 tiêu chí (Đúng AC, Test, Thiết kế, An toàn, Hiệu năng, Dễ đọc, Truy vết — để trống cột điểm cho reviewer L2), checklist hoàn thành SOP §9 dạng ô chưa tích |

## Quy tắc
- Không tin báo cáo của subagent về test: orchestrator đọc output lệnh thật.
- Không sửa test để "cho qua"; lỗi không sửa được trong 2 vòng → gap mở trong review record.
- Agent không đánh dấu approve, không merge. Rubric L2 và chữ ký để trống.

## Tiêu chí qua cổng G6 (bàn giao L2)
- L0 xanh; E2E kết quả thật có trong test report (hoặc lý do không chạy).
- Không còn phát hiện Critical; Major còn lại có quyết định của người dùng ở cổng.
- Tỉ lệ AC P0/P1 có test tự động được nêu bằng số; checklist IEEE 829 và IEEE 1028 đã xuất xlsx.
