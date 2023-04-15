// Import libraries
import supertest from "supertest"; 
import app from "../server";

const request: supertest.SuperTest<supertest.Test> = supertest(app);

describe("Test server", () => {
  it("should get response from server", async () => {
    const response = await request.get("/");
    expect(response.statusCode).toBe(200);
  });
});
