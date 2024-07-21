"use client";
import React, { FC , useState, useEffect} from "react";
import dynamic from 'next/dynamic';
import ShimmerPlaceholder from "./shimmer";

const ReactPlayer = dynamic(() => import('react-player'), { ssr: false });
interface VideoPlayerProps {
  url: string;
}
const VideoPlayer = ({ url }: VideoPlayerProps) => {
  const [isReady, setIsReady] = useState(true);
  const [error, setError] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);

  const handlePlay = () => {
    setIsPlaying(true);
  };

  const handlePause = () => {
    setIsPlaying(false);
  };

  const handleReady = () => {
    setIsReady(false);
  };

  const handleError = () => {
    setError(true);
  };


  return (
  
    <div className="relative flex flex-col max-w-full h-[47vh] rounded-md overflow-hidden shadow-lg md:shadow-gray-500 shadow-gray-200">
    <div
      className="flex flex-col md:flex-row max-w-full h-[47vh] relative  overflow-hidden"
      style={
        !isReady && !isPlaying
          ? {
              borderImage: 'linear-gradient(45deg, blue, red) 1',
              animation: isPlaying ? 'none' : 'gradient-border 3s ease infinite',
              borderWidth: '3px',
              borderStyle: 'solid',
            }
          : {}
      }
    >
      {error ? (
        <ShimmerPlaceholder />
      ) : (
        <>
          {isReady && <ShimmerPlaceholder/>}
          <ReactPlayer
            url={url}
            width="100%"
            height="100%"
            controls={true}
            light={false}
            pip={false}
            style={{ flex: 1}} 
            playing={isPlaying}
            muted={false}
            volume={0.5}
            onPlay={handlePlay}
            onPause={handlePause}
            onReady={handleReady}
            onError={handleError}
          />
        </>
      )}
    </div>
    </div>
  );
};

export default VideoPlayer;
