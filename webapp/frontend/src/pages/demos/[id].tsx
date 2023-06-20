import Layout from "@/components/layout/Layout";
import { GetServerSidePropsContext } from "next";

export default function DemoPage({
  id,
  backendURLEndpoint,
}: {
  id: number;
  backendURLEndpoint: string;
}) {
  return (
    <Layout>
      <main className="flex flex-col items-center justify-between min-h-screen px-24 py-8">
        <div className="grid grid-cols-2 gap-2 mt-8">
          <video
            className="w-full h-full"
            controls
            width={640}
            height={480}
            src={`${backendURLEndpoint}/video${id}`}
            // The src will be updated to the actual video url
          />
          {/* TODO: ADD  CHAT SECTION */}
          <div className="h-full bg-red-400">chat goes here</div>
        </div>
      </main>
    </Layout>
  );
}

export async function getServerSideProps(context: GetServerSidePropsContext) {
  const { id } = context.query;
  const backendURLEndpoint = process.env.BACKEND_VIDEOS_URL;
  return {
    props: { id, backendURLEndpoint },
  };
}
