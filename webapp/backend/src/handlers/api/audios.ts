import { Request, Response, Router } from "express";
import extractAudio from "ffmpeg-extract-audio";
import allDemoVideos from "../../videoData";

// Initialise router object
const audioExtractionRoutes = Router();

audioExtractionRoutes.get("/:id", async (req: Request, res: Response) => {
    const id = req.params.id;

    // Check if id is a non-empty string
    if (!id) {
        return res.status(400).json({ error: "Invalid id parameter" });
    }

    // Check for valid id
    if (allDemoVideos.filter((videoData) => videoData.id == id).length == 0) {
        return res.status(400).json({ error: "Invalid id parameter" });
    }

    console.log(`Extracting audio from ${id}.mp4`);

    const videoPath = `./assets/video/${id}.mp4`;
    const audioPath = `./assets/audio/audio_${id}.mp3`;
    
    extractAudioFromVideo(videoPath, audioPath);

    const msg = "Audio extracted successfully!";

    console.log(msg);
    return res.send(msg);
  }
);

export const extractAudioFromVideo = async (videoPath: string, audioPath: string) => {
    await extractAudio({
      input: videoPath,
      output: audioPath,
      log: (msg) => console.log(msg),
    });
}

export default audioExtractionRoutes;
