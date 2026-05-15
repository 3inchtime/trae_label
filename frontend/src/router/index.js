import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Tools from '../views/Tools.vue'
import TimestampTool from '../views/TimestampTool.vue'
import JsonTool from '../views/JsonTool.vue'

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
  },
  {
    path: '/tools/json',
    name: 'JsonTool',
    component: JsonTool
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
