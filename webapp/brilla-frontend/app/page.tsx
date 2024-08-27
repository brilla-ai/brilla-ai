"use client";

import AnswerBox from "@/components/answer-box";
import Navbar from "@/components/navbar";
import QuizFooter from "@/components/quiz-footer";
import VideoPlayer from "@/components/videoplayer";
import { useVideosStore, Video } from "@/stores";
import React from "react";

export default function Home() {
  const { liveVideo, videoLinks, changeVideoStatus } = useVideosStore();
  const [data, setData] = React.useState(liveVideo ?? "");
  const [scheduledVideos, setScheduledVideos] = React.useState<Video[]>([]);

  const youtubeUrl = React.useMemo(() => data, [data]);

  window.addEventListener("storage", (event) => {
    setData(JSON.parse(event.newValue!).state.liveVideo ?? "");
  });

  React.useEffect(() => {
    const savedVideos = videoLinks;
    if (savedVideos) {
      setScheduledVideos(savedVideos);
    }

    const interval = setInterval(() => {
      checkScheduledVideos();
      console.log("checking scheduled videos");
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const checkScheduledVideos = () => {
    const now = new Date();
    const currentTime = now.getTime();
    console.log("currentTime", currentTime);

    const updatedVideos = videoLinks.filter((video) => {
      console.log("video", video);
      const scheduleDateTime = new Date(
        `${video.schedule_date}T${video.schedule_time}`
      ).getTime();
      console.log("scheduleDateTime", scheduleDateTime);
      if (currentTime >= scheduleDateTime && video.status === "Scheduled") {
        setData(video.link);
        changeVideoStatus(video.id, "Live");
        video.status = "Played"; // Update status to prevent it from showing again
        return false; // Remove the video from the array once played
      }
      return true;
    });

    console.log("updatedVideos", updatedVideos);

    setScheduledVideos(updatedVideos);
    localStorage.setItem("scheduledVideos", JSON.stringify(updatedVideos));
  };

  return (
    <main className="flex flex-col ">
      <Navbar gradientBg={true} />
      <div className="flex flex-col md:flex-row justify-evenly md:items-start items-center md:align-top mt-6 md:mt-8 md:mx-16 md:gap-8 ">
        <div className="md:mt-[24px] flex-1 ">
          <VideoPlayer url={youtubeUrl} />
        </div>
        <div className="min-h-[580px]">
          <AnswerBox
            chatHistory={[
              "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vitae aliquam quam. Nulla facilisi. Integer ac dapibus libero, eu efficitur purus. Nam consectetur venenatis libero, in rutrum ex. Vestibulum nec est tortor",
              "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vitae aliquam quam. Nulla facilisi. Integer ac dapibus libero, eu efficitur purus. Nam consectetur venenatis libero, in rutrum ex. Vestibulum nec est tortor",
              "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vitae aliquam quam. Nulla facilisi. Integer ac dapibus libero, eu efficitur purus. Nam consectetur venenatis libero, in rutrum ex. Vestibulum nec est tortor",
            ]}
          />
        </div>
      </div>
      <QuizFooter />
    </main>
  );
}
