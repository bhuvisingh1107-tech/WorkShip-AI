'use client';

import { FormEvent, useState } from "react";
import { AlertTriangle, Check, LoaderCircle } from "lucide-react";
import { RequireAuth } from "@/components/RequireAuth";
import { fetcher } from '@/lib/fetcher';

type SimulationResponse = {
  incident: { title: string; severity: string; status: string };
  similarIncidents: { title: string; similarity: number }[];
  relatedDocuments: { title: string; similarity: number }[];
  recommendedActions: string[];
  timeline: string[];
};

const IncidentsPageInner = () => {
  const [title, setTitle] = useState("Payment service outage");
  const [description, setDescription] = useState("Users are receiving 500 errors");
  const [severity, setSeverity] = useState("critical");
  const [result, setResult] = useState<SimulationResponse | null>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function simulate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setIsLoading(true);
    try {
      const response = await fetcher<SimulationResponse>("/api/incidents/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, description, severity }),
      });
      setResult(response);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Something went wrong.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8 lg:py-10">
      <div className="rounded-xl border border-[#E9E5FF] bg-white shadow-sm shadow-[B8B5FF]/10">
        <div className="border-b border-slate-200 px-5 py-5 sm:px-6">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-gradient-to-br from-[#FBCFE8] to-[#FDE68A] p-2 text-[#7C3D66]"><AlertTriangle className="size-5" /></div>
            <div><h1 className="text-xl font-semibold text-slate-950">Incident Intelligence</h1><p className="mt-1 text-sm text-slate-500">Simulate an incident and surface related enterprise knowledge.</p></div>
          </div>
        </div>

        <form className="grid gap-4 border-b border-slate-200 p-5 sm:grid-cols-2 sm:p-6" onSubmit={simulate}>
          <label className="text-sm font-medium text-slate-700">Title<input className="mt-1.5 w-full rounded-lg border border-slate-300 px-3 py-2.5 font-normal outline-none focus:border-slate-900" onChange={(event) => setTitle(event.target.value)} required value={title} /></label>
          <label className="text-sm font-medium text-slate-700">Severity<select className="mt-1.5 w-full rounded-lg border border-slate-300 bg-white px-3 py-2.5 font-normal outline-none focus:border-slate-900" onChange={(event) => setSeverity(event.target.value)} value={severity}><option value="critical">Critical</option><option value="high">High</option><option value="medium">Medium</option><option value="low">Low</option></select></label>
          <label className="text-sm font-medium text-slate-700 sm:col-span-2">Description<textarea className="mt-1.5 min-h-24 w-full rounded-lg border border-slate-300 px-3 py-2.5 font-normal outline-none focus:border-slate-900" onChange={(event) => setDescription(event.target.value)} required value={description} /></label>
          <div className="sm:col-span-2"><button className="inline-flex items-center gap-2 rounded-lg bg-[#7C6CE7] px-4 py-2.5 text-sm font-medium text-white shadow-sm shadow-[B8B5FF]/50 disabled:bg-slate-400" disabled={isLoading} type="submit">{isLoading && <LoaderCircle className="size-4 animate-spin" />}{isLoading ? "Investigating…" : "Simulate incident"}</button></div>
        </form>

        <div className="space-y-5 p-5 sm:p-6">
          {error && <p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
          {!result && !isLoading && !error && <p className="text-sm text-slate-500">Submit the simulation to investigate related incidents and knowledge.</p>}
          {result && <div className="space-y-5">
            <div className="rounded-lg bg-[#F5F3FF] p-4"><p className="text-xs font-semibold uppercase tracking-wide text-[#818CF8]">Simulated incident</p><p className="mt-1 font-semibold text-[#312E81]">{result.incident.title}</p><p className="mt-2 flex items-center gap-2 text-sm text-slate-600"><span className="rounded-full bg-[#FBCFE8] px-2 py-1 text-xs font-medium capitalize text-[#8A4166]">{result.incident.severity}</span>{result.incident.status}</p></div>
            <div className="grid gap-5 md:grid-cols-2"><ResultList title="Similar incidents" items={result.similarIncidents.map((item) => `${item.title} · ${Math.round(item.similarity * 100)}% match`)} /><ResultList title="Related documents" items={result.relatedDocuments.map((item) => item.title)} /></div>
            <div><h2 className="text-sm font-semibold text-slate-900">Recommended actions</h2><ul className="mt-2 space-y-2">{result.recommendedActions.map((action) => <li className="flex items-center gap-2 text-sm text-slate-700" key={action}><Check className="size-4 text-emerald-600" />{action}</li>)}</ul></div>
            <div><h2 className="text-sm font-semibold text-slate-900">Investigation progress</h2><ol className="mt-3 space-y-3 border-l-2 border-[C4B5FD] pl-4">{result.timeline.map((step, index) => <li className="relative text-sm text-slate-700" key={step}><span className="absolute -left-[23px] flex size-4 items-center justify-center rounded-full bg-[#B8B5FF] text-[9px] text-[#312E81]">{index + 1}</span>{step}</li>)}</ol></div>
          </div>}
        </div>
      </div>
    </section>
  );
};

function ResultList({ title, items }: { title: string; items: string[] }) {
  return <div><h2 className="text-sm font-semibold text-slate-900">{title}</h2><ul className="mt-2 space-y-2">{items.length ? items.map((item) => <li className="rounded-lg border border-slate-200 p-3 text-sm text-slate-700" key={item}>{item}</li>) : <li className="text-sm text-slate-500">No related results found.</li>}</ul></div>;
};

export default function IncidentsPage() {
  return <RequireAuth><IncidentsPageInner /></RequireAuth>;
}