import { Bell, Building2, CheckCircle2, ShieldCheck, Sparkles, UserRound } from "lucide-react";

const sections = [
  { title: "Profile", icon: UserRound, rows: [["User name", "WorkShip Administrator"], ["Role", "Operations Administrator"], ["Organization", "WorkShip AI"]] },
  { title: "Workspace Settings", icon: Building2, rows: [["Workspace", "WorkShip AI"], ["Type", "Enterprise Operations Intelligence"]] },
  { title: "Preferences", icon: Sparkles, rows: [["Theme preference", "Use the navigation theme toggle"], ["Notifications", "Operational alerts enabled"]] },
  { title: "Security", icon: ShieldCheck, rows: [["Authentication status", "Demo workspace session"], ["Admin access", "Enabled"]] },
  { title: "System Information", icon: CheckCircle2, rows: [["Version", "0.1.0"], ["Retrieval Engine", "Active"], ["Semantic Search", "Enabled"]] },
];

export default function SettingsPage() {
  return <section className="mx-auto max-w-4xl space-y-6 px-4 py-8 sm:px-6 lg:px-8 lg:py-10">
    <div className="rounded-2xl bg-gradient-to-br from-[#C4B5FD] via-[#B8B5FF] to-[#CFFAFE] px-6 py-7 text-[#312E81] dark:from-indigo-950 dark:via-slate-900 dark:to-indigo-900 dark:text-indigo-100"><p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#5B54A6] dark:text-indigo-300">Workspace</p><h1 className="mt-2 text-2xl font-semibold">Settings</h1><p className="mt-2 text-sm text-[#5B54A6] dark:text-slate-300">Manage your WorkShip AI workspace preferences and system information.</p></div>
    <div className="grid gap-5 md:grid-cols-2">{sections.map(({ title, icon: Icon, rows }) => <article className="rounded-xl border border-[#E9E5FF] bg-white p-5 shadow-sm shadow-[#B8B5FF]/10 dark:border-indigo-900 dark:bg-slate-900" key={title}><div className="flex items-center gap-3"><div className="rounded-lg bg-[#F5F3FF] p-2 text-[#7C6CE7] dark:bg-indigo-950 dark:text-indigo-300"><Icon className="size-5" /></div><h2 className="font-semibold text-[#312E81] dark:text-indigo-100">{title}</h2></div><dl className="mt-5 space-y-3">{rows.map(([label, value]) => <div className="flex items-start justify-between gap-5 border-b border-[#F5F3FF] pb-3 last:border-0 last:pb-0 dark:border-slate-800" key={label}><dt className="text-sm text-slate-500 dark:text-slate-400">{label}</dt><dd className="text-right text-sm font-medium text-[#312E81] dark:text-slate-200">{value}</dd></div>)}</dl></article>)}</div>
    <div className="flex items-center gap-3 rounded-xl border border-[#E9E5FF] bg-[#F5F3FF] p-4 text-sm text-slate-600 dark:border-indigo-900 dark:bg-indigo-950/50 dark:text-slate-300"><Bell className="size-5 text-[#7C6CE7]" />Settings are configured for the WorkShip AI hackathon demonstration environment.</div>
  </section>;
}
