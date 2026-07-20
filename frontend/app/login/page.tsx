'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useRef, useState } from 'react';
import { useAuth, UserRole } from '@/context/AuthProvider';
import { Logo } from '@/components/logo';

const ROLES: { value: UserRole; label: string; description: string }[] = [
  { value: 'Employee', label: 'Employee', description: 'Access dashboards, copilot & knowledge' },
  { value: 'Manager', label: 'Manager', description: 'Full access including sales analytics' },
  { value: 'CEO', label: 'CEO', description: 'Complete organizational overview' },
];

export default function LoginPage() {
  const router = useRouter();
  const { login, user } = useAuth();
  const emailRef = useRef<HTMLInputElement>(null);

  const [selectedRole, setSelectedRole] = useState<UserRole>('Employee');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Auto-focus email on mount
  useEffect(() => {
    emailRef.current?.focus();
  }, []);

  // If already logged in, redirect to dashboard
  useEffect(() => {
    if (user) {
      router.replace('/dashboard');
    }
  }, [user, router]);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(email, password, selectedRole);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  // Don't show login form if already authenticated
  if (user) return null;

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden px-4 py-12">
      {/* Animated gradient background */}
      <div className="animate-gradient absolute inset-0 bg-gradient-to-br from-[#312E81] via-[#4338CA] to-[#6D28D9]" />

      {/* Decorative orbs */}
      <div className="absolute left-[10%] top-[15%] h-72 w-72 rounded-full bg-[#A5B4FC] opacity-20 blur-3xl" />
      <div className="absolute bottom-[10%] right-[15%] h-96 w-96 rounded-full bg-[#C4B5FD] opacity-15 blur-3xl" />
      <div className="absolute left-[50%] top-[60%] h-48 w-48 rounded-full bg-[#CFFAFE] opacity-10 blur-3xl" />

      {/* Login card */}
      <div className="animate-fade-in-up relative z-10 w-full max-w-md">
        <form
          className="rounded-2xl border border-white/20 bg-white/95 p-8 shadow-2xl shadow-black/20 backdrop-blur-xl"
          onSubmit={handleSubmit}
        >
          {/* Logo + title */}
          <div className="flex flex-col items-center text-center">
            <Logo />
            <p className="mt-4 text-xs font-semibold uppercase tracking-[0.2em] text-[#818CF8]">
              Operations Intelligence
            </p>
            <h1 className="mt-2 text-2xl font-bold text-[#312E81]">
              Welcome back
            </h1>
            <p className="mt-1.5 text-sm text-[#5B54A6]">
              Sign in to your workspace
            </p>
          </div>

          {/* Role selector */}
          <fieldset className="mt-7">
            <legend className="text-sm font-semibold text-[#312E81]">Sign in as</legend>
            <div className="mt-2.5 grid grid-cols-3 gap-2">
              {ROLES.map((r) => (
                <label
                  key={r.value}
                  className={`group relative flex cursor-pointer flex-col items-center rounded-xl border-2 px-3 py-3 text-center transition-all duration-200 ${
                    selectedRole === r.value
                      ? 'border-[#7C6CE7] bg-[#F5F3FF] shadow-sm shadow-[#B8B5FF]/30'
                      : 'border-[#E9E5FF] bg-white hover:border-[#C4B5FD] hover:bg-[#FAFAF9]'
                  }`}
                >
                  <input
                    type="radio"
                    name="role"
                    value={r.value}
                    checked={selectedRole === r.value}
                    onChange={() => setSelectedRole(r.value)}
                    className="sr-only"
                  />
                  <span
                    className={`text-sm font-semibold ${
                      selectedRole === r.value ? 'text-[#312E81]' : 'text-slate-600'
                    }`}
                  >
                    {r.label}
                  </span>
                  <span
                    className={`mt-0.5 text-[10px] leading-tight ${
                      selectedRole === r.value ? 'text-[#5B54A6]' : 'text-slate-400'
                    }`}
                  >
                    {r.description}
                  </span>
                  {/* Active indicator dot */}
                  {selectedRole === r.value && (
                    <div className="absolute -top-1 -right-1 h-3 w-3 rounded-full border-2 border-white bg-[#7C6CE7]" />
                  )}
                </label>
              ))}
            </div>
          </fieldset>

          {/* Email */}
          <label className="mt-6 block text-sm font-medium text-slate-700">
            Email address
            <input
              ref={emailRef}
              type="email"
              className="mt-1.5 w-full rounded-lg border border-[#DCD6FF] px-3 py-2.5 text-sm text-[#312E81] outline-none transition-colors placeholder:text-slate-400 focus:border-[#7C6CE7] focus:ring-2 focus:ring-[#B8B5FF]/40"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@company.com"
              required
              autoComplete="email"
              disabled={loading}
            />
          </label>

          {/* Password */}
          <label className="mt-4 block text-sm font-medium text-slate-700">
            Password
            <input
              type="password"
              className="mt-1.5 w-full rounded-lg border border-[#DCD6FF] px-3 py-2.5 text-sm text-[#312E81] outline-none transition-colors placeholder:text-slate-400 focus:border-[#7C6CE7] focus:ring-2 focus:ring-[#B8B5FF]/40"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              autoComplete="current-password"
              disabled={loading}
            />
          </label>

          {/* Remember me */}
          <div className="mt-4 flex items-center">
            <label className="flex items-center gap-2 text-sm text-slate-600">
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="h-4 w-4 rounded border-[#DCD6FF] text-[#7C6CE7] focus:ring-[#B8B5FF]"
                disabled={loading}
              />
              Remember me
            </label>
          </div>

          {/* Error */}
          {error && (
            <div className="mt-4 flex items-start gap-2 rounded-lg border border-red-200 bg-red-50 p-3">
              <svg className="mt-0.5 h-4 w-4 shrink-0 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z" clipRule="evenodd" />
              </svg>
              <p className="text-sm text-red-700">{error}</p>
            </div>
          )}

          {/* Submit */}
          <button
            type="submit"
            disabled={loading}
            className="mt-6 flex w-full items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-[#7C6CE7] to-[#6D28D9] px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-[#7C6CE7]/30 transition-all duration-200 hover:shadow-xl hover:shadow-[#7C6CE7]/40 focus:outline-none focus:ring-2 focus:ring-[#B8B5FF] disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <svg className="animate-spin-smooth h-4 w-4" viewBox="0 0 24 24" fill="none">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Signing in…
              </>
            ) : (
              'Sign in'
            )}
          </button>

          {/* Footer */}
          <p className="mt-6 text-center text-xs text-slate-400">
            Secured by Supabase Authentication
          </p>
        </form>
      </div>
    </div>
  );
}