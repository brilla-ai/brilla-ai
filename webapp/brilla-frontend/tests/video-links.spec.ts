import test, { expect } from "@playwright/test";

test.describe("Live video links", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("http://localhost:3000/settings");
  });

  test("Stop live video", async ({ page }) => {
    await expect(page.getByText("Live Video Links")).toBeVisible();

    await page.getByTestId("action-trigger").first().click();

    await page.getByTestId("dropdown-menu-item-0").click();

    await expect(page.getByText("Stop live video")).toBeVisible();
  });

  test("Delete live video", async ({ page }) => {
    await expect(page.getByText("Live Video Links")).toBeVisible();

    await page.getByTestId("action-trigger").first().click();

    await page.getByTestId("dropdown-menu-item-1").click();

    await expect(page.getByText("Delete live video")).toBeVisible();
  });
});
