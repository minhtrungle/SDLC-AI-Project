# 12. AC-304.1 / AC-303.1 câu hỏi ngoài tài liệu được báo không tìm thấy, không trích dẫn

| Mục | Giá trị |
|---|---|
| Chức năng | Hỏi đáp có trích dẫn |
| Nhóm | US-301..US-501 Hỏi đáp có trích dẫn |
| Tiêu chí chấp nhận | AC-304.1, AC-303.1 |
| Kết quả | ✅ Đạt |
| Thời gian chạy | 1.6 s |
| Bắt đầu (UTC) | 2026-10-28 16:26:21 |
| Mã test | `app/e2e/tests/chat.spec.ts:42` |

Tệp: [screenshot.png](screenshot.png) · [video.mp4](video.mp4) · [result.json](result.json) · [← Mục lục](../report.md)

## Các bước kiểm thử (mã Playwright)

```ts
test("AC-304.1 / AC-303.1 câu hỏi ngoài tài liệu được báo không tìm thấy, không trích dẫn", async ({ page }) => {
  await ask(page, "Thủ đô của nước Pháp là gì?");
  const answer = page.locator(".msg-a").last();
  await expect(answer).toHaveClass(/not-found/);
  await expect(answer).toContainText("Không tìm thấy thông tin trong tài liệu đã tải lên");
  await expect(answer.locator(".sources")).toHaveCount(0);
});
```

## Video

<video src="video.mp4" controls width="960"></video>

[Mở video.mp4](video.mp4)

## Ảnh chụp màn hình cuối test

![AC-304.1 / AC-303.1 câu hỏi ngoài tài liệu được báo không tìm thấy, không trích dẫn](screenshot.png)
