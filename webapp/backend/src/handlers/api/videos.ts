import { Request, Response, Router } from "express";
import fs from "fs";
import allVideos from "../../videoData";
import path from "path";

// Initialise router object
const demoVideosRoutes = Router();

// Metadata for all videos
demoVideosRoutes.get("/", (req: Request, res: Response) => {
  res.json(allVideos);
});

// Metadata for a single video
demoVideosRoutes.get("/:id/metadata", (req: Request, res: Response) => {
  const id = parseInt(req.params.id, 10);
  res.json(allVideos[id]);
});

// Endpoint for a single video to stream
demoVideosRoutes.get("/:id", (req: Request, res: Response) => {
    try{
        // Constant range
        const range = req.headers.range;

        // Request parameter id
        const id = req.params.id;

        // Video path
        const videoPath = path.join(__dirname, `../../../assets/${id}.mp4`);

        // Size of the video
        const videoSize = fs.statSync(videoPath).size;

        // Set chunk size
        const chunkSize = 1 * 1e6;

        // Const start and end of video
        const start = range ? Number(range?.replace(/\D/g, "")) : 0;
        const end = Math.min(start + chunkSize, videoSize - 1);

        // Content length
        const contentLength = end - start + 1;

        // Headers for playing video
        const headers = {
            "Content-Range": `bytes ${start} - ${end}/${videoSize}`,
             "Accept-Ranges": "bytes",
            "Content-Length": contentLength,
            "Content-Type": "video/mp4",
         };

        res.writeHead(206, headers);

        // Create video stream and pipe it to the response
        const stream = fs.createReadStream(videoPath, { start, end });
        stream.pipe(res);
    } catch (err) {
        console.log(err);
    }
});

export default demoVideosRoutes;
