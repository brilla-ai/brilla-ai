import test, { expect } from "@playwright/test";

test("quiz page footer", async ({ page }) => {
  await page.goto("http://localhost:3000");

  await expect(page.getByText("Powered by Brilla AI")).toBeVisible();
});
