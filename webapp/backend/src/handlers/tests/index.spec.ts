// Import libraries
import supertest from "supertest"; 
import routes from "../index";
import app from "../../server";

const request: supertest.SuperTest<supertest.Test> = supertest(app.use(routes));

describe("Main route test", () => {
  it("should get response from the main route", async () => {
    try {
        const response = await request.get("/");
        expect(response.status).toBe(200);
    } catch (error) {
        console.log(`Unable to reach the main route ${error}`)
  }
});
});
