import {Request, Response, Router} from "express";

// Router object
const routes = Router();

routes.get("/", (req: Request, res: Response) => {
    res.send("Welcome to NSMQ AI Web backend")
});

export default routes;
