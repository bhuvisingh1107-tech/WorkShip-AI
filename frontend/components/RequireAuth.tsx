'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth, UserRole } from '@/context/AuthProvider';
import { ShieldAlert } from 'lucide-react';

type Props = {
  children: React.ReactNode;
  allowedRoles?: UserRole[];
};

function Forbidden() {
  const router = useRouter();
  return (
    <section className="flex min-h-[60vh] flex-col items-center justify-center px-4 text-center">
      <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-red-50">
        <ShieldAlert className="h-8 w-8 text-red-500" />
      </div>
      <h1 className="mt-6 text-2xl font-bold text-[#312E81]">403 — Unauthorized</h1>
      <p className="mt-2 max-w-md text-sm text-slate-500">
        You don't have permission to access this page. Contact your administrator if you believe this is an error.
      </p>
      <button
        onClick={() => router.push('/dashboard')}
        className="mt-6 rounded-lg bg-[#7C6CE7] px-5 py-2.5 text-sm font-medium text-white shadow-sm shadow-[#B8B5FF]/50 transition-colors hover:bg-[#6D28D9]"
      >
        Back to Dashboard
      </button>
    </section>
  );
}

export function RequireAuth({ children, allowedRoles }: Props) {
  const { user, role, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.replace('/login');
    }
  }, [user, loading, router]);

  // While loading, show skeleton
  if (loading) {
    return (
      <section className="p-8 space-y-4">
        <div className="skeleton h-28 w-full rounded-2xl" />
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="skeleton h-20 w-full rounded-xl" />
          ))}
        </div>
      </section>
    );
  }

  if (!user) {
    return null;
  }

  // Role-based access check
  if (allowedRoles && role && !allowedRoles.includes(role)) {
    return <Forbidden />;
  }

  return children;
}