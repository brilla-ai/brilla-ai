"use client";
import React, { FC } from "react";
import ReactPlayer from "react-player/youtube";

interface VideoPlayerProps {
  url: string;
}
const VideoPlayer: FC<VideoPlayerProps> = ({ url }) => {
  return (
    <div className="flex flex-col md:flex-row md:max-w-[45vw] h-[28vh]">
      <ReactPlayer
        url={url}
        width={"100%"}
        height={"65vh"}
        controls={true}
        light={false}
        pip={false}
        style={{ flex: 1 }}
        muted={false}
        volume={0.5}
        playing={true}
      />
      <source src={url} type="video/mp4" />
    </div>
  );
};

export default VideoPlayer;
