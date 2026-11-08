
import { createRouter, createWebHistory } from 'vue-router'
import { supabase } from '../lib/supabase'

import HomeView from '../views/HomeView.vue'
import MenuView from '../views/MenuView.vue'
import AdminView from '../views/AdminView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
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
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    }
  ]
})

// Provjera prijave prije otvaranja zaštićenih stranica
router.beforeEach(async (to) => {
  if (!to.meta.requiresAuth) {
    return true
  }

  const {
    data: { user },
    error
  } = await supabase.auth.getUser()

  if (error || !user) {
    return {
      name: 'login',
      query: { redirect: to.fullPath }
    }
  }

  return true
})

export default router
