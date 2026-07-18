import Image from "next/image";

type LogoProps = {
  compact?: boolean;
};

export function Logo({ compact = false }: LogoProps) {
  return (
    <div className="flex items-center gap-3">
      <Image alt="WorkShip AI" className="size-10 rounded-xl object-contain shadow-lg shadow-[#B8B5FF]/30" height={40} priority src="/logo.png" width={40} />
      {!compact && (
        <span><span className="block text-base font-semibold tracking-tight text-[#312E81]">WorkShip AI</span><span className="block text-[10px] font-medium uppercase tracking-[0.16em] text-[#818CF8]">Operations intelligence</span></span>
      )}
    </div>
  );
}
