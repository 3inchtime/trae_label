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
        <div class="nav-auth">
          <div v-if="user" class="user-info">
            <div class="user-avatar">
              <Icon name="user" :size="18" />
            </div>
            <span class="username">{{ user.username }}</span>
            <button @click="logout" class="logout-btn" title="退出登录">
              <Icon name="lock" :size="16" />
            </button>
          </div>
          <router-link v-else to="/auth" class="login-btn">
            <Icon name="user" :size="18" />
            <span>登录/注册</span>
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
          <router-link to="/tools/color" class="sidebar-link" :class="{ active: $route.path === '/tools/color' }">
            <Icon name="palette" :size="18" />
            <span>颜色选择器</span>
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
import { useRouter } from 'vue-router'
import Icon from './components/Icon.vue'

const router = useRouter()
const isDark = ref(false)
const user = ref(null)

const toggleDarkMode = () => {
  isDark.value = !isDark.value
}

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  user.value = null
  router.push('/')
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDark.value = true
  }
  
  const savedUser = localStorage.getItem('user')
  if (savedUser) {
    try {
      user.value = JSON.parse(savedUser)
    } catch (e) {
      localStorage.removeItem('user')
    }
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
  backdrop-filter: var(--glass-backdrop-strong);
  -webkit-backdrop-filter: var(--glass-backdrop-strong);
  border-bottom: 1px solid var(--glass-border);
  box-shadow: var(--shadow-glass);
  position: sticky;
  top: 0;
  z-index: 100;
  transition: all var(--transition-slow);
}

.navbar::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--gradient-primary);
  opacity: 0.4;
}

.nav-container {
  max-width: 100%;
  margin: 0 auto;
  padding: 0 1.5rem;
  height: 72px;
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  font-size: 1.5rem;
  font-weight: 800;
  background: var(--gradient-primary);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  flex-shrink: 0;
  transition: all var(--transition-normal);
  animation: gradientShift 8s ease infinite;
  position: relative;
}

.nav-brand::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--gradient-primary);
  border-radius: 2px;
  transform: scaleX(0);
  transition: transform var(--transition-normal);
  transform-origin: left;
  box-shadow: 0 0 8px rgba(59, 130, 246, 0.3);
}

.nav-brand:hover {
  transform: scale(1.03);
}

.nav-brand:hover::after {
  transform: scaleX(1);
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}

.nav-auth {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-right: 0.5rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 1rem;
  background: var(--glass-bg-strong);
  backdrop-filter: var(--glass-backdrop-strong);
  -webkit-backdrop-filter: var(--glass-backdrop-strong);
  border-radius: var(--radius-lg);
  border: 1px solid var(--glass-border);
  transition: all var(--transition-normal);
  box-shadow: var(--shadow-sm);
}

.user-info:hover {
  box-shadow: var(--shadow-md), 0 8px 25px rgba(59, 130, 246, 0.1);
  transform: translateY(-1px);
  border-color: var(--border-medium);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--gradient-primary);
  background-size: 200% 200%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.35);
  animation: gradientShift 6s ease infinite;
}

.username {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.9rem;
}

.logout-btn {
  padding: 0.5rem;
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: all var(--transition-normal);
  display: flex;
  align-items: center;
  justify-content: center;
}

.logout-btn:hover {
  color: var(--accent-error);
  background: rgba(239, 68, 68, 0.1);
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.15);
}

.login-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: var(--gradient-primary);
  background-size: 200% 200%;
  color: white;
  text-decoration: none;
  border-radius: var(--radius-lg);
  font-weight: 600;
  font-size: 0.9rem;
  transition: all var(--transition-normal);
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.25);
  animation: gradientShift 8s ease infinite;
  position: relative;
  overflow: hidden;
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
}

.login-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  transition: left var(--transition-slow);
}

.login-btn:hover::before {
  left: 100%;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(59, 130, 246, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.35);
  border-color: rgba(255, 255, 255, 0.45);
}

.login-btn:active {
  transform: translateY(-1px);
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: var(--radius-lg);
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
  inset: 0;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(14, 165, 233, 0.05) 100%);
  opacity: 0;
  transition: opacity var(--transition-normal);
  border-radius: inherit;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 3px;
  background: var(--gradient-primary);
  transition: all var(--transition-normal);
  transform: translateX(-50%);
  border-radius: 2px;
  box-shadow: 0 0 8px rgba(59, 130, 246, 0.3);
}

.nav-link:hover {
  color: var(--accent-primary);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.15);
}

.nav-link:hover::before {
  opacity: 1;
}

.nav-link:hover::after {
  width: 60%;
}

.nav-link.active {
  color: var(--accent-primary);
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(14, 165, 233, 0.1) 100%);
  box-shadow: 0 4px 20px rgba(59, 130, 246, 0.2);
}

.nav-link.active::before {
  opacity: 1;
}

.nav-link.active::after {
  width: 60%;
}

.theme-toggle {
  padding: 0.75rem;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-normal);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-sm);
  position: relative;
  overflow: hidden;
}

.theme-toggle::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(14, 165, 233, 0.05) 100%);
  opacity: 0;
  transition: opacity var(--transition-normal);
  border-radius: inherit;
}

.theme-toggle:hover::before {
  opacity: 1;
}

.theme-toggle:hover {
  border-color: var(--accent-primary);
  color: var(--accent-primary);
  transform: scale(1.1) rotate(15deg);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.2);
}

.app-body {
  display: flex;
  flex: 1;
  min-height: 0;
}

.sidebar {
  width: 280px;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop-strong);
  -webkit-backdrop-filter: var(--glass-backdrop-strong);
  border-right: 1px solid var(--glass-border);
  display: flex;
  flex-direction: column;
  transition: all var(--transition-slow);
  flex-shrink: 0;
  box-shadow: 8px 0 30px rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
}

.sidebar::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 1px;
  height: 100%;
  background: linear-gradient(180deg, transparent, var(--accent-primary), var(--accent-secondary), var(--accent-tertiary), transparent);
  opacity: 0.3;
}

.sidebar-header {
  padding: 1.75rem 1.5rem 1.25rem;
  border-bottom: 1px solid var(--glass-border);
  position: relative;
}

.sidebar-header::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 1.5rem;
  right: 1.5rem;
  height: 2px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary), var(--accent-tertiary), transparent);
  border-radius: 1px;
}

.sidebar-header h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent-primary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.sidebar-header h3::before {
  content: '';
  width: 8px;
  height: 8px;
  background: var(--gradient-primary);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
}

.sidebar-nav {
  padding: 1.5rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
  overflow-y: auto;
}

.sidebar-link {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 1rem 1.25rem;
  border-radius: var(--radius-lg);
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
  inset: 0;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(14, 165, 233, 0.05) 100%);
  opacity: 0;
  transition: opacity var(--transition-normal);
  border-radius: inherit;
}

.sidebar-link::after {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  width: 0;
  height: 0;
  background: var(--gradient-primary);
  border-radius: 0 4px 4px 0;
  transition: all var(--transition-normal);
  transform: translateY(-50%);
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
}

.sidebar-link:hover {
  color: var(--accent-primary);
  transform: translateX(6px);
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.15);
}

.sidebar-link:hover::before {
  opacity: 1;
}

.sidebar-link:hover::after {
  width: 4px;
  height: 60%;
}

.sidebar-link.active {
  color: var(--accent-primary);
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.18) 0%, rgba(14, 165, 233, 0.12) 100%);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.2);
  transform: translateX(4px);
}

.sidebar-link.active::before {
  opacity: 1;
}

.sidebar-link.active::after {
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
    gap: 0.75rem;
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
  
  .nav-auth {
    margin-right: 0;
    gap: 0.5rem;
  }
  
  .username {
    display: none;
  }
  
  .login-btn span {
    display: none;
  }
  
  .login-btn {
    padding: 0.5rem;
  }
  
  .sidebar {
    display: none;
  }
  
  .main-content {
    padding: 1.5rem 1rem;
  }
}
</style>
