import RootLayout from "./layout";
import Navbar from "@/components/navbar";
import HomeBase from "@/components/home-page";
import Footer from "@/components/footer";
import React from "react";

const HomePage = () => {
  return (
    <RootLayout>
      <main className="flex flex-col">
      <Navbar gradientBg={false} />
      <HomeBase />
      <Footer />
      </main>
    </RootLayout>
  );
};

export default HomePage;
