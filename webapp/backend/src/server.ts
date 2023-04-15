// Import libraries
import express from "express";
import bodyParser from "body-parser";
import cors from "cors";

// Server
const app: express.Application = express();
const address = "http://localhost:3000";
const port = 3000;

app.use(bodyParser.json());
app.use(cors());

// Endpoint
app.get("/", (req: express.Request, res: express.Response) => {
  res.send("Welcome to NSMQ AI Web backend");
});

app.listen(port, () => {
  console.log(`Starting app on: ${address}`);
});

export default app;
