"use client";

import {
  Bot,
  BookOpenText,
  ChartNoAxesCombined,
  LayoutDashboard,
  Settings,
  ShieldAlert,
  X,
} from "lucide-react";
import { usePathname } from "next/navigation";
import { Logo } from "@/components/logo";
import { NavItem } from "@/components/nav-item";

const navigation = [
  { href: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { href: "/copilot", icon: Bot, label: "AI Copilot" },
  { href: "/incidents", icon: ShieldAlert, label: "Incident Intelligence" },
  { href: "/knowledge", icon: BookOpenText, label: "Enterprise Knowledge" },
  { href: "/company-sales", icon: ChartNoAxesCombined, label: "Company Sales" },
  { href: "/settings", icon: Settings, label: "Settings" },
];

type SidebarProps = {
  isOpen: boolean;
  onClose: () => void;
};

export function Sidebar({ isOpen, onClose }: SidebarProps) {
  const pathname = usePathname();

  return (
    <>
      {isOpen && (
        <button
          aria-label="Close navigation"
          className="fixed inset-0 z-30 bg-slate-950/35 lg:hidden"
          onClick={onClose}
          type="button"
        />
      )}
      <aside
        className={`fixed inset-y-0 left-0 z-40 flex w-72 flex-col border-r border-[#E9E5FF] bg-[#F5F3FF] px-4 py-5 ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        } lg:translate-x-0`}
      >
        <div className="flex items-center justify-between px-2">
          <Logo />
          <button
            aria-label="Close navigation"
            className="rounded-md p-2 text-slate-500 hover:bg-[#EDE9FE] lg:hidden"
            onClick={onClose}
            type="button"
          >
            <X aria-hidden="true" className="size-5" />
          </button>
        </div>
        <p className="mt-10 px-3 text-[10px] font-semibold uppercase tracking-[0.16em] text-[#8B85C8]">Workspace</p>
        <nav aria-label="Primary navigation" className="mt-3 space-y-1">
          {navigation.map((item) => (
            <NavItem
              {...item}
              isActive={
                pathname === item.href ||
                (item.href === "/dashboard" && pathname === "/")
              }
              key={item.href}
              onNavigate={onClose}
            />
          ))}
        </nav>
      </aside>
    </>
  );
}
