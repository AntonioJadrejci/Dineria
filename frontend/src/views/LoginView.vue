<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../lib/supabase'
import AppHeader from '../components/AppHeader.vue'

const router = useRouter()
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
onMounted(async () => {
  const { data } = await supabase.auth.getUser()
  if (data.user) router.replace('/admin')
})
async function login() {
  if (loading.value) return
  loading.value = true
  error.value = ''
  try {
    const { error: loginError } = await supabase.auth.signInWithPassword({ email: email.value.trim(), password: password.value })
    if (loginError) throw loginError
    await router.push('/admin')
  } catch {
    error.value = 'Prijava nije uspjela. Provjeri email i lozinku.'
  } finally { loading.value = false }
}
</script>
<template>
  <div class="min-h-screen bg-stone-50 text-stone-900">
    <AppHeader />
    <main class="flex items-center justify-center px-4 py-10 sm:py-20">
      <div class="w-full max-w-md rounded-3xl border border-stone-200 bg-white p-8 shadow-sm">
        <div class="mb-8 text-center">
          <RouterLink to="/" class="text-4xl font-extrabold">dineria<span class="text-orange-500">.</span></RouterLink>
          <p class="mt-3 text-stone-500">Prijavi se za upravljanje restoranom.</p>
        </div>
        <form @submit.prevent="login" class="space-y-5">
          <div><label for="email" class="mb-2 block text-sm font-medium">Email</label><input id="email" v-model="email" type="email" autocomplete="email" required placeholder="admin@restoran.hr" class="w-full rounded-xl border border-stone-200 px-4 py-3 outline-none focus:border-orange-500" /></div>
          <div><label for="password" class="mb-2 block text-sm font-medium">Lozinka</label><input id="password" v-model="password" type="password" autocomplete="current-password" required placeholder="Unesi lozinku" class="w-full rounded-xl border border-stone-200 px-4 py-3 outline-none focus:border-orange-500" /></div>
          <p v-if="error" role="alert" class="text-sm text-red-600">{{ error }}</p>
          <button type="submit" :disabled="loading" class="w-full rounded-xl bg-orange-500 px-4 py-3 font-semibold text-white transition hover:bg-orange-600 disabled:opacity-50">{{ loading ? 'Prijava...' : 'Prijavi se' }}</button>
        </form>
        <p class="mt-6 text-center text-xs text-stone-400">Dineria Restaurant Management</p>
      </div>
    </main>
  </div>
</template>
