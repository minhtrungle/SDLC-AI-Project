import { expect, test } from "@playwright/test";

import { expectStatus, login, PASSWORD, send, upload } from "./helpers";

test.describe("US-101 Đăng nhập", () => {
  test("AC-101.1 chưa đăng nhập chỉ thấy màn hình đăng nhập", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("heading", { name: "Đăng nhập" })).toBeVisible();
    await expect(page.getByText("Tài liệu (")).toHaveCount(0);
  });

  test("AC-101.3 sai mật khẩu hiển thị thông báo chung", async ({ page }) => {
    await page.goto("/");
    await page.getByLabel("Tên đăng nhập").fill("auth_user");
    await page.getByLabel("Mật khẩu").fill("sai-mat-khau");
    await page.getByRole("button", { name: "Đăng nhập" }).click();
    await expect(page.getByRole("alert")).toHaveText("Tên đăng nhập hoặc mật khẩu không đúng.");
  });

  test("AC-101.2 / AC-101.6 đăng nhập vào workspace, đăng xuất về màn hình đăng nhập", async ({ page }) => {
    await login(page, "auth_user");
    await expect(page.getByText("🔒 Xử lý cục bộ")).toBeVisible(); // AC-102.1: chế độ xử lý hiển thị cho người dùng
    await page.getByRole("button", { name: "Đăng xuất" }).click();
    await expect(page.getByRole("heading", { name: "Đăng nhập" })).toBeVisible();
    await page.reload();
    await expect(page.getByRole("heading", { name: "Đăng nhập" })).toBeVisible();
  });

  test("AC-101.4 gọi API trực tiếp khi chưa đăng nhập bị từ chối", async ({ page }) => {
    // Opened in the browser so the screenshot/video show the raw 401 problem+json response.
    const r = await page.goto("/api/documents");
    expect(r?.status()).toBe(401);
    expect((await r?.json()).code).toBe("auth.required");
    await expect(page.locator("body")).toContainText("auth.required");
  });

  test("EC-15 phiên hết hạn giữ lại câu hỏi đang soạn", async ({ page, context }) => {
    await login(page, "auth_user");
    await upload(page, "DuAn_Beta.pdf");
    await expectStatus(page, "DuAn_Beta.pdf", "Sẵn sàng");
    await context.clearCookies(); // phiên mất phía trình duyệt ⇒ request tiếp theo nhận 401
    await send(page, "Dự án Beta triển khai ở đâu?");
    await expect(page.getByText("Phiên đăng nhập đã hết hạn")).toBeVisible();
    await page.getByLabel("Tên đăng nhập").fill("auth_user");
    await page.getByLabel("Mật khẩu").fill(PASSWORD);
    await page.getByRole("button", { name: "Đăng nhập" }).click();
    await expect(page.getByLabel("Câu hỏi", { exact: true })).toHaveValue("Dự án Beta triển khai ở đâu?");
  });
});
