// Import libraries
import { config } from "dotenv";
import express, { Application, Request, Response } from "express";
import json from "body-parser";
import cors from "cors";
import { connectToDatabase } from "./services/database.service";

// Server
config();
const app: Application = express();
const port = String(process.env.BACKEND_PORT);
const address = "http://localhost:".concat(port);

app.use(json.json());
app.use(cors());

// Endpoint
app.get("/", (req: Request, res: Response) => {
  res.send("Welcome to NSMQ AI Web backend");
});

app.listen(port, () => {
  console.log(`Starting backend app on: ${address}`);
  connectToDatabase();
});

export default app;
