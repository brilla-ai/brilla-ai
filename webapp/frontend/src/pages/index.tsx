import VideoCard from "../components/homepage/VideoCard";
import Layout from "../components/layout/Layout";

export default function Home() {
  return (
    <Layout>
      <main className="flex min-h-screen flex-col items-center justify-between px-24 py-8">
        <div>
          <h5 className="tracking-tight text-center text-[30px]">
            Demo Videos
          </h5>
          <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-8 w-full">
            <VideoCard id={1} image="/thumbnail.png" />
            <VideoCard id={2} image="/thumbnail.png" />
            <VideoCard id={3} image="/thumbnail.png" />
          </div>
        </div>
      </main>
    </Layout>
  );
}
