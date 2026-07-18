import { Menu, Moon } from "lucide-react";
import { Logo } from "@/components/logo";

type NavbarProps = {
  onMenuClick: () => void;
};

export function Navbar({ onMenuClick }: NavbarProps) {
  return (
    <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-4 sm:px-6">
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
        <p className="text-sm font-semibold text-slate-900">WorkShip AI</p>
      </div>
      <div className="flex items-center gap-3">
        <button
          aria-label="Theme toggle placeholder"
          className="rounded-md p-2 text-slate-600 hover:bg-slate-100"
          type="button"
        >
          <Moon aria-hidden="true" className="size-4" />
        </button>
        <div
          aria-label="User avatar placeholder"
          className="flex size-8 items-center justify-center rounded-full bg-slate-200 text-xs font-semibold text-slate-600"
          role="img"
        >
          U
        </div>
      </div>
    </header>
  );
}
