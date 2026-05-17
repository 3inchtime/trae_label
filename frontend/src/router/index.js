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
import CalendarTool from '../views/CalendarTool.vue'
import LengthConverter from '../views/LengthConverter.vue'
import ColorPicker from '../views/ColorPicker.vue'
import UrlTool from '../views/UrlTool.vue'
import YamlTool from '../views/YamlTool.vue'
import ReactionTest from '../views/ReactionTest.vue'
import Auth from '../views/Auth.vue'

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
  },
  {
    path: '/tools/calendar',
    name: 'CalendarTool',
    component: CalendarTool
  },
  {
    path: '/tools/length',
    name: 'LengthConverter',
    component: LengthConverter
  },
  {
    path: '/tools/color',
    name: 'ColorPicker',
    component: ColorPicker
  },
  {
    path: '/tools/url',
    name: 'UrlTool',
    component: UrlTool
  },
  {
    path: '/tools/yaml',
    name: 'YamlTool',
    component: YamlTool
  },
  {
    path: '/tools/reaction-test',
    name: 'ReactionTest',
    component: ReactionTest
  },
  {
    path: '/auth',
    name: 'Auth',
    component: Auth
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
