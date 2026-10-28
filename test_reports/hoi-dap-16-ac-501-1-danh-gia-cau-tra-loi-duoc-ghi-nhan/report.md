# 16. AC-501.1 đánh giá câu trả lời được ghi nhận

| Mục | Giá trị |
|---|---|
| Chức năng | Hỏi đáp có trích dẫn |
| Nhóm | US-301..US-501 Hỏi đáp có trích dẫn |
| Tiêu chí chấp nhận | AC-501.1 |
| Kết quả | ✅ Đạt |
| Thời gian chạy | 1.7 s |
| Bắt đầu (UTC) | 2026-10-28 16:26:28 |
| Mã test | `app/e2e/tests/chat.spec.ts:75` |

Tệp: [screenshot.png](screenshot.png) · [video.mp4](video.mp4) · [result.json](result.json) · [← Mục lục](../report.md)

## Các bước kiểm thử (mã Playwright)

```ts
test("AC-501.1 đánh giá câu trả lời được ghi nhận", async ({ page }) => {
  await ask(page, "Giá trị hợp đồng Alpha là bao nhiêu?");
  const up = page.locator(".msg-a").last().getByRole("button", { name: "Hữu ích", exact: true });
  await up.click();
  await expect(up).toHaveAttribute("aria-pressed", "true");
});
```

## Video

<video src="video.mp4" controls width="960"></video>

[Mở video.mp4](video.mp4)

## Ảnh chụp màn hình cuối test

![AC-501.1 đánh giá câu trả lời được ghi nhận](screenshot.png)
