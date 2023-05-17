import Layout from "@/components/layout/Layout";

import ReactPlayer from "react-player/lazy";

export default function DemoPage() {
  return (
    <Layout>
      <main className="flex min-h-screen flex-col items-center justify-between px-24 py-8">
        <div className="grid grid-cols-2 gap-2 mt-8">
          <ReactPlayer
            url="https://youtu.be/P8vtPmJE1FY"
            // Update to stream url once #18 is merged
            width="600px"
            height="400px"
          />
          {/* TODO: ADD  CHAT SECTION */}
          <div className="h-full bg-red-400">chat goes here</div>
        </div>
      </main>
    </Layout>
  );
}
