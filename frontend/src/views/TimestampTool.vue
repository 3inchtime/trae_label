<template>
  <div class="timestamp-tool">
    <h2>⏰ 时间戳转换工具</h2>
    
    <div class="current-time">
      <h3>当前时间</h3>
      <div class="time-display">
        <div class="time-item">
          <label>时间戳 (秒):</label>
          <span>{{ currentData.timestamp }}</span>
          <button @click="copyToClipboard(currentData.timestamp)" class="copy-btn">复制</button>
        </div>
        <div class="time-item">
          <label>时间戳 (毫秒):</label>
          <span>{{ currentData.milliseconds }}</span>
          <button @click="copyToClipboard(currentData.milliseconds)" class="copy-btn">复制</button>
        </div>
        <div class="time-item">
          <label>格式化时间:</label>
          <span>{{ currentData.datetime_str }}</span>
        </div>
      </div>
      <button @click="refreshCurrentTime" class="refresh-btn">🔄 刷新</button>
    </div>

    <div class="converter-section">
      <h3>时间戳转时间</h3>
      <div class="input-group">
        <input
          v-model.number="timestampInput"
          type="number"
          placeholder="输入时间戳 (秒)"
          class="input-field"
        />
        <button @click="convertFromTimestamp" class="convert-btn">转换</button>
      </div>
      <div v-if="timestampResult" class="result">
        <p>转换结果: <strong>{{ timestampResult }}</strong></p>
        <button @click="copyToClipboard(timestampResult)" class="copy-btn">复制</button>
      </div>
    </div>

    <div class="converter-section">
      <h3>时间转时间戳</h3>
      <div class="input-group">
        <input
          v-model="datetimeInput"
          type="text"
          placeholder="格式: 2024-01-01 12:00:00"
          class="input-field"
        />
        <button @click="convertToTimestamp" class="convert-btn">转换</button>
      </div>
      <div v-if="datetimeResult" class="result">
        <p>转换结果 (秒): <strong>{{ datetimeResult }}</strong></p>
        <button @click="copyToClipboard(datetimeResult)" class="copy-btn">复制</button>
      </div>
    </div>

    <div class="quick-timestamps">
      <h3>快捷时间戳</h3>
      <div class="quick-buttons">
        <button @click="setQuickTimestamp(0)">今天 00:00</button>
        <button @click="setQuickTimestamp(1)">今天 12:00</button>
        <button @click="setQuickTimestamp(2)">明天 00:00</button>
        <button @click="setQuickTimestamp(3)">本周一 00:00</button>
      </div>
    </div>

    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { convertTimestamp, getCurrentTimestamp } from '../api'

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
    error.value = '获取当前时间失败'
    setTimeout(() => error.value = '', 3000)
  }
}

const convertFromTimestamp = async () => {
  if (!timestampInput.value) {
    error.value = '请输入时间戳'
    setTimeout(() => error.value = '', 3000)
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
    error.value = '转换失败'
    setTimeout(() => error.value = '', 3000)
  }
}

const convertToTimestamp = async () => {
  if (!datetimeInput.value) {
    error.value = '请输入时间'
    setTimeout(() => error.value = '', 3000)
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
    error.value = err.response?.data?.detail || '转换失败，请检查时间格式'
    setTimeout(() => error.value = '', 3000)
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
    successMessage.value = '已复制到剪贴板'
    setTimeout(() => successMessage.value = '', 2000)
  })
}

onMounted(() => {
  refreshCurrentTime()
})
</script>

<style scoped>
.timestamp-tool {
  max-width: 800px;
  margin: 0 auto;
}

h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: var(--text-primary);
  transition: color 0.3s;
}

.current-time {
  background: var(--bg-secondary);
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px var(--shadow);
  transition: background 0.3s, box-shadow 0.3s;
}

.current-time h3 {
  margin-bottom: 1rem;
  color: var(--text-primary);
  transition: color 0.3s;
}

.time-display {
  margin-bottom: 1rem;
}

.time-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  flex-wrap: wrap;
}

.time-item label {
  font-weight: 500;
  min-width: 120px;
  color: var(--text-secondary);
  transition: color 0.3s;
}

.time-item span {
  font-family: monospace;
  font-size: 1.1rem;
  color: var(--accent);
  font-weight: 600;
  transition: color 0.3s;
}

.copy-btn {
  padding: 0.25rem 0.75rem;
  background: var(--btn-bg);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: background 0.2s, color 0.2s;
  color: var(--btn-text);
}

.copy-btn:hover {
  background: var(--btn-bg-hover);
}

.refresh-btn {
  padding: 0.5rem 1rem;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.refresh-btn:hover {
  background: var(--accent-hover);
}

.converter-section {
  background: var(--bg-secondary);
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px var(--shadow);
  transition: background 0.3s, box-shadow 0.3s;
}

.converter-section h3 {
  margin-bottom: 1rem;
  color: var(--text-primary);
  transition: color 0.3s;
}

.input-group {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.input-field {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid var(--input-border);
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s, background-color 0.3s, color 0.3s;
  background-color: var(--input-bg);
  color: var(--input-text);
}

.input-field::placeholder {
  color: var(--input-placeholder);
}

.input-field:focus {
  outline: none;
  border-color: var(--accent);
}

.convert-btn {
  padding: 0.75rem 1.5rem;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: background 0.2s;
}

.convert-btn:hover {
  background: var(--accent-hover);
}

.result {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background: var(--result-bg);
  border-radius: 4px;
  transition: background 0.3s;
}

.result p {
  margin: 0;
  flex: 1;
  color: var(--text-primary);
  transition: color 0.3s;
}

.result strong {
  color: var(--accent);
  font-family: monospace;
  font-size: 1.1rem;
  transition: color 0.3s;
}

.quick-timestamps {
  background: var(--bg-secondary);
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px var(--shadow);
  transition: background 0.3s, box-shadow 0.3s;
}

.quick-timestamps h3 {
  margin-bottom: 1rem;
  color: var(--text-primary);
  transition: color 0.3s;
}

.quick-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 0.75rem;
}

.quick-buttons button {
  padding: 0.75rem;
  background: var(--btn-bg);
  color: var(--text-primary);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.quick-buttons button:hover {
  background: var(--accent);
  color: white;
}

.error-message {
  background: var(--error-bg);
  color: var(--error-text);
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
  transition: background 0.3s, color 0.3s;
}

.success-message {
  background: var(--success-bg);
  color: var(--success-text);
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
  transition: background 0.3s, color 0.3s;
}
</style>
