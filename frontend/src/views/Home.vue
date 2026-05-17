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
        
        <router-link to="/tools/color" class="tool-card">
          <div class="tool-icon-wrapper color">
            <Icon name="palette" :size="28" />
          </div>
          <div class="tool-content">
            <h3>颜色选择器</h3>
            <p>可视化选择颜色，支持 HEX/RGB/HSL 格式转换、配色方案生成和对比度检查</p>
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
  gap: 0.875rem;
  font-size: 1.625rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent-primary) 50%, var(--accent-secondary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1.75rem;
  position: relative;
  padding-bottom: 0.5rem;
}

.section-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 120px;
  height: 4px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary), transparent);
  border-radius: 2px;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.5rem;
}

.tool-card {
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  text-decoration: none;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-glass);
}

.tool-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.08), transparent);
  transition: left var(--transition-slow);
}

.tool-card:hover::before {
  left: 100%;
}

.tool-card:hover {
  border-color: var(--accent-primary);
  box-shadow: 0 12px 40px rgba(59, 130, 246, 0.2);
  transform: translateY(-6px) scale(1.01);
}

.tool-icon-wrapper {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.tool-icon-wrapper::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, transparent 50%);
  opacity: 0;
  transition: opacity var(--transition-normal);
}

.tool-card:hover .tool-icon-wrapper {
  transform: scale(1.1) rotate(5deg);
}

.tool-card:hover .tool-icon-wrapper::after {
  opacity: 1;
}

.tool-icon-wrapper.clock {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(14, 165, 233, 0.15) 100%);
  color: var(--accent-primary);
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
}

.tool-icon-wrapper.json {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%);
  color: var(--accent-secondary);
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2);
}

.tool-icon-wrapper.lock {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.15) 100%);
  color: var(--accent-success);
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
}

.tool-icon-wrapper.money {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.15) 100%);
  color: var(--accent-warning);
  box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);
}

.tool-icon-wrapper.key {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(124, 58, 237, 0.15) 100%);
  color: #8b5cf6;
  box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2);
}

.tool-icon-wrapper.timer {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.15) 100%);
  color: var(--accent-warning);
  box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);
}

.tool-icon-wrapper.weight {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(124, 58, 237, 0.15) 100%);
  color: #8b5cf6;
  box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2);
}

.tool-icon-wrapper.time-diff {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(22, 163, 74, 0.15) 100%);
  color: #22c55e;
  box-shadow: 0 4px 15px rgba(34, 197, 94, 0.2);
}

.tool-icon-wrapper.calendar {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(124, 58, 237, 0.15) 100%);
  color: #8b5cf6;
  box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2);
}

.tool-icon-wrapper.length {
  background: linear-gradient(135deg, rgba(251, 146, 60, 0.2) 0%, rgba(249, 115, 22, 0.15) 100%);
  color: #fb923c;
  box-shadow: 0 4px 15px rgba(251, 146, 60, 0.2);
}

.tool-icon-wrapper.color {
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.2) 0%, rgba(124, 58, 237, 0.15) 100%);
  color: #ec4899;
  box-shadow: 0 4px 15px rgba(236, 72, 153, 0.2);
}

.tool-content {
  flex: 1;
  min-width: 0;
}

.tool-content h3 {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  transition: all var(--transition-normal);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.tool-content h3::after {
  content: '';
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  transition: width var(--transition-normal);
  border-radius: 1px;
}

.tool-card:hover .tool-content h3 {
  color: var(--accent-primary);
}

.tool-card:hover .tool-content h3::after {
  width: 30px;
}

.tool-content p {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
  transition: color var(--transition-normal);
}

.tool-card:hover .tool-content p {
  color: var(--text-primary);
}

.tool-arrow {
  color: var(--text-tertiary);
  opacity: 0;
  transform: translateX(-10px) scale(0.8);
  transition: all var(--transition-normal);
  flex-shrink: 0;
  align-self: center;
}

.tool-card:hover .tool-arrow {
  opacity: 1;
  transform: translateX(0) scale(1);
  color: var(--accent-primary);
}

@media (max-width: 768px) {
  .tools-grid {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }
  
  .tool-card {
    padding: 1.25rem;
  }
  
  .tool-icon-wrapper {
    width: 56px;
    height: 56px;
  }
  
  .section-header {
    font-size: 1.375rem;
  }
}

@media (max-width: 480px) {
  .tool-arrow {
    display: none;
  }
}
</style>
