<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { API_URL, apiFetch } from '../services/api'
import { useAuth } from '../composables/useAuth'
import AppHeader from '../components/AppHeader.vue'

const route = useRoute()
const { user, authReady } = useAuth()
const restaurant = ref(null)
const loading = ref(true)
const error = ref('')
const activeCategory = ref('all')
const canEdit = ref(false)
let accessRequest = 0

async function checkAccess() {
  const requestId = ++accessRequest
  canEdit.value = false
  if (!authReady.value || !user.value || !restaurant.value) return
  try {
    const response = await apiFetch('/api/my/restaurants')
    if (!response.ok) return
    const restaurants = await response.json()
    if (requestId === accessRequest) {
      canEdit.value = restaurants.some(item => item.id === restaurant.value?.id)
    }
  } catch {
    canEdit.value = false
  }
}

async function loadMenu() {
  loading.value = true
  error.value = ''
  restaurant.value = null
  activeCategory.value = 'all'
  canEdit.value = false
  try {
    const slug = encodeURIComponent(route.params.slug)
    const response = await fetch(`${API_URL}/api/restaurants/${slug}/menu`)
    if (!response.ok) throw new Error('Jelovnik nije moguće učitati.')
    restaurant.value = await response.json()
    await checkAccess()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const visibleCategories = computed(() => {
  if (!restaurant.value) return []
  return activeCategory.value === 'all'
    ? restaurant.value.categories
    : restaurant.value.categories.filter(category => category.id === activeCategory.value)
})

function formatPrice(price) {
  return new Intl.NumberFormat('hr-HR', { style: 'currency', currency: 'EUR' }).format(Number(price))
}

onMounted(loadMenu)
watch(() => route.params.slug, loadMenu)
watch([user, authReady], () => { checkAccess() })
</script>

<template>
  <div class="min-h-screen bg-stone-50 text-stone-900">
    <AppHeader mode="menu" :menu-slug="restaurant?.slug ?? ''" :can-edit="canEdit" />
    <main class="mx-auto max-w-5xl px-5 py-8">
      <p v-if="loading" class="text-center text-stone-500">Učitavanje jelovnika...</p>
      <p v-else-if="error" class="text-center text-red-600">{{ error }}</p>
      <template v-else-if="restaurant">
        <section class="rounded-3xl bg-orange-50 px-6 py-10 sm:px-10">
          <p class="mb-2 text-sm font-semibold uppercase tracking-widest text-orange-600">Dobrodošli</p>
          <h2 class="text-3xl font-bold sm:text-5xl">{{ restaurant.name }}</h2>
          <p class="mt-4 max-w-xl text-stone-600">{{ restaurant.description }}</p>
        </section>
        <nav class="my-8 flex gap-3 overflow-x-auto pb-2" aria-label="Kategorije jelovnika">
          <button @click="activeCategory = 'all'" :class="activeCategory === 'all' ? 'bg-orange-500 text-white' : 'bg-white text-stone-700 border border-stone-200'" class="shrink-0 rounded-full px-5 py-2.5 text-sm font-medium transition">Sve</button>
          <button v-for="category in restaurant.categories" :key="category.id" @click="activeCategory = category.id" :class="activeCategory === category.id ? 'bg-orange-500 text-white' : 'bg-white text-stone-700 border border-stone-200'" class="shrink-0 rounded-full px-5 py-2.5 text-sm font-medium transition">{{ category.name }}</button>
        </nav>
        <section v-for="category in visibleCategories" :key="category.id" class="mb-10">
          <h3 class="mb-5 text-2xl font-bold">{{ category.name }}</h3>
          <div class="grid gap-4 md:grid-cols-2">
            <article v-for="product in category.products" :key="product.id" class="overflow-hidden rounded-2xl border border-stone-200 bg-white shadow-sm transition hover:shadow-md">
              <div class="flex h-full flex-col sm:flex-row">
                <img v-if="product.image_url" :src="product.image_url" :alt="product.name" loading="lazy" class="h-48 w-full object-cover sm:h-auto sm:w-40" />
                <div class="flex flex-1 flex-col justify-between p-5">
                  <div><h4 class="text-lg font-semibold">{{ product.name }}</h4><p class="mt-2 text-sm leading-relaxed text-stone-500">{{ product.description }}</p></div>
                  <p class="mt-4 text-lg font-bold text-orange-600">{{ formatPrice(product.price) }}</p>
                </div>
              </div>
            </article>
          </div>
        </section>
      </template>
    </main>
    <footer class="border-t border-stone-200 py-6 text-center text-sm text-stone-400">Powered by Dineria</footer>
  </div>
</template>
