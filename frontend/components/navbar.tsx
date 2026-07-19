"use client";

import { useEffect, useState } from "react";
import { Menu, Moon, Sun } from "lucide-react";
import { Logo } from "@/components/logo";

type NavbarProps = {
  onMenuClick: () => void;
};

export function Navbar({ onMenuClick }: NavbarProps) {
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
    localStorage.setItem("workship-theme", nextTheme ? "dark" : "light");
    setIsDark(nextTheme);
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
        <div
          aria-label="User avatar placeholder"
          className="flex size-8 items-center justify-center rounded-full bg-[#FBCFE8] text-xs font-semibold text-[#7C3D66]"
          role="img"
        >
          U
        </div>
      </div>
    </header>
  );
}
