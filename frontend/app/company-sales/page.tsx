'use client';
import { FormEvent, useEffect, useState } from "react";
import {
  AlertCircle,
  CalendarClock,
  LogOut,
  Menu,
  Sun,
  TrendingDown,
  TrendingUp,
  Users,
} from "lucide-react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthProvider";
import { Logo } from "@/components/logo";
import { RequireAuth } from "@/components/RequireAuth";

const trend = [
  { year: "2022", sales: 2.4 },
  { year: "2023", sales: 3.1 },
  { year: "2024", sales: 3.8 },
  { year: "2025", sales: 3.2 },
  { year: "2026", sales: 4.1 },
];
const clients = [
  ["Northstar Health", "Healthcare", "$680K", "Active", "Jul 12", "Up"],
  ["Apex Manufacturing", "Manufacturing", "$540K", "Active", "Jul 08", "Up"],
  [
    "Cobalt Finance",
    "Financial Services",
    "$430K",
    "Renewal",
    "Jun 28",
    "Down",
  ],
  ["VentureWorks", "Technology", "$315K", "Inactive", "May 19", "Down"],
];

const CompanySalesPageInner = () => {
  const router = useRouter();
  const { user, logout } = useAuth();
  const [loading, setLoading] = useState(false);

  // Role-based access: only CEO can view
  const shouldRedirect = !user || user.role !== "CEO";

  useEffect(() => {
    if (shouldRedirect) {
      // Redirect to login or show 403
      // For simplicity, we redirect to login
      router.push("/login");
    }
  }, [shouldRedirect, router]);

  if (shouldRedirect) return null;

  const handleLogout = async () => {
    setLoading(true);
    try {
      await logout();
    } catch (err) {
      console.error("Logout failed", err);
    } finally {
      setLoading(false);
    }
    router.push("/login");
  };

  return (
    <>
      <header className="flex h-16 items-center justify-between border-b border-[#E9E5FF] bg-white/90 px-4 backdrop-blur dark:border-indigo-800 dark:bg-slate-900/90 sm:px-6">
        <div className="flex items-center gap-3">
          <button
            aria-label="Open navigation"
            className="rounded-md p-2 text-slate-600 hover:bg-slate-100 lg:hidden"
            onClick={() => {
              /* TODO: implement sidebar toggle */
            }}
            type="button"
          >
            <Menu aria-hidden="true" className="size-5" />
          </button>
          <Logo compact />
          <p className="text-sm font-semibold text-[#312E81]">
            Operations workspace
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            aria-label="Toggle theme"
            className="rounded-md p-2 text-slate-600 hover:bg-slate-100 dark:text-indigo-200 dark:hover:bg-slate-800"
            onClick={() => {
              // TODO: implement theme toggle
            }}
            type="button"
          >
            <Sun aria-hidden="true" className="size-4" />
          </button>
          <div
            onClick={() => router.push("/settings")}
            className="cursor-pointer flex items-center gap-2"
          >
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-[#FBCFE8] text-xs font-semibold text-[#7C3D66]">
              {(() => {
                if (user.user_metadata?.full_name) {
                  return user.user_metadata.full_name
                    .split(" ")
                    .map((part: string) => part[0])
                    .join("")
                    .toUpperCase();
                }
                if (user.email) {
                  return user.email.split("@")[0].toUpperCase();
                }
                return "U";
              })()}
            </div>
            <div>
              <p className="text-sm font-medium text-[#312E81]">
                {user.user_metadata?.full_name ?? user.email}
              </p>
              <p className="text-xs text-slate-500">{user.role ?? "User"}</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="rounded-md p-2 text-slate-500 hover:bg-slate-100"
            title="Log out"
            disabled={loading}
          >
            {loading ? (
              <span className="inline-flex h-4 w-4 items-center justify-center rounded-full border border-slate-200 animate-spin">
                Loading
              </span>
            ) : (
              <LogOut className="size-4" />
            )}
          </button>
        </div>
      </header>

      <main className="pt-8">
        <section className="space-y-6 px-4 py-8 sm:px-6 lg:px-8 lg:py-10">
          <div className="flex items-start justify-between gap-4 rounded-2xl bg-gradient-to-br from-[#C4B5FD] via-[#B8B5FF] to-[#CFFAFE] px-6 py-7 text-[#312E81]">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#5B54A6]">
                Executive view
              </p>
              <h1 className="mt-2 text-2xl font-semibold">Company Sales</h1>
              <p className="mt-2 text-sm text-[#5B54A6]">
                Revenue performance, client health, and recommended commercial
                actions.
              </p>
            </div>
            <button
              onClick={handleLogout}
              className="inline-flex items-center gap-2 rounded-lg bg-white/70 px-3 py-2 text-xs font-medium text-[#312E81]"
            >
              <LogOut className="size-4" />
              Logout
            </button>
          </div>
          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <Metric
              label="Total clients"
              value="42"
              icon={Users}
              tone="[#CFFAFE]"
            />
            <Metric
              label="Active clients"
              value="36"
              icon={Users}
              tone="[#A7F3D0]"
            />
            <Metric
              label="Revenue this year"
              value="$4.1M"
              icon={TrendingUp}
              tone="[#FDE68A]"
            />
            <Metric
              label="Growth"
              value="+28%"
              icon={TrendingUp}
              tone="[#FBCFE8]"
            />
          </div>
          <div className="grid gap-5 lg:grid-cols-3">
            <div className="rounded-xl border border-[#E9E5FF] bg-white p-5 shadow-sm shadow-[B8B5FF]/10 lg:col-span-2">
              <div className="flex items-center justify-between">
                <h2 className="font-semibold text-[#312E81]">
                  Five year revenue trend
                </h2>
                <span className="rounded-full bg-[#A7F3D0] px-2 py-1 text-xs font-medium text-[#246B57]">
                  +28% growth
                </span>
              </div>
              <svg
                aria-label="Five year revenue trend"
                className="mt-5 h-48 w-full"
                viewBox="0 0 500 180"
              >
                <defs>
                  <linearGradient id="sales-area" x1="0" x2="0" y1="0" y2="1">
                    <stop stopColor="#B8B5FF" stopOpacity=".55" />
                    <stop offset="1" stopColor="#CFFAFE" stopOpacity=".1" />
                  </linearGradient>
                </defs>
                <path
                  d="M30 140 L145 105 L260 70 L375 110 L470 45 L470 155 L30 155 Z"
                  fill="url(#sales-area)"
                />
                <path
                  d="M30 140 L145 105 L260 70 L375 110 L470 45"
                  fill="none"
                  stroke="#7C6CE7"
                  strokeWidth="4"
                />
                {trend.map((item, index) => (
                  <g key={item.year}>
                    <circle
                      cx={[30, 145, 260, 375, 470][index]}
                      cy={[140, 105, 70, 110, 45][index]}
                      fill="#fff"
                      r="5"
                      stroke="#7C6CE7"
                      strokeWidth="3"
                    />
                    <text
                      fill="#64748B"
                      fontSize="12"
                      textAnchor="middle"
                      x={[30, 145, 260, 375, 470][index]}
                      y="175"
                    >
                      {item.year}
                    </text>
                  </g>
                ))}
              </svg>
            </div>
            <div className="rounded-xl border border-[#E9E5FF] bg-white p-5">
              <h2 className="font-semibold text-[#312E81]">Sales alerts</h2>
              <ul className="mt-4 space-y-4 text-sm text-slate-700">
                <li className="flex gap-2">
                  <TrendingDown className="size-4 shrink-0 text-[#D977A7]" />
                  Sales decreased 15% compared to previous year
                </li>
                <li className="flex gap-2">
                  <AlertCircle className="size-4 shrink-0 text-[#D977A7]" />3
                  clients require follow-up
                </li>
                <li className="flex gap-2">
                  <CalendarClock className="size-4 shrink-0 text-[#5B54A6]" />
                  Renewal meetings recommended
                </li>
              </ul>
            </div>
          </div>
          <div className="grid gap-5 lg:grid-cols-2">
            <div className="rounded-xl border border-[#E9E5FF] bg-white p-5 shadow-sm shadow-[B8B5FF]/10">
              <h2 className="font-semibold text-[#312E81]">
                Top client performance
              </h2>
              <div className="mt-4 space-y-3">
                {clients.slice(0, 3).map((client, index) => (
                  <div key={client[0]}>
                    <div className="flex justify-between text-sm text-slate-600">
                      <span>{client[0]}</span>
                      <span>{client[2]}</span>
                    </div>
                    <div className="mt-1 h-2 rounded-full bg-[#F5F3FF]">
                      <div
                        className="h-2 rounded-full bg-gradient-to-r from-[#A5B4FC] to-[#A7F3D0]"
                        style={{ width: `${[100, 79, 63][index]}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="rounded-xl border border-[#E9E5FF] bg-white p-5">
              <h2 className="font-semibold text-[#312E81]">
                Client distribution
              </h2>
              <div className="mt-4 grid grid-cols-3 gap-3 text-center">
                <MiniStat label="Active" value="36" tone="bg-[#A7F3D0]" />
                <MiniStat label="At risk" value="3" tone="bg-[#FBCFE8]" />
                <MiniStat label="Renewals" value="7" tone="bg-[#FDE68A]" />
              </div>
            </div>
          </div>
          <div className="rounded-xl border border-[#E9E5FF] bg-white p-5">
            <h2 className="font-semibold text-[#312E81]">Client portfolio</h2>
            <div className="mt-4 overflow-x-auto">
              <table className="w-full min-w-[700px] text-left text-sm">
                <thead className="border-b border-[#E9E5FF] text-xs uppercase tracking-wide text-slate-500">
                  <tr>
                    {[
                      "Client",
                      "Industry",
                      "Annual sales",
                      "Status",
                      "Last meeting",
                      "Trend",
                    ].map((heading) => (
                      <th className="pb-3 font-medium" key={heading}>
                        {heading}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {clients.map((client) => (
                    <tr
                      className="border-b border-slate-100 last:border-0"
                      key={client[0]}
                    >
                      {client.map((value, index) => (
                        <td
                          className={`py-3 ${
                            index === 0
                              ? "font-medium text-[#312E81]"
                              : "text-slate-600"
                          }`}
                          key={index}
                        >
                          {index === 3 ? (
                            <span className="rounded-full bg-[#F5F3FF] px-2 py-1 text-xs">
                              {value}
                            </span>
                          ) : index === 5 ? (
                            <span
                              className={
                                value === "Up"
                                  ? "text-emerald-600"
                                  : "text-[#D977A7]"
                              }
                            >
                              {value}
                            </span>
                          ) : (
                            value
                          )}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
          <div className="grid gap-4 md:grid-cols-3">
            {[
              "Schedule follow-up with declining clients",
              "Contact inactive clients",
              "Arrange renewal discussions",
            ].map((suggestion) => (
              <div
                key={suggestion}
                className="rounded-xl border border-[#E9E5FF] bg-white p-4"
              >
                <CalendarClock className="size-5 text-[#818CF8]" />
                <p className="mt-3 text-sm font-medium text-[#312E81]">
                  {suggestion}
                </p>
              </div>
            ))}
          </div>
        </section>
      </main>
    </>
  );
};

function Metric({
  label,
  value,
  icon: Icon,
  tone,
}: {
  label: string;
  value: string;
  icon: typeof Users;
  tone: string;
}) {
  return (
    <div className="rounded-xl border border-[#E9E5FF] bg-white p-4 shadow-sm shadow-[B8B5FF]/10">
      <div
        className={`flex size-9 items-center justify-center rounded-lg ${tone}`}
      >
        <Icon className="size-4 text-[#312E81]" />
      </div>
      <p className="mt-4 text-2xl font-semibold text-[#312E81]">{value}</p>
      <p className="mt-1 text-sm text-slate-500">{label}</p>
    </div>
  );
}

function MiniStat({
  label,
  value,
  tone,
}: {
  label: string;
  value: string;
  tone: string;
}) {
  return (
    <div className={`rounded-xl ${tone} p-3`}>
      <p className="text-lg font-semibold text-[#312E81]">{value}</p>
      <p className="mt-1 text-xs text-[#5B54A6]">{label}</p>
    </div>
  );
}

export default function CompanySalesPage() {
  return (
    <RequireAuth>
      <CompanySalesPageInner />
    </RequireAuth>
  );
}
