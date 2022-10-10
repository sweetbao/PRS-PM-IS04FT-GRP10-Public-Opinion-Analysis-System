import { createRouter, createWebHistory } from 'vue-router'
import TextEmotion from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: TextEmotion
    }
  ]
})

export default router
