// Import libraries
import express, { Application, Request, Response } from "express";
import json from "body-parser";
import cors from "cors";

// Server
const app: Application = express();
const address = "http://localhost:5000";
const port = 5000;

app.use(json.json());
app.use(cors());

// Endpoint
app.get("/", (req: Request, res: Response) => {
  res.send("Welcome to NSMQ AI Web backend");
});

app.listen(port, () => {
  console.log(`Starting app on: ${address}`);
});

export default app;
