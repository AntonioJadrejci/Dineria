
import { createRouter, createWebHistory } from 'vue-router'
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
      component: AdminView
    },
    {
  path: '/login',
  name: 'login',
  component: LoginView
}
  ],
})

export default router
