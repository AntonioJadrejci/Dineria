<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../lib/supabase'
import AppHeader from '../components/AppHeader.vue'

const router = useRouter()
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')
onMounted(async () => {
  const { data } = await supabase.auth.getUser()
  if (data.user) router.replace('/admin')
})
async function register() {
  if (loading.value) return

  error.value = ''
  success.value = ''

  if (password.value.length < 8) {
    error.value = 'Lozinka mora imati najmanje 8 znakova.'
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = 'Lozinke se ne podudaraju.'
    return
  }

  loading.value = true

  try {
    const { data, error: registerError } = await supabase.auth.signUp({
      email: email.value.trim(),
      password: password.value
    })

    if (registerError) throw registerError

    if (data.session) {
      await router.replace('/admin')
    } else {
      error.value = 'Račun je kreiran, ali automatska prijava nije uspjela. Provjeri postavku Confirm email u Supabaseu.'
    }
  } catch (err) {
    error.value = err.message || 'Registracija nije uspjela.'
  } finally {
    loading.value = false
  }
}
</script>
<template>
  <div class="min-h-screen bg-stone-50 text-stone-900">
    <AppHeader />
    <main class="flex items-center justify-center px-4 py-10 sm:py-20">
      <div class="w-full max-w-md rounded-3xl border border-stone-200 bg-white p-8 shadow-sm">
        <div class="mb-8 text-center"><RouterLink to="/" class="text-4xl font-extrabold">dineria<span class="text-orange-500">.</span></RouterLink><h2 class="mt-6 text-2xl font-bold">Kreiraj račun</h2><p class="mt-2 text-stone-500">Registriraj se i izradi digitalni jelovnik za svoj restoran.</p></div>
        <form @submit.prevent="register" class="space-y-5">
          <div><label for="email" class="mb-2 block text-sm font-medium">Email</label><input id="email" v-model="email" type="email" autocomplete="email" required placeholder="admin@restoran.hr" class="w-full rounded-xl border border-stone-200 px-4 py-3 outline-none focus:border-orange-500" /></div>
          <div><label for="password" class="mb-2 block text-sm font-medium">Lozinka</label><input id="password" v-model="password" type="password" autocomplete="new-password" minlength="8" required placeholder="Najmanje 8 znakova" class="w-full rounded-xl border border-stone-200 px-4 py-3 outline-none focus:border-orange-500" /></div>
          <div><label for="confirm-password" class="mb-2 block text-sm font-medium">Potvrdi lozinku</label><input id="confirm-password" v-model="confirmPassword" type="password" autocomplete="new-password" required placeholder="Ponovi lozinku" class="w-full rounded-xl border border-stone-200 px-4 py-3 outline-none focus:border-orange-500" /></div>
          <p v-if="error" role="alert" class="text-sm text-red-600">{{ error }}</p><p v-if="success" role="status" class="text-sm text-green-600">{{ success }}</p>
          <button type="submit" :disabled="loading" class="w-full rounded-xl bg-orange-500 px-4 py-3 font-semibold text-white transition hover:bg-orange-600 disabled:opacity-50">{{ loading ? 'Registracija...' : 'Registriraj se' }}</button>
        </form>
        <p class="mt-6 text-center text-sm text-stone-500">Već imaš račun? <RouterLink to="/login" class="font-semibold text-orange-600 hover:text-orange-700">Prijavi se</RouterLink></p>
      </div>
    </main>
  </div>
</template>
