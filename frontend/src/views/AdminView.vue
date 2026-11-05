
<script setup>
import { ref, computed, onMounted } from 'vue'

const restaurant = ref(null)
const loading = ref(true)
const error = ref('')

const API_URL = 'http://127.0.0.1:8000'
const RESTAURANT_SLUG = 'dineria-demo'


const showProductForm = ref(false)
const saving = ref(false)
const formError = ref('')

const productForm = ref({
  name: '',
  description: '',
  price: '',
  category_id: ''
})

const editingProductId = ref(null)

async function loadDashboard() {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch(
      `${API_URL}/api/restaurants/${RESTAURANT_SLUG}/menu`
    )

    if (!response.ok) {
      throw new Error('Nije moguće učitati podatke.')
    }

    restaurant.value = await response.json()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const products = computed(() => {
  if (!restaurant.value) return []

  return restaurant.value.categories.flatMap(
    category => category.products.map(product => ({
      ...product,
      categoryName: category.name
    }))
  )
})

const categoryCount = computed(() =>
  restaurant.value?.categories.length ?? 0
)

const productCount = computed(() => products.value.length)

function formatPrice(price) {
  return new Intl.NumberFormat('hr-HR', {
    style: 'currency',
    currency: 'EUR'
  }).format(Number(price))
}


function openProductForm(product = null) {
  editingProductId.value = product?.id ?? null

  productForm.value = {
    name: product?.name ?? '',
    description: product?.description ?? '',
    price: product?.price ?? '',
    category_id: product?.category_id ??
      restaurant.value?.categories[0]?.id ?? ''
  }

  formError.value = ''
  showProductForm.value = true
}


function closeProductForm() {
  showProductForm.value = false
  formError.value = ''
}


async function saveProduct() {
  if (saving.value) return

  saving.value = true
  formError.value = ''

  try {
    const isEditing = editingProductId.value !== null

    const url = isEditing
      ? `${API_URL}/api/products/${editingProductId.value}`
      : `${API_URL}/api/products`

    const response = await fetch(url, {
      method: isEditing ? 'PATCH' : 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: productForm.value.name.trim(),
        description: productForm.value.description.trim(),
        price: productForm.value.price,
        category_id: Number(productForm.value.category_id)
      })
    })

    if (!response.ok) {
      throw new Error('Spremanje proizvoda nije uspjelo.')
    }

    closeProductForm()
    await loadDashboard()
  } catch (err) {
    formError.value = err.message
  } finally {
    saving.value = false
  }
}


async function deleteProduct(product) {
  const confirmed = window.confirm(
    `Jesi li siguran da želiš obrisati proizvod "${product.name}"?`
  )

  if (!confirmed) return

  try {
    const response = await fetch(
      `${API_URL}/api/products/${product.id}`,
      {
        method: 'DELETE'
      }
    )

    if (!response.ok) {
      throw new Error('Brisanje proizvoda nije uspjelo.')
    }

    await loadDashboard()
  } catch (err) {
    window.alert(err.message)
  }
}


onMounted(loadDashboard)
</script>

<template>
  <div class="min-h-screen bg-stone-50 text-stone-900">
    <header class="border-b border-stone-200 bg-white">
      <div class="mx-auto flex max-w-6xl items-center justify-between px-5 py-5">
        <h1 class="text-2xl font-extrabold">
          dineria<span class="text-orange-500">.</span>
          <span class="ml-2 text-sm font-medium text-stone-400">Admin</span>
        </h1>

        <a
          :href="`/menu/${RESTAURANT_SLUG}`"
          class="text-sm font-medium text-orange-600 hover:text-orange-700"
        >
          Pogledaj jelovnik
        </a>
      </div>
    </header>

    <main class="mx-auto max-w-6xl px-5 py-10">
      <div v-if="loading" class="text-stone-500">
        Učitavanje dashboarda...
      </div>

      <div v-else-if="error" class="text-red-600">
        {{ error }}
      </div>

      <template v-else-if="restaurant">
        <div class="mb-8">
          <p class="mb-2 text-sm font-semibold text-orange-600">
            ADMIN DASHBOARD
          </p>

          <h2 class="text-3xl font-bold">
            {{ restaurant.name }}
          </h2>

          <p class="mt-2 text-stone-500">
            Upravljaj kategorijama i proizvodima svojeg restorana.
          </p>
        </div>

        <div class="mb-10 grid gap-4 sm:grid-cols-3">
          <div class="rounded-2xl border border-stone-200 bg-white p-6">
            <p class="text-sm text-stone-500">Kategorije</p>
            <p class="mt-2 text-3xl font-bold">{{ categoryCount }}</p>
          </div>

          <div class="rounded-2xl border border-stone-200 bg-white p-6">
            <p class="text-sm text-stone-500">Proizvodi</p>
            <p class="mt-2 text-3xl font-bold">{{ productCount }}</p>
          </div>

          <div class="rounded-2xl border border-stone-200 bg-white p-6">
            <p class="text-sm text-stone-500">Restoran</p>
            <p class="mt-2 text-lg font-bold">Aktivan</p>
          </div>
        </div>

        <section class="overflow-hidden rounded-2xl border border-stone-200 bg-white">
          <div class="flex items-center justify-between border-b border-stone-200 p-6">
            <h3 class="text-xl font-bold">Proizvodi</h3>

            
<button
  type="button"
  @click="openProductForm"
  class="rounded-xl bg-orange-500 px-4 py-2 text-sm font-semibold text-white transition hover:bg-orange-600"
>
  + Dodaj proizvod
</button>

          </div>

          <div class="divide-y divide-stone-100">
            <div
              v-for="product in products"
              :key="product.id"
              class="flex flex-wrap items-center justify-between gap-4 p-5"
            >
              <div>
                <h4 class="font-semibold">{{ product.name }}</h4>
                <p class="mt-1 text-sm text-stone-500">
                  {{ product.categoryName }}
                </p>
              </div>

              <div class="flex items-center gap-5">
                <span class="font-semibold text-orange-600">
                  {{ formatPrice(product.price) }}
                </span>

               
<button
  type="button"
  @click="openProductForm(product)"
  class="text-sm font-medium text-orange-600 hover:text-orange-700"
>
  Uredi
</button>


               
<button
  type="button"
  @click="deleteProduct(product)"
  class="text-sm font-medium text-red-500 transition hover:text-red-700"
>
  Obriši
</button>

              </div>
            </div>

            <p
              v-if="products.length === 0"
              class="p-6 text-sm text-stone-500"
            >
              Trenutačno nema proizvoda.
            </p>
          </div>
        </section>
      </template>
    </main>
  </div>
  
<div
  v-if="showProductForm"
  class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
>
  <div class="w-full max-w-lg rounded-3xl bg-white p-6 shadow-xl sm:p-8">
    <div class="mb-6 flex items-center justify-between">
     <h3 class="text-2xl font-bold">
  {{ editingProductId !== null ? 'Uredi proizvod' : 'Novi proizvod' }}
</h3>

      <button
        type="button"
        @click="closeProductForm"
        class="text-2xl text-stone-400 hover:text-stone-700"
        aria-label="Zatvori obrazac"
      >
        &times;
      </button>
    </div>

    <form @submit.prevent="saveProduct" class="space-y-5">
      <div>
        <label for="product-name" class="mb-2 block text-sm font-medium">
          Naziv proizvoda
        </label>

        <input
          id="product-name"
          v-model="productForm.name"
          type="text"
          required
          maxlength="150"
          placeholder="npr. Pizza Margherita"
          class="w-full rounded-xl border border-stone-200 px-4 py-3 outline-none focus:border-orange-500"
        />
      </div>

      <div>
        <label for="product-category" class="mb-2 block text-sm font-medium">
          Kategorija
        </label>

        <select
          id="product-category"
          v-model="productForm.category_id"
          required
          class="w-full rounded-xl border border-stone-200 bg-white px-4 py-3 outline-none focus:border-orange-500"
        >
          <option value="" disabled>Odaberi kategoriju</option>

          <option
            v-for="category in restaurant?.categories ?? []"
            :key="category.id"
            :value="category.id"
          >
            {{ category.name }}
          </option>
        </select>
      </div>

      <div>
        <label for="product-description" class="mb-2 block text-sm font-medium">
          Opis proizvoda
        </label>

        <textarea
          id="product-description"
          v-model="productForm.description"
          rows="3"
          placeholder="Sastojci i opis proizvoda..."
          class="w-full resize-none rounded-xl border border-stone-200 px-4 py-3 outline-none focus:border-orange-500"
        ></textarea>
      </div>

      <div>
        <label for="product-price" class="mb-2 block text-sm font-medium">
          Cijena (€)
        </label>

        <input
          id="product-price"
          v-model="productForm.price"
          type="number"
          min="0.01"
          max="99999999.99"
          step="0.01"
          required
          placeholder="10.50"
          class="w-full rounded-xl border border-stone-200 px-4 py-3 outline-none focus:border-orange-500"
        />
      </div>

      <p v-if="formError" role="alert" class="text-sm text-red-600">
        {{ formError }}
      </p>

      <div class="flex gap-3 pt-2">
        <button
          type="button"
          @click="closeProductForm"
          class="flex-1 rounded-xl border border-stone-200 px-4 py-3 font-medium hover:bg-stone-50"
        >
          Odustani
        </button>

        <button
          type="submit"
          :disabled="saving"
          class="flex-1 rounded-xl bg-orange-500 px-4 py-3 font-semibold text-white transition hover:bg-orange-600 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {{ saving ? 'Spremanje...' : editingProductId !== null ? 'Spremi promjene' : 'Dodaj proizvod' }}
        </button>
      </div>
    </form>
  </div>
</div>

</template>
