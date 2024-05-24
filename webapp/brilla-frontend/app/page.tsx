import Footer from "@/components/footer";
import Navbar from "@/components/navbar";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col">
      <Navbar gradientBg={false} />
      <div>Live is meant to be easy, bruh!</div>

      <Footer />
    </main>
  );
}
