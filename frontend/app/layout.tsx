import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/context/AuthProvider";
import { ConditionalShell } from "@/components/app-shell";

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
    <html lang="en" className="h-full antialiased" suppressHydrationWarning>
      <body className="min-h-full" suppressHydrationWarning>
        <AuthProvider>
          <ConditionalShell>{children}</ConditionalShell>
        </AuthProvider>
      </body>
    </html>
  );
}