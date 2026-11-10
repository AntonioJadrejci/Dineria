<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../lib/supabase'
import { useAuth } from '../composables/useAuth'

const props = defineProps({
  mode: { type: String, default: 'default' },
  menuSlug: { type: String, default: '' },
  canEdit: { type: Boolean, default: false }
})
const router = useRouter()
const { user, authReady } = useAuth()
const signingOut = ref(false)

function editMenu() {
  if (!props.menuSlug) return
  sessionStorage.setItem('dineria-selected-restaurant', props.menuSlug)
  router.push('/admin')
}
async function logout() {
  if (signingOut.value) return
  signingOut.value = true
  const { error } = await supabase.auth.signOut()
  signingOut.value = false
  if (error) {
    window.alert('Odjava nije uspjela. Pokušaj ponovno.')
    return
  }
  sessionStorage.removeItem('dineria-selected-restaurant')
  await router.push('/')
}
</script>

<template>
  <header class="border-b border-stone-200 bg-white">
    <div class="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-3 px-5 py-5">
      <RouterLink to="/" class="text-2xl font-extrabold tracking-tight text-stone-900" aria-label="Dineria - početna">
        dineria<span class="text-orange-500">.</span>
        <span v-if="mode === 'admin'" class="ml-2 text-sm font-medium text-stone-400">Admin</span>
      </RouterLink>
      <nav v-if="authReady" class="flex flex-wrap items-center justify-end gap-3 sm:gap-5" aria-label="Glavna navigacija">
        <template v-if="user">
          <RouterLink v-if="mode === 'admin' && menuSlug" :to="`/menu/${encodeURIComponent(menuSlug)}`" class="text-sm font-semibold text-orange-600 hover:text-orange-700">Pogledaj jelovnik</RouterLink>
          <button v-else-if="mode === 'menu' && canEdit" type="button" @click="editMenu" class="rounded-xl bg-orange-500 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-orange-600">Admin Edit</button>
          <RouterLink v-else-if="mode !== 'admin'" to="/admin" class="text-sm font-semibold text-stone-700 hover:text-orange-600">Dashboard</RouterLink>
          <button type="button" :disabled="signingOut" @click="logout" class="text-sm font-semibold text-red-600 hover:text-red-700 disabled:opacity-50">{{ signingOut ? 'Odjava...' : 'Odjava' }}</button>
        </template>
        <template v-else>
          <RouterLink to="/login" class="text-sm font-semibold text-stone-700 hover:text-orange-600">Prijava</RouterLink>
          <RouterLink to="/register" class="rounded-xl bg-orange-500 px-4 py-2.5 text-sm font-semibold text-white hover:bg-orange-600">Registracija</RouterLink>
        </template>
      </nav>
    </div>
  </header>
</template>
