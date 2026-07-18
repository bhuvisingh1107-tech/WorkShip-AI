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
          ? "bg-indigo-50 text-indigo-950 shadow-sm ring-1 ring-inset ring-indigo-100"
          : "text-slate-600 hover:bg-slate-100 hover:text-slate-950"
      }`}
      href={href}
      onClick={onNavigate}
    >
      <Icon aria-hidden="true" className="size-4" />
      <span>{label}</span>
    </Link>
  );
}
