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
  max-width: 850px;
  margin: 0 auto;
  animation: fadeInUp 0.5s ease-out;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  margin-bottom: 2.5rem;
  padding: 1.5rem;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
  border-radius: var(--radius-xl);
  border: 1px solid var(--glass-border);
  box-shadow: var(--shadow-glass);
  position: relative;
  overflow: hidden;
}

.page-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary), var(--accent-primary));
  background-size: 200% 100%;
  animation: shimmerBorder 3s linear infinite;
}

.page-icon {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-lg);
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(14, 165, 233, 0.15) 100%);
  color: var(--accent-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
  transition: all var(--transition-normal);
  flex-shrink: 0;
}

.page-header:hover .page-icon {
  transform: scale(1.08) rotate(5deg);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3);
}

.page-title h1 {
  font-size: 1.75rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent-primary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.page-title p {
  font-size: 0.95rem;
  color: var(--text-secondary);
  margin: 0;
}

.card {
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-xl);
  padding: 1.75rem;
  margin-bottom: 1.5rem;
  transition: all var(--transition-normal);
  box-shadow: var(--shadow-glass);
  position: relative;
  overflow: hidden;
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.06), transparent);
  transition: left var(--transition-slow);
}

.card:hover::before {
  left: 100%;
}

.card:hover {
  border-color: var(--accent-primary);
  box-shadow: 0 12px 40px rgba(59, 130, 246, 0.18);
  transform: translateY(-4px);
}

.current-time-card {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(14, 165, 233, 0.04) 100%);
  border-color: rgba(59, 130, 246, 0.2);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.card-header h2 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.card-header h2::before {
  content: '';
  width: 4px;
  height: 20px;
  background: linear-gradient(180deg, var(--accent-primary), var(--accent-secondary));
  border-radius: 2px;
}

.btn-sm {
  padding: 0.625rem 1rem;
  font-size: 0.875rem;
  gap: 0.5rem;
}

.time-display {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.time-item {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.time-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.time-value-wrapper {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.time-value {
  flex: 1;
  font-family: 'Monaco', 'Menlo', 'SF Mono', monospace;
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--accent-primary);
  padding: 1rem 1.25rem;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(14, 165, 233, 0.05) 100%);
  border: 1px solid rgba(59, 130, 246, 0.15);
  border-radius: var(--radius-md);
  box-shadow: inset 0 2px 8px rgba(59, 130, 246, 0.08);
  transition: all var(--transition-normal);
}

.time-value:hover {
  border-color: var(--accent-primary);
  box-shadow: inset 0 2px 12px rgba(59, 130, 246, 0.12);
}

.time-value.formatted {
  color: var(--text-primary);
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%);
  border-color: rgba(16, 185, 129, 0.15);
}

.copy-btn {
  padding: 0.75rem;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-normal);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.08);
}

.copy-btn:hover {
  background: rgba(59, 130, 246, 0.1);
  border-color: var(--accent-primary);
  color: var(--accent-primary);
  transform: scale(1.08);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.copy-btn:active {
  transform: scale(0.95);
}

.input-group {
  display: flex;
  gap: 0.875rem;
}

.input-field {
  flex: 1;
  padding: 1rem 1.25rem;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-md);
  font-size: 1rem;
  transition: all var(--transition-normal);
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
  color: var(--text-primary);
  font-family: inherit;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.06);
}

.input-field::placeholder {
  color: var(--text-tertiary);
}

.input-field:focus {
  outline: none;
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15), 0 4px 12px rgba(59, 130, 246, 0.1);
  transform: translateY(-1px);
}

.result-box {
  margin-top: 1.25rem;
  padding: 1.25rem;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  animation: fadeInUp 0.3s ease-out;
}

.result-box.success {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(5, 150, 105, 0.06) 100%);
  border: 1px solid rgba(16, 185, 129, 0.25);
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.12);
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  flex: 1;
  min-width: 0;
}

.result-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.result-value {
  font-family: 'Monaco', 'Menlo', 'SF Mono', monospace;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--accent-success);
  word-break: break-all;
}

.quick-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 0.875rem;
}

.quick-buttons button {
  padding: 0.875rem 1rem;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all var(--transition-normal);
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
  color: var(--text-primary);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.06);
  position: relative;
  overflow: hidden;
}

.quick-buttons button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left var(--transition-normal);
}

.quick-buttons button:hover::before {
  left: 100%;
}

.quick-buttons button:hover {
  background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
  color: white;
  border-color: transparent;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3);
}

.alert {
  padding: 1.125rem 1.25rem;
  border-radius: var(--radius-md);
  margin-top: 1rem;
  display: flex;
  align-items: center;
  gap: 0.875rem;
  font-weight: 600;
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
  animation: fadeInUp 0.3s ease-out;
}

.alert-error {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.12) 0%, rgba(220, 38, 38, 0.06) 100%);
  color: var(--accent-error);
  border: 1px solid rgba(239, 68, 68, 0.25);
  box-shadow: 0 4px 15px rgba(239, 68, 68, 0.12);
}

.alert-success {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(5, 150, 105, 0.06) 100%);
  color: var(--accent-success);
  border: 1px solid rgba(16, 185, 129, 0.25);
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.12);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes shimmerBorder {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

@media (max-width: 768px) {
  .input-group {
    flex-direction: column;
  }
  
  .quick-buttons {
    grid-template-columns: 1fr 1fr;
  }
  
  .page-header {
    padding: 1.25rem;
    flex-direction: column;
    text-align: center;
  }
  
  .page-icon {
    width: 56px;
    height: 56px;
  }
  
  .page-title h1 {
    font-size: 1.5rem;
  }
  
  .card {
    padding: 1.5rem;
  }
}

@media (max-width: 480px) {
  .quick-buttons {
    grid-template-columns: 1fr;
  }
  
  .time-value-wrapper {
    flex-direction: column;
    align-items: stretch;
  }
  
  .copy-btn {
    align-self: flex-end;
  }
}
</style>
