import { expect, test } from "@playwright/test";

import { ask, ensureUploaded, login } from "./helpers";

test.describe("NFR-004 Cô lập workspace", () => {
  test("AC-NFR-004 người dùng khác không thấy và không hỏi được tài liệu của mình", async ({ browser, page: b }) => {
    // Setup as user A in a separate context; the recorded page is user B's point of view.
    const contextA = await browser.newContext();
    const a = await contextA.newPage();
    await login(a, "iso_a");
    await ensureUploaded(a, "HopDong_Alpha.pdf");
    await contextA.close();

    await login(b, "iso_b");
    await expect(b.locator(".doc-name", { hasText: "HopDong_Alpha.pdf" })).toHaveCount(0);
    await ensureUploaded(b, "DuAn_Beta.pdf");
    await ask(b, "Giá trị hợp đồng Alpha là bao nhiêu?");
    // B may get an answer from B's own similar page ("Giá trị hợp đồng Beta"), but never A's document.
    const answer = b.locator(".msg-a").last();
    await expect(answer).not.toContainText("HopDong_Alpha.pdf");
    await expect(answer).not.toContainText("2,5 tỷ");
  });
});

test.describe("US-502 Số liệu sử dụng", () => {
  test("AC-502.2 người dùng thường không có mục Số liệu sử dụng", async ({ page }) => {
    await login(page, "dash_user");
    await expect(page.getByRole("button", { name: "Số liệu sử dụng" })).toHaveCount(0);
    expect((await page.request.get("/api/metrics/weekly")).status()).toBe(403);
  });

  test("AC-502.1 quản lý xem số liệu theo tuần", async ({ page, browser }) => {
    // Own data: one question asked this week by dash_user (no dependency on other spec files).
    // Closed afterwards: open contexts would leak into later tests' screenshots/videos.
    const askerContext = await browser.newContext();
    const asker = await askerContext.newPage();
    await login(asker, "dash_user");
    await ensureUploaded(asker, "DuAn_Beta.pdf");
    await ask(asker, "Dự án Beta triển khai ở đâu?");
    await expect(asker.locator(".msg-a").last()).toContainText("Đà Nẵng");
    await askerContext.close();
    await login(page, "hung");
    await page.getByRole("button", { name: "Số liệu sử dụng" }).click();
    await expect(page.getByRole("heading", { name: "Số liệu sử dụng theo tuần" })).toBeVisible();
    const rows = page.locator("tbody tr");
    await expect(rows).toHaveCount(8);
    // các spec trước đã đặt câu hỏi trong tuần này ⇒ tuần hiện tại có người dùng hoạt động
    await expect(rows.last().locator("td").nth(1)).not.toHaveText("0");
    await page.getByRole("button", { name: "Về màn hình chính" }).click();
    await expect(page.getByRole("heading", { name: /Tài liệu/ })).toBeVisible();
  });
});
