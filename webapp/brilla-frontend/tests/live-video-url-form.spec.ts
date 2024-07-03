import test, { expect } from "@playwright/test";

test("live video url form", async ({ page }) => {
  await page.goto("http://localhost:3000/settings");

  await expect(page.getByText("Settings")).toBeVisible();

  await page
    .getByLabel("Video link")
    .fill("https://www.youtube.com/watch?v=1234");
  await page.getByLabel("Tags").fill("Semi Finals");

  await page.getByTestId("switch").click();
  
  await page.getByLabel("Select date").fill("2024-09-02");
  await page.getByLabel("Select time").fill("13:15");

  await page.getByText("Save changes").click();
});
