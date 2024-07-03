import Footer from "@/components/footer";
import LiveVideoUrlForm from "@/components/live-video-url-form";
import Navbar from "@/components/navbar";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col">
      <Navbar gradientBg={false} />
      <div>Live is meant to be easy, bruh!</div>

      <div className="self-center border border-[#CBD5E1] rounded-lg p-6">
        <LiveVideoUrlForm />
      </div>

      <Footer />
    </main>
  );
}
