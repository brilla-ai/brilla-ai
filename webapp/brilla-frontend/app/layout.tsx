import type { Metadata } from "next";
import translations from "../public/i18n/en.json";
import "../styles/globals.css";


export const metadata: Metadata = {
  title : translations["brilla-ai"],
  description: translations["heroText"]
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body >{children}</body>
    </html>
  );
}
