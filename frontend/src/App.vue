

<script setup>
import { ref, onMounted } from 'vue'
import { checkBackendHealth } from './services/api'

const backendStatus = ref('Checking...')
const isConnected = ref(false)

onMounted(async () => {
  try {
    const data = await checkBackendHealth()

    backendStatus.value = data.status
    isConnected.value = true
  } catch (error) {
    backendStatus.value = 'Disconnected'
    console.error(error)
  }
})
</script>

<template>
  <main class="container">
    <h1>Welcome to Dineria</h1>

    <p>Modern digital menus for restaurants.</p>
<div class="rounded-2xl bg-orange-500 p-6 text-center text-2xl font-bold text-white">
  Dineria – Tailwind CSS radi!
</div>
    <div class="status-card">
      <h2>Backend Connection</h2>

      <p>
        Status:
        <strong :class="isConnected ? 'online' : 'offline'">
          {{ backendStatus }}
        </strong>
      </p>
    </div>
  </main>
</template>

<style scoped>
.container {
  max-width: 800px;
  margin: 100px auto;
  padding: 20px;
  text-align: center;
  font-family: Arial, sans-serif;
}

.status-card {
  margin-top: 30px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 12px;
}

.online {
  color: green;
}

.offline {
  color: red;
}
</style>
