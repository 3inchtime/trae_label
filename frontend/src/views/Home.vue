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
  gap: 1rem;
  font-size: 1.75rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent-primary) 30%, var(--accent-secondary) 60%, var(--accent-tertiary) 100%);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 2rem;
  position: relative;
  padding-bottom: 0.75rem;
  animation: gradientShift 10s ease infinite;
}

.section-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 150px;
  height: 4px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary), var(--accent-tertiary), transparent);
  border-radius: 2px;
  box-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
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
  border-radius: var(--radius-xl);
  padding: 1.75rem;
  text-decoration: none;
  display: flex;
  align-items: flex-start;
  gap: 1.25rem;
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-glass);
  animation: fadeInUp 0.6s ease-out forwards;
  opacity: 0;
}

.tool-card:nth-child(1) { animation-delay: 0.1s; }
.tool-card:nth-child(2) { animation-delay: 0.2s; }
.tool-card:nth-child(3) { animation-delay: 0.3s; }
.tool-card:nth-child(4) { animation-delay: 0.4s; }
.tool-card:nth-child(5) { animation-delay: 0.5s; }
.tool-card:nth-child(6) { animation-delay: 0.6s; }

.tool-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 2px;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary), var(--accent-tertiary), var(--accent-pink), transparent);
  background-size: 300% 300%;
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity var(--transition-normal);
  animation: gradientBorder 8s ease infinite;
  pointer-events: none;
}

.tool-card::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.05) 0%, transparent 60%);
  opacity: 0;
  transition: opacity var(--transition-slow);
  pointer-events: none;
}

.tool-card:hover::before {
  opacity: 1;
}

.tool-card:hover::after {
  opacity: 1;
}

.tool-card:hover {
  box-shadow: 0 20px 50px rgba(99, 102, 241, 0.15), 0 8px 20px rgba(0, 0, 0, 0.08);
  transform: translateY(-8px) scale(1.02);
  border-color: transparent;
}

.tool-icon-wrapper {
  width: 72px;
  height: 72px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.tool-icon-wrapper::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.4) 0%, transparent 50%);
  opacity: 0;
  transition: opacity var(--transition-normal);
}

.tool-icon-wrapper::after {
  content: '';
  position: absolute;
  inset: -10px;
  background: radial-gradient(circle, currentColor 0%, transparent 70%);
  opacity: 0;
  transition: opacity var(--transition-normal);
  filter: blur(10px);
}

.tool-card:hover .tool-icon-wrapper {
  transform: scale(1.15) rotate(8deg);
}

.tool-card:hover .tool-icon-wrapper::before,
.tool-card:hover .tool-icon-wrapper::after {
  opacity: 0.15;
}

.tool-icon-wrapper.clock {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(139, 92, 246, 0.15) 100%);
  color: var(--accent-primary);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.25);
}

.tool-icon-wrapper.json {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.25) 0%, rgba(124, 58, 237, 0.15) 100%);
  color: var(--accent-secondary);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.25);
}

.tool-icon-wrapper.lock {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.25) 0%, rgba(5, 150, 105, 0.15) 100%);
  color: var(--accent-success);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.25);
}

.tool-icon-wrapper.money {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.25) 0%, rgba(217, 119, 6, 0.15) 100%);
  color: var(--accent-warning);
  box-shadow: 0 6px 20px rgba(245, 158, 11, 0.25);
}

.tool-icon-wrapper.key {
  background: linear-gradient(135deg, rgba(124, 58, 237, 0.25) 0%, rgba(99, 102, 241, 0.15) 100%);
  color: #7c3aed;
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.25);
}

.tool-icon-wrapper.timer {
  background: linear-gradient(135deg, rgba(251, 146, 60, 0.25) 0%, rgba(249, 115, 22, 0.15) 100%);
  color: #f97316;
  box-shadow: 0 6px 20px rgba(251, 146, 60, 0.25);
}

.tool-icon-wrapper.weight {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.25) 0%, rgba(22, 163, 74, 0.15) 100%);
  color: #22c55e;
  box-shadow: 0 6px 20px rgba(34, 197, 94, 0.25);
}

.tool-icon-wrapper.time-diff {
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.25) 0%, rgba(8, 145, 178, 0.15) 100%);
  color: #06b6d4;
  box-shadow: 0 6px 20px rgba(6, 182, 212, 0.25);
}

.tool-icon-wrapper.calendar {
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.25) 0%, rgba(219, 39, 119, 0.15) 100%);
  color: #ec4899;
  box-shadow: 0 6px 20px rgba(236, 72, 153, 0.25);
}

.tool-icon-wrapper.length {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.25) 0%, rgba(220, 38, 38, 0.15) 100%);
  color: #ef4444;
  box-shadow: 0 6px 20px rgba(239, 68, 68, 0.25);
}

.tool-icon-wrapper.color {
  background: linear-gradient(135deg, rgba(244, 114, 182, 0.25) 0%, rgba(236, 72, 153, 0.15) 100%);
  color: #f472b6;
  box-shadow: 0 6px 20px rgba(244, 114, 182, 0.25);
}

.tool-content {
  flex: 1;
  min-width: 0;
}

.tool-content h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.625rem;
  transition: all var(--transition-normal);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
}

.tool-content h3::after {
  content: '';
  width: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary), var(--accent-tertiary));
  transition: width var(--transition-normal);
  border-radius: 2px;
  box-shadow: 0 0 8px rgba(99, 102, 241, 0.3);
}

.tool-card:hover .tool-content h3 {
  color: var(--accent-primary);
}

.tool-card:hover .tool-content h3::after {
  width: 40px;
}

.tool-content p {
  font-size: 0.95rem;
  color: var(--text-secondary);
  line-height: 1.7;
  margin: 0;
  transition: all var(--transition-normal);
}

.tool-card:hover .tool-content p {
  color: var(--text-primary);
}

.tool-arrow {
  color: var(--text-tertiary);
  opacity: 0;
  transform: translateX(-15px) scale(0.7);
  transition: all var(--transition-normal);
  flex-shrink: 0;
  align-self: center;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
}

.tool-card:hover .tool-arrow {
  opacity: 1;
  transform: translateX(0) scale(1);
  color: var(--accent-primary);
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.25);
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
