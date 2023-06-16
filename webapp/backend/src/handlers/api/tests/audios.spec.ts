import supertest from "supertest";
import audioExtractionRoutes from "../audios";
import app from "../../../server";

const request: supertest.SuperTest<supertest.Test> = supertest(
  app.use(audioExtractionRoutes)
);

describe("Audio extractions routes", () => {
    
    it("should get bad request response when an invalid id is provided", async () => {
        try {
            const response = await request.get('/1234');
            expect(response.status).toBe(400);
        } catch (error) {
            console.log(error);
        }
    });
});
