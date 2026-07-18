"use client";

import { useEffect, useState } from "react";
import { AlertTriangle, BookOpen, BriefcaseBusiness, LoaderCircle, Users } from "lucide-react";

type DashboardData = {
  overview: { totalEmployees: number; totalTeams: number; totalServices: number; totalDocuments: number; totalIncidents: number };
  incidentAnalytics: { critical: number; high: number; medium: number; low: number };
  serviceAnalytics: { byStatus: Record<string, number> };
  recentActivity: {
    incidents: { id: string; title: string; severity: string; status: string }[];
    meetings: { id: string; title: string; date: string }[];
    documents: { id: string; title: string; category: string | null }[];
  };
};

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/api/dashboard")
      .then((response) => {
        if (!response.ok) throw new Error("Unable to load dashboard data.");
        return response.json() as Promise<DashboardData>;
      })
      .then(setData)
      .catch((requestError) => setError(requestError instanceof Error ? requestError.message : "Something went wrong."));
  }, []);

  if (error) return <section className="p-8"><p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p></section>;
  if (!data) return <section className="flex items-center gap-2 p-8 text-sm text-slate-600"><LoaderCircle className="size-4 animate-spin" />Loading dashboard…</section>;

  const cards = [
    ["Employees", data.overview.totalEmployees, Users],
    ["Teams", data.overview.totalTeams, Users],
    ["Services", data.overview.totalServices, BriefcaseBusiness],
    ["Documents", data.overview.totalDocuments, BookOpen],
    ["Incidents", data.overview.totalIncidents, AlertTriangle],
  ] as const;

  return <section className="space-y-7 px-4 py-8 sm:px-6 lg:px-8 lg:py-10">
    <div><h1 className="text-2xl font-semibold tracking-tight text-slate-950">Dashboard</h1><p className="mt-1 text-sm text-slate-500">Enterprise operations overview.</p></div>
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">{cards.map(([label, value, Icon]) => <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm" key={label}><Icon className="size-5 text-slate-500" /><p className="mt-4 text-2xl font-semibold text-slate-950">{value}</p><p className="mt-1 text-sm text-slate-500">{label}</p></div>)}</div>
    <div className="grid gap-5 lg:grid-cols-2">
      <Panel title="Incident severity"><div className="grid grid-cols-4 gap-3">{Object.entries(data.incidentAnalytics).map(([severity, count]) => <div className="rounded-lg bg-slate-50 p-3 text-center" key={severity}><p className="text-lg font-semibold text-slate-900">{count}</p><p className="mt-1 text-xs capitalize text-slate-500">{severity}</p></div>)}</div></Panel>
      <Panel title="Service status"><div className="space-y-3">{Object.entries(data.serviceAnalytics.byStatus).map(([status, count]) => <div className="flex items-center justify-between rounded-lg bg-slate-50 p-3 text-sm" key={status}><span className="capitalize text-slate-700">{status}</span><span className="font-semibold text-slate-950">{count}</span></div>)}</div></Panel>
    </div>
    <div className="grid gap-5 lg:grid-cols-3"><Activity title="Recent incidents" items={data.recentActivity.incidents.map((item) => `${item.title} · ${item.severity}`)} /><Activity title="Recent documents" items={data.recentActivity.documents.map((item) => item.title)} /><Activity title="Recent meetings" items={data.recentActivity.meetings.map((item) => item.title)} /></div>
  </section>;
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) { return <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"><h2 className="text-sm font-semibold text-slate-900">{title}</h2><div className="mt-4">{children}</div></div>; }
function Activity({ title, items }: { title: string; items: string[] }) { return <Panel title={title}><ul className="space-y-3">{items.map((item) => <li className="border-b border-slate-100 pb-3 text-sm text-slate-700 last:border-0 last:pb-0" key={item}>{item}</li>)}</ul></Panel>; }
