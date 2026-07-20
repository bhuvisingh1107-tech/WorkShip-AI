"use client";

import {
  Bot,
  BookOpenText,
  ChartNoAxesCombined,
  LayoutDashboard,
  LogOut,
  Settings,
  ShieldAlert,
  X,
} from "lucide-react";
import { usePathname, useRouter } from "next/navigation";
import { Logo } from "@/components/logo";
import { NavItem } from "@/components/nav-item";
import { useAuth, UserRole } from "@/context/AuthProvider";

type NavEntry = {
  href: string;
  icon: typeof LayoutDashboard;
  label: string;
  allowedRoles: UserRole[];
};

const navigation: NavEntry[] = [
  { href: "/dashboard", icon: LayoutDashboard, label: "Dashboard", allowedRoles: ['Employee', 'Manager', 'CEO'] },
  { href: "/copilot", icon: Bot, label: "AI Copilot", allowedRoles: ['Employee', 'Manager', 'CEO'] },
  { href: "/incidents", icon: ShieldAlert, label: "Incident Intelligence", allowedRoles: ['Employee', 'Manager', 'CEO'] },
  { href: "/knowledge", icon: BookOpenText, label: "Enterprise Knowledge", allowedRoles: ['Employee', 'Manager', 'CEO'] },
  { href: "/company-sales", icon: ChartNoAxesCombined, label: "Company Sales", allowedRoles: ['Manager', 'CEO'] },
  { href: "/settings", icon: Settings, label: "Settings", allowedRoles: ['Employee', 'Manager', 'CEO'] },
];

type SidebarProps = {
  isOpen: boolean;
  onClose: () => void;
};

export function Sidebar({ isOpen, onClose }: SidebarProps) {
  const pathname = usePathname();
  const router = useRouter();
  const { user, role, logout } = useAuth();

  // Filter navigation based on role
  const visibleNav = navigation.filter(
    (item) => role && item.allowedRoles.includes(role)
  );

  const handleLogout = async () => {
    try {
      await logout();
      router.push('/login');
    } catch (err) {
      console.error('Logout failed', err);
    }
  };

  // Get initials from user
  const initials = (() => {
    if (user?.user_metadata?.full_name) {
      return user.user_metadata.full_name
        .split(' ')
        .map((part: string) => part[0])
        .join('')
        .toUpperCase()
        .slice(0, 2);
    }
    if (user?.email) {
      return user.email.split('@')[0].slice(0, 2).toUpperCase();
    }
    return 'U';
  })();

  const displayName = user?.user_metadata?.full_name ?? user?.email ?? 'User';

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
        className={`fixed inset-y-0 left-0 z-40 flex w-72 flex-col border-r border-[#E9E5FF] bg-[#F5F3FF] px-4 py-5 transition-transform duration-300 dark:border-indigo-900 dark:bg-slate-900 ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        } lg:translate-x-0`}
      >
        {/* Header */}
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

        {/* Navigation */}
        <p className="mt-10 px-3 text-[10px] font-semibold uppercase tracking-[0.16em] text-[#8B85C8]">Workspace</p>
        <nav aria-label="Primary navigation" className="mt-3 flex-1 space-y-1">
          {visibleNav.map((item) => (
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

        {/* User info + Logout */}
        <div className="mt-auto border-t border-[#E9E5FF] pt-4 dark:border-indigo-800">
          <div className="flex items-center gap-3 rounded-lg px-2 py-2">
            {/* Avatar */}
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-[#C4B5FD] to-[#FBCFE8] text-xs font-bold text-[#312E81]">
              {initials}
            </div>
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-medium text-[#312E81] dark:text-indigo-100">
                {displayName}
              </p>
              {role && (
                <span className="inline-block mt-0.5 rounded-full bg-[#E9E5FF] px-2 py-0.5 text-[10px] font-semibold text-[#5B54A6] dark:bg-indigo-900 dark:text-indigo-300">
                  {role}
                </span>
              )}
            </div>
            <button
              onClick={handleLogout}
              className="rounded-md p-1.5 text-slate-400 transition-colors hover:bg-[#EDE9FE] hover:text-[#312E81]"
              title="Log out"
            >
              <LogOut className="size-4" />
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}
