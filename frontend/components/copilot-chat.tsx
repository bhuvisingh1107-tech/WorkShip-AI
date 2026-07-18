"use client";

import { FormEvent, useState } from "react";
import { LoaderCircle, Send, Sparkles } from "lucide-react";

type CopilotResponse = {
  answer: string;
  sources: { title: string; category: string | null; similarity: number }[];
  context: string[];
};

export function CopilotChat() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState<CopilotResponse | null>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedQuestion = question.trim();
    if (!trimmedQuestion) return;

    setError("");
    setIsLoading(true);
    try {
      const result = await fetch("/api/copilot/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: trimmedQuestion }),
      });
      if (!result.ok) throw new Error("Unable to reach the Copilot service.");
      setResponse((await result.json()) as CopilotResponse);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Something went wrong.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8 lg:py-10">
      <div className="rounded-xl border border-[#E9E5FF] bg-white shadow-sm shadow-[#B8B5FF]/10">
        <div className="border-b border-slate-200 px-5 py-5 sm:px-6">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-gradient-to-br from-[#C4B5FD] to-[#CFFAFE] p-2 text-[#312E81]"><Sparkles className="size-5" /></div>
            <div>
              <h1 className="text-xl font-semibold text-slate-950">Enterprise Copilot</h1>
              <p className="mt-1 text-sm text-slate-500">Ask questions across company knowledge and operations runbooks.</p>
            </div>
          </div>
        </div>

        <div className="min-h-72 space-y-5 p-5 sm:p-6">
          {!response && !isLoading && !error && <p className="text-sm text-slate-500">Try: “How do we handle production incidents?”</p>}
          {isLoading && <div className="flex items-center gap-2 text-sm text-slate-600"><LoaderCircle className="size-4 animate-spin" />Searching enterprise knowledge…</div>}
          {error && <p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
          {response && (
            <div className="space-y-5">
              <div className="rounded-xl bg-[#F5F3FF] p-4"><p className="text-xs font-semibold uppercase tracking-wide text-[#818CF8]">Answer</p><p className="mt-2 text-sm leading-6 text-[#312E81]">{response.answer}</p></div>
              <div><p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Sources</p><div className="mt-2 grid gap-2 sm:grid-cols-2">{response.sources.map((source) => <div className="rounded-lg border border-[#E9E5FF] bg-[#FFFEFF] p-3" key={source.title}><p className="text-sm font-medium text-[#312E81]">{source.title}</p><p className="mt-1 text-xs text-slate-500">{source.category ?? "Enterprise knowledge"} · {Math.round(source.similarity * 100)}% match</p></div>)}</div></div>
            </div>
          )}
        </div>

        <form className="border-t border-slate-200 p-4 sm:p-5" onSubmit={handleSubmit}>
          <div className="flex gap-3"><input className="min-w-0 flex-1 rounded-lg border border-slate-300 px-3 py-2.5 text-sm outline-none placeholder:text-slate-400 focus:border-slate-900" disabled={isLoading} onChange={(event) => setQuestion(event.target.value)} placeholder="Ask about policies, incidents, or operations…" value={question} /><button className="inline-flex items-center gap-2 rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-medium text-white disabled:cursor-not-allowed disabled:bg-slate-400" disabled={isLoading} type="submit"><Send className="size-4" />Ask</button></div>
        </form>
      </div>
    </section>
  );
}
