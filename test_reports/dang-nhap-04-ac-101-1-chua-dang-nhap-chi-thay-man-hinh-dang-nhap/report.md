# 04. AC-101.1 chưa đăng nhập chỉ thấy màn hình đăng nhập

| Mục | Giá trị |
|---|---|
| Chức năng | Đăng nhập và phiên |
| Nhóm | US-101 Đăng nhập |
| Tiêu chí chấp nhận | AC-101.1 |
| Kết quả | ✅ Đạt |
| Thời gian chạy | 0.7 s |
| Bắt đầu (UTC) | 2026-10-28 16:26:04 |
| Mã test | `app/e2e/tests/auth.spec.ts:6` |

Tệp: [screenshot.png](screenshot.png) · [video.mp4](video.mp4) · [result.json](result.json) · [← Mục lục](../report.md)

## Các bước kiểm thử (mã Playwright)

```ts
test("AC-101.1 chưa đăng nhập chỉ thấy màn hình đăng nhập", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Đăng nhập" })).toBeVisible();
  await expect(page.getByText("Tài liệu (")).toHaveCount(0);
});
```

## Video

<video src="video.mp4" controls width="960"></video>

[Mở video.mp4](video.mp4)

## Ảnh chụp màn hình cuối test

![AC-101.1 chưa đăng nhập chỉ thấy màn hình đăng nhập](screenshot.png)
