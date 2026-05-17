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
          <router-link to="/tools/calendar" class="sidebar-link" :class="{ active: $route.path === '/tools/calendar' }">
            <Icon name="calendar" :size="18" />
            <span>万年历</span>
          </router-link>
          <router-link to="/tools/length" class="sidebar-link" :class="{ active: $route.path === '/tools/length' }">
            <Icon name="ruler" :size="18" />
            <span>长度单位换算</span>
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
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
  border-bottom: 1px solid var(--glass-border);
  box-shadow: var(--shadow-glass);
  position: sticky;
  top: 0;
  z-index: 100;
  transition: all var(--transition-slow);
}

.nav-container {
  max-width: 100%;
  margin: 0 auto;
  padding: 0 1.5rem;
  height: 70px;
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  font-size: 1.375rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  flex-shrink: 0;
  transition: transform var(--transition-normal);
}

.nav-brand:hover {
  transform: scale(1.02);
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
  padding: 0.625rem 1.125rem;
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.nav-link::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  transition: all var(--transition-normal);
  transform: translateX(-50%);
  border-radius: 2px;
}

.nav-link:hover {
  color: var(--accent-primary);
  background: rgba(59, 130, 246, 0.08);
  transform: translateY(-2px);
}

.nav-link:hover::before {
  width: 80%;
}

.nav-link.active {
  color: var(--accent-primary);
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.12) 0%, rgba(14, 165, 233, 0.08) 100%);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
}

.nav-link.active::before {
  width: 80%;
}

.theme-toggle {
  padding: 0.75rem;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-normal);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
}

.theme-toggle:hover {
  background: rgba(59, 130, 246, 0.1);
  border-color: var(--accent-primary);
  color: var(--accent-primary);
  transform: scale(1.08) rotate(10deg);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}

.app-body {
  display: flex;
  flex: 1;
  min-height: 0;
}

.sidebar {
  width: 280px;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
  border-right: 1px solid var(--glass-border);
  display: flex;
  flex-direction: column;
  transition: all var(--transition-slow);
  flex-shrink: 0;
  box-shadow: 4px 0 20px rgba(59, 130, 246, 0.05);
}

.sidebar-header {
  padding: 1.5rem 1.25rem 1rem;
  border-bottom: 1px solid var(--glass-border);
  position: relative;
}

.sidebar-header::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 1.25rem;
  right: 1.25rem;
  height: 2px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary), transparent);
  border-radius: 1px;
}

.sidebar-header h3 {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sidebar-header h3::before {
  content: '';
  width: 6px;
  height: 6px;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

.sidebar-nav {
  padding: 1.25rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  flex: 1;
  overflow-y: auto;
}

.sidebar-link {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 0.875rem 1.125rem;
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.sidebar-link::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  width: 0;
  height: 0;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  border-radius: 0 4px 4px 0;
  transition: all var(--transition-normal);
  transform: translateY(-50%);
}

.sidebar-link:hover {
  color: var(--accent-primary);
  background: rgba(59, 130, 246, 0.08);
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
}

.sidebar-link:hover::before {
  width: 4px;
  height: 60%;
}

.sidebar-link.active {
  color: var(--accent-primary);
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(14, 165, 233, 0.1) 100%);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.sidebar-link.active::before {
  width: 4px;
  height: 60%;
}

.main-content {
  flex: 1;
  padding: 2.5rem 2rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  overflow-y: auto;
  animation: fadeInUp 0.5s ease-out;
}

@media (max-width: 1024px) {
  .sidebar {
    width: 240px;
  }
  
  .main-content {
    padding: 2rem 1.5rem;
  }
}

@media (max-width: 768px) {
  .nav-container {
    padding: 0 1rem;
    gap: 1rem;
    height: 64px;
  }
  
  .nav-brand {
    font-size: 1.125rem;
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
