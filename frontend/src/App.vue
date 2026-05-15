<template>
  <div id="app" :class="{ dark: isDark }">
    <nav class="navbar">
      <div class="nav-container">
        <div class="nav-brand">
          <Icon name="tools" :size="24" />
          <span>便携工具平台</span>
        </div>
        <div class="nav-links">
          <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">
            <Icon name="home" :size="18" />
            <span>首页</span>
          </router-link>
          <router-link to="/tools" class="nav-link" :class="{ active: $route.path === '/tools' }">
            <Icon name="tools" :size="18" />
            <span>工具列表</span>
          </router-link>
        </div>
        <button @click="toggleDarkMode" class="theme-toggle" :title="isDark ? '切换到浅色模式' : '切换到深色模式'">
          <Icon :name="isDark ? 'sun' : 'moon'" :size="20" />
        </button>
      </div>
    </nav>
    <div class="app-body">
      <aside class="sidebar">
        <div class="sidebar-header">
          <h3>功能列表</h3>
        </div>
        <nav class="sidebar-nav">
          <router-link to="/tools/timestamp" class="sidebar-link" :class="{ active: $route.path === '/tools/timestamp' }">
            <Icon name="clock" :size="18" />
            <span>时间戳转换</span>
          </router-link>
          <router-link to="/tools/json" class="sidebar-link" :class="{ active: $route.path === '/tools/json' }">
            <Icon name="json" :size="18" />
            <span>JSON格式化</span>
          </router-link>
          <router-link to="/tools/md5" class="sidebar-link" :class="{ active: $route.path === '/tools/md5' }">
            <Icon name="lock" :size="18" />
            <span>MD5加密</span>
          </router-link>
          <router-link to="/tools/number-to-chinese" class="sidebar-link" :class="{ active: $route.path === '/tools/number-to-chinese' }">
            <Icon name="money" :size="18" />
            <span>数字转中文</span>
          </router-link>
          <router-link to="/tools/rsa" class="sidebar-link" :class="{ active: $route.path === '/tools/rsa' }">
            <Icon name="lock" :size="18" />
            <span>RSA加密解密</span>
          </router-link>
          <router-link to="/tools/timer" class="sidebar-link" :class="{ active: $route.path === '/tools/timer' }">
            <Icon name="clock" :size="18" />
            <span>在线计时器</span>
          </router-link>
          <router-link to="/tools/weight" class="sidebar-link" :class="{ active: $route.path === '/tools/weight' }">
          <Icon name="box" :size="18" />
          <span>重量单位换算</span>
        </router-link>
        <router-link to="/tools/time-difference" class="sidebar-link" :class="{ active: $route.path === '/tools/time-difference' }">
          <Icon name="clock" :size="18" />
          <span>时间差计算</span>
        </router-link>
      </nav>
      </aside>
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import Icon from './components/Icon.vue'

const isDark = ref(false)

const toggleDarkMode = () => {
  isDark.value = !isDark.value
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDark.value = true
  }
})

watch(isDark, (newValue) => {
  if (newValue) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
})
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-light);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 100;
  transition: all var(--transition-slow);
}

.nav-container {
  max-width: 100%;
  margin: 0 auto;
  padding: 0 1.5rem;
  height: 64px;
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--accent-primary);
  flex-shrink: 0;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  transition: all var(--transition-normal);
}

.nav-link:hover {
  color: var(--text-primary);
  background: var(--bg-tertiary);
}

.nav-link.active {
  color: var(--accent-primary);
  background: rgba(59, 130, 246, 0.1);
}

.theme-toggle {
  padding: 0.5rem;
  background: var(--bg-tertiary);
  border: none;
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-normal);
  display: flex;
  align-items: center;
  justify-content: center;
}

.theme-toggle:hover {
  background: var(--border-medium);
  color: var(--text-primary);
}

.app-body {
  display: flex;
  flex: 1;
  min-height: 0;
}

.sidebar {
  width: 260px;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-light);
  display: flex;
  flex-direction: column;
  transition: all var(--transition-slow);
  flex-shrink: 0;
}

.sidebar-header {
  padding: 1.5rem 1.25rem 1rem;
  border-bottom: 1px solid var(--border-light);
}

.sidebar-header h3 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.sidebar-nav {
  padding: 1rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
  overflow-y: auto;
}

.sidebar-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  transition: all var(--transition-normal);
}

.sidebar-link:hover {
  color: var(--text-primary);
  background: var(--bg-tertiary);
}

.sidebar-link.active {
  color: var(--accent-primary);
  background: rgba(59, 130, 246, 0.1);
}

.main-content {
  flex: 1;
  padding: 2rem 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  overflow-y: auto;
}

@media (max-width: 1024px) {
  .sidebar {
    width: 220px;
  }
}

@media (max-width: 768px) {
  .nav-container {
    padding: 0 1rem;
    gap: 1rem;
  }
  
  .nav-brand span {
    display: none;
  }
  
  .nav-link span {
    display: none;
  }
  
  .sidebar {
    display: none;
  }
  
  .main-content {
    padding: 1.5rem 1rem;
  }
}
</style>
