<template>
  <div class="timestamp-tool">
    <div class="page-header">
      <div class="page-icon">
        <Icon name="clock" :size="28" />
      </div>
      <div class="page-title">
        <h1>时间戳转换工具</h1>
        <p>时间戳与日期时间的相互转换，支持快捷时间点选择</p>
      </div>
    </div>
    
    <div class="card current-time-card">
      <div class="card-header">
        <h2>当前时间</h2>
        <button @click="refreshCurrentTime" class="btn-secondary btn-sm">
          <Icon name="refresh" :size="16" />
          <span>刷新</span>
        </button>
      </div>
      <div class="time-display">
        <div class="time-item">
          <span class="time-label">时间戳 (秒)</span>
          <div class="time-value-wrapper">
            <span class="time-value">{{ currentData.timestamp }}</span>
            <button @click="copyToClipboard(currentData.timestamp)" class="copy-btn" title="复制">
              <Icon name="copy" :size="16" />
            </button>
          </div>
        </div>
        <div class="time-item">
          <span class="time-label">时间戳 (毫秒)</span>
          <div class="time-value-wrapper">
            <span class="time-value">{{ currentData.milliseconds }}</span>
            <button @click="copyToClipboard(currentData.milliseconds)" class="copy-btn" title="复制">
              <Icon name="copy" :size="16" />
            </button>
          </div>
        </div>
        <div class="time-item">
          <span class="time-label">格式化时间</span>
          <div class="time-value-wrapper">
            <span class="time-value formatted">{{ currentData.datetime_str }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>时间戳转时间</h2>
      </div>
      <div class="input-group">
        <input
          v-model.number="timestampInput"
          type="number"
          placeholder="输入时间戳 (秒)"
          class="input-field"
        />
        <button @click="convertFromTimestamp" class="btn-primary">转换</button>
      </div>
      <div v-if="timestampResult" class="result-box success">
        <div class="result-content">
          <span class="result-label">转换结果</span>
          <span class="result-value">{{ timestampResult }}</span>
        </div>
        <button @click="copyToClipboard(timestampResult)" class="copy-btn" title="复制">
          <Icon name="copy" :size="18" />
        </button>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>时间转时间戳</h2>
      </div>
      <div class="input-group">
        <input
          v-model="datetimeInput"
          type="text"
          placeholder="格式: 2024-01-01 12:00:00"
          class="input-field"
        />
        <button @click="convertToTimestamp" class="btn-primary">转换</button>
      </div>
      <div v-if="datetimeResult" class="result-box success">
        <div class="result-content">
          <span class="result-label">转换结果 (秒)</span>
          <span class="result-value">{{ datetimeResult }}</span>
        </div>
        <button @click="copyToClipboard(datetimeResult)" class="copy-btn" title="复制">
          <Icon name="copy" :size="18" />
        </button>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>快捷时间戳</h2>
      </div>
      <div class="quick-buttons">
        <button @click="setQuickTimestamp(0)" class="btn-secondary">今天 00:00</button>
        <button @click="setQuickTimestamp(1)" class="btn-secondary">今天 12:00</button>
        <button @click="setQuickTimestamp(2)" class="btn-secondary">明天 00:00</button>
        <button @click="setQuickTimestamp(3)" class="btn-secondary">本周一 00:00</button>
      </div>
    </div>

    <div v-if="error" class="alert alert-error">
      <Icon name="error" :size="20" />
      <span>{{ error }}</span>
    </div>
    <div v-if="successMessage" class="alert alert-success">
      <Icon name="check" :size="20" />
      <span>{{ successMessage }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { convertTimestamp, getCurrentTimestamp } from '../api'
import Icon from '../components/Icon.vue'

const currentData = ref({
  timestamp: 0,
  milliseconds: 0,
  datetime_str: ''
})

const timestampInput = ref(null)
const datetimeInput = ref('')
const timestampResult = ref('')
const datetimeResult = ref(null)
const error = ref('')
const successMessage = ref('')

const refreshCurrentTime = async () => {
  try {
    const response = await getCurrentTimestamp()
    currentData.value = response.data
  } catch (err) {
    showError('获取当前时间失败')
  }
}

const convertFromTimestamp = async () => {
  if (!timestampInput.value) {
    showError('请输入时间戳')
    return
  }
  try {
    const response = await convertTimestamp({
      timestamp: timestampInput.value,
      format: '%Y-%m-%d %H:%M:%S'
    })
    timestampResult.value = response.data.datetime_str
    datetimeResult.value = null
  } catch (err) {
    showError('转换失败')
  }
}

const convertToTimestamp = async () => {
  if (!datetimeInput.value) {
    showError('请输入时间')
    return
  }
  try {
    const response = await convertTimestamp({
      datetime_str: datetimeInput.value,
      format: '%Y-%m-%d %H:%M:%S'
    })
    datetimeResult.value = response.data.timestamp
    timestampResult.value = ''
  } catch (err) {
    showError(err.response?.data?.detail || '转换失败，请检查时间格式')
  }
}

const setQuickTimestamp = (type) => {
  const now = new Date()
  let target = new Date()
  
  switch (type) {
    case 0:
      target.setHours(0, 0, 0, 0)
      break
    case 1:
      target.setHours(12, 0, 0, 0)
      break
    case 2:
      target.setDate(now.getDate() + 1)
      target.setHours(0, 0, 0, 0)
      break
    case 3:
      const day = now.getDay()
      const diff = now.getDate() - day + (day === 0 ? -6 : 1)
      target = new Date(now.setDate(diff))
      target.setHours(0, 0, 0, 0)
      break
  }
  
  const timestamp = Math.floor(target.getTime() / 1000)
  timestampInput.value = timestamp
}

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(String(text)).then(() => {
    showSuccess('已复制到剪贴板')
  })
}

const showError = (msg) => {
  error.value = msg
  setTimeout(() => error.value = '', 3000)
}

const showSuccess = (msg) => {
  successMessage.value = msg
  setTimeout(() => successMessage.value = '', 2000)
}

onMounted(() => {
  refreshCurrentTime()
})
</script>

<style scoped>
.timestamp-tool {
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
}

.card-header h2 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.btn-sm {
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  gap: 0.375rem;
}

.time-display {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.time-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.time-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
}

.time-value-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.time-value {
  flex: 1;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--accent-primary);
  padding: 0.75rem 1rem;
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
}

.time-value.formatted {
  color: var(--text-primary);
}

.copy-btn {
  padding: 0.5rem;
  background: var(--bg-tertiary);
  border: none;
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
}

.copy-btn:hover {
  background: var(--border-medium);
  color: var(--text-primary);
}

.input-group {
  display: flex;
  gap: 0.75rem;
}

.input-field {
  flex: 1;
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

.result-box {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.result-box.success {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
  min-width: 0;
}

.result-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.result-value {
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--accent-success);
  word-break: break-all;
}

.quick-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 0.75rem;
}

.quick-buttons button {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all var(--transition-normal);
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.quick-buttons button:hover {
  background: var(--accent-primary);
  color: white;
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

.alert-success {
  background: rgba(16, 185, 129, 0.1);
  color: var(--accent-success);
  border: 1px solid rgba(16, 185, 129, 0.2);
}

@media (max-width: 640px) {
  .input-group {
    flex-direction: column;
  }
  
  .quick-buttons {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
