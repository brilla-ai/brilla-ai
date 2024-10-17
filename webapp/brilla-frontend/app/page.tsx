"use client";

import AnswerBox from "@/components/answer-box";
import Navbar from "@/components/navbar";
import QuizFooter from "@/components/quiz-footer";
import VideoPlayer from "@/components/videoplayer";
import { useVideosStore, Video } from "@/stores";
import { ENV_VARS } from "@/utils/constants";
import React from "react";
import { useWebSocket } from "react-use-websocket/dist/lib/use-websocket";

export default function Home() {
  const { liveVideo, videoLinks, changeVideoStatus } = useVideosStore();
  const [data, setData] = React.useState(liveVideo ?? "");
  const [scheduledVideos, setScheduledVideos] = React.useState<Video[]>([]);
  const [videoUrl, setVideoUrl] = React.useState("");

  const youtubeUrl = React.useMemo(() => data, [data]);

  const { lastMessage } = useWebSocket(ENV_VARS.WS_BASE_URL || "");

  React.useEffect(() => {
    const savedVideos = videoLinks;
    if (savedVideos) {
      setScheduledVideos(savedVideos);
    }

    const interval = setInterval(() => {
      // checkScheduledVideos();
      console.log("checking scheduled videos");
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  React.useEffect(() => {
    if (lastMessage) {
      const message = JSON.parse(lastMessage.data);

      if (message.video_url) {
        console.log("message.video_url", message.video_url);
        setVideoUrl(message.video_url);
      }
    }
  }, [lastMessage]);

  return (
    <main className="flex flex-col ">
      <Navbar gradientBg={true} />
      <div className="flex flex-col md:flex-row justify-evenly md:items-start items-center md:align-top mt-6 md:mt-8 md:mx-16 md:gap-8 ">
        <div className="md:mt-[24px] flex-1 ">
          <VideoPlayer url={videoUrl} />
        </div>
        <div className="min-h-[580px]">
          <AnswerBox />
        </div>
      </div>
      <QuizFooter />
    </main>
  );
}
