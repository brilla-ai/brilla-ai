import {Request, Response, Router} from "express";
import demoVideoRoutes from "./api/videos";
import audioExtractionRoutes from "./api/audios";

// Router object
const routes = Router();

// Main route
routes.get("/", (req: Request, res: Response) => {
    res.send("Welcome to NSMQ AI Web backend")
});

// Demo video route
routes.use("/demo-videos", demoVideoRoutes);

// Audio Extraction route
routes.use("/extract-audio", audioExtractionRoutes);

export default routes;
