
import { supabase } from '../lib/supabase'

export const API_URL =
  import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export async function checkBackendHealth() {
  const response = await fetch(`${API_URL}/api/health`)

  if (!response.ok) {
    throw new Error('Backend is unavailable')
  }

  return await response.json()
}

export async function apiFetch(endpoint, options = {}) {
  const {
    data: { session },
    error
  } = await supabase.auth.getSession()

  if (error || !session?.access_token) {
    throw new Error('Nisi prijavljen. Prijavi se ponovno.')
  }

  const headers = new Headers(options.headers)
  headers.set('Authorization', `Bearer ${session.access_token}`)

  return fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers
  })
}
