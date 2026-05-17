<template>
  <div class="home">
    <div class="section">
      <h2 class="section-header">
        <Icon name="tools" :size="24" />
        <span>可用工具</span>
      </h2>
      <div class="tools-grid">
        <router-link
          v-for="tool in tools"
          :key="tool.id"
          :to="tool.path"
          class="tool-card"
        >
          <div :class="['tool-icon-wrapper', tool.iconClass]">
            <Icon :name="tool.icon" :size="28" />
          </div>
          <div class="tool-content">
            <h3>{{ tool.name }}</h3>
            <p>{{ tool.description }}</p>
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
import { toolsConfig } from '../config/toolsConfig'

const tools = toolsConfig
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
