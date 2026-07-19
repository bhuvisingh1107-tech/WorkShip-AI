import Link from "next/link";
import type { LucideIcon } from "lucide-react";

type NavItemProps = {
  href: string;
  icon: LucideIcon;
  isActive: boolean;
  label: string;
  onNavigate?: () => void;
};

export function NavItem({
  href,
  icon: Icon,
  isActive,
  label,
  onNavigate,
}: NavItemProps) {
  return (
    <Link
      aria-current={isActive ? "page" : undefined}
      className={`flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium ${
        isActive
          ? "bg-white text-[#312E81] shadow-sm ring-1 ring-inset ring-[#C4B5FD] dark:bg-indigo-950 dark:text-indigo-100 dark:ring-indigo-700"
          : "text-slate-600 hover:bg-white/80 hover:text-[#312E81] dark:text-slate-300 dark:hover:bg-slate-800 dark:hover:text-indigo-100"
      }`}
      href={href}
      onClick={onNavigate}
    >
      <Icon aria-hidden="true" className="size-4" />
      <span>{label}</span>
    </Link>
  );
}
