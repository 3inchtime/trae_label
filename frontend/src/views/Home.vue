<template>
  <div class="home">
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
        
        <router-link to="/tools/rsa" class="tool-card">
          <div class="tool-icon-wrapper key">
            <Icon name="lock" :size="28" />
          </div>
          <div class="tool-content">
            <h3>RSA 加密解密</h3>
            <p>生成RSA密钥对，使用公钥加密、私钥解密，支持多种密钥长度</p>
          </div>
          <div class="tool-arrow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </div>
        </router-link>
        
        <router-link to="/tools/timer" class="tool-card">
          <div class="tool-icon-wrapper timer">
            <Icon name="clock" :size="28" />
          </div>
          <div class="tool-content">
            <h3>在线计时器</h3>
            <p>创建和管理多个倒计时计时器，支持暂停、重置和历史记录</p>
          </div>
          <div class="tool-arrow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </div>
        </router-link>
        
        <router-link to="/tools/weight" class="tool-card">
          <div class="tool-icon-wrapper weight">
            <Icon name="box" :size="28" />
          </div>
          <div class="tool-content">
            <h3>重量单位换算</h3>
            <p>支持克、千克、吨、磅、盎司、斤、两等多种重量单位的相互转换</p>
          </div>
          <div class="tool-arrow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </div>
        </router-link>
        
        <router-link to="/tools/time-difference" class="tool-card">
          <div class="tool-icon-wrapper time-diff">
            <Icon name="clock" :size="28" />
          </div>
          <div class="tool-content">
            <h3>时间差计算</h3>
            <p>计算两个时间之间的年、月、日、秒差距，支持多种时间格式</p>
          </div>
          <div class="tool-arrow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </div>
        </router-link>
        
        <router-link to="/tools/calendar" class="tool-card">
          <div class="tool-icon-wrapper calendar">
            <Icon name="calendar" :size="28" />
          </div>
          <div class="tool-content">
            <h3>万年历</h3>
            <p>查看公历、农历、节气、节日等信息，支持快速跳转任意年月</p>
          </div>
          <div class="tool-arrow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </div>
        </router-link>
        
        <router-link to="/tools/length" class="tool-card">
          <div class="tool-icon-wrapper length">
            <Icon name="ruler" :size="28" />
          </div>
          <div class="tool-content">
            <h3>长度单位换算</h3>
            <p>支持米、千米、英寸、英尺、英里、里、丈、尺、寸等多种长度单位的相互转换</p>
          </div>
          <div class="tool-arrow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </div>
        </router-link>
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

.tool-icon-wrapper.key {
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
}

.tool-icon-wrapper.timer {
  background: rgba(245, 158, 11, 0.1);
  color: var(--accent-warning);
}

.tool-icon-wrapper.weight {
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
}

.tool-icon-wrapper.time-diff {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.tool-icon-wrapper.calendar {
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
}

.tool-icon-wrapper.length {
  background: rgba(251, 146, 60, 0.1);
  color: #fb923c;
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

@media (max-width: 640px) {
  .tools-grid {
    grid-template-columns: 1fr;
  }
}
</style>
