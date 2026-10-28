import { fileURLToPath } from "node:url";

import { expect, type Page } from "@playwright/test";

export const PASSWORD = "e2e-pass-123"; // secret-scan: allow (throwaway E2E account, see serve.py)

export function fixture(name: string): string {
  return fileURLToPath(new URL(`../.data/pdfs/${name}`, import.meta.url));
}

export async function login(page: Page, username: string): Promise<void> {
  await page.goto("/");
  await page.getByLabel("Tên đăng nhập").fill(username);
  await page.getByLabel("Mật khẩu").fill(PASSWORD);
  await page.getByRole("button", { name: "Đăng nhập" }).click();
  await expect(page.getByRole("heading", { name: /Tài liệu \(\d+\)/ })).toBeVisible();
}

export async function upload(page: Page, ...files: string[]): Promise<void> {
  await page.getByTestId("file-input").setInputFiles(files.map(fixture));
}

/** Upload only the files not yet in the list (beforeAll may re-run after a worker restart). */
export async function ensureUploaded(page: Page, ...files: string[]): Promise<void> {
  const present = await page.locator(".doc-name").allInnerTexts();
  const missing = files.filter((f) => !present.includes(f));
  if (missing.length) await upload(page, ...missing);
  for (const f of files) await expectStatus(page, f, "Sẵn sàng");
}

/** Wait until the document row shows the given status label. */
export async function expectStatus(page: Page, filename: string, label: string): Promise<void> {
  const row = page.locator(".doc").filter({ has: page.getByText(filename, { exact: true }) });
  await expect(row.locator(".status")).toContainText(label);
}

/** Ask and wait until the answer is rendered (the pending "Đang trả lời…" bubble is gone). */
export async function ask(page: Page, question: string): Promise<void> {
  const box = page.getByLabel("Câu hỏi", { exact: true });
  const before = await page.locator(".msg-q").count();
  await box.fill(question);
  await box.press("Enter");
  await expect(page.locator(".msg-a.muted")).toHaveCount(0);
  await expect(page.locator(".msg-q")).toHaveCount(before + 1);
}

/** Send without waiting — for flows where the request is expected to fail (e.g. expired session). */
export async function send(page: Page, question: string): Promise<void> {
  const box = page.getByLabel("Câu hỏi", { exact: true });
  await box.fill(question);
  await box.press("Enter");
}
