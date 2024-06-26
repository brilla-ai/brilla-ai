import RootLayout from "../layout";
import Sidebar from "@/components/sidebar";
import Navbar from "@/components/navbar";

const SettingsPage = () => {
  return (
    <RootLayout>
      <Navbar gradientBg={false} />
      <div className="flex h-full">
        <Sidebar />
        <div className="p-8 space-y-8">
          <h1 className="text-3xl font-bold">Settings</h1>
        </div>
      </div>
    </RootLayout>
  );
};

export default SettingsPage;
