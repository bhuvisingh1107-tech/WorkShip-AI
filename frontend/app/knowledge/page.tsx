"use client";

import { FormEvent, useEffect, useState } from "react";
import { BookOpen, LoaderCircle, Search } from "lucide-react";

type Document = { id: string; title: string; category: string | null; source: string | null; content: string; summary: string | null; tags: string[] | null };
type DocumentsResponse = { items: Document[]; total: number };
const categories = ["All", "Engineering", "HR", "Security", "Operations", "Incident Reports", "Policies"];

export default function KnowledgePage() {
  const [search, setSearch] = useState("");
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("All");
  const [documents, setDocuments] = useState<Document[]>([]);
  const [total, setTotal] = useState(0);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const params = new URLSearchParams({ limit: "50" });
    if (query) params.set("query", query);
    if (category !== "All") params.set("category", category);
    fetch(`/api/documents?${params}`)
      .then((response) => { if (!response.ok) throw new Error("Unable to load enterprise knowledge."); return response.json() as Promise<DocumentsResponse>; })
      .then((result) => { setDocuments(result.items); setTotal(result.total); setError(""); })
      .catch((requestError) => setError(requestError instanceof Error ? requestError.message : "Something went wrong."))
      .finally(() => setIsLoading(false));
  }, [query, category]);

  function submit(event: FormEvent<HTMLFormElement>) { event.preventDefault(); setIsLoading(true); setQuery(search.trim()); }

  return <section className="space-y-6 px-4 py-8 sm:px-6 lg:px-8 lg:py-10">
    <div><h1 className="text-2xl font-semibold tracking-tight text-slate-950">Enterprise Knowledge</h1><p className="mt-1 text-sm text-slate-500">Browse policies, runbooks, and operational guidance.</p></div>
    <form className="flex gap-3" onSubmit={submit}><div className="relative flex-1"><Search className="absolute left-3 top-3 size-4 text-slate-400" /><input className="w-full rounded-lg border border-[#DCD6FF] py-2.5 pl-9 pr-3 text-sm outline-none focus:border-[#A5B4FC]" onChange={(event) => setSearch(event.target.value)} placeholder="Search enterprise knowledge…" value={search} /></div><button className="rounded-lg bg-[#7C6CE7] px-4 text-sm font-medium text-white shadow-sm shadow-[#B8B5FF]/50" type="submit">Search</button></form>
    <div className="flex flex-wrap gap-2">{categories.map((item) => <button className={`rounded-full px-3 py-1.5 text-sm ${category === item ? "bg-[#B8B5FF] text-[#312E81]" : "bg-[#F5F3FF] text-slate-600 hover:bg-[#EDE9FE]"}`} key={item} onClick={() => { setIsLoading(true); setCategory(item); }} type="button">{item}</button>)}</div>
    {isLoading && <p className="flex items-center gap-2 text-sm text-slate-600"><LoaderCircle className="size-4 animate-spin" />Loading documents…</p>}
    {error && <p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
    {!isLoading && !error && <><p className="text-sm text-slate-500">{total} documents found</p>{documents.length > 0 && <div className="rounded-xl border border-[#E9E5FF] bg-white p-4 shadow-sm shadow-[#B8B5FF]/10"><p className="text-sm font-semibold text-[#312E81]">Knowledge base distribution</p><div className="mt-3 flex h-3 overflow-hidden rounded-full bg-[#F5F3FF]">{Object.entries(documents.reduce<Record<string,number>>((counts, item) => ({...counts,[item.category ?? "Other"]:(counts[item.category ?? "Other"] ?? 0)+1}),{})).map(([categoryName,count],index)=><div className={["bg-[#B8B5FF]","bg-[#A7F3D0]","bg-[#CFFAFE]","bg-[#FBCFE8]"][index%4]} key={categoryName} style={{width:`${count/documents.length*100}%`}} />)}</div><div className="mt-2 flex flex-wrap gap-3 text-xs text-slate-500">{Object.entries(documents.reduce<Record<string,number>>((counts, item) => ({...counts,[item.category ?? "Other"]:(counts[item.category ?? "Other"] ?? 0)+1}),{})).map(([categoryName,count])=><span key={categoryName}>{categoryName}: {count}</span>)}</div></div>}{documents.length === 0 ? <div className="rounded-xl border border-dashed border-[#DCD6FF] p-10 text-center text-sm text-slate-500">No documents match your search.</div> : <div className="grid gap-4 lg:grid-cols-2">{documents.map((document) => <article className="rounded-xl border border-[#E9E5FF] bg-white p-5 shadow-sm shadow-[#B8B5FF]/10" key={document.id}><div className="flex items-start gap-3"><BookOpen className="mt-0.5 size-5 shrink-0 text-[#818CF8]" /><div><h2 className="font-semibold text-[#312E81]">{document.title}</h2><p className="mt-1 text-xs text-slate-500">{document.category ?? "Enterprise knowledge"} · {readingTime(document.content)} min read</p></div></div><p className="mt-4 text-sm leading-6 text-slate-600">{document.summary ?? document.content.slice(0, 220)}</p><div className="mt-4 flex flex-wrap gap-2">{document.tags?.map((tag) => <span className="rounded-full bg-[#CFFAFE] px-2 py-1 text-xs text-[#315E70]" key={tag}>{tag}</span>)}</div><p className="mt-4 text-xs text-slate-500">Source: {document.source ?? "Internal knowledge base"}</p></article>)}</div>}</>}
  </section>;
}

function readingTime(content: string) { return Math.max(1, Math.ceil(content.trim().split(/\s+/).length / 200)); }
