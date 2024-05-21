import Footer from "@/components/footer";
import Navbar from "@/components/navbar";
import VideoPlayer from "@/components/videoplayer";

export default function Home() {
  const youtubeUrl =
    "https://www.youtube.com/watch?v=lKMm0FDxj9s&pp=ygUJbnNtcSAyMDIz";
  return (
    <main className="flex min-h-screen flex-col">
      <Navbar gradientBg={false} />
      {/* <div>Live is meant to be easy, bruh!</div> */}
      <div className="mx-5 mt-8 md:m-10">
        <VideoPlayer url={youtubeUrl} />
      </div>
      <Footer />
    </main>
  );
}
