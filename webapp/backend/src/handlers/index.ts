import {Request, Response, Router} from "express";
import demoVideoRoutes from "./api/videos";

// Router object
const routes = Router();

// Main route
routes.get("/", (req: Request, res: Response) => {
    res.send("Welcome to NSMQ AI Web backend")
});

// Demo video route
routes.use("/demo-videos", demoVideoRoutes);

export default routes;
