
import { createRouter, createWebHistory } from 'vue-router'
import { supabase } from '../lib/supabase'

import MenuView from '../views/MenuView.vue'
import AdminView from '../views/AdminView.vue'
import LoginView from '../views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/menu/:slug',
      name: 'menu',
      component: MenuView
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    }
  ]
})

// Provjera prijave prije otvaranja stranice
router.beforeEach(async (to) => {
  if (!to.meta.requiresAuth) {
    return true
  }

  const { data: { user }, error } =
    await supabase.auth.getUser()

  if (error || !user) {
    return {
      name: 'login',
      query: { redirect: to.fullPath }
    }
  }

  return true
})

export default router
