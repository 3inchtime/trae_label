<template>
  <div class="calendar-tool">
    <div class="page-header">
      <div class="page-icon">
        <Icon name="calendar" :size="28" />
      </div>
      <div class="page-title">
        <h1>万年历</h1>
        <p>查看公历、农历、节气、节日等信息</p>
      </div>
    </div>

    <div class="card today-card">
      <div class="today-header">
        <h2>今日</h2>
        <span class="today-date">{{ todayInfo.year }}年{{ todayInfo.month }}月{{ todayInfo.day }}日</span>
      </div>
      <div class="today-info">
        <div class="today-info-item">
          <span class="label">星期</span>
          <span class="value">{{ todayInfo.weekday }}</span>
        </div>
        <div class="today-info-item">
          <span class="label">农历</span>
          <span class="value">{{ todayInfo.lunar_year }} {{ todayInfo.lunar_month }} {{ todayInfo.lunar_day }}</span>
        </div>
        <div v-if="todayInfo.solar_term" class="today-info-item solar-term">
          <span class="label">节气</span>
          <span class="value">{{ todayInfo.solar_term }}</span>
        </div>
        <div v-if="todayInfo.is_holiday" class="today-info-item holiday">
          <span class="label">节日</span>
          <span class="value">{{ todayInfo.holiday_name }}</span>
        </div>
      </div>
    </div>

    <div class="card calendar-card">
      <div class="calendar-header">
        <button @click="prevMonth" class="nav-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
        </button>
        <h3 class="calendar-title">{{ currentYear }}年{{ currentMonth }}月</h3>
        <button @click="nextMonth" class="nav-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </button>
        <button @click="goToToday" class="btn-secondary btn-sm today-btn">今天</button>
      </div>

      <div class="calendar-weekdays">
        <div v-for="day in weekdays" :key="day" class="weekday">{{ day }}</div>
      </div>

      <div class="calendar-grid">
        <div v-for="(day, index) in calendarDays" :key="index" 
             class="calendar-day" 
             :class="{ 
               'empty': !day,
               'today': day?.is_today,
               'holiday': day?.is_holiday,
               'weekend': day && (day.weekday_en === 'Saturday' || day.weekday_en === 'Sunday')
             }">
          <template v-if="day">
            <div class="day-number">{{ day.day }}</div>
            <div class="day-lunar">{{ day.lunar_day }}</div>
            <div v-if="day.solar_term" class="day-solar-term">{{ day.solar_term }}</div>
            <div v-if="day.is_holiday" class="day-holiday">{{ day.holiday_name }}</div>
          </template>
        </div>
      </div>
    </div>

    <div class="card quick-nav">
      <div class="card-header">
        <h2>快速跳转</h2>
      </div>
      <div class="quick-nav-content">
        <div class="year-selector">
          <label>年份</label>
          <select v-model.number="selectYear" @change="jumpToDate">
            <option v-for="y in yearOptions" :key="y" :value="y">{{ y }}年</option>
          </select>
        </div>
        <div class="month-selector">
          <label>月份</label>
          <select v-model.number="selectMonth" @change="jumpToDate">
            <option v-for="m in 12" :key="m" :value="m">{{ m }}月</option>
          </select>
        </div>
      </div>
    </div>

    <div v-if="error" class="alert alert-error">
      <Icon name="error" :size="20" />
      <span>{{ error }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getCalendarMonth, getTodayInfo } from '../api'
import Icon from '../components/Icon.vue'

const todayInfo = ref({
  year: new Date().getFullYear(),
  month: new Date().getMonth() + 1,
  day: new Date().getDate(),
  weekday: '',
  lunar_year: '',
  lunar_month: '',
  lunar_day: '',
  solar_term: null,
  is_holiday: false,
  holiday_name: null
})

const currentYear = ref(new Date().getFullYear())
const currentMonth = ref(new Date().getMonth() + 1)
const calendarData = ref(null)
const error = ref('')

const weekdays = ['一', '二', '三', '四', '五', '六', '日']

const selectYear = computed({
  get: () => currentYear.value,
  set: (val) => currentYear.value = val
})

const selectMonth = computed({
  get: () => currentMonth.value,
  set: (val) => currentMonth.value = val
})

const yearOptions = computed(() => {
  const years = []
  for (let y = 1900; y <= 2100; y++) {
    years.push(y)
  }
  return years
})

const calendarDays = computed(() => {
  if (!calendarData.value) return []
  
  const days = []
  const firstDayWeekday = calendarData.value.first_day_weekday
  
  for (let i = 0; i < firstDayWeekday; i++) {
    days.push(null)
  }
  
  for (const day of calendarData.value.days) {
    days.push(day)
  }
  
  while (days.length < 42) {
    days.push(null)
  }
  
  return days
})

const fetchTodayInfo = async () => {
  try {
    const response = await getTodayInfo()
    todayInfo.value = response.data
  } catch (err) {
    showError('获取今日信息失败')
  }
}

const fetchCalendarMonth = async () => {
  try {
    const response = await getCalendarMonth({
      year: currentYear.value,
      month: currentMonth.value
    })
    calendarData.value = response.data
  } catch (err) {
    showError('获取日历数据失败')
  }
}

const prevMonth = () => {
  if (currentMonth.value === 1) {
    currentMonth.value = 12
    currentYear.value--
  } else {
    currentMonth.value--
  }
  fetchCalendarMonth()
}

const nextMonth = () => {
  if (currentMonth.value === 12) {
    currentMonth.value = 1
    currentYear.value++
  } else {
    currentMonth.value++
  }
  fetchCalendarMonth()
}

const goToToday = () => {
  currentYear.value = new Date().getFullYear()
  currentMonth.value = new Date().getMonth() + 1
  fetchCalendarMonth()
}

const jumpToDate = () => {
  fetchCalendarMonth()
}

const showError = (msg) => {
  error.value = msg
  setTimeout(() => error.value = '', 3000)
}

onMounted(() => {
  fetchTodayInfo()
  fetchCalendarMonth()
})
</script>

<style scoped>
.calendar-tool {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.page-icon {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-lg);
  background: rgba(14, 165, 233, 0.1);
  color: #8b5cf6;
  display: flex;
  align-items: center;
  justify-content: center;
}

.page-title h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.page-title p {
  font-size: 0.95rem;
  color: var(--text-secondary);
  margin: 0;
}

.card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  margin-bottom: 1.25rem;
  transition: all var(--transition-normal);
}

.card:hover {
  border-color: var(--border-medium);
}

.card-header {
  margin-bottom: 1.25rem;
}

.card-header h2 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.today-card {
  background: linear-gradient(135deg, rgba(14, 165, 233, 0.1), rgba(59, 130, 246, 0.1));
  border-color: rgba(14, 165, 233, 0.2);
}

.today-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.today-header h2 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--accent-primary);
  margin: 0;
}

.today-date {
  font-size: 0.95rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.today-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.today-info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.today-info-item .label {
  font-size: 0.8rem;
  color: var(--text-tertiary);
  font-weight: 500;
}

.today-info-item .value {
  font-size: 1rem;
  color: var(--text-primary);
  font-weight: 600;
}

.today-info-item.solar-term .value {
  color: #10b981;
}

.today-info-item.holiday .value {
  color: #ef4444;
}

.calendar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.nav-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.nav-btn:hover {
  background: var(--accent-primary);
  color: white;
}

.calendar-title {
  flex: 1;
  text-align: center;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.today-btn {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

.calendar-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.25rem;
  margin-bottom: 0.5rem;
}

.weekday {
  text-align: center;
  padding: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.25rem;
}

.calendar-day {
  aspect-ratio: 1;
  border-radius: var(--radius-md);
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  cursor: pointer;
  transition: all var(--transition-fast);
  position: relative;
  min-height: 80px;
}

.calendar-day.empty {
  background: transparent;
  cursor: default;
}

.calendar-day:hover:not(.empty) {
  background: var(--bg-tertiary);
}

.calendar-day.today {
  background: var(--accent-primary);
  color: white;
}

.calendar-day.today .day-number {
  color: white;
  font-weight: 700;
}

.calendar-day.weekend .day-number {
  color: #ef4444;
}

.calendar-day.today.weekend .day-number {
  color: white;
}

.calendar-day.holiday {
  background: rgba(239, 68, 68, 0.1);
}

.calendar-day.today.holiday {
  background: var(--accent-primary);
}

.day-number {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.day-lunar {
  font-size: 0.7rem;
  color: var(--text-tertiary);
  margin-bottom: 0.25rem;
}

.calendar-day.today .day-lunar {
  color: rgba(255, 255, 255, 0.8);
}

.day-solar-term {
  font-size: 0.65rem;
  color: #10b981;
  font-weight: 500;
  margin-top: 0.125rem;
}

.calendar-day.today .day-solar-term {
  color: rgba(16, 185, 129, 1);
}

.day-holiday {
  font-size: 0.65rem;
  color: #ef4444;
  font-weight: 500;
  margin-top: 0.125rem;
}

.calendar-day.today .day-holiday {
  color: rgba(255, 255, 255, 0.9);
}

.quick-nav-content {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.year-selector,
.month-selector {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 150px;
}

.year-selector label,
.month-selector label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
}

.year-selector select,
.month-selector select {
  padding: 0.625rem 1rem;
  border: 2px solid var(--border-light);
  border-radius: var(--radius-md);
  font-size: 1rem;
  background: var(--bg-secondary);
  color: var(--text-primary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.year-selector select:focus,
.month-selector select:focus {
  outline: none;
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.btn-sm {
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
}

.btn-secondary {
  background: var(--bg-tertiary);
  border: none;
  color: var(--text-primary);
  padding: 0.75rem 1.25rem;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-secondary:hover {
  background: var(--border-medium);
}

.alert {
  padding: 1rem;
  border-radius: var(--radius-md);
  margin-top: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 500;
}

.alert-error {
  background: rgba(239, 68, 68, 0.1);
  color: var(--accent-error);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

@media (max-width: 640px) {
  .today-info {
    grid-template-columns: 1fr;
  }
  
  .calendar-day {
    min-height: 60px;
    padding: 0.25rem;
  }
  
  .day-number {
    font-size: 0.875rem;
  }
  
  .day-lunar {
    font-size: 0.6rem;
  }
  
  .day-solar-term,
  .day-holiday {
    font-size: 0.55rem;
  }
  
  .quick-nav-content {
    flex-direction: column;
  }
  
  .year-selector,
  .month-selector {
    min-width: 100%;
  }
}
</style>
