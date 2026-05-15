import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Tools from '../views/Tools.vue'
import TimestampTool from '../views/TimestampTool.vue'
import NumberToChinese from '../views/NumberToChinese.vue'

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
    path: '/tools/number-to-chinese',
    name: 'NumberToChinese',
    component: NumberToChinese
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
