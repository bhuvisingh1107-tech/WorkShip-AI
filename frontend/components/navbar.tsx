'use client';

import { useEffect, useState } from "react";
import { Menu, Moon, Sun, LogOut } from "lucide-react";
import { Logo } from "@/components/logo";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthProvider";

type NavbarProps = {
  onMenuClick: () => void;
};

export function Navbar({ onMenuClick }: NavbarProps) {
  const router = useRouter();
  const { user, logout } = useAuth();
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      const savedTheme = localStorage.getItem("workship-theme") === "dark";
      document.documentElement.classList.toggle("dark", savedTheme);
      setIsDark(savedTheme);
    });
    return () => window.clearTimeout(timer);
  }, []);

  function toggleTheme() {
    const nextTheme = !isDark;
    document.documentElement.classList.toggle("dark", nextTheme);
    localStorage.setItem("workspace-theme", nextTheme ? "dark" : "light");
    setIsDark(nextTheme);
  }

  const handleLogout = async () => {
    logout();
    // TODO: we need to handle async logout
    }

  return (
    <header className="flex h-16 items-center justify-between border-b border-[#E9E5FF] bg-white/90 px-4 backdrop-blur dark:border-indigo-800 dark:bg-slate-900/90 sm:px-6">
      <div className="flex items-center gap-3">
        <button
          aria-label="Open navigation"
          className="rounded-md p-2 text-slate-600 hover:bg-slate-100 lg:hidden"
          onClick={onMenuClick}
          type="button"
        >
          <Menu aria-hidden="true" className="size-5" />
        </button>
        <Logo compact />
        <p className="text-sm font-semibold text-[#312E81]">Operations workspace</p>
      </div>
      <div className="flex items-center gap-3">
        <button
          aria-label={isDark ? "Switch to light mode" : "Switch to dark mode"}
          className="rounded-md p-2 text-slate-600 hover:bg-slate-100 dark:text-indigo-200 dark:hover:bg-slate-800"
          onClick={toggleTheme}
          type="button"
        >
          {isDark ? <Sun aria-hidden="true" className="size-4" /> : <Moon aria-hidden="true" className="size-4" />}
        </button>
        {user ? (
          <>
            <div
              onClick={() => router.push('/settings')}
              className="cursor-pointer flex items-center gap-2"
            >
              <div
                className="flex h-9 w-9 items-center justify-center rounded-full bg-[#FBCFE8] text-xs font-semibold text-[#7C3D66]"
              >
                {(() => {
                  if (user.user_metadata?.full_name) {
                    return user.user_metadata.full_name
                      .split(' ')
                      .map((part: string) => part[0])
                      .join('')
                      .toUpperCase();
                  }
                  if (user.email) {
                    return user.email.split('@')[0].toUpperCase();
                  }
                  return 'U';
                })()}
              </div>
              <div>
                <p className="text-sm font-medium text-[#312E81]">{user.user_metadata?.full_name ?? user.email}</p>
                <p className="text-xs text-slate-500">{user.role ?? 'User'}</p>
              </div>
            </div>
            <button
              onClick={async () => {
                await logout();
                router.push('/login');
              }}
              className="rounded-md p-2 text-slate-500 hover:bg-slate-100"
              title="Log out"
            >
              <LogOut className="size-4" />
            </button>
          </>
        ) : (
          <div
            aria-label="User avatar placeholder"
            className="flex size-8 items-center justify-center rounded-full bg-[#FBCFE8] text-xs font-semibold text-[#7C3D66]"
            role="img"
          >
            U
          </div>
        )}
      </div>
    </header>
  );
}