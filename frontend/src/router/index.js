import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Tools from '../views/Tools.vue'
import TimestampTool from '../views/TimestampTool.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/tools',
    name: 'Tools',
    component: Tools
  },
  {
    path: '/tools/timestamp',
    name: 'TimestampTool',
    component: TimestampTool
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
