import type { Metadata } from "next";
import translations from "../public/i18n/en.json";
import "../styles/globals.css";
import QueryProvider from "@/components/query-client";


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
    <QueryProvider>
      <html lang="en">
        <body>{children}</body>
      </html>
    </QueryProvider>
  );
}
