# 06. AC-101.2 / AC-101.6 đăng nhập vào workspace, đăng xuất về màn hình đăng nhập

| Mục | Giá trị |
|---|---|
| Chức năng | Đăng nhập và phiên |
| Nhóm | US-101 Đăng nhập |
| Tiêu chí chấp nhận | AC-101.2, AC-101.6 |
| Kết quả | ✅ Đạt |
| Thời gian chạy | 1.3 s |
| Bắt đầu (UTC) | 2026-10-28 16:26:06 |
| Mã test | `app/e2e/tests/auth.spec.ts:20` |

Tệp: [screenshot.png](screenshot.png) · [video.mp4](video.mp4) · [result.json](result.json) · [← Mục lục](../report.md)

## Các bước kiểm thử (mã Playwright)

```ts
test("AC-101.2 / AC-101.6 đăng nhập vào workspace, đăng xuất về màn hình đăng nhập", async ({ page }) => {
  await login(page, "auth_user");
  await expect(page.getByText("🔒 Xử lý cục bộ")).toBeVisible(); // AC-102.1: chế độ xử lý hiển thị cho người dùng
  await page.getByRole("button", { name: "Đăng xuất" }).click();
  await expect(page.getByRole("heading", { name: "Đăng nhập" })).toBeVisible();
  await page.reload();
  await expect(page.getByRole("heading", { name: "Đăng nhập" })).toBeVisible();
});
```

## Video

<video src="video.mp4" controls width="960"></video>

[Mở video.mp4](video.mp4)

## Ảnh chụp màn hình cuối test

![AC-101.2 / AC-101.6 đăng nhập vào workspace, đăng xuất về màn hình đăng nhập](screenshot.png)
