<template>
  <div class="home">
    <h2>欢迎使用便携工具平台</h2>
    <p>这是一个前后端分离的工具平台，集成了多个实用工具。</p>
    
    <h3 class="tools-title">可用工具</h3>
    <div class="tools-grid">
      <router-link to="/tools/timestamp" class="tool-card">
        <div class="tool-icon">⏰</div>
        <h4>时间戳转换</h4>
        <p>时间戳与日期时间的相互转换，支持快捷时间点</p>
      </router-link>
    </div>

    <h3 class="features-title">平台特性</h3>
    <div class="features">
      <div class="feature-card">
        <h3>🚀 快速开发</h3>
        <p>基于 FastAPI + Vue 3 构建，开发效率高</p>
      </div>
      <div class="feature-card">
        <h3>💾 轻量数据库</h3>
        <p>使用 SQLite，无需额外配置</p>
      </div>
      <div class="feature-card">
        <h3>🔧 工具扩展</h3>
        <p>轻松添加新的便携工具</p>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.home {
  max-width: 1000px;
  margin: 0 auto;
}

h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: var(--text-primary);
  transition: color 0.3s;
}

p {
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin-bottom: 2rem;
  transition: color 0.3s;
}

.tools-title, .features-title {
  font-size: 1.5rem;
  margin: 2.5rem 0 1.5rem;
  color: var(--text-primary);
  transition: color 0.3s;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.tools-grid .tool-card {
  background: var(--bg-secondary);
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px var(--shadow);
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s, box-shadow 0.2s, background 0.3s;
  display: block;
}

.tools-grid .tool-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px var(--shadow-hover);
}

.tool-icon {
  font-size: 2.5rem;
  margin-bottom: 0.75rem;
}

.tools-grid h4 {
  margin-bottom: 0.5rem;
  color: var(--text-primary);
  font-size: 1.1rem;
  transition: color 0.3s;
}

.tools-grid p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-secondary);
  transition: color 0.3s;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.feature-card {
  background: var(--bg-secondary);
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px var(--shadow);
  transition: background 0.3s, box-shadow 0.3s;
}

.feature-card h3 {
  margin-bottom: 0.5rem;
  color: var(--text-primary);
  transition: color 0.3s;
}

.feature-card p {
  margin: 0;
  font-size: 0.95rem;
  color: var(--text-secondary);
  transition: color 0.3s;
}
</style>
