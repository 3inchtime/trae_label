<template>
  <div id="app">
    <nav>
      <h1>便携工具平台</h1>
      <router-link to="/">首页</router-link>
      <router-link to="/tools/timestamp">⏰ 时间戳转换</router-link>
      <router-link to="/tools">工具列表</router-link>
    </nav>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

nav {
  background: #42b983;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  gap: 2rem;
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

main {
  flex: 1;
  padding: 2rem;
}
</style>
