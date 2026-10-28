# 11. AC-301.2 câu hỏi không dấu vẫn tìm được nội dung có dấu

| Mục | Giá trị |
|---|---|
| Chức năng | Hỏi đáp có trích dẫn |
| Nhóm | US-301..US-501 Hỏi đáp có trích dẫn |
| Tiêu chí chấp nhận | AC-301.2 |
| Kết quả | ✅ Đạt |
| Thời gian chạy | 2.6 s |
| Bắt đầu (UTC) | 2026-10-28 16:26:18 |
| Mã test | `app/e2e/tests/chat.spec.ts:37` |

Tệp: [screenshot.png](screenshot.png) · [video.mp4](video.mp4) · [result.json](result.json) · [← Mục lục](../report.md)

## Các bước kiểm thử (mã Playwright)

```ts
test("AC-301.2 câu hỏi không dấu vẫn tìm được nội dung có dấu", async ({ page }) => {
  await ask(page, "gia tri hop dong beta la bao nhieu");
  await expect(page.locator(".msg-a").last()).toContainText("900 triệu");
});
```

## Video

<video src="video.mp4" controls width="960"></video>

[Mở video.mp4](video.mp4)

## Ảnh chụp màn hình cuối test

![AC-301.2 câu hỏi không dấu vẫn tìm được nội dung có dấu](screenshot.png)
