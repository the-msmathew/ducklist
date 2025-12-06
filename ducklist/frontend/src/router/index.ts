import { createRouter, createWebHistory } from 'vue-router'
import ListPage from '../views/ListPage.vue'
import HomePage from '../views/HomePage.vue'

const routes = [
  { path: '/', component: HomePage },
  { path: '/lists/:id', component: ListPage, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
