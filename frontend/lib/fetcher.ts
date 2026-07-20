import { supabase } from '@/lib/supabaseClient'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

/**
 * Fetch wrapper that automatically attaches the current Supabase session token
 * as an Authorization Bearer header.Throws on non-ok responses.
 */
export async function fetcher<T = any>(
  input: RequestInfo,
  init: RequestInit = {}
): Promise<T> {
  const session = await supabase.auth.getSession()
  const token = session.data?.session?.access_token
  const headers = new Headers(init.headers ?? {})
  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }
  const url = typeof input === 'string' && input.startsWith('/') ? `${API_BASE}${input}` : input
  const response = await fetch(url, { ...init, headers })
  if (!response.ok) {
    // Throw a generic error; callers can catch and use .message
    throw new Error(`HTTP ${response.status}`)
  }
  return response.json()
}