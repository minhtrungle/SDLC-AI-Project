import { expect, test } from "@playwright/test";

import { ask, ensureUploaded, login } from "./helpers";

test.describe("US-301..US-501 Hỏi đáp có trích dẫn", () => {
  test.beforeAll(async ({ browser }) => {
    const page = await browser.newPage();
    await login(page, "chat_user");
    await ensureUploaded(page, "HopDong_Alpha.pdf", "DuAn_Beta.pdf", "BangGia_2026.pdf");
    await page.close();
  });

  test.beforeEach(async ({ page }) => {
    await login(page, "chat_user");
    await page.getByRole("button", { name: "Cuộc hội thoại mới" }).click();
  });

  test("AC-301.1 / AC-305.1 câu trả lời kèm trích dẫn tên tài liệu và trang", async ({ page }) => {
    await ask(page, "Giá trị hợp đồng Alpha là bao nhiêu?");
    const answer = page.locator(".msg-a").last();
    await expect(answer).toContainText("2,5 tỷ đồng");
    await expect(answer.getByRole("button", { name: "HopDong_Alpha.pdf — tr. 2" })).toBeVisible();
  });

  test("AC-305.2 bấm trích dẫn mở đoạn gốc; Esc đóng và trả focus", async ({ page }) => {
    await ask(page, "Giá trị hợp đồng Alpha là bao nhiêu?");
    const cite = page.locator("button.cite").first();
    await cite.click();
    const drawer = page.getByRole("dialog", { name: "Nguồn trích dẫn" });
    await expect(drawer).toContainText("HopDong_Alpha.pdf — trang 2");
    await expect(drawer.locator(".drawer-text")).toContainText("Giá trị hợp đồng Alpha là 2,5 tỷ đồng");
    await page.keyboard.press("Escape");
    await expect(drawer).toHaveCount(0);
    await expect(cite).toBeFocused();
  });

  test("AC-301.2 câu hỏi không dấu vẫn tìm được nội dung có dấu", async ({ page }) => {
    await ask(page, "gia tri hop dong beta la bao nhieu");
    await expect(page.locator(".msg-a").last()).toContainText("900 triệu");
  });

  test("AC-304.1 / AC-303.1 câu hỏi ngoài tài liệu được báo không tìm thấy, không trích dẫn", async ({ page }) => {
    await ask(page, "Thủ đô của nước Pháp là gì?");
    const answer = page.locator(".msg-a").last();
    await expect(answer).toHaveClass(/not-found/);
    await expect(answer).toContainText("Không tìm thấy thông tin trong tài liệu đã tải lên");
    await expect(answer.locator(".sources")).toHaveCount(0);
  });

  test("AC-401.1 hỏi tiếp hiểu ngữ cảnh lượt trước", async ({ page }) => {
    await ask(page, "Giá trị hợp đồng Alpha là bao nhiêu?");
    await ask(page, "Thời hạn của nó?");
    await expect(page.locator(".msg-a").nth(1).getByRole("button", { name: "HopDong_Alpha.pdf — tr. 3" })).toBeVisible();
  });

  test("AC-402.1 / AC-402.2 giới hạn phạm vi vào một tài liệu", async ({ page }) => {
    await page.getByRole("checkbox", { name: "Chọn HopDong_Alpha.pdf làm phạm vi câu hỏi" }).check();
    await expect(page.getByText("Phạm vi: 1 tài liệu đã chọn")).toBeVisible();
    await ask(page, "Dự án Beta triển khai ở đâu?");
    const answer = page.locator(".msg-a").last();
    await expect(answer).toHaveClass(/not-found/);
    await expect(answer).not.toContainText("DuAn_Beta.pdf");
  });

  test("AC-403.1 / AC-403.2 hội thoại giữ thứ tự; cuộc hội thoại mới trống", async ({ page }) => {
    await ask(page, "Giá trị hợp đồng Alpha là bao nhiêu?");
    await ask(page, "Phí bảo trì hằng năm là bao nhiêu?");
    await expect(page.locator(".msg-q")).toHaveText(["Giá trị hợp đồng Alpha là bao nhiêu?", "Phí bảo trì hằng năm là bao nhiêu?"]);
    await page.reload(); // US-403: hội thoại của phiên trình duyệt được khôi phục
    await expect(page.locator(".msg-q")).toHaveCount(2);
    await page.getByRole("button", { name: "Cuộc hội thoại mới" }).click();
    await expect(page.locator(".msg-q")).toHaveCount(0);
  });

  test("AC-501.1 đánh giá câu trả lời được ghi nhận", async ({ page }) => {
    await ask(page, "Giá trị hợp đồng Alpha là bao nhiêu?");
    const up = page.locator(".msg-a").last().getByRole("button", { name: "Hữu ích", exact: true });
    await up.click();
    await expect(up).toHaveAttribute("aria-pressed", "true");
  });

  test("AC-301.4 câu hỏi rỗng không được gửi", async ({ page }) => {
    await page.getByLabel("Câu hỏi", { exact: true }).fill("   ");
    await expect(page.getByRole("button", { name: "Gửi" })).toBeDisabled();
  });
});
