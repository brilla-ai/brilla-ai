import { config } from 'dotenv';
import { MongoClient } from "mongodb";

config();

export async function connectToDatabase() {
  let mongoClient: MongoClient;

  try {
    mongoClient = new MongoClient(String(process.env.DB_URI));
    console.log("Connecting to MongoDB Atlas cluster...");
    await mongoClient.connect();
    console.log("Successfully connected to MongoDB Atlas!");

    return mongoClient;
  } catch (error) {
    console.error("Connection to MongoDB Atlas failed!", error);
    process.exit();
  }
}
