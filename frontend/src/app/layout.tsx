import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Parliament Watch Nepal | पार्लियामेन्ट वाच नेपाल",
  description: "Independent, source-backed parliamentary transparency for Nepal.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ne">
      <body>{children}</body>
    </html>
  );
}
