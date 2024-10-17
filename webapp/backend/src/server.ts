// Import libraries
import { config } from "dotenv";
import express, { Application } from "express";
import json from "body-parser";
import cors from "cors";
import { connectToDatabase } from "./services/database.service";
import routes from "./handlers/index";

// Server
config();
const app: Application = express();
const port = String(process.env.BACKEND_PORT);
const address = "http://localhost:".concat(port);

app.use(json.json());
app.use(cors());

// Main route
app.use("/", routes)

app.listen(port, () => {
  console.log(`Starting backend app on: ${address}`);
  connectToDatabase();
});

export default app;
