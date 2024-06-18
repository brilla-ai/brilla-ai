import test, { expect } from "@playwright/test";

test("home page footer", async ({ page }) => {
  await page.goto("http://localhost:3000");

  await expect(page.getByText("Open Source Contributors")).toBeVisible();
});

test("link to contributors page", async ({ page }) => {
  await page.goto("http://localhost:3000");

  await page.getByTestId("contributors-link").click();

  await page.goto("https://github.com/brilla-ai/brilla-ai/graphs/contributors");

  await expect(page.getByText("Contributors")).toBeVisible();
});
