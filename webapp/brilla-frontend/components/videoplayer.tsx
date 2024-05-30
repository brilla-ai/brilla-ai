"use client";
import React, { FC, useState, useEffect } from "react";
import dynamic from "next/dynamic";
// import Spinner from "./ui/spinner";
import Shimmer from "./ui/shimmer";

interface VideoPlayerProps {
  url: string;
}

const ReactPlayer = dynamic(() => import("react-player/youtube"), {
  ssr: false,
});

const VideoPlayer: FC<VideoPlayerProps> = ({ url }) => {
  const [loading, setLoading] = useState(true);

  const handleReady = () => {
    setLoading(false);
  };

  return (
    <div className="flex flex-col md:flex-row md:max-w-[45vw] h-[28vh] relative">
      {/* {loading && <Spinner />} */}
      {loading && <Shimmer />}
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
        onReady={handleReady}
      />
    </div>
  );
};

export default VideoPlayer;
