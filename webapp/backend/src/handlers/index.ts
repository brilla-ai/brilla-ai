import {Request, Response, Router} from "express";
import demoVideos from "./api/videos";

// Router object
const routes = Router();

routes.get("/", (req: Request, res: Response) => {
    res.send("Welcome to NSMQ AI Web backend")
});

// Demo video route
routes.use("/videos", demoVideos);

export default routes;
