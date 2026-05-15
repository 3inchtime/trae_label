<template>
  <div id="app" :class="{ dark: isDark }">
    <nav>
      <h1>便携工具平台</h1>
      <router-link to="/">首页</router-link>
      <router-link to="/tools/timestamp">⏰ 时间戳转换</router-link>
      <router-link to="/tools">工具列表</router-link>
      <button @click="toggleDarkMode" class="theme-toggle-btn">
        {{ isDark ? '☀️ 浅色' : '🌙 深色' }}
      </button>
    </nav>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

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
  transition: background 0.3s;
}

nav {
  background: var(--accent);
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  gap: 2rem;
  transition: background 0.3s;
}

nav h1 {
  color: white;
  margin: 0;
  font-size: 1.5rem;
}

nav a {
  color: white;
  text-decoration: none;
  font-weight: 500;
}

nav a:hover {
  text-decoration: underline;
}

.theme-toggle-btn {
  margin-left: auto;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.theme-toggle-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

main {
  flex: 1;
  padding: 2rem;
}
</style>
