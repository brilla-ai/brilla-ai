import RootLayout from "../layout";
import Sidebar from "@/components/sidebar";
import Navbar from "@/components/navbar";
import LiveVideoUrlForm from "@/components/live-video-url-form";
import AIOperations from "@/components/ai-operations";

const SettingsPage = () => {
  return (
    <RootLayout>
      <Navbar gradientBg={false} />
      <div className="flex h-full">
        <Sidebar />
        <div className="p-8 space-y-8">
          <h1 className="text-3xl font-bold">Settings</h1>
            <AIOperations />
          <div className="self-center border border-[#CBD5E1] rounded-lg p-6 max-w-[435px]">
            <LiveVideoUrlForm />
          </div>
        </div>
      </div>
    </RootLayout>
  );
};

export default SettingsPage;
