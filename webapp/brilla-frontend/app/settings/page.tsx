import RootLayout from "../layout";
import Sidebar from "@/components/sidebar";
import Navbar from "@/components/navbar";
import LiveVideoUrlForm from "@/components/live-video-url-form";
import LiveVideoLinks from "@/components/live-video-links";

const SettingsPage = () => {
  return (
    <RootLayout>
      <Navbar gradientBg={false} />
      <div className="flex h-full">
        <Sidebar />
        <div className="p-8 space-y-8 w-full">
          <h1 className="text-3xl font-bold">Settings</h1>
          <div className="flex gap-12 flex-col md:flex-row">
            <div className="self-center border border-[#CBD5E1] rounded-lg p-6 max-w-[435px]">
              <LiveVideoUrlForm />
            </div>
            <LiveVideoLinks />
          </div>
        </div>
      </div>
    </RootLayout>
  );
};

export default SettingsPage;
