<template>
  <div class="home">
    <div class="hero-section">
      <h1 class="hero-title">欢迎使用便携工具平台</h1>
      <p class="hero-subtitle">集成多个实用工具，提升工作效率，让开发更简单</p>
    </div>
    
    <div class="section">
      <h2 class="section-header">
        <Icon name="tools" :size="24" />
        <span>可用工具</span>
      </h2>
      <div class="tools-grid">
        <router-link to="/tools/timestamp" class="tool-card">
          <div class="tool-icon-wrapper clock">
            <Icon name="clock" :size="28" />
          </div>
          <div class="tool-content">
            <h3>时间戳转换</h3>
            <p>时间戳与日期时间的相互转换，支持快捷时间点</p>
          </div>
          <div class="tool-arrow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </div>
        </router-link>
        
        <router-link to="/tools/json" class="tool-card">
          <div class="tool-icon-wrapper json">
            <Icon name="json" :size="28" />
          </div>
          <div class="tool-content">
            <h3>JSON格式化</h3>
            <p>验证JSON格式正确性，支持格式化和压缩功能</p>
          </div>
          <div class="tool-arrow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </div>
        </router-link>
        
        <router-link to="/tools/md5" class="tool-card">
          <div class="tool-icon-wrapper lock">
            <Icon name="lock" :size="28" />
          </div>
          <div class="tool-content">
            <h3>MD5 加密</h3>
            <p>文本MD5哈希加密与对比验证工具</p>
          </div>
          <div class="tool-arrow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </div>
        </router-link>
        
        <router-link to="/tools/number-to-chinese" class="tool-card">
          <div class="tool-icon-wrapper money">
            <Icon name="money" :size="28" />
          </div>
          <div class="tool-content">
            <h3>数字转中文大写</h3>
            <p>将数字金额转换为标准中文大写金额，支持小数和负数</p>
          </div>
          <div class="tool-arrow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </div>
        </router-link>
      </div>
    </div>

    <div class="section">
      <h2 class="section-header">
        <Icon name="star" :size="24" />
        <span>平台特性</span>
      </h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon rocket">
            <Icon name="rocket" :size="28" />
          </div>
          <h3>快速开发</h3>
          <p>基于 FastAPI + Vue 3 构建，开发效率高，性能优异</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon database">
            <Icon name="database" :size="28" />
          </div>
          <h3>轻量数据库</h3>
          <p>使用 SQLite，无需额外配置，开箱即用</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon wrench">
            <Icon name="wrench" :size="28" />
          </div>
          <h3>工具扩展</h3>
          <p>模块化设计，轻松添加新的便携工具，持续扩展</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Icon from '../components/Icon.vue'
</script>

<style scoped>
.home {
  width: 100%;
}

.hero-section {
  text-align: center;
  margin-bottom: 3rem;
  padding: 2rem 0;
}

.hero-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 0.75rem;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.125rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
}

.section {
  margin-bottom: 3rem;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.25rem;
}

.tool-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  text-decoration: none;
  display: flex;
  align-items: flex-start;
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

.tool-icon-wrapper {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.tool-icon-wrapper.clock {
  background: rgba(59, 130, 246, 0.1);
  color: var(--accent-primary);
}

.tool-icon-wrapper.json {
  background: rgba(99, 102, 241, 0.1);
  color: var(--accent-secondary);
}

.tool-icon-wrapper.lock {
  background: rgba(16, 185, 129, 0.1);
  color: var(--accent-success);
}

.tool-icon-wrapper.money {
  background: rgba(245, 158, 11, 0.1);
  color: var(--accent-warning);
}

.tool-content {
  flex: 1;
  min-width: 0;
}

.tool-content h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  transition: color var(--transition-fast);
}

.tool-card:hover .tool-content h3 {
  color: var(--accent-primary);
}

.tool-content p {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0;
}

.tool-arrow {
  color: var(--text-tertiary);
  opacity: 0;
  transform: translateX(-10px);
  transition: all var(--transition-normal);
  flex-shrink: 0;
  align-self: center;
}

.tool-card:hover .tool-arrow {
  opacity: 1;
  transform: translateX(0);
  color: var(--accent-primary);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
}

.feature-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  text-align: center;
  transition: all var(--transition-normal);
}

.feature-card:hover {
  border-color: var(--border-medium);
  box-shadow: var(--shadow-md);
}

.feature-icon {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
}

.feature-icon.rocket {
  background: rgba(59, 130, 246, 0.1);
  color: var(--accent-primary);
}

.feature-icon.database {
  background: rgba(99, 102, 241, 0.1);
  color: var(--accent-secondary);
}

.feature-icon.wrench {
  background: rgba(16, 185, 129, 0.1);
  color: var(--accent-success);
}

.feature-card h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.75rem;
}

.feature-card p {
  font-size: 0.95rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}

@media (max-width: 640px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
  }
  
  .tools-grid {
    grid-template-columns: 1fr;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>
