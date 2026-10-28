# 17. AC-301.4 câu hỏi rỗng không được gửi

| Mục | Giá trị |
|---|---|
| Chức năng | Hỏi đáp có trích dẫn |
| Nhóm | US-301..US-501 Hỏi đáp có trích dẫn |
| Tiêu chí chấp nhận | AC-301.4 |
| Kết quả | ✅ Đạt |
| Thời gian chạy | 1.2 s |
| Bắt đầu (UTC) | 2026-10-28 16:26:30 |
| Mã test | `app/e2e/tests/chat.spec.ts:82` |

Tệp: [screenshot.png](screenshot.png) · [video.mp4](video.mp4) · [result.json](result.json) · [← Mục lục](../report.md)

## Các bước kiểm thử (mã Playwright)

```ts
test("AC-301.4 câu hỏi rỗng không được gửi", async ({ page }) => {
  await page.getByLabel("Câu hỏi", { exact: true }).fill("   ");
  await expect(page.getByRole("button", { name: "Gửi" })).toBeDisabled();
});
```

## Video

<video src="video.mp4" controls width="960"></video>

[Mở video.mp4](video.mp4)

## Ảnh chụp màn hình cuối test

![AC-301.4 câu hỏi rỗng không được gửi](screenshot.png)
