import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Tools from '../views/Tools.vue'
import TimestampTool from '../views/TimestampTool.vue'
import JsonTool from '../views/JsonTool.vue'
import Md5Tool from '../views/Md5Tool.vue'
import NumberToChinese from '../views/NumberToChinese.vue'
import RsaTool from '../views/RsaTool.vue'
import TimerTool from '../views/TimerTool.vue'
import WeightConverter from '../views/WeightConverter.vue'
import TimeDifferenceTool from '../views/TimeDifferenceTool.vue'

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
  },
  {
    path: '/tools/md5',
    name: 'Md5Tool',
    component: Md5Tool
  },
  {
    path: '/tools/number-to-chinese',
    name: 'NumberToChinese',
    component: NumberToChinese
  },
  {
    path: '/tools/rsa',
    name: 'RsaTool',
    component: RsaTool
  },
  {
    path: '/tools/timer',
    name: 'TimerTool',
    component: TimerTool
  },
  {
    path: '/tools/weight',
    name: 'WeightConverter',
    component: WeightConverter
  },
  {
    path: '/tools/time-difference',
    name: 'TimeDifferenceTool',
    component: TimeDifferenceTool
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
