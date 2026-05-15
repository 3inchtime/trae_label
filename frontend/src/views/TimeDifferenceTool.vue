<template>
  <div class="time-difference-tool">
    <div class="page-header">
      <div class="page-icon">
        <Icon name="clock" :size="28" />
      </div>
      <div class="page-title">
        <h1>时间差计算</h1>
        <p>计算两个时间之间的年、月、日、秒差距</p>
      </div>
    </div>
    
    <div class="card">
      <div class="card-header">
        <h2>输入时间</h2>
      </div>
      <div class="input-group">
        <div class="input-wrapper">
          <label class="input-label">开始时间</label>
          <input
            v-model="startTime"
            type="text"
            placeholder="格式: 2024-01-01 12:00:00"
            class="input-field"
          />
        </div>
        <div class="input-wrapper">
          <label class="input-label">结束时间</label>
          <input
            v-model="endTime"
            type="text"
            placeholder="格式: 2024-01-01 12:00:00"
            class="input-field"
          />
        </div>
      </div>
      <div class="button-group">
        <button @click="calculateDifference" class="btn-primary">计算时间差</button>
        <button @click="setCurrentTime" class="btn-secondary">设置当前时间</button>
      </div>
    </div>

    <div v-if="result" class="card">
      <div class="card-header">
        <h2>计算结果</h2>
      </div>
      <div class="result-grid">
        <div class="result-card">
          <div class="result-value">{{ result.years }}</div>
          <div class="result-label">年</div>
        </div>
        <div class="result-card">
          <div class="result-value">{{ result.months }}</div>
          <div class="result-label">月</div>
        </div>
        <div class="result-card">
          <div class="result-value">{{ result.days }}</div>
          <div class="result-label">日</div>
        </div>
        <div class="result-card">
          <div class="result-value">{{ result.hours }}</div>
          <div class="result-label">时</div>
        </div>
        <div class="result-card">
          <div class="result-value">{{ result.minutes }}</div>
          <div class="result-label">分</div>
        </div>
        <div class="result-card">
          <div class="result-value">{{ result.seconds }}</div>
          <div class="result-label">秒</div>
        </div>
      </div>
      
      <div class="total-section">
        <h3>总计</h3>
        <div class="total-items">
          <div class="total-item">
            <span class="total-label">总天数：</span>
            <span class="total-value">{{ result.total_days }}</span>
          </div>
          <div class="total-item">
            <span class="total-label">总小时：</span>
            <span class="total-value">{{ result.total_hours }}</span>
          </div>
          <div class="total-item">
            <span class="total-label">总分钟：</span>
            <span class="total-value">{{ result.total_minutes }}</span>
          </div>
          <div class="total-item">
            <span class="total-label">总秒数：</span>
            <span class="total-value">{{ result.total_seconds }}</span>
          </div>
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
import { ref } from 'vue'
import { calculateTimeDifference } from '../api'
import Icon from '../components/Icon.vue'

const startTime = ref('')
const endTime = ref('')
const result = ref(null)
const error = ref('')

const formatDateTime = (date) => {
  const pad = (n) => n.toString().padStart(2, '0')
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`
}

const setCurrentTime = () => {
  const now = new Date()
  endTime.value = formatDateTime(now)
  const yesterday = new Date(now)
  yesterday.setDate(yesterday.getDate() - 1)
  startTime.value = formatDateTime(yesterday)
}

const calculateDifference = async () => {
  if (!startTime.value || !endTime.value) {
    showError('请输入开始时间和结束时间')
    return
  }
  
  try {
    const response = await calculateTimeDifference({
      start_time: startTime.value,
      end_time: endTime.value
    })
    result.value = response.data
    error.value = ''
  } catch (err) {
    showError(err.response?.data?.detail || '计算失败，请检查时间格式')
  }
}

const showError = (msg) => {
  error.value = msg
  setTimeout(() => error.value = '', 3000)
}
</script>

<style scoped>
.time-difference-tool {
  width: 100%;
  max-width: 800px;
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
  background: rgba(59, 130, 246, 0.1);
  color: var(--accent-primary);
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

.input-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
}

.input-field {
  padding: 0.75rem 1rem;
  border: 2px solid var(--border-light);
  border-radius: var(--radius-md);
  font-size: 1rem;
  transition: all var(--transition-normal);
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-family: inherit;
}

.input-field::placeholder {
  color: var(--text-tertiary);
}

.input-field:focus {
  outline: none;
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.button-group {
  display: flex;
  gap: 0.75rem;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  background: var(--accent-primary);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-normal);
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: none;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-normal);
}

.btn-secondary:hover {
  background: var(--border-medium);
}

.result-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.result-card {
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
  padding: 1rem;
  text-align: center;
}

.result-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--accent-primary);
  margin-bottom: 0.25rem;
}

.result-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.total-section {
  padding-top: 1rem;
  border-top: 1px solid var(--border-light);
}

.total-section h3 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.total-items {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.total-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.total-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.total-value {
  font-size: 1rem;
  font-weight: 600;
  color: var(--accent-success);
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

@media (max-width: 768px) {
  .result-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .total-items {
    grid-template-columns: 1fr;
  }
  
  .button-group {
    flex-direction: column;
  }
}
</style>
