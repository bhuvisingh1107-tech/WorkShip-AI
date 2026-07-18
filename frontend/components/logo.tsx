import { Compass } from "lucide-react";

type LogoProps = {
  compact?: boolean;
};

export function Logo({ compact = false }: LogoProps) {
  return (
    <div className="flex items-center gap-3">
      <div className="flex size-10 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-slate-950 text-white shadow-lg shadow-indigo-950/20">
        <Compass aria-hidden="true" className="size-5" />
      </div>
      {!compact && (
        <span><span className="block text-base font-semibold tracking-tight text-slate-950">WorkShip AI</span><span className="block text-[10px] font-medium uppercase tracking-[0.16em] text-indigo-600">Operations intelligence</span></span>
      )}
    </div>
  );
}
