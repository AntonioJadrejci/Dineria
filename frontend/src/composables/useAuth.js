import { ref } from 'vue'
import { supabase } from '../lib/supabase'

const user = ref(null)
const authReady = ref(false)
let initialized = false

export function useAuth() {
  if (!initialized) {
    initialized = true
    supabase.auth.onAuthStateChange((_event, session) => {
      user.value = session?.user ?? null
      authReady.value = true
    })
    supabase.auth.getSession().then(({ data }) => {
      user.value = data.session?.user ?? null
      authReady.value = true
    }).catch(() => { authReady.value = true })
  }
  return { user, authReady }
}
