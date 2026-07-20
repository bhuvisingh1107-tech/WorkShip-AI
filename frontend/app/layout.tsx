import type { Metadata } from "next";
import { AppShell } from "@/components/app-shell";
import "./globals.css";
import { AuthProvider } from "@/context/AuthProvider";
import AuthRedirectHandler from "./AuthRedirectHandler";

export const metadata: Metadata = {
  title: { default: "WorkShip AI | Operations Intelligence", template: "%s | WorkShip AI" },
  description: "Enterprise operations intelligence for knowledge, incidents, and teams.",
  icons: { icon: "/logo.png", apple: "/logo.png" },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full">
        <AuthProvider>
          <AuthRedirectHandler />
          <AppShell>{children}</AppShell>
        </AuthProvider>
      </body>
    </html>
  );
}