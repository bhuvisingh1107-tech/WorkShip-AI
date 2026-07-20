"use client";

import { useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthProvider";
import { Navbar } from "@/components/navbar";
import { Sidebar } from "@/components/sidebar";

const PUBLIC_PATHS = ["/login", "/signup"];

/* ── Full-screen loading skeleton shown while auth resolves ── */
function AuthLoadingSkeleton() {
  return (
    <div className="flex min-h-screen bg-[#FAFAF9]">
      {/* Sidebar skeleton */}
      <div className="hidden lg:flex w-72 flex-col border-r border-[#E9E5FF] bg-[#F5F3FF] px-4 py-5">
        <div className="skeleton h-8 w-32 mb-10" />
        <div className="skeleton h-4 w-16 mb-4" />
        <div className="space-y-2">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="skeleton h-10 w-full" />
          ))}
        </div>
      </div>
      {/* Main content skeleton */}
      <div className="flex-1">
        <div className="h-16 border-b border-[#E9E5FF] bg-white/90 flex items-center px-6">
          <div className="skeleton h-6 w-48" />
          <div className="ml-auto skeleton h-9 w-9 rounded-full" />
        </div>
        <div className="p-8 space-y-6">
          <div className="skeleton h-28 w-full rounded-2xl" />
          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="skeleton h-24 w-full rounded-xl" />
            ))}
          </div>
          <div className="grid gap-5 lg:grid-cols-2">
            <div className="skeleton h-48 w-full rounded-xl" />
            <div className="skeleton h-48 w-full rounded-xl" />
          </div>
        </div>
      </div>
    </div>
  );
}

/* ── Conditional shell: bare layout for auth pages, full AppShell for app ── */
export function ConditionalShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { user, loading } = useAuth();
  const router = useRouter();
  const isPublicPage = PUBLIC_PATHS.some((p) => pathname.startsWith(p));

  // On public pages (login/signup): render children directly, no sidebar
  if (isPublicPage) {
    return <>{children}</>;
  }

  // While auth is loading, show skeleton
  if (loading) {
    return <AuthLoadingSkeleton />;
  }

  // Not logged in on a protected page: redirect to login
  if (!user) {
    // We can't call router.push during render, but the AuthRedirect logic
    // in RequireAuth handles this. For the shell, just render nothing.
    return <AuthLoadingSkeleton />;
  }

  // Authenticated on a protected page: render full AppShell
  return <AppShell>{children}</AppShell>;
}

/* ── The original AppShell (sidebar + navbar + main) ── */
export function AppShell({ children }: { children: React.ReactNode }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#FAFAF9] dark:bg-slate-950">
      <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />
      <div className="min-h-screen lg:pl-72">
        <Navbar onMenuClick={() => setIsSidebarOpen(true)} />
        <main>{children}</main>
      </div>
    </div>
  );
}
