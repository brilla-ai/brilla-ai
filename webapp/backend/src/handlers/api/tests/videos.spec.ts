// Import libraries
import supertest from "supertest"; 
import demoVideosRoutes from "../videos";
import allDemoVideos from "../../../videoData";
import app from "../../../server";

const request: supertest.SuperTest<supertest.Test> = supertest(app.use(demoVideosRoutes));

const id = allDemoVideos[0].id;

describe("Demo video routes", () => {
  it("should get response from demo videos routes", async () => {
    try {
        const response = await request.get("/");
        expect(response.status).toBe(200);
    } catch(error){
        console.log(error);
    }
  });

  it("should get video from demo videos routes with id", async () => {
    try {
        const response = await request.get(`/${id}`);
        expect(response.status).toBe(206);
    } catch(error){
        console.log(error);
  }
});

  it("should get response from demo videos metadata with id", async () => {
    try {
        const response = await request.get(`/${id})/metadata`);
        expect(response.status).toBe(400);
    } catch(error){
        console.log(error);
    }
});
});
