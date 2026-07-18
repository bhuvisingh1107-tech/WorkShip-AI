import { BriefcaseBusiness } from "lucide-react";

type LogoProps = {
  compact?: boolean;
};

export function Logo({ compact = false }: LogoProps) {
  return (
    <div className="flex items-center gap-3">
      <div className="flex size-9 items-center justify-center rounded-md bg-slate-900 text-white">
        <BriefcaseBusiness aria-hidden="true" className="size-5" />
      </div>
      {!compact && (
        <span className="text-base font-semibold tracking-tight text-slate-950">
          WorkShip AI
        </span>
      )}
    </div>
  );
}
