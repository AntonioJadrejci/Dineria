<script setup>
import { ref } from 'vue'

const mobileMenuOpen = ref(false)

const features = [
  {
    number: '01',
    title: 'Jelovnik uvijek ažuran',
    description: 'Dodaj, uredi ili ukloni proizvode i cijene bez ponovnog tiskanja jelovnika.',
    icon: 'edit'
  },
  {
    number: '02',
    title: 'Fotografije koje privlače',
    description: 'Predstavi svoju ponudu fotografijama i jasnim opisima svakog proizvoda.',
    icon: 'image'
  },
  {
    number: '03',
    title: 'Prilagođeno mobitelima',
    description: 'Gosti pregledavaju jelovnik jednostavno, na bilo kojem uređaju.',
    icon: 'phone'
  }
]
</script>

<template>
  <div class="min-h-screen bg-[#faf9f6] text-stone-900">
    <header class="sticky top-0 z-30 border-b border-stone-200/80 bg-[#faf9f6]/95 backdrop-blur">
      <nav class="mx-auto flex max-w-7xl items-center justify-between px-5 py-4 sm:px-8">
        <RouterLink to="/" class="text-2xl font-extrabold tracking-tight">
          dineria<span class="text-orange-500">.</span>
        </RouterLink>

        <div class="hidden items-center gap-8 md:flex">
          <a href="#prednosti" class="text-sm font-medium text-stone-600 transition hover:text-orange-600">Prednosti</a>
          <a href="#kako-radi" class="text-sm font-medium text-stone-600 transition hover:text-orange-600">Kako radi</a>
          <RouterLink to="/login" class="text-sm font-semibold text-stone-700 transition hover:text-orange-600">Prijava</RouterLink>
          <RouterLink to="/register" class="rounded-xl bg-orange-500 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-orange-600">Započni besplatno</RouterLink>
        </div>

        <button type="button" class="rounded-lg border border-stone-200 p-2 text-stone-700 md:hidden" :aria-expanded="mobileMenuOpen" aria-label="Otvori izbornik" @click="mobileMenuOpen = !mobileMenuOpen">
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
            <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" d="M4 7h16M4 12h16M4 17h16" />
            <path v-else stroke-linecap="round" stroke-linejoin="round" d="M6 6l12 12M18 6L6 18" />
          </svg>
        </button>
      </nav>

      <div v-if="mobileMenuOpen" class="flex flex-col gap-4 border-t border-stone-200 bg-white px-5 py-5 md:hidden">
        <a href="#prednosti" class="text-sm font-medium" @click="mobileMenuOpen = false">Prednosti</a>
        <a href="#kako-radi" class="text-sm font-medium" @click="mobileMenuOpen = false">Kako radi</a>
        <RouterLink to="/login" class="text-sm font-medium" @click="mobileMenuOpen = false">Prijava</RouterLink>
        <RouterLink to="/register" class="rounded-xl bg-orange-500 px-4 py-3 text-center text-sm font-semibold text-white" @click="mobileMenuOpen = false">Započni besplatno</RouterLink>
      </div>
    </header>

    <main>
      <section class="relative overflow-hidden">
        <div class="pointer-events-none absolute -right-32 top-12 h-96 w-96 rounded-full bg-orange-100/70 blur-3xl"></div>
        <div class="mx-auto grid max-w-7xl items-center gap-12 px-5 pb-20 pt-16 sm:px-8 md:pt-24 lg:grid-cols-2 lg:gap-16 lg:pb-28">
          <div class="relative z-10">
            <div class="mb-7 inline-flex items-center gap-2 rounded-full border border-orange-200 bg-orange-50 px-4 py-2 text-xs font-bold uppercase tracking-widest text-orange-700">
              <span class="h-2 w-2 rounded-full bg-orange-500"></span>
              Digitalni jelovnici za restorane
            </div>
            <h1 class="max-w-xl text-5xl font-extrabold leading-[1.08] tracking-tight text-stone-900 sm:text-6xl lg:text-[4.4rem]">
              Vaš jelovnik.<br />
              <span class="text-orange-500">Digitalno.</span><br />
              Jednostavno.
            </h1>
            <p class="mt-7 max-w-lg text-lg leading-relaxed text-stone-600">
              Kreirajte moderan digitalni jelovnik, uredite ponudu u nekoliko klikova i omogućite gostima da je pregledaju putem QR koda.
            </p>
            <div class="mt-9 flex flex-col gap-3 sm:flex-row">
              <RouterLink to="/register" class="inline-flex items-center justify-center gap-2 rounded-xl bg-orange-500 px-7 py-4 text-sm font-bold text-white shadow-lg shadow-orange-500/20 transition hover:-translate-y-0.5 hover:bg-orange-600">
                Kreiraj svoj jelovnik <span aria-hidden="true">→</span>
              </RouterLink>
              <RouterLink to="/menu/dineria-demo" class="inline-flex items-center justify-center gap-2 rounded-xl border border-stone-300 bg-white px-7 py-4 text-sm font-bold text-stone-800 transition hover:border-orange-300 hover:text-orange-600">
                Pogledaj demo jelovnik <span aria-hidden="true">↗</span>
              </RouterLink>
            </div>
            <div class="mt-9 flex flex-wrap items-center gap-x-6 gap-y-3 text-sm text-stone-500">
              <span class="flex items-center gap-2"><span class="font-bold text-orange-500">✓</span> Bez instalacije</span>
              <span class="flex items-center gap-2"><span class="font-bold text-orange-500">✓</span> Jednostavno uređivanje</span>
              <span class="flex items-center gap-2"><span class="font-bold text-orange-500">✓</span> Prilagođeno mobitelima</span>
            </div>
          </div>

          <div class="relative mx-auto w-full max-w-xl lg:max-w-none" aria-label="Ilustracija digitalnog jelovnika">
            <div class="absolute inset-5 rotate-3 rounded-[2.5rem] bg-orange-100"></div>
            <div class="relative overflow-hidden rounded-[2rem] border border-stone-200 bg-white p-5 shadow-2xl shadow-stone-300/50 sm:p-7">
              <div class="mb-6 flex items-center justify-between">
                <div>
                  <p class="text-xs font-semibold uppercase tracking-[.2em] text-orange-500">Digitalni jelovnik</p>
                  <h2 class="mt-1 text-2xl font-extrabold">Bistro & Co.</h2>
                </div>
                <div class="rounded-full bg-orange-50 px-3 py-2 text-xs font-bold text-orange-600">MENU</div>
              </div>
              <div class="mb-5 flex gap-2 overflow-hidden text-xs font-semibold">
                <span class="whitespace-nowrap rounded-full bg-orange-500 px-4 py-2 text-white">Popularno</span>
                <span class="whitespace-nowrap rounded-full bg-stone-100 px-4 py-2 text-stone-600">Glavna jela</span>
                <span class="whitespace-nowrap rounded-full bg-stone-100 px-4 py-2 text-stone-600">Pića</span>
              </div>
              <div class="space-y-3">
                <div class="flex items-center gap-4 rounded-2xl bg-stone-50 p-3">
                  <div class="flex h-20 w-20 shrink-0 items-center justify-center rounded-xl bg-orange-100 text-4xl">🍕</div>
                  <div class="min-w-0 flex-1"><p class="font-bold">Pizza Margherita</p><p class="mt-1 text-xs text-stone-500">Rajčica, mozzarella, bosiljak</p><p class="mt-2 text-sm font-extrabold text-orange-600">10,50 €</p></div>
                </div>
                <div class="flex items-center gap-4 rounded-2xl bg-stone-50 p-3">
                  <div class="flex h-20 w-20 shrink-0 items-center justify-center rounded-xl bg-amber-100 text-4xl">🍝</div>
                  <div class="min-w-0 flex-1"><p class="font-bold">Pasta Carbonara</p><p class="mt-1 text-xs text-stone-500">Tjestenina, jaja, panceta</p><p class="mt-2 text-sm font-extrabold text-orange-600">12,00 €</p></div>
                </div>
                <div class="flex items-center gap-4 rounded-2xl bg-stone-50 p-3">
                  <div class="flex h-20 w-20 shrink-0 items-center justify-center rounded-xl bg-lime-100 text-4xl">🥗</div>
                  <div class="min-w-0 flex-1"><p class="font-bold">Svježa salata</p><p class="mt-1 text-xs text-stone-500">Sezonsko povrće i dressing</p><p class="mt-2 text-sm font-extrabold text-orange-600">8,50 €</p></div>
                </div>
              </div>
              <p class="mt-4 text-center text-xs text-stone-400">Primjer prikaza jelovnika</p>
            </div>
            <div class="absolute -bottom-5 -left-3 hidden rotate-[-7deg] rounded-2xl border border-orange-100 bg-white px-5 py-4 shadow-xl sm:block">
              <div class="flex items-center gap-3"><span class="text-2xl">📱</span><div><p class="text-xs font-bold">Skeniraj QR kod</p><p class="text-xs text-stone-500">I jelovnik je tu!</p></div></div>
            </div>
          </div>
        </div>
      </section>

      <section id="prednosti" class="bg-white py-20 sm:py-24">
        <div class="mx-auto max-w-7xl px-5 sm:px-8">
          <div class="mx-auto max-w-2xl text-center">
            <p class="text-sm font-bold uppercase tracking-widest text-orange-500">Sve na jednom mjestu</p>
            <h2 class="mt-4 text-3xl font-extrabold tracking-tight sm:text-4xl">Manje posla oko jelovnika.<br />Više vremena za goste.</h2>
            <p class="mt-5 text-stone-600">Jednostavan način da ponuda vašeg restorana uvijek bude spremna za goste.</p>
          </div>
          <div class="mt-12 grid gap-5 md:grid-cols-3">
            <article v-for="feature in features" :key="feature.number" class="rounded-3xl border border-stone-200 bg-[#faf9f6] p-8 transition hover:-translate-y-1 hover:shadow-lg">
              <div class="mb-8 flex h-14 w-14 items-center justify-center rounded-2xl bg-orange-100 text-2xl text-orange-600">
                <svg v-if="feature.icon === 'edit'" class="h-7 w-7" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 20h9M16.5 3.5a2.12 2.12 0 013 3L9 17l-4 1 1-4L16.5 3.5z"/></svg>
                <svg v-else-if="feature.icon === 'image'" class="h-7 w-7" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>
                <svg v-else class="h-7 w-7" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/></svg>
              </div>
              <p class="text-xs font-bold tracking-widest text-orange-500">{{ feature.number }}</p>
              <h3 class="mt-3 text-xl font-bold">{{ feature.title }}</h3>
              <p class="mt-3 leading-relaxed text-stone-600">{{ feature.description }}</p>
            </article>
          </div>
        </div>
      </section>

      <section id="kako-radi" class="py-20 sm:py-24">
        <div class="mx-auto max-w-7xl px-5 sm:px-8">
          <div class="text-center"><p class="text-sm font-bold uppercase tracking-widest text-orange-500">Kako radi</p><h2 class="mt-4 text-3xl font-extrabold sm:text-4xl">Od registracije do jelovnika u tri koraka.</h2></div>
          <div class="mt-14 grid gap-8 md:grid-cols-3">
            <div class="text-center"><div class="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-white text-2xl font-extrabold text-orange-500 shadow-sm">1</div><h3 class="mt-5 text-xl font-bold">Kreiraj račun</h3><p class="mt-3 text-stone-600">Registriraj se i unesi podatke svojeg restorana.</p></div>
            <div class="text-center"><div class="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-white text-2xl font-extrabold text-orange-500 shadow-sm">2</div><h3 class="mt-5 text-xl font-bold">Uredi ponudu</h3><p class="mt-3 text-stone-600">Dodaj kategorije, proizvode, cijene i fotografije.</p></div>
            <div class="text-center"><div class="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-white text-2xl font-extrabold text-orange-500 shadow-sm">3</div><h3 class="mt-5 text-xl font-bold">Podijeli jelovnik</h3><p class="mt-3 text-stone-600">Gosti pristupaju tvojem javnom jelovniku putem poveznice, a uskoro i QR koda.</p></div>
          </div>
        </div>
      </section>

      <section class="bg-stone-900 py-20 text-white sm:py-24">
        <div class="mx-auto max-w-3xl px-5 text-center sm:px-8">
          <p class="text-sm font-bold uppercase tracking-widest text-orange-400">Spremni za digitalni jelovnik?</p>
          <h2 class="mt-5 text-3xl font-extrabold leading-tight sm:text-5xl">Vaš restoran zaslužuje jednostavniji način rada.</h2>
          <p class="mx-auto mt-6 max-w-xl text-stone-300">Otvorite račun i počnite izrađivati jelovnik svojeg restorana.</p>
          <RouterLink to="/register" class="mt-9 inline-flex items-center justify-center rounded-xl bg-orange-500 px-8 py-4 text-sm font-bold text-white transition hover:bg-orange-600">Započni besplatno →</RouterLink>
        </div>
      </section>
    </main>

    <footer class="border-t border-stone-200 bg-white">
      <div class="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 px-5 py-7 text-sm text-stone-500 sm:flex-row sm:px-8">
        <RouterLink to="/" class="text-xl font-extrabold text-stone-900">dineria<span class="text-orange-500">.</span></RouterLink>
        <p>Digitalni jelovnici, jednostavno.</p>
        <div class="flex gap-5"><RouterLink to="/login" class="hover:text-orange-600">Prijava</RouterLink><RouterLink to="/register" class="hover:text-orange-600">Registracija</RouterLink></div>
      </div>
    </footer>
  </div>
</template>
