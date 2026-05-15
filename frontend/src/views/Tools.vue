<template>
  <div class="tools-page">
    <div class="page-header">
      <div class="page-icon">
        <Icon name="tools" :size="28" />
      </div>
      <div class="page-title">
        <h1>工具列表</h1>
        <p>便捷的在线工具箱，提高您的工作效率</p>
      </div>
    </div>
    
    <div v-if="loading" class="loading-state">
      <div class="spinner-icon">
        <Icon name="tools" :size="32" class="spinning" />
      </div>
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <Icon name="error" :size="48" />
      <p>{{ error }}</p>
    </div>
    
    <div v-else class="tools-grid">
      <router-link to="/tools/timestamp" class="tool-card">
        <div class="tool-icon clock">
          <Icon name="clock" :size="32" />
        </div>
        <div class="tool-info">
          <h3>时间戳转换</h3>
          <p>时间戳与日期时间的相互转换</p>
        </div>
        <div class="tool-arrow">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </div>
      </router-link>
      
      <router-link to="/tools/json" class="tool-card">
        <div class="tool-icon json">
          <Icon name="json" :size="32" />
        </div>
        <div class="tool-info">
          <h3>JSON格式化</h3>
          <p>验证JSON格式，支持格式化和压缩</p>
        </div>
        <div class="tool-arrow">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </div>
      </router-link>
      
      <router-link to="/tools/md5" class="tool-card">
        <div class="tool-icon lock">
          <Icon name="lock" :size="32" />
        </div>
        <div class="tool-info">
          <h3>MD5加密</h3>
          <p>文本MD5哈希加密与对比验证</p>
        </div>
        <div class="tool-arrow">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </div>
      </router-link>
      
      <router-link to="/tools/number-to-chinese" class="tool-card">
        <div class="tool-icon money">
          <Icon name="money" :size="32" />
        </div>
        <div class="tool-info">
          <h3>数字转中文大写</h3>
          <p>将数字金额转换为标准中文大写</p>
        </div>
        <div class="tool-arrow">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </div>
      </router-link>
      
      <router-link to="/tools/rsa" class="tool-card">
        <div class="tool-icon key">
          <Icon name="lock" :size="32" />
        </div>
        <div class="tool-info">
          <h3>RSA加密解密</h3>
          <p>生成密钥对，使用公钥加密、私钥解密</p>
        </div>
        <div class="tool-arrow">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTools } from '../api'
import Icon from '../components/Icon.vue'

const tools = ref([])
const loading = ref(false)
const error = ref('')

const fetchTools = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await getTools()
    tools.value = response.data
  } catch (err) {
    error.value = '加载工具列表失败'
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchTools)
</script>

<style scoped>
.tools-page {
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

.loading-state,
.error-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-secondary);
}

.spinner-icon {
  margin-bottom: 1rem;
  color: var(--accent-primary);
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-state {
  color: var(--accent-error);
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.25rem;
}

.tool-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.tool-card:hover {
  border-color: var(--accent-primary);
  box-shadow: var(--shadow-lg);
  transform: translateY(-4px);
}

.tool-icon {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.tool-icon.clock {
  background: rgba(59, 130, 246, 0.1);
  color: var(--accent-primary);
}

.tool-icon.json {
  background: rgba(99, 102, 241, 0.1);
  color: var(--accent-secondary);
}

.tool-icon.lock {
  background: rgba(16, 185, 129, 0.1);
  color: var(--accent-success);
}

.tool-icon.money {
  background: rgba(245, 158, 11, 0.1);
  color: var(--accent-warning);
}

.tool-icon.key {
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
}

.tool-info {
  flex: 1;
  min-width: 0;
}

.tool-info h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  transition: color var(--transition-fast);
}

.tool-card:hover .tool-info h3 {
  color: var(--accent-primary);
}

.tool-info p {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.4;
}

.tool-arrow {
  color: var(--text-tertiary);
  opacity: 0;
  transform: translateX(-10px);
  transition: all var(--transition-normal);
  flex-shrink: 0;
}

.tool-card:hover .tool-arrow {
  opacity: 1;
  transform: translateX(0);
  color: var(--accent-primary);
}

@media (max-width: 640px) {
  .tools-grid {
    grid-template-columns: 1fr;
  }
}
</style>
