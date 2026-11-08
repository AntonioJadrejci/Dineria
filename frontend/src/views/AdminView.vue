
<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiFetch } from '../services/api'

const API_URL = 'http://127.0.0.1:8000'
const restaurantSlug = computed(() => restaurant.value?.slug ?? '')
const hasNoRestaurant = ref(false)
const creatingRestaurant = ref(false)
const restaurantFormError = ref('')

const restaurantForm = ref({
  name: '',
  slug: '',
  description: ''
})

const restaurant = ref(null)
const loading = ref(true)
const error = ref('')

const showProductForm = ref(false)
const saving = ref(false)
const formError = ref('')
const editingProductId = ref(null)
const selectedImage = ref(null)
const currentImageUrl = ref(null)

const productForm = ref({
  name: '',
  description: '',
  price: '',
  category_id: ''
})


const showCategoryForm = ref(false)
const editingCategoryId = ref(null)
const categoryName = ref('')
const categorySaving = ref(false)
const categoryError = ref('')



// Dohvaćanje podataka restorana

async function loadDashboard() {
  loading.value = true
  error.value = ''
  hasNoRestaurant.value = false

  try {
    // Pronađi restorane prijavljenog korisnika
    const myRestaurantsResponse = await apiFetch('/api/my/restaurants')

    if (!myRestaurantsResponse.ok) {
      throw new Error('Nije moguće dohvatiti tvoje restorane.')
    }

    const myRestaurants = await myRestaurantsResponse.json()

    if (myRestaurants.length === 0) {
      restaurant.value = null
      hasNoRestaurant.value = true
      return
    }

    // Zasad prikazujemo prvi restoran korisnika
    const slug = myRestaurants[0].slug

    const response = await fetch(
      `${API_URL}/api/restaurants/${encodeURIComponent(slug)}/menu`
    )

    if (!response.ok) {
      throw new Error('Nije moguće učitati podatke restorana.')
    }

    restaurant.value = await response.json()
  } catch (err) {
    restaurant.value = null
    error.value = err.message
  } finally {
    loading.value = false
  }
}


async function createRestaurant() {
  if (creatingRestaurant.value) return

  creatingRestaurant.value = true
  restaurantFormError.value = ''

  try {
    const response = await apiFetch('/api/restaurants', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: restaurantForm.value.name.trim(),
        slug: restaurantForm.value.slug.trim().toLowerCase(),
        description: restaurantForm.value.description.trim()
      })
    })

    if (response.status === 409) {
      throw new Error('Ova URL oznaka restorana već postoji. Odaberi drugu.')
    }

    if (!response.ok) {
      throw new Error('Kreiranje restorana nije uspjelo.')
    }

    // Ponovno učitaj dashboard novog restorana
    await loadDashboard()
  } catch (err) {
    restaurantFormError.value = err.message
  } finally {
    creatingRestaurant.value = false
  }
}



// Pretvaranje kategorija u jedinstveni popis proizvoda
const products = computed(() => {
  if (!restaurant.value) return []

  return restaurant.value.categories.flatMap(category =>
    category.products.map(product => ({
      ...product,
      categoryName: category.name
    }))
  )
})

const categoryCount = computed(
  () => restaurant.value?.categories.length ?? 0
)

const productCount = computed(
  () => products.value.length
)

// Formatiranje cijena
function formatPrice(price) {
  return new Intl.NumberFormat('hr-HR', {
    style: 'currency',
    currency: 'EUR'
  }).format(Number(price))
}

// Otvaranje obrasca za dodavanje ili uređivanje
function openProductForm(product = null) {
  selectedImage.value = null
  editingProductId.value = product?.id ?? null
  currentImageUrl.value = product?.image_url ?? null

  productForm.value = {
    name: product?.name ?? '',
    description: product?.description ?? '',
    price: product?.price ?? '',
    category_id:
      product?.category_id ??
      restaurant.value?.categories[0]?.id ??
      ''
  }

  formError.value = ''
  showProductForm.value = true
}

// Zatvaranje obrasca
function closeProductForm() {
  if (saving.value) return

  showProductForm.value = false
  formError.value = ''
  selectedImage.value = null
  editingProductId.value = null
  currentImageUrl.value = null
}

// Odabir i provjera fotografije
function handleImageChange(event) {
  const file = event.target.files?.[0]

  selectedImage.value = null
  formError.value = ''

  if (!file) return

  const allowedTypes = [
    'image/jpeg',
    'image/png',
    'image/webp'
  ]

  if (!allowedTypes.includes(file.type)) {
    formError.value = 'Dopušteni su samo JPG, PNG i WebP.'
    event.target.value = ''
    return
  }

  if (file.size > 5 * 1024 * 1024) {
    formError.value = 'Fotografija ne smije biti veća od 5 MB.'
    event.target.value = ''
    return
  }

  selectedImage.value = file
}

// Slanje fotografije FastAPI backendu
async function uploadProductImage(productId) {
  if (!selectedImage.value) return

  const formData = new FormData()
  formData.append('file', selectedImage.value)

  const response = await apiFetch(
    `/api/products/${productId}/image`,
    {
      method: 'POST',
      body: formData
    }
  )

  if (!response.ok) {
    throw new Error('Upload fotografije nije uspio.')
  }

  return await response.json()
}

// Dodavanje i uređivanje proizvoda
async function saveProduct() {
  if (saving.value) return

  saving.value = true
  formError.value = ''

  try {
    const isEditing = editingProductId.value !== null

    const url = isEditing
      ? `/api/products/${editingProductId.value}`
      : `/api/products`

    const response = await apiFetch(url, {
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

    const savedProduct = await response.json()

    // Ako je odabrana fotografija, šaljemo je zasebno
    if (selectedImage.value) {
      try {
        await uploadProductImage(savedProduct.id)
      } catch {
        await loadDashboard()

        throw new Error(
          'Proizvod je spremljen, ali fotografija nije. ' +
          'Pokušaj ponovno dodati fotografiju.'
        )
      }
    }

    // Zatvaranje nakon uspješnog spremanja
    showProductForm.value = false
    selectedImage.value = null
    editingProductId.value = null
    currentImageUrl.value = null

    await loadDashboard()
  } catch (err) {
    formError.value = err.message
  } finally {
    saving.value = false
  }
}

// Brisanje proizvoda
async function deleteProduct(product) {
  const confirmed = window.confirm(
    `Jesi li siguran da želiš obrisati proizvod "${product.name}"?`
  )

  if (!confirmed) return

  try {
    const response = await apiFetch(
      `/api/products/${product.id}`,
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


function openCategoryForm(category = null) {
  editingCategoryId.value = category?.id ?? null
  categoryName.value = category?.name ?? ''
  categoryError.value = ''
  showCategoryForm.value = true
}

function closeCategoryForm() {
  if (categorySaving.value) return

  showCategoryForm.value = false
  categoryError.value = ''
}

async function saveCategory() {
  if (categorySaving.value) return

  const name = categoryName.value.trim()

  if (!name) {
    categoryError.value = 'Unesi naziv kategorije.'
    return
  }

  categorySaving.value = true
  categoryError.value = ''

  try {
    const isEditing = editingCategoryId.value !== null

    const url = isEditing
      ? `/api/categories/${editingCategoryId.value}`
      : `/api/categories`

    const body = isEditing
      ? { name }
      : {
          name,
          restaurant_id: restaurant.value.id
        }

    const response = await apiFetch(url, {
      method: isEditing ? 'PATCH' : 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    })

    if (!response.ok) {
      throw new Error('Spremanje kategorije nije uspjelo.')
    }

    showCategoryForm.value = false
    await loadDashboard()
  } catch (err) {
    categoryError.value = err.message
  } finally {
    categorySaving.value = false
  }
}

async function deleteCategory(category) {
  if (category.products.length > 0) {
    window.alert(
      'Ne možeš obrisati kategoriju koja sadrži proizvode.'
    )
    return
  }

  const confirmed = window.confirm(
    `Želiš li obrisati kategoriju "${category.name}"?`
  )

  if (!confirmed) return

  try {
    const response = await apiFetch(
      `/api/categories/${category.id}`,
      { method: 'DELETE' }
    )

    if (!response.ok) {
      throw new Error('Brisanje kategorije nije uspjelo.')
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
    <!-- HEADER -->
    <header class="border-b border-stone-200 bg-white">
      <div
        class="mx-auto flex max-w-6xl items-center justify-between px-5 py-5"
      >
        <h1 class="text-2xl font-extrabold">
          dineria<span class="text-orange-500">.</span>
          <span class="ml-2 text-sm font-medium text-stone-400">
            Admin
          </span>
        </h1>

        <RouterLink
          v-if="restaurantSlug"
          :to="`/menu/${restaurantSlug}`"
          class="text-sm font-medium text-orange-600 hover:text-orange-700"
        >
          Pogledaj jelovnik
        </RouterLink>
      </div>
    </header>

    <!-- DASHBOARD -->
    <main class="mx-auto max-w-6xl px-5 py-10">
      <p v-if="loading" class="text-stone-500">
        Učitavanje dashboarda...
      </p>

      <p v-else-if="error" class="text-red-600">
        {{ error }}
      </p>

      
<div
  v-else-if="hasNoRestaurant"
  class="mx-auto max-w-xl rounded-3xl border border-stone-200 bg-white p-8 shadow-sm"
>
  <div class="mb-8 text-center">
    <h2 class="text-3xl font-bold">
      Dobrodošao u Dineriju!
    </h2>

    <p class="mt-3 text-stone-500">
      Kreiraj svoj restoran i počni uređivati digitalni jelovnik.
    </p>
  </div>

  <form @submit.prevent="createRestaurant" class="space-y-5">
    <div>
      <label class="mb-2 block text-sm font-medium">
        Naziv restorana
      </label>

      <input
        v-model="restaurantForm.name"
        type="text"
        required
        maxlength="150"
        placeholder="npr. Pizzeria Roma"
        class="w-full rounded-xl border border-stone-200 px-4 py-3 outline-none focus:border-orange-500"
      />
    </div>

    <div>
      <label class="mb-2 block text-sm font-medium">
        URL oznaka restorana
      </label>

      <input
        v-model="restaurantForm.slug"
        type="text"
        required
        pattern="[a-z0-9]+(-[a-z0-9]+)*"
        maxlength="150"
        placeholder="npr. pizzeria-roma"
        class="w-full rounded-xl border border-stone-200 px-4 py-3 outline-none focus:border-orange-500"
      />

      <p class="mt-2 text-xs text-stone-400">
        Koristi mala slova, brojeve i crtice, bez razmaka.
        Primjer: pizzeria-roma
      </p>
    </div>

    <div>
      <label class="mb-2 block text-sm font-medium">
        Opis restorana (neobavezno)
      </label>

      <textarea
        v-model="restaurantForm.description"
        rows="3"
        maxlength="1000"
        placeholder="Kratki opis restorana..."
        class="w-full resize-none rounded-xl border border-stone-200 px-4 py-3 outline-none focus:border-orange-500"
      ></textarea>
    </div>

    <p
      v-if="restaurantFormError"
      role="alert"
      class="text-sm text-red-600"
    >
      {{ restaurantFormError }}
    </p>

    <button
      type="submit"
      :disabled="creatingRestaurant"
      class="w-full rounded-xl bg-orange-500 px-4 py-3 font-semibold text-white transition hover:bg-orange-600 disabled:opacity-50"
    >
      {{ creatingRestaurant ? 'Kreiranje...' : 'Kreiraj restoran' }}
    </button>
  </form>
</div>


      <template v-else-if="restaurant">
        <!-- Naslov -->
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

        <!-- Statistika -->
        <div class="mb-10 grid gap-4 sm:grid-cols-3">
          <div
            class="rounded-2xl border border-stone-200 bg-white p-6"
          >
            <p class="text-sm text-stone-500">Kategorije</p>
            <p class="mt-2 text-3xl font-bold">
              {{ categoryCount }}
            </p>
          </div>

          <div
            class="rounded-2xl border border-stone-200 bg-white p-6"
          >
            <p class="text-sm text-stone-500">Proizvodi</p>
            <p class="mt-2 text-3xl font-bold">
              {{ productCount }}
            </p>
          </div>

          <div
            class="rounded-2xl border border-stone-200 bg-white p-6"
          >
            <p class="text-sm text-stone-500">Restoran</p>
            <p class="mt-2 text-lg font-bold">
              Aktivan
            </p>
          </div>
        </div>

<!-- KATEGORIJE -->
<section
  class="mb-8 overflow-hidden rounded-2xl border border-stone-200 bg-white"
>
  <div
    class="flex flex-wrap items-center justify-between gap-4 border-b border-stone-200 p-6"
  >
    <h3 class="text-xl font-bold">Kategorije</h3>

    <button
      type="button"
      @click="openCategoryForm()"
      class="rounded-xl bg-orange-500 px-4 py-2 text-sm font-semibold text-white hover:bg-orange-600"
    >
      + Dodaj kategoriju
    </button>
  </div>

  <div class="divide-y divide-stone-100">
    <div
      v-for="category in restaurant.categories"
      :key="category.id"
      class="flex flex-wrap items-center justify-between gap-4 p-5"
    >
      <div>
        <h4 class="font-semibold">
          {{ category.name }}
        </h4>

        <p class="mt-1 text-sm text-stone-500">
          {{ category.products.length }} proizvoda
        </p>
      </div>

      <div class="flex items-center gap-5">
        <button
          type="button"
          @click="openCategoryForm(category)"
          class="text-sm font-medium text-orange-600 hover:text-orange-700"
        >
          Uredi
        </button>

        <button
          type="button"
          @click="deleteCategory(category)"
          class="text-sm font-medium text-red-500 hover:text-red-700"
        >
          Obriši
        </button>
      </div>
    </div>

    <p
      v-if="restaurant.categories.length === 0"
      class="p-6 text-sm text-stone-500"
    >
      Još nema kategorija.
    </p>
  </div>
</section>

        <!-- Popis proizvoda -->
        <section
          class="overflow-hidden rounded-2xl border border-stone-200 bg-white"
        >
          <div
            class="flex flex-wrap items-center justify-between gap-4 border-b border-stone-200 p-6"
          >
            <h3 class="text-xl font-bold">Proizvodi</h3>

            <button
              type="button"
              @click="openProductForm()"
              :disabled="categoryCount === 0"
              class="rounded-xl bg-orange-500 px-4 py-2 text-sm font-semibold text-white transition hover:bg-orange-600 disabled:cursor-not-allowed disabled:opacity-50"
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
              <!-- Fotografija i naziv -->
              <div class="flex min-w-0 items-center gap-4">
                <img
                  v-if="product.image_url"
                  :src="product.image_url"
                  :alt="product.name"
                  class="h-16 w-16 shrink-0 rounded-xl object-cover"
                />

                <div
                  v-else
                  class="flex h-16 w-16 shrink-0 items-center justify-center rounded-xl bg-stone-100 text-xs text-stone-400"
                >
                  Bez slike
                </div>

                <div class="min-w-0">
                  <h4 class="font-semibold">
                    {{ product.name }}
                  </h4>

                  <p class="mt-1 text-sm text-stone-500">
                    {{ product.categoryName }}
                  </p>
                </div>
              </div>

              <!-- Cijena i akcije -->
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
                  class="text-sm font-medium text-red-500 hover:text-red-700"
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

    <!-- MODAL ZA DODAVANJE I UREĐIVANJE -->
    <div
      v-if="showProductForm"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="product-modal-title"
        class="max-h-[90vh] w-full max-w-lg overflow-y-auto rounded-3xl bg-white p-6 shadow-xl sm:p-8"
      >
        <div class="mb-6 flex items-center justify-between">
          <h3
            id="product-modal-title"
            class="text-2xl font-bold"
          >
            {{
              editingProductId !== null
                ? 'Uredi proizvod'
                : 'Novi proizvod'
            }}
          </h3>

          <button
            type="button"
            @click="closeProductForm"
            :disabled="saving"
            class="text-2xl text-stone-400 hover:text-stone-700 disabled:opacity-50"
            aria-label="Zatvori obrazac"
          >
            &times;
          </button>
        </div>

        <form
          @submit.prevent="saveProduct"
          class="space-y-5"
        >
          <!-- Naziv -->
          <div>
            <label
              for="product-name"
              class="mb-2 block text-sm font-medium"
            >
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

          <!-- Kategorija -->
          <div>
            <label
              for="product-category"
              class="mb-2 block text-sm font-medium"
            >
              Kategorija
            </label>

            <select
              id="product-category"
              v-model="productForm.category_id"
              required
              class="w-full rounded-xl border border-stone-200 bg-white px-4 py-3 outline-none focus:border-orange-500"
            >
              <option value="" disabled>
                Odaberi kategoriju
              </option>

              <option
                v-for="category in restaurant?.categories ?? []"
                :key="category.id"
                :value="category.id"
              >
                {{ category.name }}
              </option>
            </select>
          </div>

          <!-- Opis -->
          <div>
            <label
              for="product-description"
              class="mb-2 block text-sm font-medium"
            >
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

          <!-- Cijena -->
          <div>
            <label
              for="product-price"
              class="mb-2 block text-sm font-medium"
            >
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

          <!-- Postojeća fotografija -->
          <div v-if="currentImageUrl">
            <p class="mb-2 text-sm font-medium">
              Trenutačna fotografija
            </p>

            <img
              :src="currentImageUrl"
              alt="Trenutačna fotografija proizvoda"
              class="h-28 w-28 rounded-xl object-cover"
            />
          </div>

          <!-- Nova fotografija -->
          <div>
            <label
              for="product-image"
              class="mb-2 block text-sm font-medium"
            >
              {{
                currentImageUrl
                  ? 'Promijeni fotografiju (neobavezno)'
                  : 'Fotografija proizvoda (neobavezno)'
              }}
            </label>

            <input
              id="product-image"
              type="file"
              accept="image/jpeg,image/png,image/webp"
              @change="handleImageChange"
              class="block w-full rounded-xl border border-stone-200 bg-white p-3 text-sm file:mr-4 file:rounded-lg file:border-0 file:bg-orange-50 file:px-4 file:py-2 file:font-medium file:text-orange-600"
            />

            <p class="mt-2 text-xs text-stone-400">
              JPG, PNG ili WebP. Maksimalno 5 MB.
            </p>

            <p
              v-if="selectedImage"
              class="mt-2 text-sm text-orange-600"
            >
              Odabrana fotografija: {{ selectedImage.name }}
            </p>
          </div>

          <!-- Greška -->
          <p
            v-if="formError"
            role="alert"
            class="text-sm text-red-600"
          >
            {{ formError }}
          </p>

          <!-- Gumbi -->
          <div class="flex gap-3 pt-2">
            <button
              type="button"
              @click="closeProductForm"
              :disabled="saving"
              class="flex-1 rounded-xl border border-stone-200 px-4 py-3 font-medium hover:bg-stone-50 disabled:opacity-50"
            >
              Odustani
            </button>

            <button
              type="submit"
              :disabled="saving || !!formError"
              class="flex-1 rounded-xl bg-orange-500 px-4 py-3 font-semibold text-white transition hover:bg-orange-600 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {{
                saving
                  ? 'Spremanje...'
                  : editingProductId !== null
                    ? 'Spremi promjene'
                    : 'Dodaj proizvod'
              }}
            </button>
          </div>
        </form>
      </div>
    </div>
    
<!-- MODAL ZA KATEGORIJE -->
<div
  v-if="showCategoryForm"
  class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
>
  <div
    role="dialog"
    aria-modal="true"
    aria-labelledby="category-modal-title"
    class="w-full max-w-md rounded-3xl bg-white p-6 shadow-xl"
  >
    <div class="mb-6 flex items-center justify-between">
      <h3
        id="category-modal-title"
        class="text-2xl font-bold"
      >
        {{
          editingCategoryId !== null
            ? 'Uredi kategoriju'
            : 'Nova kategorija'
        }}
      </h3>

      <button
        type="button"
        @click="closeCategoryForm"
        :disabled="categorySaving"
        class="text-2xl text-stone-400 disabled:opacity-50"
        aria-label="Zatvori obrazac"
      >
        &times;
      </button>
    </div>

    <form @submit.prevent="saveCategory" class="space-y-5">
      <div>
        <label
          for="category-name"
          class="mb-2 block text-sm font-medium"
        >
          Naziv kategorije
        </label>

        <input
          id="category-name"
          v-model="categoryName"
          type="text"
          required
          maxlength="100"
          placeholder="npr. Deserti"
          class="w-full rounded-xl border border-stone-200 px-4 py-3 outline-none focus:border-orange-500"
        />
      </div>

      <p
        v-if="categoryError"
        role="alert"
        class="text-sm text-red-600"
      >
        {{ categoryError }}
      </p>

      <div class="flex gap-3">
        <button
          type="button"
          @click="closeCategoryForm"
          :disabled="categorySaving"
          class="flex-1 rounded-xl border border-stone-200 px-4 py-3 font-medium disabled:opacity-50"
        >
          Odustani
        </button>

        <button
          type="submit"
          :disabled="categorySaving"
          class="flex-1 rounded-xl bg-orange-500 px-4 py-3 font-semibold text-white hover:bg-orange-600 disabled:opacity-50"
        >
          {{ categorySaving ? 'Spremanje...' : 'Spremi' }}
        </button>
      </div>
    </form>
  </div>
</div>

  </div>
</template>
