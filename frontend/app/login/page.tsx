'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { useAuth } from '@/context/AuthProvider';

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(email, password, rememberMe);
      router.push('/');
    } catch (err: any) {
      setError(err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleForgotPassword = async (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
    e.preventDefault();
    if (!email) {
      setError('Please enter your email');
      return;
    }
    try {
      // For demo, we just show a message
      alert('Password reset email sent to ' + email);
    } catch (err: any) {
      setError(err.message || 'Failed to send reset email');
    }
  };

  return (
    <section className="flex min-h-[calc(100vh-4rem)] items-center justify-center px-4">
      <form
        className="w-full max-w-md rounded-2xl border border-[#E9E5FF] bg-white p-7 shadow-xl shadow-[#B8B5FF]/15"
        onSubmit={handleSubmit}
      >
        <div className="flex size-11 items-center justify-center rounded-xl bg-gradient-to-br from-[#C4B5FD] to-[#CFFAFE] text-[#312E81]">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="size-5"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21h-4.5A2.25 2.25 0 019 18.75V8.25"
            />
          </svg>
        </div>
        <p className="mt-5 text-xs font-semibold uppercase tracking-[0.18em] text-[#818CF8]">
          Sign in to your account
        </p>
        <h1 className="mt-2 text-2xl font-extrabold text-[#312E81]">
          Welcome back
        </h1>
        <p className="mt-2 text-sm text-[#5B54A6]">
          Access your workspace and continue your operations.
        </p>

        <label className="mt-6 block text-sm font-medium text-slate-700">
          Email address
          <input
            type="email"
            className="mt-1.5 w-full rounded-lg border border-[#DCD6FF] px-3 py-2.5 outline-none focus:border-[#A5B4FC]"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>

        <label className="mt-4 block text-sm font-medium text-slate-700">
          Password
          <input
            type="password"
            className="mt-1.5 w-full rounded-lg border border-[#DCD6FF] px-3 py-2.5 outline-none focus:border-[#A5B4FC]"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>

        <div className="mt-4 flex items-center">
          <label className="flex items-center gap-2 text-sm font-medium text-slate-700">
            <input
              type="checkbox"
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
              className="h-4 w-4 text-[#A5B4FC] border-gray-300 rounded"
            />
            Remember me
          </label>
        </div>

        {error && (
          <p className="mt-4 rounded-lg bg-[#FFF1F7] p-3 text-sm text-[#A34A72]">
            {error}
          </p>
        )}

        <div className="mt-6 flex items-center justify-between">
          <button
            type="button"
            onClick={handleForgotPassword}
            className="text-sm font-medium text-[#818CF8] hover:underline"
          >
            Forgot password?
          </button>
          <button
            type="submit"
            disabled={loading}
            className="disabled:opacity-50 w-full md:w-auto px-4 py-2.5 rounded-lg bg-[#7C6CE7] px-4 py-2.5 text-sm font-medium text-white shadow-sm shadow-[#B8B5FF]/50"
          >
            {loading ? 'Signing in...' : 'Sign in'}
          </button>
        </div>

        <p className="mt-6 text-xs text-slate-500">
          Don't have an account?{' '}
          <a href="/signup" className="text-[#7C6CE7] hover:underline">
            Sign up
          </a>
        </p>
      </form>
    </section>
  );
}