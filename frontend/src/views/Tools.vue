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
    
    <div class="tools-grid">
      <router-link
        v-for="tool in tools"
        :key="tool.id"
        :to="tool.path"
        class="tool-card"
      >
        <div :class="['tool-icon', tool.iconClass]">
          <Icon :name="tool.icon" :size="32" />
        </div>
        <div class="tool-info">
          <h3>{{ tool.name }}</h3>
          <p>{{ tool.shortDescription }}</p>
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
import Icon from '../components/Icon.vue'
import { toolsConfig } from '../config/toolsConfig'

const tools = toolsConfig
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

.tool-icon.timer {
  background: rgba(245, 158, 11, 0.1);
  color: var(--accent-warning);
}

.tool-icon.weight {
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
}

.tool-icon.time-diff {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.tool-icon.calendar {
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
}

.tool-icon.length {
  background: rgba(251, 146, 60, 0.1);
  color: #fb923c;
}

.tool-icon.color {
  background: rgba(236, 72, 153, 0.1);
  color: #ec4899;
}

.tool-icon.url {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.tool-icon.yaml {
  background: rgba(168, 85, 247, 0.1);
  color: #a855f7;
}

.tool-icon.reaction {
  background: rgba(249, 115, 22, 0.1);
  color: #f97316;
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
