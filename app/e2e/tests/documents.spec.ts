import { expect, test } from "@playwright/test";

import { expectStatus, login, upload } from "./helpers";

test.describe("US-201..US-205 Quản lý tài liệu", () => {
  test.beforeEach(async ({ page }) => {
    await login(page, "doc_user");
  });

  test("AC-204.2 workspace trống hướng dẫn tải tài liệu và khóa ô hỏi", async ({ page }) => {
    await expect(page.getByRole("button", { name: "Tải tài liệu đầu tiên" })).toBeVisible();
    await expect(page.getByLabel("Câu hỏi", { exact: true })).toBeDisabled();
    await expect(page.getByText("Hãy tải tài liệu để bắt đầu hỏi.")).toBeVisible();
  });

  test("AC-201.1 / AC-201.2 / AC-202.1 tải song song nhiều file, file sai định dạng bị từ chối riêng", async ({ page }) => {
    await upload(page, "HopDong_Alpha.pdf", "DuAn_Beta.pdf", "ghi-chu.docx");
    await expect(page.getByText("ghi-chu.docx —")).toContainText("Sai định dạng, chỉ chấp nhận PDF.");
    // AC-203.2: trạng thái chuyển "Sẵn sàng" không cần tải lại trang
    await expectStatus(page, "HopDong_Alpha.pdf", "Sẵn sàng");
    await expectStatus(page, "DuAn_Beta.pdf", "Sẵn sàng");
    await expect(page.locator(".doc-name", { hasText: "ghi-chu.docx" })).toHaveCount(0);
    // AC-204.1: tên, trạng thái, số trang
    await expect(page.locator(".doc", { hasText: "HopDong_Alpha.pdf" })).toContainText("3 trang");
    await expect(page.getByRole("heading", { name: "Tài liệu (2)" })).toBeVisible();
  });

  test("AC-205.1 / AC-205.3 xóa tài liệu phải xác nhận; Hủy giữ nguyên", async ({ page }) => {
    await expectStatus(page, "DuAn_Beta.pdf", "Sẵn sàng");
    await page.getByRole("button", { name: "Xóa DuAn_Beta.pdf" }).click();
    const dialog = page.getByRole("dialog", { name: "Xóa tài liệu?" });
    await expect(dialog).toBeVisible();
    await dialog.getByRole("button", { name: "Hủy" }).click();
    await expect(page.locator(".doc-name", { hasText: "DuAn_Beta.pdf" })).toHaveCount(1);

    await page.getByRole("button", { name: "Xóa DuAn_Beta.pdf" }).click();
    await page.getByRole("dialog", { name: "Xóa tài liệu?" }).getByRole("button", { name: "Xóa" }).click();
    await expect(page.locator(".doc-name", { hasText: "DuAn_Beta.pdf" })).toHaveCount(0);
    await expect(page.getByRole("heading", { name: "Tài liệu (1)" })).toBeVisible();
  });
});
