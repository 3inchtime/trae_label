<template>
  <div class="reaction-test">
    <div class="page-header">
      <div class="page-icon">
        <Icon name="zap" :size="28" />
      </div>
      <div class="page-title">
        <h1>反应速度测试</h1>
        <p>测试你的反应速度，当颜色变为绿色时尽快点击</p>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>开始测试</h2>
      </div>
      
      <div 
        class="reaction-area" 
        :class="gameState"
        @click="handleClick"
      >
        <div class="reaction-content">
          <span v-if="gameState === 'waiting'" class="waiting-text">点击开始测试</span>
          <span v-else-if="gameState === 'ready'" class="ready-text">等待变绿...</span>
          <span v-else-if="gameState === 'go'" class="go-text">现在点击！</span>
          <span v-else-if="gameState === 'result'" class="result-text">
            反应时间: {{ reactionTime }}ms
          </span>
          <span v-else-if="gameState === 'too-early'" class="too-early-text">
            太早了！请等变绿后再点击
          </span>
        </div>
      </div>

      <div class="stats-section">
        <div class="stat-item">
          <span class="stat-label">当前</span>
          <span class="stat-value">{{ reactionTime || '--' }}ms</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">最佳</span>
          <span class="stat-value">{{ bestTime || '--' }}ms</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">平均</span>
          <span class="stat-value">{{ averageTime || '--' }}ms</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">次数</span>
          <span class="stat-value">{{ history.length }}</span>
        </div>
      </div>

      <div class="controls">
        <button @click="resetTest" class="btn-secondary">
          <Icon name="refresh" :size="18" />
          <span>重新开始</span>
        </button>
        <button @click="clearHistory" class="btn-secondary" :disabled="history.length === 0">
          <Icon name="trash" :size="18" />
          <span>清除记录</span>
        </button>
      </div>
    </div>

    <div class="card history-card" v-if="history.length > 0">
      <div class="card-header">
        <h2>历史记录</h2>
      </div>
      <div class="history-list">
        <div 
          v-for="(item, index) in history.slice().reverse()" 
          :key="index" 
          class="history-item"
          :class="{ best: item === bestTime }"
        >
          <span class="history-index">#{{ history.length - index }}</span>
          <span class="history-time">{{ item }}ms</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import Icon from '../components/Icon.vue'

const gameState = ref('waiting')
const startTime = ref(null)
const reactionTime = ref(null)
const timeoutId = ref(null)
const history = ref([])

const bestTime = computed(() => {
  if (history.value.length === 0) return null
  return Math.min(...history.value)
})

const averageTime = computed(() => {
  if (history.value.length === 0) return null
  const sum = history.value.reduce((a, b) => a + b, 0)
  return Math.round(sum / history.value.length)
})

const handleClick = () => {
  if (gameState.value === 'waiting') {
    startTest()
  } else if (gameState.value === 'ready') {
    clearTimeout(timeoutId.value)
    gameState.value = 'too-early'
  } else if (gameState.value === 'go') {
    const endTime = Date.now()
    reactionTime.value = endTime - startTime.value
    history.value.push(reactionTime.value)
    gameState.value = 'result'
  } else if (gameState.value === 'result' || gameState.value === 'too-early') {
    startTest()
  }
}

const startTest = () => {
  gameState.value = 'ready'
  reactionTime.value = null
  
  const delay = Math.random() * 4000 + 1000
  timeoutId.value = setTimeout(() => {
    gameState.value = 'go'
    startTime.value = Date.now()
  }, delay)
}

const resetTest = () => {
  clearTimeout(timeoutId.value)
  gameState.value = 'waiting'
  reactionTime.value = null
}

const clearHistory = () => {
  history.value = []
}

onUnmounted(() => {
  if (timeoutId.value) {
    clearTimeout(timeoutId.value)
  }
})
</script>

<style scoped>
.reaction-test {
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
  background: rgba(147, 51, 234, 0.1);
  color: #9333ea;
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

.reaction-area {
  width: 100%;
  height: 300px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-normal);
  user-select: none;
  margin-bottom: 1.5rem;
}

.reaction-area.waiting {
  background: #3b82f6;
}

.reaction-area.ready {
  background: #ef4444;
}

.reaction-area.go {
  background: #10b981;
}

.reaction-area.result {
  background: #8b5cf6;
}

.reaction-area.too-early {
  background: #f59e0b;
}

.reaction-content {
  text-align: center;
}

.waiting-text,
.ready-text,
.go-text,
.result-text,
.too-early-text {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
  gap: 0.5rem;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  font-family: 'Monaco', 'Menlo', monospace;
}

.controls {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn-secondary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius-md);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-normal);
  border: 2px solid var(--border-light);
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.btn-secondary:hover:not(:disabled) {
  border-color: var(--border-medium);
  background: var(--bg-secondary);
}

.btn-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.history-card {
}

.history-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.history-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.75rem 1rem;
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
  min-width: 80px;
  border: 2px solid transparent;
}

.history-item.best {
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.history-index {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.history-time {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--text-primary);
  font-family: 'Monaco', 'Menlo', monospace;
}

@media (max-width: 768px) {
  .stats-section {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .waiting-text,
  .ready-text,
  .go-text,
  .result-text,
  .too-early-text {
    font-size: 1.5rem;
  }
}
</style>
