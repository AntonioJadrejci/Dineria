
import { supabase } from '../lib/supabase'

const API_URL = 'http://127.0.0.1:8000'

// Postojeća funkcija - ostaje!
export async function checkBackendHealth() {
  const response = await fetch(`${API_URL}/api/health`)

  if (!response.ok) {
    throw new Error('Backend is unavailable')
  }

  return await response.json()
}

// Nova funkcija - automatski šalje JWT token
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
