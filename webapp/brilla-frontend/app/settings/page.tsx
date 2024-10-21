"use client";

import RootLayout from "../layout";
import Sidebar from "@/components/sidebar";
import Navbar from "@/components/navbar";
import LiveVideoUrlForm from "@/components/live-video-url-form";
import AIOperations from "@/components/ai-operations";
import LiveVideoLinks from "@/components/live-video-links";
import { ENV_VARS } from "@/utils/constants";
import React from "react";
import useWebSocket from "react-use-websocket";

const SettingsPage = () => {
  const { lastMessage, sendJsonMessage, lastJsonMessage } = useWebSocket(
    ENV_VARS.WS_BASE_URL || ""
  );

  React.useEffect(() => {
    if (lastMessage) {
      const message = JSON.parse(lastMessage.data);

      if (message.video_link) {
        console.log("message.video_link", message.video_link);
        // setVideoUrl(message.video_link);
      }
      if (message.connection_id) {
        sendJsonMessage({
          type: 1,
          target: "add_to_group",
          arguments: [message.connection_id, "ai_operations"],
        });
        sendJsonMessage({
          type: 1,
          target: "add_to_group",
          arguments: [message.connection_id, "admin_videos"],
        });
      }
    }
  }, [lastMessage]);

  return (
    <main>
      <Navbar gradientBg={false} />
      <div className="flex h-screen w-full">
        <Sidebar />
        <div className="p-8 h-full space-y-8 w-full overflow-auto">
          <h1 className="text-3xl font-bold">Settings</h1>
          <AIOperations lastJsonMessage={lastJsonMessage} />
          <div className="flex gap-12 flex-col md:flex-row">
            <div className="self-center border border-[#CBD5E1] rounded-lg p-6 max-w-[435px]">
              <LiveVideoUrlForm />
            </div>
            <LiveVideoLinks lastJsonMessage={lastJsonMessage} />
          </div>
        </div>
      </div>
    </main>
  );
};

export default SettingsPage;
