import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";

import { defineConfig, devices } from "@playwright/test";

const here = fileURLToPath(new URL(".", import.meta.url));
const venvPython = process.platform === "win32" ? "../../.venv/Scripts/python.exe" : "../../.venv/bin/python";
const python = process.env.PYTHON ?? (existsSync(new URL(venvPython, import.meta.url)) ? venvPython : "python");
const PORT = 8799;
const REPORT_DIR = "../../test_reports"; // screenshots, mp4 videos, results.json, report.md (tools/e2e_report.py)

export default defineConfig({
  testDir: "./tests",
  // One shared backend and database: run serially so every scenario is deterministic.
  fullyParallel: false,
  workers: 1,
  retries: process.env.CI ? 1 : 0,
  timeout: 30_000,
  expect: { timeout: 10_000 },
  forbidOnly: !!process.env.CI,
  reporter: [
    ["list"],
    ["html", { outputFolder: `${REPORT_DIR}/html`, open: "never" }],
    ["junit", { outputFile: `${REPORT_DIR}/results.xml` }],
    ["json", { outputFile: `${REPORT_DIR}/results.json` }],
  ],
  // Raw per-test artifacts (webm, png, trace); tools/e2e_report.py turns them into screenshots/ + videos/*.mp4.
  outputDir: `${REPORT_DIR}/.raw`,
  use: {
    baseURL: `http://127.0.0.1:${PORT}`,
    locale: "vi-VN",
    trace: "retain-on-failure",
    // Evidence for every scenario, not only failures: final screenshot + full video of each test.
    screenshot: "on",
    video: { mode: "on", size: { width: 1280, height: 800 } },
  },
  projects: [
    {
      name: "chromium",
      // Locally use the installed Google Chrome (no browser download); CI installs Playwright's Chromium.
      use: { ...devices["Desktop Chrome"], viewport: { width: 1280, height: 800 }, channel: process.env.CI ? undefined : "chrome" },
    },
  ],
  webServer: {
    command: `"${python}" serve.py --port ${PORT}`,
    cwd: here,
    url: `http://127.0.0.1:${PORT}/api/health`,
    reuseExistingServer: false,
    timeout: 120_000,
    stdout: "pipe",
    stderr: "pipe",
  },
});
