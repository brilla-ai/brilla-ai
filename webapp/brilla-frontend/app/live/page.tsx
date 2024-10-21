"use client";

import AnswerBox from "@/components/answer-box";
import Navbar from "@/components/navbar";
import QuizFooter from "@/components/quiz-footer";
import VideoPlayer from "@/components/videoplayer";
import { ENV_VARS } from "@/utils/constants";
import React from "react";
import useWebSocket from "react-use-websocket";

export default function Home() {
  // const { liveVideo, videoLinks, changeVideoStatus } = useVideosStore();
  // const [data, setData] = React.useState(liveVideo ?? "");
  // const [scheduledVideos, setScheduledVideos] = React.useState<Video[]>([]);
  const [videoUrl, setVideoUrl] = React.useState("");

  const { lastMessage, sendJsonMessage, lastJsonMessage } = useWebSocket(
    ENV_VARS.WS_BASE_URL || ""
  );

  React.useEffect(() => {
    if (lastMessage) {
      const message = JSON.parse(lastMessage.data);

      if (message.target === "video_started") {
        console.log("message.video_link", message.arguments.data.video_link);
        const video = message.arguments.data.video_link;
        setVideoUrl(video);
      } else if (message.target === "video_ended") {
        setVideoUrl("");
      }
      if (message.connection_id) {
        sendJsonMessage({
          type: 1,
          target: "add_to_group",
          arguments: [message.connection_id, "live_video"],
        });
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
            <AnswerBox lastMessage={lastMessage} />
          </div>
        </div>
      <QuizFooter />
    </main>
  );
}
