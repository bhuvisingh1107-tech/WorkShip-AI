"use client";

import { FormEvent, useEffect, useState } from "react";
import { AlertCircle, CalendarClock, LockKeyhole, LogOut, TrendingDown, TrendingUp, Users } from "lucide-react";

const trend = [{ year: "2022", sales: 2.4 }, { year: "2023", sales: 3.1 }, { year: "2024", sales: 3.8 }, { year: "2025", sales: 3.2 }, { year: "2026", sales: 4.1 }];
const clients = [
  ["Northstar Health", "Healthcare", "$680K", "Active", "Jul 12", "Up"],
  ["Apex Manufacturing", "Manufacturing", "$540K", "Active", "Jul 08", "Up"],
  ["Cobalt Finance", "Financial Services", "$430K", "Renewal", "Jun 28", "Down"],
  ["VentureWorks", "Technology", "$315K", "Inactive", "May 19", "Down"],
];

function SalesDashboard({ onLogout }: { onLogout: () => void }) {
  return <section className="space-y-6 px-4 py-8 sm:px-6 lg:px-8 lg:py-10">
    <div className="flex items-start justify-between gap-4 rounded-2xl bg-gradient-to-br from-[#C4B5FD] via-[#B8B5FF] to-[#CFFAFE] px-6 py-7 text-[#312E81]"><div><p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#5B54A6]">Executive view</p><h1 className="mt-2 text-2xl font-semibold">Company Sales</h1><p className="mt-2 text-sm text-[#5B54A6]">Revenue performance, client health, and recommended commercial actions.</p></div><button className="inline-flex items-center gap-2 rounded-lg bg-white/70 px-3 py-2 text-xs font-medium text-[#312E81]" onClick={onLogout} type="button"><LogOut className="size-4" />Logout</button></div>
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4"><Metric label="Total clients" value="42" icon={Users} tone="[#CFFAFE]" /><Metric label="Active clients" value="36" icon={Users} tone="[#A7F3D0]" /><Metric label="Revenue this year" value="$4.1M" icon={TrendingUp} tone="[#FDE68A]" /><Metric label="Growth" value="+28%" icon={TrendingUp} tone="[#FBCFE8]" /></div>
    <div className="grid gap-5 lg:grid-cols-3"><div className="rounded-xl border border-[#E9E5FF] bg-white p-5 shadow-sm shadow-[#B8B5FF]/10 lg:col-span-2"><h2 className="font-semibold text-[#312E81]">Five year sales trend</h2><div className="mt-6 flex h-52 items-end justify-between gap-4">{trend.map((item) => <div className="flex flex-1 flex-col items-center gap-2" key={item.year}><span className="text-xs font-medium text-[#5B54A6]">${item.sales}M</span><div className="w-full rounded-t-lg bg-gradient-to-t from-[#A5B4FC] to-[#CFFAFE]" style={{ height: `${item.sales / 4.5 * 100}%` }} /><span className="text-xs text-slate-500">{item.year}</span></div>)}</div></div><div className="rounded-xl border border-[#E9E5FF] bg-[#F5F3FF] p-5"><h2 className="font-semibold text-[#312E81]">Sales alerts</h2><ul className="mt-4 space-y-4 text-sm text-slate-700"><li className="flex gap-2"><TrendingDown className="size-4 shrink-0 text-[#D977A7]" />Sales decreased 15% compared to previous year</li><li className="flex gap-2"><AlertCircle className="size-4 shrink-0 text-[#D977A7]" />3 clients require follow-up</li><li className="flex gap-2"><CalendarClock className="size-4 shrink-0 text-[#5B54A6]" />Renewal meetings recommended</li></ul></div></div>
    <div className="rounded-xl border border-[#E9E5FF] bg-white p-5 shadow-sm shadow-[#B8B5FF]/10"><h2 className="font-semibold text-[#312E81]">Client portfolio</h2><div className="mt-4 overflow-x-auto"><table className="w-full min-w-[700px] text-left text-sm"><thead className="border-b border-[#E9E5FF] text-xs uppercase tracking-wide text-slate-500"><tr>{["Client", "Industry", "Annual sales", "Status", "Last meeting", "Trend"].map((heading) => <th className="pb-3 font-medium" key={heading}>{heading}</th>)}</tr></thead><tbody>{clients.map((client) => <tr className="border-b border-slate-100 last:border-0" key={client[0]}>{client.map((value, index) => <td className={`py-3 ${index === 0 ? "font-medium text-[#312E81]" : "text-slate-600"}`} key={index}>{index === 3 ? <span className="rounded-full bg-[#F5F3FF] px-2 py-1 text-xs">{value}</span> : index === 5 ? <span className={value === "Up" ? "text-emerald-600" : "text-[#D977A7]"}>{value}</span> : value}</td>)}</tr>)}</tbody></table></div></div>
    <div className="grid gap-4 md:grid-cols-3">{["Schedule follow-up with declining clients", "Contact inactive clients", "Arrange renewal discussions"].map((suggestion) => <div className="rounded-xl border border-[#E9E5FF] bg-white p-4 shadow-sm shadow-[#B8B5FF]/10" key={suggestion}><CalendarClock className="size-5 text-[#818CF8]" /><p className="mt-3 text-sm font-medium text-[#312E81]">{suggestion}</p></div>)}</div>
  </section>;
}

function Metric({ label, value, icon: Icon, tone }: { label: string; value: string; icon: typeof Users; tone: string }) { return <div className="rounded-xl border border-[#E9E5FF] bg-white p-4 shadow-sm shadow-[#B8B5FF]/10"><div className={`flex size-9 items-center justify-center rounded-lg ${tone}`}><Icon className="size-4 text-[#312E81]" /></div><p className="mt-4 text-2xl font-semibold text-[#312E81]">{value}</p><p className="mt-1 text-sm text-slate-500">{label}</p></div>; }

export default function CompanySalesPage() {
  const [authorized, setAuthorized] = useState<boolean | null>(null);
  const [username, setUsername] = useState("");
  const [pin, setPin] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const timer = window.setTimeout(() => setAuthorized(localStorage.getItem("workship-ceo-access") === "granted"));
    return () => window.clearTimeout(timer);
  }, []);

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (username === "ceo_admin" && pin === "WSAI2026") {
      localStorage.setItem("workship-ceo-access", "granted");
      setAuthorized(true);
      setError("");
    } else setError("Unauthorized access. CEO credentials required.");
  }

  function logout() { localStorage.removeItem("workship-ceo-access"); setAuthorized(false); setPin(""); }

  if (authorized === null) return null;
  if (authorized) return <SalesDashboard onLogout={logout} />;
  return <section className="flex min-h-[calc(100vh-4rem)] items-center justify-center px-4"><form className="w-full max-w-md rounded-2xl border border-[#E9E5FF] bg-white p-7 shadow-xl shadow-[#B8B5FF]/15" onSubmit={submit}><div className="flex size-11 items-center justify-center rounded-xl bg-gradient-to-br from-[#C4B5FD] to-[#CFFAFE] text-[#312E81]"><LockKeyhole className="size-5" /></div><p className="mt-5 text-xs font-semibold uppercase tracking-[0.18em] text-[#818CF8]">Executive security</p><h1 className="mt-2 text-2xl font-semibold text-[#312E81]">CEO Access</h1><p className="mt-2 text-sm leading-6 text-slate-500">Company Sales contains executive-only revenue and client portfolio data.</p><label className="mt-6 block text-sm font-medium text-slate-700">Username<input className="mt-1.5 w-full rounded-lg border border-[#DCD6FF] px-3 py-2.5 outline-none focus:border-[#A5B4FC]" onChange={(event) => setUsername(event.target.value)} value={username} /></label><label className="mt-4 block text-sm font-medium text-slate-700">PIN<input className="mt-1.5 w-full rounded-lg border border-[#DCD6FF] px-3 py-2.5 outline-none focus:border-[#A5B4FC]" onChange={(event) => setPin(event.target.value)} type="password" value={pin} /></label>{error && <p className="mt-4 rounded-lg bg-[#FFF1F7] p-3 text-sm text-[#A34A72]">{error}</p>}<button className="mt-6 w-full rounded-lg bg-[#7C6CE7] px-4 py-2.5 text-sm font-medium text-white shadow-sm shadow-[#B8B5FF]/50" type="submit">Access Company Sales</button></form></section>;
}
