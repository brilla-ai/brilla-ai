
import Navbar from "@/components/navbar";
import Sidebar from "@/components/sidebar";
import RootLayout from "../layout";
import AdminUser from "@/components/admin-user-table";

const AdminUserPage = () => {
    return (
      <RootLayout>
        <Navbar gradientBg={false} />
        <div className="flex h-full">
          <Sidebar />
          <div className="p-8 space-y-8 w-full">
            <h1 className="text-3xl font-bold">Users</h1>
           <AdminUser/>
          </div>
        </div>
      </RootLayout>
    );
  };
  
  export default AdminUserPage;