<template>
  <div class="timer-tool">
    <div class="page-header">
      <div class="page-icon">
        <Icon name="clock" :size="28" />
      </div>
      <div class="page-title">
        <h1>在线计时器</h1>
        <p>创建和管理多个倒计时计时器，支持暂停、重置功能</p>
      </div>
    </div>
    
    <div class="card create-timer-card">
      <div class="card-header">
        <h2>创建计时器</h2>
      </div>
      <div class="create-form">
        <div class="input-row">
          <div class="input-group">
            <label>名称</label>
            <input
              v-model="newTimerName"
              type="text"
              placeholder="例如：煮面、开会"
              class="input-field"
            />
          </div>
          <div class="input-group">
            <label>时长 (秒)</label>
            <input
              v-model.number="newTimerDuration"
              type="number"
              :min="1"
              placeholder="60"
              class="input-field"
            />
          </div>
        </div>
        <div class="quick-presets">
          <span class="preset-label">快捷时长:</span>
          <button @click="setPreset(60)" class="btn-secondary btn-sm">1分钟</button>
          <button @click="setPreset(300)" class="btn-secondary btn-sm">5分钟</button>
          <button @click="setPreset(600)" class="btn-secondary btn-sm">10分钟</button>
          <button @click="setPreset(1800)" class="btn-secondary btn-sm">30分钟</button>
          <button @click="setPreset(3600)" class="btn-secondary btn-sm">1小时</button>
        </div>
        <button @click="createNewTimer" class="btn-primary create-btn">
          <Icon name="plus" :size="18" />
          <span>创建计时器</span>
        </button>
      </div>
    </div>

    <div class="card active-timers-section">
      <div class="card-header">
        <h2>活动计时器</h2>
        <span class="timer-count">{{ activeTimers.length }} 个</span>
      </div>
      <div v-if="activeTimers.length === 0" class="empty-state">
        <Icon name="clock" :size="48" />
        <p>暂无活动计时器</p>
      </div>
      <div class="timers-grid">
        <div v-for="timer in activeTimers" :key="timer.id" class="timer-card" :class="timer.status">
          <div class="timer-header">
            <h3 class="timer-name">{{ timer.name }}</h3>
            <button @click="removeTimer(timer.id)" class="delete-btn" title="删除">
              <Icon name="close" :size="18" />
            </button>
          </div>
          
          <div class="timer-display">
            <span class="time-value">{{ formatTime(timer.remaining) }}</span>
            <span class="time-label">/ {{ formatTime(timer.duration) }}</span>
          </div>
          
          <div class="timer-progress">
            <div class="progress-bar">
              <div 
                class="progress-fill" 
                :style="{ width: ((timer.duration - timer.remaining) / timer.duration * 100) + '%' }"
              ></div>
            </div>
          </div>
          
          <div class="timer-controls">
            <button 
              v-if="timer.status === 'pending' || timer.status === 'paused'"
              @click="startTimer(timer.id)"
              class="btn-primary btn-sm"
            >
              <Icon name="play" :size="16" />
              <span>开始</span>
            </button>
            <button 
              v-if="timer.status === 'running'"
              @click="pauseTimer(timer.id)"
              class="btn-warning btn-sm"
            >
              <Icon name="pause" :size="16" />
              <span>暂停</span>
            </button>
            <button 
              @click="resetTimer(timer.id)"
              class="btn-secondary btn-sm"
            >
              <Icon name="refresh" :size="16" />
              <span>重置</span>
            </button>
          </div>
          
          <div class="timer-status">
            <span class="status-badge" :class="timer.status">
              {{ getStatusText(timer.status) }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="card history-section">
      <div class="card-header">
        <h2>历史记录</h2>
        <button @click="refreshHistory" class="btn-secondary btn-sm">
          <Icon name="refresh" :size="16" />
          <span>刷新</span>
        </button>
      </div>
      <div v-if="timerHistory.length === 0" class="empty-state">
        <Icon name="history" :size="48" />
        <p>暂无历史记录</p>
      </div>
      <div v-else class="history-list">
        <div v-for="item in timerHistory" :key="item.id + item.completed_at" class="history-item">
          <div class="history-info">
            <span class="history-name">{{ item.name }}</span>
            <span class="history-duration">时长: {{ formatTime(item.duration) }}</span>
          </div>
          <span class="history-time">{{ formatDateTime(item.completed_at) }}</span>
        </div>
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
import { ref, onMounted, onUnmounted } from 'vue'
import {
  createTimer,
  startTimer as apiStartTimer,
  pauseTimer as apiPauseTimer,
  resetTimer as apiResetTimer,
  deleteTimer,
  getActiveTimers,
  getTimerHistory
} from '../api'
import Icon from '../components/Icon.vue'

const newTimerName = ref('')
const newTimerDuration = ref(60)
const activeTimers = ref([])
const timerHistory = ref([])
const error = ref('')
const successMessage = ref('')
let refreshInterval = null

const formatTime = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  
  if (hours > 0) {
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }
  return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

const formatDateTime = (isoString) => {
  const date = new Date(isoString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const getStatusText = (status) => {
  const statusMap = {
    pending: '待开始',
    running: '进行中',
    paused: '已暂停',
    completed: '已完成'
  }
  return statusMap[status] || status
}

const setPreset = (seconds) => {
  newTimerDuration.value = seconds
}

const createNewTimer = async () => {
  if (!newTimerName.value.trim()) {
    showError('请输入计时器名称')
    return
  }
  if (!newTimerDuration.value || newTimerDuration.value < 1) {
    showError('请输入有效的时长')
    return
  }
  
  try {
    await createTimer({
      name: newTimerName.value.trim(),
      duration: newTimerDuration.value
    })
    newTimerName.value = ''
    showSuccess('计时器创建成功')
    await refreshActiveTimers()
  } catch (err) {
    showError('创建计时器失败')
  }
}

const startTimer = async (timerId) => {
  try {
    await apiStartTimer(timerId)
    await refreshActiveTimers()
  } catch (err) {
    showError('启动计时器失败')
  }
}

const pauseTimer = async (timerId) => {
  try {
    await apiPauseTimer(timerId)
    await refreshActiveTimers()
  } catch (err) {
    showError('暂停计时器失败')
  }
}

const resetTimer = async (timerId) => {
  try {
    await apiResetTimer(timerId)
    await refreshActiveTimers()
  } catch (err) {
    showError('重置计时器失败')
  }
}

const removeTimer = async (timerId) => {
  try {
    await deleteTimer(timerId)
    await refreshActiveTimers()
    showSuccess('计时器已删除')
  } catch (err) {
    showError('删除计时器失败')
  }
}

const refreshActiveTimers = async () => {
  try {
    const response = await getActiveTimers()
    activeTimers.value = response.data
  } catch (err) {
    console.error('刷新计时器状态失败')
  }
}

const refreshHistory = async () => {
  try {
    const response = await getTimerHistory()
    timerHistory.value = response.data
  } catch (err) {
    showError('获取历史记录失败')
  }
}

const showError = (msg) => {
  error.value = msg
  setTimeout(() => error.value = '', 3000)
}

const showSuccess = (msg) => {
  successMessage.value = msg
  setTimeout(() => successMessage.value = '', 2000)
}

onMounted(async () => {
  await refreshActiveTimers()
  await refreshHistory()
  refreshInterval = setInterval(refreshActiveTimers, 1000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<style scoped>
.timer-tool {
  width: 100%;
  max-width: 1000px;
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
  background: rgba(245, 158, 11, 0.1);
  color: var(--accent-warning);
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

.create-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-group label {
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

.quick-presets {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.preset-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.create-btn {
  align-self: flex-start;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.timer-count {
  font-size: 0.875rem;
  color: var(--text-secondary);
  background: var(--bg-tertiary);
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-full);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  color: var(--text-tertiary);
  gap: 1rem;
}

.empty-state p {
  margin: 0;
}

.timers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.timer-card {
  background: var(--bg-tertiary);
  border: 2px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  transition: all var(--transition-normal);
}

.timer-card.running {
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.timer-card.completed {
  border-color: var(--accent-success);
  background: rgba(16, 185, 129, 0.05);
}

.timer-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.timer-name {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
  flex: 1;
}

.delete-btn {
  padding: 0.375rem;
  background: transparent;
  border: none;
  border-radius: var(--radius-sm);
  color: var(--text-tertiary);
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
}

.delete-btn:hover {
  background: rgba(239, 68, 68, 0.1);
  color: var(--accent-error);
}

.timer-display {
  text-align: center;
  padding: 1rem 0;
}

.timer-display .time-value {
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
}

.timer-display .time-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-left: 0.5rem;
}

.timer-progress {
  width: 100%;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: var(--border-light);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-success));
  border-radius: var(--radius-full);
  transition: width 0.3s ease;
}

.timer-controls {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.timer-status {
  display: flex;
  justify-content: center;
}

.status-badge {
  padding: 0.375rem 0.75rem;
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.pending {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
}

.status-badge.running {
  background: rgba(59, 130, 246, 0.1);
  color: var(--accent-primary);
}

.status-badge.paused {
  background: rgba(245, 158, 11, 0.1);
  color: var(--accent-warning);
}

.status-badge.completed {
  background: rgba(16, 185, 129, 0.1);
  color: var(--accent-success);
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.875rem 1rem;
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
}

.history-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.history-name {
  font-weight: 600;
  color: var(--text-primary);
}

.history-duration {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.history-time {
  font-size: 0.875rem;
  color: var(--text-tertiary);
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

@media (max-width: 768px) {
  .input-row {
    grid-template-columns: 1fr;
  }
  
  .timers-grid {
    grid-template-columns: 1fr;
  }
}
</style>
